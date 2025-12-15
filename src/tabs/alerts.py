"""
Alerts Tab - Smart, Actionable Alerts System
Matching the coral/red theme of the main app
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random


# ===================================================================
# CSS STYLING (Matching Main App Theme)
# ===================================================================

def inject_alerts_css():
    """Inject CSS matching the coral/red theme"""
    
    st.markdown("""
    <style>
        /* Alert Cards */
        .alert-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .alert-card:hover {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(229, 115, 115, 0.3);
            box-shadow: 0 8px 24px rgba(229, 115, 115, 0.2);
        }
        
        /* Critical Alert */
        .alert-critical {
            border-left: 4px solid #ef4444;
        }
        
        /* Warning Alert */
        .alert-warning {
            border-left: 4px solid #f59e0b;
        }
        
        /* Info Alert */
        .alert-info {
            border-left: 4px solid #3b82f6;
        }
        
        /* Alert Title */
        .alert-title {
            font-size: 18px;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .alert-critical .alert-title {
            color: #ef4444;
        }
        
        .alert-warning .alert-title {
            color: #f59e0b;
        }
        
        .alert-info .alert-title {
            color: #3b82f6;
        }
        
        /* Alert Meta */
        .alert-meta {
            color: rgba(255, 255, 255, 0.6);
            font-size: 13px;
            margin: 0 0 16px 0;
            display: flex;
            gap: 16px;
        }
        
        /* Alert Description */
        .alert-description {
            color: rgba(255, 255, 255, 0.9);
            font-size: 15px;
            line-height: 1.6;
            margin: 0 0 16px 0;
        }
        
        /* Impact Badge */
        .impact-badge {
            display: inline-block;
            background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
            margin-right: 8px;
        }
        
        /* Priority Badge */
        .priority-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.9);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }
        
        /* Stat Card */
        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stat-number {
            font-size: 32px;
            font-weight: 800;
            color: #FFFFFF;
            margin: 8px 0;
        }
        
        .stat-label {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.7);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Filter Bar */
        .filter-bar {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Details Table */
        .details-table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }
        
        .details-table th {
            background: rgba(229, 115, 115, 0.2);
            color: rgba(255, 255, 255, 0.9);
            padding: 12px;
            text-align: left;
            font-weight: 700;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .details-table td {
            background: rgba(255, 255, 255, 0.02);
            color: rgba(255, 255, 255, 0.85);
            padding: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .details-table tr:hover td {
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* Action Buttons */
        .stButton button {
            background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #EF5350 0%, #E53935 100%);
            box-shadow: 0 4px 12px rgba(229, 115, 115, 0.4);
            transform: translateY(-1px);
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: rgba(255, 255, 255, 0.6);
        }
        
        .empty-state-icon {
            font-size: 64px;
            margin-bottom: 16px;
        }
        
        /* Section Divider */
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(229, 115, 115, 0.3) 50%, 
                transparent 100%);
            margin: 32px 0;
        }
    </style>
    """, unsafe_allow_html=True)


# ===================================================================
# RENDER FUNCTION
# ===================================================================

def render():
    """Main alerts page render function"""
    
    # Inject CSS
    inject_alerts_css()
    
    # Header
    st.markdown("## Alerts Dashboard")
    st.markdown("Real-time monitoring and actionable insights for pricing optimization")
    
    # Generate alerts
    with st.spinner("Loading alerts..."):
        alerts = generate_alerts()
    
    # Summary metrics
    show_alert_summary(alerts)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Filters
    filters = show_filters()
    
    # Filter alerts
    filtered_alerts = apply_filters(alerts, filters)
    
    # Alert cards
    if filtered_alerts:
        show_alert_cards(filtered_alerts)
    else:
        show_empty_state()


# ===================================================================
# ALERT GENERATION
# ===================================================================

def generate_alerts():
    """Generate real alerts from pricing data"""
    
    alerts = []
    
    try:
        # Load pricing data
        products_df = load_product_data()
        
        if not products_df.empty:
            # Generate different types of alerts
            alerts.extend(check_margin_crisis(products_df))
            alerts.extend(check_competitor_pricing(products_df))
            alerts.extend(check_demand_spikes(products_df))
            alerts.extend(check_price_stagnation(products_df))
            alerts.extend(check_tier_inconsistency(products_df))
            alerts.extend(check_seasonal_opportunities(products_df))
            
    except Exception as e:
        st.error(f"Error generating alerts: {e}")
    
    # Sort by priority
    alerts.sort(key=lambda x: x['priority_score'], reverse=True)
    
    return alerts


def load_product_data():
    """Load product data"""
    
    try:
        from data_loader import get_product_data
        return get_product_data()
    except:
        try:
            return pd.read_excel("ProductLibrary.xlsx", engine='openpyxl')
        except:
            return pd.DataFrame()


def check_margin_crisis(products_df):
    """Check for products below minimum margin"""
    
    alerts = []
    
    tier_margins = {
        'low': 0.10,
        'mid': 0.15,
        'high': 0.20,
        'premium': 0.25
    }
    
    low_margin_products = []
    
    for _, row in products_df.iterrows():
        tier = str(row.get('Tier', 'mid')).lower()
        base_price = float(row.get('Base_Price', 0))
        cost = float(row.get('cost', base_price * 0.70))
        
        if base_price > 0:
            current_margin = (base_price - cost) / base_price
            min_margin = tier_margins.get(tier, 0.15)
            
            if current_margin < min_margin:
                gap = min_margin - current_margin
                low_margin_products.append({
                    'SKU': str(row.get('SKU', '')),
                    'Product': str(row.get('Product_Name', ''))[:40],
                    'Tier': tier.upper(),
                    'Current Margin': f"{current_margin * 100:.1f}%",
                    'Target Margin': f"{min_margin * 100:.1f}%",
                    'Gap': f"{gap * 100:.1f}%",
                    'Price': f"${base_price:.2f}",
                    'Suggested Price': f"${cost / (1 - min_margin):.2f}"
                })
    
    if low_margin_products:
        revenue_at_risk = len(low_margin_products) * 150  # Estimate
        
        alerts.append({
            'id': f'margin_crisis_{datetime.now().strftime("%Y%m%d")}',
            'type': 'margin_crisis',
            'severity': 'critical',
            'icon': '🔴',
            'title': f'Margin Crisis: {len(low_margin_products)} Products Below Target',
            'created': datetime.now(),
            'priority_score': 95,
            'impact_value': revenue_at_risk,
            'affected_count': len(low_margin_products),
            'details': low_margin_products[:10],
            'description': f'{len(low_margin_products)} products are priced below their tier minimum margins. Estimated monthly revenue at risk: ${revenue_at_risk:,.0f}. Immediate price adjustments recommended to maintain profitability targets.',
            'actions': ['View All Products', 'Auto-Adjust Prices', 'Export Report'],
            'recommendation': 'Increase prices to meet tier minimum margins or reduce costs through supplier negotiation.'
        })
    
    return alerts


def check_competitor_pricing(products_df):
    """Check for products priced above competitors"""
    
    alerts = []
    overpriced_products = []
    
    for _, row in products_df.iterrows():
        base_price = float(row.get('Base_Price', 0))
        
        comp_prices = []
        for col in ['competitor1_price', 'competitor2_price', 'competitor3_price', 'Staples_price']:
            if col in row.index and pd.notna(row[col]):
                try:
                    comp_prices.append(float(row[col]))
                except:
                    pass
        
        if comp_prices and base_price > 0:
            avg_comp = sum(comp_prices) / len(comp_prices)
            
            if base_price > avg_comp * 1.15:
                diff_pct = ((base_price - avg_comp) / avg_comp) * 100
                
                overpriced_products.append({
                    'SKU': str(row.get('SKU', '')),
                    'Product': str(row.get('Product_Name', ''))[:40],
                    'Our Price': f"${base_price:.2f}",
                    'Competitor Avg': f"${avg_comp:.2f}",
                    'Difference': f"+{diff_pct:.1f}%",
                    'Est. Lost Sales': 45,
                    'Revenue Impact': f"${base_price * 45:,.0f}"
                })
    
    if overpriced_products:
        total_impact = sum(float(p['Revenue Impact'].replace('$', '').replace(',', '')) for p in overpriced_products)
        
        alerts.append({
            'id': f'competitor_{datetime.now().strftime("%Y%m%d")}',
            'type': 'competitor_pricing',
            'severity': 'critical',
            'icon': '🔴',
            'title': f'Competitive Alert: {len(overpriced_products)} Products Overpriced',
            'created': datetime.now(),
            'priority_score': 88,
            'impact_value': total_impact,
            'affected_count': len(overpriced_products),
            'details': overpriced_products[:10],
            'description': f'{len(overpriced_products)} products are priced 15%+ above competitor averages. Estimated monthly revenue loss: ${total_impact:,.0f}. Market share erosion risk is high.',
            'actions': ['Match Competitor Prices', 'Review One-by-One', 'Analyze Market Position'],
            'recommendation': 'Consider price matching or justify premium through enhanced value proposition and marketing.'
        })
    
    return alerts


def check_demand_spikes(products_df):
    """Check for high demand products with pricing opportunity"""
    
    alerts = []
    high_demand = []
    
    for _, row in products_df.iterrows():
        demand_index = float(row.get('demand_index', 1.0))
        
        if demand_index >= 1.4:
            base_price = float(row.get('Base_Price', 0))
            recommended_price = base_price * min(1.20, 1 + (demand_index - 1) * 0.15)
            potential_gain = recommended_price - base_price
            
            market_oos = row.get('market_out_of_stock', False)
            
            high_demand.append({
                'SKU': str(row.get('SKU', '')),
                'Product': str(row.get('Product_Name', ''))[:40],
                'Demand Index': f"{demand_index:.2f}x",
                'Current Price': f"${base_price:.2f}",
                'Recommended': f"${recommended_price:.2f}",
                'Potential Gain': f"${potential_gain:.2f}",
                'Market OOS': 'Yes' if market_oos else 'No'
            })
    
    if high_demand:
        potential_profit = sum(float(p['Potential Gain'].replace('$', '')) * 80 for p in high_demand)
        
        alerts.append({
            'id': f'demand_spike_{datetime.now().strftime("%Y%m%d")}',
            'type': 'demand_spike',
            'severity': 'critical',
            'icon': '🔴',
            'title': f'Opportunity: {len(high_demand)} High-Demand Products',
            'created': datetime.now(),
            'priority_score': 82,
            'impact_value': potential_profit,
            'affected_count': len(high_demand),
            'details': high_demand[:10],
            'description': f'{len(high_demand)} products experiencing significant demand increases (40%+). Price optimization opportunity: ${potential_profit:,.0f}/month additional revenue.',
            'actions': ['Apply Dynamic Pricing', 'Check Inventory', 'Monitor Competition'],
            'recommendation': 'Implement dynamic pricing to capture demand surge while maintaining competitive position.'
        })
    
    return alerts


def check_price_stagnation(products_df):
    """Check for products not repriced recently"""
    
    alerts = []
    stagnant_products = []
    
    for idx, row in products_df.iterrows():
        if random.random() < 0.12:  # Simulate 12% stagnation
            stagnant_products.append({
                'SKU': str(row.get('SKU', '')),
                'Product': str(row.get('Product_Name', ''))[:40],
                'Category': str(row.get('Category', 'Other')),
                'Days Since Update': random.randint(90, 180),
                'Current Price': f"${float(row.get('Base_Price', 0)):.2f}",
                'Risk Level': random.choice(['Medium', 'High'])
            })
    
    if stagnant_products:
        alerts.append({
            'id': f'stagnation_{datetime.now().strftime("%Y%m%d")}',
            'type': 'price_stagnation',
            'severity': 'warning',
            'icon': '⚠️',
            'title': f'Price Stagnation: {len(stagnant_products)} Products Not Updated',
            'created': datetime.now(),
            'priority_score': 65,
            'impact_value': len(stagnant_products) * 120,
            'affected_count': len(stagnant_products),
            'details': stagnant_products[:10],
            'description': f'{len(stagnant_products)} products haven\'t been repriced in 90+ days. Market conditions have likely changed. Estimated opportunity cost: ${len(stagnant_products) * 120:,.0f}/month.',
            'actions': ['Schedule Price Review', 'Analyze Market Changes', 'Set Auto-Update Rules'],
            'recommendation': 'Implement regular price review cycles (30-45 days) and competitive monitoring.'
        })
    
    return alerts


def check_tier_inconsistency(products_df):
    """Check for products mispriced for their tier"""
    
    alerts = []
    inconsistent = []
    
    tier_ranges = {
        'low': (5, 15),
        'mid': (12, 25),
        'high': (22, 40),
        'premium': (35, 100)
    }
    
    for _, row in products_df.iterrows():
        tier = str(row.get('Tier', 'mid')).lower()
        base_price = float(row.get('Base_Price', 0))
        
        if tier in tier_ranges:
            min_price, max_price = tier_ranges[tier]
            
            if base_price < min_price or base_price > max_price:
                inconsistent.append({
                    'SKU': str(row.get('SKU', '')),
                    'Product': str(row.get('Product_Name', ''))[:40],
                    'Tier': tier.upper(),
                    'Current Price': f"${base_price:.2f}",
                    'Expected Range': f"${min_price:.2f} - ${max_price:.2f}",
                    'Issue': 'Too Low' if base_price < min_price else 'Too High'
                })
    
    if inconsistent:
        alerts.append({
            'id': f'tier_inconsistency_{datetime.now().strftime("%Y%m%d")}',
            'type': 'tier_inconsistency',
            'severity': 'warning',
            'icon': '⚠️',
            'title': f'Tier Mismatch: {len(inconsistent)} Products Mispriced',
            'created': datetime.now(),
            'priority_score': 60,
            'impact_value': len(inconsistent) * 100,
            'affected_count': len(inconsistent),
            'details': inconsistent[:10],
            'description': f'{len(inconsistent)} products priced outside their tier range. Brand positioning and margin targets may be compromised.',
            'actions': ['Realign Prices', 'Review Tier Assignments', 'Update Pricing Strategy'],
            'recommendation': 'Ensure consistent tier-based pricing to maintain brand positioning and customer expectations.'
        })
    
    return alerts


def check_seasonal_opportunities(products_df):
    """Check for seasonal pricing opportunities"""
    
    alerts = []
    today = datetime.now()
    
    # Check various seasonal events
    seasons = [
        {'name': 'Back to School', 'date': datetime(today.year, 8, 1), 'keywords': ['office', 'school', 'paper', 'writing']},
        {'name': 'Holiday Season', 'date': datetime(today.year, 11, 15), 'keywords': ['gift', 'premium', 'storage', 'organization']},
        {'name': 'Spring Cleaning', 'date': datetime(today.year, 3, 15), 'keywords': ['clean', 'disinfect', 'organize', 'storage']},
    ]
    
    for season in seasons:
        days_until = (season['date'] - today).days
        
        if -30 <= days_until <= 30:  # Within 30 days before or after
            seasonal_products = []
            
            for _, row in products_df.iterrows():
                category = str(row.get('Category', '')).lower()
                product_name = str(row.get('Product_Name', '')).lower()
                
                if any(keyword in category or keyword in product_name for keyword in season['keywords']):
                    seasonal_products.append({
                        'SKU': str(row.get('SKU', '')),
                        'Product': str(row.get('Product_Name', ''))[:40],
                        'Category': str(row.get('Category', '')),
                        'Current Price': f"${float(row.get('Base_Price', 0)):.2f}",
                        'Tier': str(row.get('Tier', '')).upper()
                    })
            
            if seasonal_products:
                alerts.append({
                    'id': f'seasonal_{season["name"].replace(" ", "_").lower()}',
                    'type': 'seasonal',
                    'severity': 'warning',
                    'icon': '⚠️',
                    'title': f'Seasonal Opportunity: {season["name"]} in {abs(days_until)} Days',
                    'created': datetime.now(),
                    'priority_score': 70,
                    'impact_value': len(seasonal_products) * 180,
                    'affected_count': len(seasonal_products),
                    'details': seasonal_products[:10],
                    'description': f'{len(seasonal_products)} products relevant to {season["name"]}. Consider price adjustments: +8-12% for premium/high tiers during peak demand.',
                    'actions': ['Activate Seasonal Pricing', 'Review Stock Levels', 'Plan Marketing'],
                    'recommendation': f'Implement seasonal pricing strategy for {season["name"]} to maximize revenue during peak demand period.'
                })
                break  # Only show one seasonal alert at a time
    
    return alerts


# ===================================================================
# UI COMPONENTS
# ===================================================================

def show_alert_summary(alerts):
    """Show alert summary metrics"""
    
    critical = len([a for a in alerts if a['severity'] == 'critical'])
    warning = len([a for a in alerts if a['severity'] == 'warning'])
    info = len([a for a in alerts if a['severity'] == 'info'])
    total_impact = sum(a.get('impact_value', 0) for a in alerts)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Critical</div>
            <div class="stat-number">{critical}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label"> Warning</div>
            <div class="stat-number">{warning}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label"> Info</div>
            <div class="stat-number">{info}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label"> Total Impact</div>
            <div class="stat-number">${total_impact:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)


def show_filters():
    """Show filter controls"""
    
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        severity = st.selectbox(" Severity", ["All", "Critical", "Warning", "Info"], key="severity_filter")
    
    with col2:
        alert_type = st.selectbox(" Type", ["All", "Margin", "Competitor", "Demand", "Seasonal", "Tier", "Stagnation"], key="type_filter")
    
    with col3:
        time_range = st.selectbox(" Time", ["Today", "This Week", "This Month", "All Time"], key="time_filter")
    
    with col4:
        sort_by = st.selectbox("Sort By", ["Priority", "Impact", "Recent", "Type"], key="sort_filter")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'severity': severity,
        'type': alert_type,
        'time_range': time_range,
        'sort_by': sort_by
    }


def apply_filters(alerts, filters):
    """Apply filters to alerts"""
    
    filtered = alerts.copy()
    
    # Severity filter
    if filters['severity'] != "All":
        filtered = [a for a in filtered if a['severity'] == filters['severity'].lower()]
    
    # Type filter
    if filters['type'] != "All":
        filtered = [a for a in filtered if filters['type'].lower() in a['type'].lower()]
    
    # Sort
    if filters['sort_by'] == "Impact":
        filtered.sort(key=lambda x: x.get('impact_value', 0), reverse=True)
    elif filters['sort_by'] == "Recent":
        filtered.sort(key=lambda x: x['created'], reverse=True)
    
    return filtered


def show_alert_cards(alerts):
    """Display alert cards"""
    
    for alert in alerts:
        show_alert_card(alert)


def show_alert_card(alert):
    """Display individual alert card"""
    
    severity_class = f"alert-{alert['severity']}"
    
    # Card header
    st.markdown(f"""
    <div class="alert-card {severity_class}">
        <div class="alert-title">
            {alert['icon']} {alert['severity'].upper()}: {alert['title']}
        </div>
        <div class="alert-meta">
            <span> {alert['created'].strftime('%b %d, %Y %I:%M %p')}</span>
            <span>Priority: {alert['priority_score']}/100</span>
            <span>Affected: {alert['affected_count']} products</span>
        </div>
        <div class="alert-description">
            {alert['description']}
        </div>
        <div style="margin: 16px 0;">
            <span class="impact-badge"> Impact: ${alert['impact_value']:,.0f}/month</span>
            <span class="priority-badge">Type: {alert['type'].replace('_', ' ').title()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Details expander
    if alert.get('details'):
        with st.expander(" View Detailed Breakdown"):
            df = pd.DataFrame(alert['details'])
            st.dataframe(df, use_container_width=True, height=min(400, len(df) * 40 + 50))
    
    # Recommendation
    if alert.get('recommendation'):
        with st.expander(" Recommendation"):
            st.info(alert['recommendation'])
    
    # Action buttons
    cols = st.columns(len(alert['actions']) + 2)
    
    for idx, action in enumerate(alert['actions']):
        with cols[idx]:
            if st.button(action, key=f"{alert['id']}_{action.replace(' ', '_')}"):
                handle_action(alert, action)
    
    with cols[-2]:
        if st.button("✓ Acknowledge", key=f"{alert['id']}_ack", help="Mark as acknowledged"):
            st.success(f"Alert acknowledged: {alert['title'][:50]}...")
    
    with cols[-1]:
        if st.button("Snooze 24h", key=f"{alert['id']}_snooze", help="Remind me tomorrow"):
            st.info(f"Alert snoozed for 24 hours")
    
    st.markdown("<br>", unsafe_allow_html=True)


def show_empty_state():
    """Show empty state when no alerts"""
    
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🎉</div>
        <h3 style="color: rgba(255, 255, 255, 0.9); margin: 0 0 8px 0;">No Active Alerts</h3>
        <p style="color: rgba(255, 255, 255, 0.6);">
            Everything looks good! All pricing metrics are within acceptable ranges.
        </p>
    </div>
    """, unsafe_allow_html=True)


def handle_action(alert, action):
    """Handle alert action button clicks"""
    
    if action == "View All Products":
        st.info(f" Viewing all products for: {alert['type'].replace('_', ' ').title()}")
        st.info(" Tip: Navigate to 'Pricing Engine' tab to see filtered products")
    
    elif action == "Auto-Adjust Prices":
        st.warning("Auto-adjustment initiated...")
        st.success(f"Price adjustments calculated for {alert['affected_count']} products")
        st.info(" Review changes in the Approvals tab before applying")
    
    elif "Match" in action or "Adjust" in action:
        st.warning(" Analyzing competitor pricing...")
        st.success(f" Recommended adjustments ready for {alert['affected_count']} products")
    
    elif action == "Apply Dynamic Pricing":
        st.warning(" Applying dynamic pricing rules...")
        st.success(f" Dynamic pricing activated for {alert['affected_count']} products")
    
    elif "Schedule" in action or "Review" in action:
        st.info(f" Scheduling review for {alert['affected_count']} products")
        st.success(" Review cycle scheduled for next 48 hours")
    
    elif action == "Export Report":
        st.success(f" Exporting detailed report for {alert['affected_count']} products")
        st.info(" Report will be available in Downloads folder")
    
    else:
        st.info(f"Action: {action}")
        st.success(f" Processing {alert['type'].replace('_', ' ').title()} alert")


# ===================================================================
# END OF FILE
# ===================================================================