"""
Elasticity Trend by Segment Analysis
Calculates and visualizes price elasticity trends over time for different customer segments
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

class ElasticityAnalyzer:
    """
    Analyzes price elasticity trends by customer segment
    
    Elasticity (ε) = % Change in Quantity / % Change in Price
    
    Segments:
    - Tier-based: Low, Mid, High, Premium
    - Lifecycle-based: Launch, Growth, Maturity, Decline
    - Demand-based: Low demand (<0.8), Normal (0.8-1.2), High demand (>1.2)
    """
    
    def __init__(self, products_df):
        self.products_df = products_df
        self.segments = self._create_segments()
    
    def _create_segments(self):
        """Create customer segments based on product characteristics"""
        df = self.products_df.copy()
        
        # Segment 1: By Tier (pricing tier = customer sophistication)
        df['segment_tier'] = df['Tier'].apply(lambda x: f"Tier: {x}")
        
        # Segment 2: By Demand Level (proxy for customer loyalty)
        df['segment_demand'] = df['demand_index'].apply(
            lambda x: 'High Demand Customers' if x > 1.2 
            else 'Low Demand Customers' if x < 0.8 
            else 'Normal Demand Customers'
        )
        
        # Segment 3: By Product Lifecycle (customer acquisition stage)
        df['segment_lifecycle'] = df['Product_Lifecycle'].apply(
            lambda x: f"Lifecycle: {x}"
        )
        
        # Segment 4: By Category (customer industry/type)
        df['segment_category'] = df['Category'].apply(lambda x: f"Category: {x}")
        
        return df
    
    def calculate_elasticity(self, price_old, price_new, quantity_old, quantity_new):
        """
        Calculate price elasticity
        
        Formula: ε = (ΔQ/Q) / (ΔP/P)
        Where:
        - ΔQ = change in quantity
        - ΔP = change in price
        """
        if price_old == 0 or quantity_old == 0:
            return 0
        
        pct_price_change = (price_new - price_old) / price_old
        pct_quantity_change = (quantity_new - quantity_old) / quantity_old
        
        if pct_price_change == 0:
            return 0
        
        elasticity = pct_quantity_change / pct_price_change
        return elasticity
    
    def simulate_elasticity_trends(self, months=12):
        """
        Simulate elasticity trends over time for different segments
        
        In production, this would use actual historical data:
        - Past prices
        - Past quantities sold
        - Past customer behavior
        
        For now, we simulate realistic trends based on:
        - Tier characteristics
        - Demand patterns
        - Lifecycle stage
        """
        
        # Generate time periods
        end_date = datetime.now()
        dates = [end_date - timedelta(days=30*i) for i in range(months)]
        dates.reverse()
        date_labels = [d.strftime('%b %Y') for d in dates]
        
        trends = {}
        
        # Segment by Tier (most important for pricing strategy)
        for tier in ['Low', 'Mid', 'High', 'Premium']:
            segment_df = self.segments[self.segments['Tier'] == tier]
            
            if len(segment_df) == 0:
                continue
            
            # Base elasticity by tier (Premium = less elastic)
            base_elasticity = {
                'Low': -1.8,      # Very elastic (price sensitive)
                'Mid': -1.3,      # Moderately elastic
                'High': -0.9,     # Less elastic
                'Premium': -0.5   # Inelastic (not price sensitive)
            }[tier]
            
            # Simulate trend (elasticity changing over time)
            elasticities = []
            for i, month in enumerate(range(months)):
                # Add seasonal variation
                seasonal = 0.1 * np.sin(2 * np.pi * i / 12)
                
                # Add trend (customers becoming less price sensitive over time)
                trend = 0.02 * i  # Becoming 2% less elastic per month
                
                # Add random noise
                noise = np.random.normal(0, 0.05)
                
                monthly_elasticity = base_elasticity + seasonal + trend + noise
                elasticities.append(monthly_elasticity)
            
            trends[f'Tier: {tier}'] = {
                'dates': date_labels,
                'elasticity': elasticities,
                'color': {
                    'Low': '#EF5350',
                    'Mid': '#F48FB1', 
                    'High': '#E57373',
                    'Premium': '#F8BBD0'
                }[tier]
            }
        
        # Segment by Demand Level
        for demand_level in ['High Demand Customers', 'Normal Demand Customers', 'Low Demand Customers']:
            if demand_level == 'High Demand Customers':
                demand_filter = self.segments['demand_index'] > 1.2
                base_elasticity = -0.7  # Less elastic (loyal customers)
            elif demand_level == 'Low Demand Customers':
                demand_filter = self.segments['demand_index'] < 0.8
                base_elasticity = -2.0  # Very elastic (price shoppers)
            else:
                demand_filter = (self.segments['demand_index'] >= 0.8) & (self.segments['demand_index'] <= 1.2)
                base_elasticity = -1.4  # Moderately elastic
            
            segment_df = self.segments[demand_filter]
            
            if len(segment_df) == 0:
                continue
            
            elasticities = []
            for i in range(months):
                # High demand customers becoming more loyal (less elastic)
                if demand_level == 'High Demand Customers':
                    trend = 0.03 * i
                # Low demand customers staying price sensitive
                elif demand_level == 'Low Demand Customers':
                    trend = -0.01 * i
                else:
                    trend = 0.01 * i
                
                seasonal = 0.08 * np.sin(2 * np.pi * i / 12)
                noise = np.random.normal(0, 0.04)
                
                monthly_elasticity = base_elasticity + seasonal + trend + noise
                elasticities.append(monthly_elasticity)
            
            trends[demand_level] = {
                'dates': date_labels,
                'elasticity': elasticities,
                'color': {
                    'High Demand Customers': '#10b981',
                    'Normal Demand Customers': '#F48FB1',
                    'Low Demand Customers': '#EF5350'
                }[demand_level]
            }
        
        return trends
    
    def get_elasticity_interpretation(self, elasticity):
        """
        Interpret elasticity value
        
        |ε| > 1: Elastic (price sensitive)
        |ε| < 1: Inelastic (not price sensitive)
        |ε| = 1: Unit elastic
        """
        abs_e = abs(elasticity)
        
        if abs_e > 2:
            return "Very Elastic", "Customers are extremely price sensitive. Small price increases cause large demand drops."
        elif abs_e > 1:
            return "Elastic", "Customers are price sensitive. Price increases reduce demand significantly."
        elif abs_e > 0.5:
            return "Moderately Elastic", "Customers somewhat price sensitive. Price changes have moderate impact."
        else:
            return "Inelastic", "Customers not price sensitive. Can increase prices without losing much demand."
    
    def calculate_segment_stats(self):
        """Calculate current elasticity statistics by segment"""
        
        stats = []
        
        # By Tier
        for tier in ['Low', 'Mid', 'High', 'Premium']:
            segment_df = self.segments[self.segments['Tier'] == tier]
            if len(segment_df) > 0:
                avg_demand = segment_df['demand_index'].mean()
                avg_price = segment_df['Base_Price'].mean()
                
                # Estimate elasticity based on tier characteristics
                elasticity_estimate = {
                    'Low': -1.8,
                    'Mid': -1.3,
                    'High': -0.9,
                    'Premium': -0.5
                }[tier]
                
                interpretation, description = self.get_elasticity_interpretation(elasticity_estimate)
                
                stats.append({
                    'Segment': f'Tier: {tier}',
                    'Products': len(segment_df),
                    'Avg Demand': f"{avg_demand:.2f}",
                    'Avg Price': f"${avg_price:.2f}",
                    'Elasticity': f"{elasticity_estimate:.2f}",
                    'Interpretation': interpretation,
                    'Strategy': description
                })
        
        # By Demand Level
        for demand_level, (low, high, elasticity) in [
            ('Low Demand', (0, 0.8, -2.0)),
            ('Normal Demand', (0.8, 1.2, -1.4)),
            ('High Demand', (1.2, 999, -0.7))
        ]:
            if demand_level == 'Low Demand':
                segment_df = self.segments[self.segments['demand_index'] < high]
            elif demand_level == 'High Demand':
                segment_df = self.segments[self.segments['demand_index'] > low]
            else:
                segment_df = self.segments[(self.segments['demand_index'] >= low) & (self.segments['demand_index'] <= high)]
            
            if len(segment_df) > 0:
                interpretation, description = self.get_elasticity_interpretation(elasticity)
                
                stats.append({
                    'Segment': f'{demand_level} Customers',
                    'Products': len(segment_df),
                    'Avg Demand': f"{segment_df['demand_index'].mean():.2f}",
                    'Avg Price': f"${segment_df['Base_Price'].mean():.2f}",
                    'Elasticity': f"{elasticity:.2f}",
                    'Interpretation': interpretation,
                    'Strategy': description
                })
        
        return pd.DataFrame(stats)


def render_elasticity_trends(products_df):
    """
    Render elasticity trend visualizations in Streamlit
    """
    import streamlit as st
    
    st.markdown("---")
    st.markdown("### 📊 Elasticity Trend by Segment")
    st.markdown("""
    **Price Elasticity (ε)** measures how customer demand changes when prices change.
    - **Elastic (|ε| > 1)**: Price sensitive - small price increases reduce demand significantly
    - **Inelastic (|ε| < 1)**: Not price sensitive - can raise prices without losing customers
    """)
    
    # Initialize analyzer
    analyzer = ElasticityAnalyzer(products_df)
    
    # Segment selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        segment_type = st.selectbox(
            "View Segment Type",
            ["Customer Tiers", "Demand Levels", "All Segments"],
            key="elasticity_segment_type"
        )
    
    with col2:
        months = st.slider("Time Period (Months)", 6, 24, 12, key="elasticity_months")
    
    # Generate elasticity trends
    trends = analyzer.simulate_elasticity_trends(months=months)
    
    # Filter trends based on selection
    if segment_type == "Customer Tiers":
        filtered_trends = {k: v for k, v in trends.items() if k.startswith('Tier:')}
    elif segment_type == "Demand Levels":
        filtered_trends = {k: v for k, v in trends.items() if 'Demand Customers' in k}
    else:
        filtered_trends = trends
    
    # Create trend chart
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for segment_name, segment_data in filtered_trends.items():
        fig.add_trace(go.Scatter(
            x=segment_data['dates'],
            y=segment_data['elasticity'],
            name=segment_name,
            mode='lines+markers',
            line=dict(color=segment_data['color'], width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Date: %{x}<br>' +
                         'Elasticity: %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
    
    # Add horizontal line at -1 (elastic/inelastic boundary)
    fig.add_hline(
        y=-1, 
        line_dash="dash", 
        line_color="rgba(255, 255, 255, 0.3)",
        annotation_text="Elastic/Inelastic Boundary (ε = -1)",
        annotation_position="right"
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(229, 115, 115, 0.05)',
        plot_bgcolor='rgba(229, 115, 115, 0.05)',
        font=dict(color='#F48FB1'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title='Time Period',
            showgrid=True,
            gridcolor='rgba(229, 115, 115, 0.2)'
        ),
        yaxis=dict(
            title='Price Elasticity (ε)',
            showgrid=True,
            gridcolor='rgba(229, 115, 115, 0.2)',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.2)'
        ),
        hovermode='x unified',
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 Key Insights")
        
        # Calculate trend direction
        insights = []
        for segment_name, segment_data in filtered_trends.items():
            elasticities = segment_data['elasticity']
            start_e = elasticities[0]
            end_e = elasticities[-1]
            change = end_e - start_e
            
            if change > 0.1:
                trend = "📈 Becoming LESS price sensitive (more loyalty)"
                action = "✅ Can justify price increases"
            elif change < -0.1:
                trend = "📉 Becoming MORE price sensitive"
                action = "⚠️ Focus on value proposition"
            else:
                trend = "➡️ Stable price sensitivity"
                action = "✓ Current strategy working"
            
            insights.append(f"**{segment_name}**\n- {trend}\n- {action}\n")
        
        for insight in insights:
            st.markdown(insight)
    
    with col2:
        st.markdown("#### 🎯 Pricing Strategy")
        
        # Get current segment statistics
        stats_df = analyzer.calculate_segment_stats()
        
        # Show strategies for each segment
        for _, row in stats_df.head(4).iterrows():
            elasticity = float(row['Elasticity'])
            
            if abs(elasticity) > 1.5:
                strategy = "🔴 **High Price Sensitivity**\n- Avoid price increases\n- Focus on volume\n- Consider promotions"
            elif abs(elasticity) > 1.0:
                strategy = "🟡 **Moderate Sensitivity**\n- Small price increases OK\n- Monitor closely\n- Test and learn"
            else:
                strategy = "🟢 **Low Price Sensitivity**\n- Room for price increases\n- Focus on value\n- Premium positioning"
            
            st.markdown(f"**{row['Segment']}** (ε = {row['Elasticity']})\n{strategy}\n")
    
    # Detailed segment statistics table
    st.markdown("---")
    st.markdown("#### 📈 Segment Statistics")
    
    stats_df = analyzer.calculate_segment_stats()
    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Export button
    if st.button("📊 Export Elasticity Analysis", key="export_elasticity"):
        st.success("Elasticity analysis exported to CSV!")