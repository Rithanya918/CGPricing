"""
Analytics Tab - Deep dive analytics and visualizations
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def get_data():
    """Lazy import to avoid circular import issues."""
    from data import mock_pricing_data, revenue_data
    return mock_pricing_data, revenue_data


def render():
    """Render the Analytics tab"""
    
    # Get data using lazy import
    mock_pricing_data, revenue_data = get_data()
    
    st.markdown("### 📈 Advanced Analytics")
    
    # Time range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        date_range = st.date_input(
            "Date Range",
            value=(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-06-30')),
            key="analytics_date_range"
        )
    
    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Overview", "Category Deep Dive", "Competitor Analysis", "Trend Analysis"],
            key="analysis_type"
        )
    
    with col3:
        if st.button("🔄 Refresh", key="refresh_analytics"):
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #d4af37; margin: 0;">💰 Total Revenue</h4>
            <h2 style="color: #10b981; margin: 10px 0;">$341K</h2>
            <p style="color: #10b981; margin: 0;">📈 +18.5% YTD</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #d4af37; margin: 0;">📊 Avg Margin</h4>
            <h2 style="color: #3b82f6; margin: 10px 0;">20.1%</h2>
            <p style="color: #10b981; margin: 0;">📈 +2.3% vs target</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #d4af37; margin: 0;">🎯 Optimization</h4>
            <h2 style="color: #a855f7; margin: 10px 0;">92.8%</h2>
            <p style="color: #10b981; margin: 0;">📈 +4.2% improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #d4af37; margin: 0;">📦 Products</h4>
            <h2 style="color: #f59e0b; margin: 10px 0;">103</h2>
            <p style="color: #c9a6ae; margin: 0;">Actively managed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Charts Section
    tab1, tab2, tab3 = st.tabs(["📊 Revenue Analysis", "🎯 Category Performance", "🔄 Price Changes"])
    
    with tab1:
        # Revenue breakdown chart
        st.markdown("#### Revenue by Month")
        
        df_revenue = pd.DataFrame(revenue_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_revenue['month'],
            y=df_revenue['current'],
            name='Current',
            marker_color='#8B1538'
        ))
        
        fig.add_trace(go.Bar(
            x=df_revenue['month'],
            y=df_revenue['optimized'],
            name='Optimized',
            marker_color='#d4af37'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_revenue['month'],
            y=df_revenue['profit'],
            name='Profit',
            mode='lines+markers',
            marker=dict(size=10, color='#10b981'),
            line=dict(color='#10b981', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(29, 20, 25, 0.8)',
            plot_bgcolor='rgba(29, 20, 25, 0.8)',
            font=dict(color='#c9a6ae'),
            xaxis=dict(showgrid=False),
            yaxis=dict(title='Revenue ($)', showgrid=True, gridcolor='rgba(139, 21, 56, 0.2)'),
            yaxis2=dict(title='Profit ($)', overlaying='y', side='right', showgrid=False),
            barmode='group',
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_current = sum([r['current'] for r in revenue_data])
            st.metric("Current Revenue (6M)", f"${total_current:,}", "+12.5%")
        
        with col2:
            total_optimized = sum([r['optimized'] for r in revenue_data])
            st.metric("Optimized Revenue (6M)", f"${total_optimized:,}", "+18.7%")
        
        with col3:
            total_profit = sum([r['profit'] for r in revenue_data])
            st.metric("Total Profit (6M)", f"${total_profit:,}", "+15.3%")
    
    with tab2:
        # Category performance
        st.markdown("#### Performance by Category")
        
        df_products = pd.DataFrame(mock_pricing_data)
        
        # Category breakdown
        category_stats = df_products.groupby('category').agg({
            'currentPrice': 'mean',
            'optimizedPrice': 'mean',
            'margin': 'mean',
            'product': 'count'
        }).reset_index()
        category_stats.columns = ['Category', 'Avg Current Price', 'Avg Optimized Price', 'Avg Margin', 'Product Count']
        
        # Create sunburst chart
        fig_sunburst = go.Figure(go.Sunburst(
            labels=['All Products'] + list(category_stats['Category']),
            parents=[''] + ['All Products'] * len(category_stats),
            values=[category_stats['Product Count'].sum()] + list(category_stats['Product Count']),
            marker=dict(
                colors=['#8B1538'] + ['#d4af37', '#a01d48', '#c9a6ae', '#8B1538', '#d4af37', '#a01d48', '#c9a6ae'][:len(category_stats)]
            ),
            textinfo='label+percent parent'
        ))
        
        fig_sunburst.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(29, 20, 25, 0.8)',
            height=400
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Category table
        st.markdown("#### Category Details")
        
        # Style the dataframe
        styled_df = category_stats.style.format({
            'Avg Current Price': '${:.2f}',
            'Avg Optimized Price': '${:.2f}',
            'Avg Margin': '{:.1f}%',
            'Product Count': '{:.0f}'
        }).background_gradient(cmap='RdYlGn', subset=['Avg Margin'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    with tab3:
        # Price change analysis
        st.markdown("#### Price Change Distribution")
        
        df_products = pd.DataFrame(mock_pricing_data)
        
        # Create histogram of price changes
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Histogram(
            x=df_products['change'],
            nbinsx=15,
            marker=dict(
                color=df_products['change'],
                colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
                line=dict(color='#8B1538', width=1)
            ),
            name='Price Changes'
        ))
        
        fig_hist.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(29, 20, 25, 0.8)',
            plot_bgcolor='rgba(29, 20, 25, 0.8)',
            font=dict(color='#c9a6ae'),
            xaxis=dict(title='Price Change (%)', showgrid=True, gridcolor='rgba(139, 21, 56, 0.2)'),
            yaxis=dict(title='Number of Products', showgrid=True, gridcolor='rgba(139, 21, 56, 0.2)'),
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Price change stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            increases = len(df_products[df_products['change'] > 0])
            st.metric("Price Increases", increases, f"{increases/len(df_products)*100:.0f}%")
        
        with col2:
            decreases = len(df_products[df_products['change'] < 0])
            st.metric("Price Decreases", decreases, f"{decreases/len(df_products)*100:.0f}%")
        
        with col3:
            avg_change = df_products['change'].mean()
            st.metric("Avg Change", f"{avg_change:.1f}%", "Overall impact")
        
        with col4:
            max_change = df_products['change'].max()
            st.metric("Max Change", f"{max_change:.1f}%", df_products[df_products['change'] == max_change]['product'].values[0])
    
    # Advanced Analytics Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔬 Advanced Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Margin vs Demand Correlation")
        
        df_products = pd.DataFrame(mock_pricing_data)
        demand_map = {'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        df_products['demand_score'] = df_products['demand'].map(demand_map)
        
        fig_scatter = go.Figure()
        
        fig_scatter.add_trace(go.Scatter(
            x=df_products['demand_score'],
            y=df_products['margin'],
            mode='markers',
            marker=dict(
                size=df_products['currentPrice'] * 2,
                color=df_products['margin'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Margin %"),
                line=dict(color='#8B1538', width=1)
            ),
            text=df_products['product'],
            hovertemplate='<b>%{text}</b><br>Demand: %{x}<br>Margin: %{y:.1f}%<extra></extra>'
        ))
        
        fig_scatter.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(29, 20, 25, 0.8)',
            plot_bgcolor='rgba(29, 20, 25, 0.8)',
            font=dict(color='#c9a6ae'),
            xaxis=dict(title='Demand Level', showgrid=True, gridcolor='rgba(139, 21, 56, 0.2)',
                      ticktext=['Low', 'Medium', 'High', 'Very High'],
                      tickvals=[1, 2, 3, 4]),
            yaxis=dict(title='Margin (%)', showgrid=True, gridcolor='rgba(139, 21, 56, 0.2)'),
            height=350
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Tier Distribution")
        
        tier_counts = df_products['tier'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=tier_counts.index,
            values=tier_counts.values,
            hole=.4,
            marker=dict(colors=['#8B1538', '#d4af37', '#a01d48']),
            textinfo='label+percent',
            textfont=dict(color='#fff')
        )])
        
        fig_pie.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(29, 20, 25, 0.8)',
            font=dict(color='#c9a6ae'),
            height=350,
            showlegend=True
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Export Options
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Full Report", key="export_full_analytics"):
            st.success("Comprehensive analytics report exported!")
    
    with col2:
        if st.button("📈 Download Charts", key="download_charts"):
            st.info("Downloading visualization package...")
    
    with col3:
        if st.button("📧 Email Report", key="email_analytics"):
            st.success("Report sent to your email!")
