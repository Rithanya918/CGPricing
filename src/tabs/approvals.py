"""
Approvals Tab - Connected to ML Engine and Data Loader
Pulls real product recommendations and allows approval/rejection
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

# Import data loader and ML engine
from data_loader import get_product_data
from ml_engine import PricingEngine

# Excel file paths
PENDING_FILE = "approvals_pending.xlsx"
HISTORY_FILE = "approvals_history.xlsx"

# ============================================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================================

def get_ml_recommendations(ml_weight=0.5):
    """Get ML recommendations for all products"""
    try:
        # Load product data
        df = get_product_data()
        
        # Initialize ML engine
        engine = PricingEngine(ml_weight=ml_weight)
        
        recommendations = []
        for _, row in df.iterrows():
            try:
                base_price = float(row["Base_Price"])
                cost = float(row.get("cost", base_price * 0.70))
                competitor_avg = float(row.get("competitor_avg", base_price))
                demand_index = float(row.get("demand_index", 1.0))
                market_oos = bool(row.get("market_out_of_stock", False))
                
                rec = engine.get_recommendation(
                    product_name=str(row["Product_Name"]),
                    base_price=base_price,
                    cost=cost,
                    tier=str(row["Tier"]),
                    category=str(row.get("Category", "Other")),
                    lifecycle=str(row.get("Product_Lifecycle", "Maturity")),
                    competitor_avg=competitor_avg,
                    market_oos=market_oos,
                    demand_index=demand_index
                )
                
                # Calculate required approval level based on change percentage
                change_pct = rec.get("price_change_pct", 0)
                abs_change = abs(change_pct)
                
                if abs_change <= 3:
                    approval_level = "Auto-Approved"
                elif abs_change <= 7:
                    approval_level = "Manager"
                elif abs_change <= 15:
                    approval_level = "Director"
                else:
                    approval_level = "Executive"
                
                recommendations.append({
                    'ID': str(row["SKU"]),
                    'Product': rec.get("product_name", ""),
                    'Category': str(row.get("Category", "Other")),
                    'Tier': str(row["Tier"]),
                    'Current_Price': base_price,
                    'New_Price': rec.get("recommended_price", base_price),
                    'Change_Percent': change_pct,
                    'Margin_Percent': rec.get("margin_pct", 0),
                    'Competitor_Avg': competitor_avg,
                    'Demand_Index': demand_index,
                    'Required_Approval': approval_level,
                    'Status': 'Pending',
                    'Suggested_Date': datetime.now().strftime('%Y-%m-%d'),
                    'Confidence': rec.get("confidence", {}).get("label", "Medium")
                })
            except:
                continue
        
        return pd.DataFrame(recommendations)
    
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()


def initialize_excel_files():
    """Initialize Excel files with ML recommendations"""
    
    # Initialize pending approvals file with ML recommendations
    if not os.path.exists(PENDING_FILE):
        # Get ML recommendations
        recommendations_df = get_ml_recommendations(ml_weight=0.5)
        
        if not recommendations_df.empty:
            # Filter only items that need approval (not auto-approved)
            pending_df = recommendations_df[recommendations_df['Required_Approval'] != 'Auto-Approved'].copy()
            pending_df.to_excel(PENDING_FILE, index=False, engine='openpyxl')
            print(f"Created {PENDING_FILE} with {len(pending_df)} items")
        else:
            # Create empty file if no recommendations
            empty_data = {
                'ID': [],
                'Product': [],
                'Category': [],
                'Tier': [],
                'Current_Price': [],
                'New_Price': [],
                'Change_Percent': [],
                'Margin_Percent': [],
                'Competitor_Avg': [],
                'Demand_Index': [],
                'Required_Approval': [],
                'Status': [],
                'Suggested_Date': [],
                'Confidence': []
            }
            pd.DataFrame(empty_data).to_excel(PENDING_FILE, index=False, engine='openpyxl')
    
    # Initialize history file
    if not os.path.exists(HISTORY_FILE):
        history_data = {
            'ID': [],
            'Product': [],
            'Category': [],
            'Tier': [],
            'Current_Price': [],
            'New_Price': [],
            'Change_Percent': [],
            'Margin_Percent': [],
            'Competitor_Avg': [],
            'Demand_Index': [],
            'Required_Approval': [],
            'Status': [],
            'Suggested_Date': [],
            'Confidence': [],
            'Action': [],
            'Action_Date': [],
            'Action_By': [],
            'Notes': []
        }
        df = pd.DataFrame(history_data)
        df.to_excel(HISTORY_FILE, index=False, engine='openpyxl')
        print(f"Created {HISTORY_FILE}")


def get_mock_data():
    """Get real data metrics from ML recommendations"""
    try:
        df = get_product_data()
        recommendations_df = get_ml_recommendations(ml_weight=0.5)
        
        if recommendations_df.empty:
            return {
                'avg_profit_margin': 0,
                'margin_improvement': 0,
                'high_confidence_pct': 0,
                'optimal_pricing_pct': 0,
                'competitive_positioning_pct': 0,
                'pending_review': 0
            }
        
        # 1. Average Profit Margin
        avg_margin = recommendations_df['Margin_Percent'].mean()
        
        # 2. % of recommendations with high confidence
        high_confidence_count = len(recommendations_df[recommendations_df['Confidence'] == 'High Confidence'])
        high_confidence_pct = (high_confidence_count / len(recommendations_df) * 100) if len(recommendations_df) > 0 else 0
        
        # 3. % of products with optimal pricing (within target margin range: 20-35%)
        optimal_margin_count = len(recommendations_df[(recommendations_df['Margin_Percent'] >= 20) & 
                                                       (recommendations_df['Margin_Percent'] <= 35)])
        optimal_pricing_pct = (optimal_margin_count / len(recommendations_df) * 100) if len(recommendations_df) > 0 else 0
        
        # 4. % of products with competitive positioning (within ±5% of competitor avg)
        recommendations_df['Price_Diff_Pct'] = ((recommendations_df['New_Price'] - recommendations_df['Competitor_Avg']) / 
                                                 recommendations_df['Competitor_Avg'] * 100).abs()
        competitive_count = len(recommendations_df[recommendations_df['Price_Diff_Pct'] <= 5])
        competitive_positioning_pct = (competitive_count / len(recommendations_df) * 100) if len(recommendations_df) > 0 else 0
        
        # 5. Margin improvement (compare current vs recommended)
        total_current_revenue = recommendations_df['Current_Price'].sum()
        total_new_revenue = recommendations_df['New_Price'].sum()
        revenue_change = ((total_new_revenue - total_current_revenue) / total_current_revenue * 100) if total_current_revenue > 0 else 0
        
        pending_count = len(recommendations_df[recommendations_df['Status'] == 'Pending'])
        
        return {
            'avg_profit_margin': round(avg_margin, 1),
            'margin_improvement': round(revenue_change, 1),
            'high_confidence_pct': round(high_confidence_pct, 1),
            'optimal_pricing_pct': round(optimal_pricing_pct, 1),
            'competitive_positioning_pct': round(competitive_positioning_pct, 1),
            'pending_review': pending_count
        }
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return {
            'avg_profit_margin': 0,
            'margin_improvement': 0,
            'high_confidence_pct': 0,
            'optimal_pricing_pct': 0,
            'competitive_positioning_pct': 0,
            'pending_review': 0
        }


def get_pending_approvals():
    """Get pending approval items from Excel"""
    try:
        initialize_excel_files()
        df = pd.read_excel(PENDING_FILE, engine='openpyxl')
        return df[df['Status'] == 'Pending']
    except Exception as e:
        st.error(f"Error reading pending approvals: {str(e)}")
        return pd.DataFrame()


def get_workflow_stats():
    """Calculate workflow statistics from pending items"""
    df = get_pending_approvals()
    
    if df.empty:
        return {
            'ai_auto_approve': 0,
            'manager_pending': 0,
            'director_pending': 0,
            'executive_pending': 0
        }
    
    # Calculate absolute change percentages
    df['Abs_Change'] = df['Change_Percent'].abs()
    
    # Categorize by change percentage
    auto_approve = len(df[df['Abs_Change'] <= 3])
    manager = len(df[(df['Abs_Change'] > 3) & (df['Abs_Change'] <= 7)])
    director = len(df[(df['Abs_Change'] > 7) & (df['Abs_Change'] <= 15)])
    executive = len(df[df['Abs_Change'] > 15])
    
    return {
        'ai_auto_approve': auto_approve,
        'manager_pending': manager,
        'director_pending': director,
        'executive_pending': executive
    }


def approve_item(item_id, approved_by="User", notes=""):
    """Approve an item and move it to history"""
    try:
        # Read pending file
        pending_df = pd.read_excel(PENDING_FILE, engine='openpyxl')
        
        # Find the item
        item_mask = pending_df['ID'] == item_id
        if not item_mask.any():
            return False, "Item not found"
        
        # Get item details
        item = pending_df[item_mask].iloc[0].to_dict()
        
        # Update status in pending file
        pending_df.loc[item_mask, 'Status'] = 'Approved'
        pending_df.to_excel(PENDING_FILE, index=False, engine='openpyxl')
        
        # Add to history
        history_df = pd.read_excel(HISTORY_FILE, engine='openpyxl')
        
        history_entry = {
            'ID': item['ID'],
            'Product': item['Product'],
            'Category': item.get('Category', ''),
            'Tier': item.get('Tier', ''),
            'Current_Price': item['Current_Price'],
            'New_Price': item['New_Price'],
            'Change_Percent': item['Change_Percent'],
            'Margin_Percent': item.get('Margin_Percent', 0),
            'Competitor_Avg': item.get('Competitor_Avg', 0),
            'Demand_Index': item.get('Demand_Index', 1.0),
            'Required_Approval': item['Required_Approval'],
            'Status': 'Approved',
            'Suggested_Date': item['Suggested_Date'],
            'Confidence': item.get('Confidence', ''),
            'Action': 'Approved',
            'Action_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Action_By': approved_by,
            'Notes': notes if notes else 'Approved'
        }
        
        history_df = pd.concat([history_df, pd.DataFrame([history_entry])], ignore_index=True)
        history_df.to_excel(HISTORY_FILE, index=False, engine='openpyxl')
        
        return True, f"Approved {item['Product']}"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def reject_item(item_id, rejected_by="User", notes=""):
    """Reject an item and move it to history"""
    try:
        # Read pending file
        pending_df = pd.read_excel(PENDING_FILE, engine='openpyxl')
        
        # Find the item
        item_mask = pending_df['ID'] == item_id
        if not item_mask.any():
            return False, "Item not found"
        
        # Get item details
        item = pending_df[item_mask].iloc[0].to_dict()
        
        # Update status in pending file
        pending_df.loc[item_mask, 'Status'] = 'Rejected'
        pending_df.to_excel(PENDING_FILE, index=False, engine='openpyxl')
        
        # Add to history
        history_df = pd.read_excel(HISTORY_FILE, engine='openpyxl')
        
        history_entry = {
            'ID': item['ID'],
            'Product': item['Product'],
            'Category': item.get('Category', ''),
            'Tier': item.get('Tier', ''),
            'Current_Price': item['Current_Price'],
            'New_Price': item['New_Price'],
            'Change_Percent': item['Change_Percent'],
            'Margin_Percent': item.get('Margin_Percent', 0),
            'Competitor_Avg': item.get('Competitor_Avg', 0),
            'Demand_Index': item.get('Demand_Index', 1.0),
            'Required_Approval': item['Required_Approval'],
            'Status': 'Rejected',
            'Suggested_Date': item['Suggested_Date'],
            'Confidence': item.get('Confidence', ''),
            'Action': 'Rejected',
            'Action_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Action_By': rejected_by,
            'Notes': notes if notes else 'Rejected'
        }
        
        history_df = pd.concat([history_df, pd.DataFrame([history_entry])], ignore_index=True)
        history_df.to_excel(HISTORY_FILE, index=False, engine='openpyxl')
        
        return True, f"Rejected {item['Product']}"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_history_data():
    """Get approval history from Excel"""
    try:
        if not os.path.exists(HISTORY_FILE):
            initialize_excel_files()
        df = pd.read_excel(HISTORY_FILE, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error reading history: {str(e)}")
        return pd.DataFrame()


def export_to_excel(df, filename):
    """Export DataFrame to Excel and return bytes"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output.getvalue()


def refresh_pending_from_ml():
    """Refresh pending approvals with new ML recommendations"""
    try:
        # Get new recommendations
        new_recs = get_ml_recommendations(ml_weight=0.5)
        
        if new_recs.empty:
            return False, "No new recommendations generated"
        
        # Filter only items that need approval
        new_pending = new_recs[new_recs['Required_Approval'] != 'Auto-Approved'].copy()
        
        # Read existing pending items
        existing_df = pd.read_excel(PENDING_FILE, engine='openpyxl')
        
        # Get items that are still pending (not yet approved/rejected)
        still_pending = existing_df[existing_df['Status'] == 'Pending']
        
        # Combine with new recommendations (avoid duplicates by ID)
        combined = pd.concat([still_pending, new_pending], ignore_index=True)
        combined = combined.drop_duplicates(subset=['ID'], keep='first')
        
        # Save back
        combined.to_excel(PENDING_FILE, index=False, engine='openpyxl')
        
        new_count = len(combined) - len(still_pending)
        return True, f"Added {new_count} new recommendations"
        
    except Exception as e:
        return False, f"Error refreshing: {str(e)}"


# ============================================================================
# UI RENDERING
# ============================================================================

def render():
    """Render the Approvals tab"""
    
    # Initialize files
    initialize_excel_files()
    
    # Initialize filter state
    if 'approval_filter' not in st.session_state:
        st.session_state.approval_filter = 'All'
    
    # Custom CSS
    st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(190, 24, 93, 0.05) 100%);
            border: 1px solid rgba(236, 72, 153, 0.2);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
        }
        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: #ec4899;
            margin: 8px 0;
        }
        .metric-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .metric-delta {
            color: #10b981;
            font-size: 14px;
            font-weight: 600;
            margin-top: 4px;
        }
        .workflow-container-new {
            background: rgba(30, 20, 25, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 32px;
            margin: 24px 0;
        }
        .workflow-title-new {
            color: #ffffff;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 24px;
        }
        .workflow-steps-new {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }
        .workflow-step-new {
            flex: 1;
            text-align: center;
        }
        .workflow-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 700;
            margin: 0 auto 12px;
            border: 3px solid;
        }
        .circle-green {
            background: rgba(16, 185, 129, 0.15);
            border-color: #10b981;
            color: #10b981;
        }
        .circle-pink {
            background: rgba(236, 72, 153, 0.15);
            border-color: #ec4899;
            color: #ec4899;
        }
        .circle-gray {
            background: rgba(156, 163, 175, 0.15);
            border-color: #9ca3af;
            color: #9ca3af;
        }
        .workflow-label {
            font-size: 16px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 4px;
        }
        .workflow-description {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.5);
        }
        .workflow-count {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.6);
            margin-top: 4px;
        }
        .pending-badge-new {
            display: inline-block;
            background: rgba(236, 72, 153, 0.2);
            color: #ec4899;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 8px;
        }
        .pending-title {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            margin: 32px 0 24px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    
    # Get metrics
    metrics = get_mock_data()
    
    # Metrics row - only 3 cards now
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Confidence Recommendations</div>
            <div class="metric-value">{metrics['high_confidence_pct']:.1f}%</div>
            <div class="metric-delta">{metrics['pending_review']} pending review</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Optimal Pricing</div>
            <div class="metric-value">{metrics['optimal_pricing_pct']:.1f}%</div>
            <div class="metric-delta">Within 20-35% margin range</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Competitive Positioning</div>
            <div class="metric-value">{metrics['competitive_positioning_pct']:.1f}%</div>
            <div class="metric-delta">Within ±5% of competitors</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Workflow visualization with clickable circles
    workflow = get_workflow_stats()
    
    st.markdown(f"""
    <div class="workflow-container-new">
        <div class="workflow-title-new">Approval Pipeline (Click circles to filter)</div>
        <div class="workflow-steps-new">
            <div class="workflow-step-new">
                <div class="workflow-circle circle-green">{workflow['ai_auto_approve']}</div>
                <div class="workflow-label">AI Auto-Approve</div>
                <div class="workflow-description">≤3% changes</div>
                <div class="workflow-count">{workflow['ai_auto_approve']} items</div>
            </div>
            <div class="workflow-step-new">
                <div class="workflow-circle circle-pink">{workflow['manager_pending']}</div>
                <div class="workflow-label">Manager Review</div>
                <div class="workflow-description">3-7% changes</div>
                <span class="pending-badge-new">{workflow['manager_pending']} pending</span>
            </div>
            <div class="workflow-step-new">
                <div class="workflow-circle circle-gray">{workflow['director_pending']}</div>
                <div class="workflow-label">Director Approval</div>
                <div class="workflow-description">7-15% changes</div>
                <div class="workflow-count">{workflow['director_pending']} items</div>
            </div>
            <div class="workflow-step-new">
                <div class="workflow-circle circle-gray">{workflow['executive_pending']}</div>
                <div class="workflow-label">Executive</div>
                <div class="workflow-description">15%+ changes</div>
                <div class="workflow-count">{workflow['executive_pending']} item{'s' if workflow['executive_pending'] != 1 else ''}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clickable buttons below circles
    st.markdown("<div style='margin-top: -20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(" AI Auto", key="filter_auto", use_container_width=True, 
                     type="primary" if st.session_state.approval_filter == 'Auto-Approved' else "secondary"):
            st.session_state.approval_filter = 'Auto-Approved'
            st.rerun()
    
    with col2:
        if st.button("Manager", key="filter_manager", use_container_width=True,
                     type="primary" if st.session_state.approval_filter == 'Manager' else "secondary"):
            st.session_state.approval_filter = 'Manager'
            st.rerun()
    
    with col3:
        if st.button("Director", key="filter_director", use_container_width=True,
                     type="primary" if st.session_state.approval_filter == 'Director' else "secondary"):
            st.session_state.approval_filter = 'Director'
            st.rerun()
    
    with col4:
        if st.button(" Executive", key="filter_executive", use_container_width=True,
                     type="primary" if st.session_state.approval_filter == 'Executive' else "secondary"):
            st.session_state.approval_filter = 'Executive'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons row
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Refresh Data", use_container_width=True):
            success, message = refresh_pending_from_ml()
            if success:
                st.success(message)
            else:
                st.warning(message)
            st.rerun()
    
    with col2:
        if st.button("Show All", use_container_width=True):
            st.session_state.approval_filter = 'All'
            st.rerun()
    
    with col3:
        # Export pending items
        pending_df = get_pending_approvals()
        if not pending_df.empty:
            excel_data = export_to_excel(pending_df, "pending_approvals.xlsx")
            st.download_button(
                label="Export Pending",
                data=excel_data,
                file_name=f"pending_approvals_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with col4:
        # Export history
        history_df = get_history_data()
        if not history_df.empty:
            excel_data = export_to_excel(history_df, "approval_history.xlsx")
            st.download_button(
                label="Export History",
                data=excel_data,
                file_name=f"approval_history_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with col5:
        # Export combined report
        if not pending_df.empty or not history_df.empty:
            # Create combined report
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                if not pending_df.empty:
                    pending_df.to_excel(writer, sheet_name='Pending', index=False)
                if not history_df.empty:
                    history_df.to_excel(writer, sheet_name='History', index=False)
            output.seek(0)
            
            st.download_button(
                label=" Export All",
                data=output,
                file_name=f"approval_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Pending Review Section with Filtering
    pending_items = get_pending_approvals()
    
    # Apply filter based on selected approval level
    if st.session_state.approval_filter != 'All':
        pending_items = pending_items[pending_items['Required_Approval'] == st.session_state.approval_filter]
    
    total_pending = len(pending_items)
    
    # Display filter status
    filter_text = f" - {st.session_state.approval_filter}" if st.session_state.approval_filter != 'All' else ""
    st.markdown(f'<div class="pending-title">Pending Your Review ({total_pending}){filter_text}</div>', unsafe_allow_html=True)
    
    if pending_items.empty:
        st.info("Your approval queue is clear! No action required.")
        
        # Show history summary
        history_df = get_history_data()
        if not history_df.empty:
            st.markdown("### Recent Activity")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Processed", len(history_df))
            with col2:
                approved = len(history_df[history_df['Action'] == 'Approved'])
                st.metric("Approved", approved)
            with col3:
                rejected = len(history_df[history_df['Action'] == 'Rejected'])
                st.metric("Rejected", rejected)
        
        return
    
    # Display each pending item
    for index, row in pending_items.iterrows():
        change_val = float(row['Change_Percent'])
        change_class = "positive" if change_val >= 0 else "negative"
        change_sign = "+" if change_val >= 0 else ""
        
        # Create unique key using both index and ID
        unique_key = f"{index}_{row['ID']}"
        
        # Create card and buttons
        col_card, col_buttons = st.columns([3, 1])
        
        with col_card:
            confidence_color = {
                'High Confidence': '#10b981',
                'Review Suggested': '#f59e0b',
                'Needs Review': '#ef4444'
            }.get(row.get('Confidence', 'Medium'), '#9ca3af')
            
            st.markdown(f"""
            <div style="background-color: rgb(41, 21, 25); border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;
                        display: flex; align-items: center; gap: 16px;">
                <div style="width: 48px; height: 48px; background: rgba(255, 255, 255, 0.05);
                            border-radius: 10px; display: flex; align-items: center; 
                            justify-content: center; flex-shrink: 0;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" 
                         fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="2">
                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                        <line x1="12" y1="22.08" x2="12" y2="12"></line>
                    </svg>
                </div>
                <div style="flex: 1;">
                    <div style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 6px;">
                        {row['Product']}
                    </div>
                    <p style="margin: 0; color: #ccc;">
                        <span style="color: rgba(255, 255, 255, 0.5);">${row['Current_Price']:.2f}</span>
                        <span style="color: rgba(255, 255, 255, 0.4); margin: 0 8px;">→</span>
                        <span style="color: white; font-weight: 600;">${row['New_Price']:.2f}</span>
                        <span style="color: {'#10b981' if change_val >= 0 else '#ef4444'}; margin-left: 12px; font-weight: bold;">
                            ({change_sign}{change_val:.1f}%)
                        </span>
                        <span style="margin-left: 16px; font-size: 12px; color: rgba(255,255,255,0.5);">
                            Requires: {row['Required_Approval']}
                        </span>
                        <span style="margin-left: 12px; font-size: 12px; color: {confidence_color};">
                            • {row.get('Confidence', 'Medium')}
                        </span>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_buttons:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                if st.button("Approve", key=f"approve_{unique_key}", type="primary", use_container_width=True):
                    username = st.session_state.get('username', 'User')
                    success, message = approve_item(row['ID'], approved_by=username)
                    
                    if success:
                        st.success(f"{message}")
                        st.rerun()
                    else:
                        st.error(f" {message}")
            
            with btn_col2:
                if st.button(" Reject", key=f"reject_{unique_key}", use_container_width=True):
                    username = st.session_state.get('username', 'User')
                    success, message = reject_item(row['ID'], rejected_by=username)
                    
                    if success:
                        st.warning(f" {message}")
                        st.rerun()
                    else:
                        st.error(f" {message}")
    
    # Show history summary at bottom
    st.markdown("---")
    st.markdown("### Approval History Summary")
    
    history_df = get_history_data()
    if not history_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Processed", len(history_df))
        
        with col2:
            approved = len(history_df[history_df['Action'] == 'Approved'])
            st.metric("Approved", approved, delta=f"{(approved/len(history_df)*100):.1f}%")
        
        with col3:
            rejected = len(history_df[history_df['Action'] == 'Rejected'])
            st.metric("Rejected", rejected, delta=f"{(rejected/len(history_df)*100):.1f}%")
        
        with col4:
            if not history_df.empty and 'Action_Date' in history_df.columns:
                latest = history_df['Action_Date'].max()
                st.metric("Last Action", str(latest)[:10] if pd.notna(latest) else "N/A")
    else:
        st.info("No approval history yet. Start approving or rejecting items!")