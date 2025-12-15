"""
Overview Tab - With Proper SVG Icons (No Emojis)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import time
from datetime import datetime


def get_overview_data():
    """Lazy import to avoid circular import issues."""
    from data import revenue_data, competitor_data, elasticity_data
    return revenue_data, competitor_data, elasticity_data

# API Configuration
API_URL_KEY = "ml_forecast_api_url"

def check_forecast_api_health(api_url):
    """Check if ML Forecast API is accessible"""
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_demand_forecast(api_url):
    """Get demand forecast from ML API"""
    try:
        response = requests.get(
            f"{api_url}/forecast/demand",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Forecast API Error: {str(e)}")
        return None

def render():
    """Render the Overview tab with proper icons"""
    
    # Load data using lazy import
    revenue_data, competitor_data, elasticity_data = get_overview_data()
    
    # Initialize session state for API connection
    if API_URL_KEY not in st.session_state:
        st.session_state[API_URL_KEY] = ""
    if 'forecast_api_connected' not in st.session_state:
        st.session_state.forecast_api_connected = False
    if 'forecast_data' not in st.session_state:
        st.session_state.forecast_data = None
    if 'show_forecast_setup' not in st.session_state:
        st.session_state.show_forecast_setup = False
    
    # KPI Cards Section - 4 cards in a row with SVG icons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon green">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="2" x2="12" y2="22"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
            </div>
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">$67,340</div>
            <div class="metric-change">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                    <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                +12.5% vs last month
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon pink">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
            </div>
            <div class="metric-label">Avg Profit Margin</div>
            <div class="metric-value">21.3%</div>
            <div class="metric-change">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                    <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                +3.2% improvement
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon magenta">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                    <line x1="12" y1="22.08" x2="12" y2="12"></line>
                </svg>
            </div>
            <div class="metric-label">Active Products</div>
            <div class="metric-value">103</div>
            <div class="metric-change" style="color: #c9a6ae;">
                8 pending review
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon gold">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
            </div>
            <div class="metric-label">Price Optimization</div>
            <div class="metric-value">94.2%</div>
            <div class="metric-change">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                    <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                +5.1% efficiency
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Revenue Optimization Forecast Chart
    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        
        # Chart header with dropdown
        col_title, col_dropdown = st.columns([3, 1])
        with col_title:
            st.markdown('<div class="chart-title">Revenue Optimization Forecast</div>', unsafe_allow_html=True)
        with col_dropdown:
            time_range = st.selectbox(
                "",
                ["1 Month", "3 Months", "6 Months", "1 Year"],
                index=2,
                key="overview_time_range",
                label_visibility="collapsed"
            )
        
        # Create revenue forecast chart
        df_revenue = pd.DataFrame(revenue_data)
        
        fig_revenue = go.Figure()
        
        # AI Optimized line (gold)
        fig_revenue.add_trace(go.Scatter(
            x=df_revenue['month'],
            y=df_revenue['optimized'],
            name='AI Optimized',
            mode='lines',
            line=dict(color='#d4af37', width=3),
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.1)'
        ))
        
        # Current Pricing line (burgundy)
        fig_revenue.add_trace(go.Scatter(
            x=df_revenue['month'],
            y=df_revenue['current'],
            name='Current Pricing',
            mode='lines',
            line=dict(color='#8B1538', width=3, dash='dash'),
            fill='tozeroy',
            fillcolor='rgba(139, 21, 56, 0.2)'
        ))
        
        fig_revenue.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c9a6ae', size=12),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=14, color='#d4af37')
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                color='#c9a6ae'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(139, 21, 56, 0.2)',
                zeroline=False,
                color='#c9a6ae',
                tickformat='$,.0f'
            ),
            hovermode='x unified',
            height=350,
            margin=dict(l=20, r=20, t=20, b=60)
        )
        
        st.plotly_chart(fig_revenue, use_container_width=True, key="revenue_chart")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_side:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Price Elasticity by Tier</div>', unsafe_allow_html=True)
        
        # Elasticity bar chart
        df_elasticity = pd.DataFrame(elasticity_data)
        
        fig_elasticity = go.Figure()
        
        fig_elasticity.add_trace(go.Bar(
            y=df_elasticity['tier'],
            x=df_elasticity['elasticity'],
            orientation='h',
            marker=dict(
                color=['#d4af37', '#d4af37', '#d4af37', '#d4af37'],
                opacity=[0.4, 0.6, 0.8, 1.0]
            ),
            text=df_elasticity['elasticity'],
            texttemplate='%{text:.2f}',
            textposition='inside',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{y}</b><br>Elasticity: %{x:.2f}<extra></extra>'
        ))
        
        fig_elasticity.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c9a6ae'),
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(139, 21, 56, 0.2)',
                zeroline=False,
                range=[-2, 0],
                color='#c9a6ae'
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                color='#c9a6ae'
            ),
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_elasticity, use_container_width=True, key="elasticity_chart")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Competitive Intelligence Section
    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)
    
    col_header, col_button = st.columns([4, 1])
    with col_header:
        st.markdown('<div class="section-header">Competitive Intelligence</div>', unsafe_allow_html=True)
    with col_button:
        if st.button("📥 Export Report", key="export_overview"):
            st.success("Report exported!")
    
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    
    # Competitor cards - matching the exact 4-column layout
    cols = st.columns(4)
    
    # Display first 4 competitors
    for idx, (col, comp) in enumerate(zip(cols, competitor_data[:4])):
        with col:
            st.markdown(f"""
            <div class="competitor-card">
                <div class="competitor-name">{comp['name']}</div>
                <div class="competitor-stats">
                    <div>
                        <div class="competitor-stat-label">Avg Price</div>
                        <div class="competitor-stat-value">${comp['avgPrice']:.2f}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="competitor-stat-label">Market Share</div>
                        <div class="competitor-stat-value">{comp['marketShare']}%</div>
                    </div>
                </div>
                <div class="market-share-bar">
                    <div class="market-share-fill" style="width: {comp['marketShare']}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    