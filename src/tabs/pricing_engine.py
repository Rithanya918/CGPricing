"""
Ultra-Fast Pricing Engine - Loads Instantly
No heavy computation on initial load
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ===================================================================
# RENDER FUNCTION (Loads Instantly)
# ===================================================================

def render():
    """
    Main function - optimized for instant loading
    """
    
    # Add custom CSS for visible scrollbars
    st.markdown("""
    <style>
    /* Make scrollbars visible */
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        background-color: white;
    }
    
    /* Scrollbar styling for better visibility */
    .stDataFrame div[data-testid="stDataFrameResizable"] ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    .stDataFrame div[data-testid="stDataFrameResizable"] ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .stDataFrame div[data-testid="stDataFrameResizable"] ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
        border: 2px solid #f1f1f1;
    }
    
    .stDataFrame div[data-testid="stDataFrameResizable"] ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Firefox scrollbar */
    .stDataFrame div[data-testid="stDataFrameResizable"] {
        scrollbar-width: auto;
        scrollbar-color: #888 #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Show immediately
    st.markdown("## Pricing Engine")
    st.markdown("AI-powered dynamic pricing recommendations")
    
    # Initialize session state for caching
    if 'products_loaded' not in st.session_state:
        st.session_state.products_loaded = False
        st.session_state.products_df = None
        st.session_state.recommendations_cache = None
        st.session_state.last_ml_weight = None
        st.session_state.base_calculations = None  # Store rules and ML prices

    
    # Create tabs immediately (no waiting)
    tab1, tab2 = st.tabs(["All Products", " Single Product"])
    
    with tab1:
        show_all_products_tab()
    
    with tab2:
        show_single_product_tab()


def show_all_products_tab():
    """All products - lazy loading"""
    
    st.markdown("### All Products Pricing")
    
    # ML Weight Slider
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ml_weight = st.slider(
            "ML Weight (0 = Rules only, 1 = ML only)",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            key="ml_weight_slider",
            help="Adjust the balance between rules-based and ML-based pricing"
        )
    
    with col2:
        st.markdown("")  # Spacing
        st.markdown(f"**Current Mix:** {(1-ml_weight)*100:.0f}% Rules + {ml_weight*100:.0f}% ML")
    
    # Check if ML weight changed and we have existing data
    if (st.session_state.get('recommendations_cache') is not None and 
        st.session_state.get('base_calculations') is not None and
        st.session_state.get('last_ml_weight') != ml_weight):
        
        # Recalculate hybrid prices with new ML weight
        updated_recommendations = []
        base_calcs = st.session_state.base_calculations
        
        with st.spinner(f"Recalculating hybrid prices with {ml_weight:.0%} ML weight..."):
            for base_calc in base_calcs:
                # Extract stored values
                base_price = base_calc['base_price']
                rules_adjustment = base_calc['rules_adjustment']
                ml_adjustment = base_calc['ml_adjustment']
                cost = base_calc['cost']
                
                # Recalculate hybrid price with new ML weight
                blended_adjustment = (1 - ml_weight) * rules_adjustment + ml_weight * ml_adjustment
                hybrid_price = base_price * (1 + blended_adjustment)
                hybrid_delta = blended_adjustment * 100
                margin_pct = ((hybrid_price - cost) / hybrid_price * 100) if hybrid_price > 0 else 0
                
                # Regenerate smart tags with new hybrid delta
                smart_tags = generate_smart_tags(
                    demand_index=base_calc['demand_index'],
                    price_change_pct=hybrid_delta,
                    margin_pct=margin_pct,
                    lifecycle=base_calc['lifecycle'],
                    market_out_of_stock=base_calc['market_oos'],
                    tier=base_calc['tier'],
                    base_price=base_price,
                    cost=cost
                )
                
                # Create updated recommendation
                updated_recommendations.append({
                    'SKU': base_calc['sku'],
                    'Product': base_calc['product_name'],
                    'Tier': base_calc['tier'].upper(),
                    'Base Price': f"${base_price:.2f}",
                    'Rules Price': f"${base_calc['rules_price']:.2f}",
                    'ML Price': f"${base_calc['ml_price']:.2f}",
                    'Hybrid Price': f"${hybrid_price:.2f}",
                    'Season': base_calc['season'],
                    'Time of Day': base_calc['time_of_day'],
                    'End of Month': base_calc['end_of_month'],
                    'Smart Tags': smart_tags[:50] + '...' if len(smart_tags) > 50 else smart_tags,
                    'Demand': f"{base_calc['demand_index']:.2f}",
                    'Lifecycle': base_calc['lifecycle']
                })
        
        # Update cache
        st.session_state.recommendations_cache = updated_recommendations
        st.session_state.last_ml_weight = ml_weight
        
        st.success(f"✅ Updated {len(updated_recommendations)} products with new ML weight: {ml_weight:.0%}")
        
        # Show updated results
        st.dataframe(
            pd.DataFrame(updated_recommendations),
            use_container_width=True,
            height=600
        )
        
        # Show summary stats
        st.markdown("---")
        st.markdown("### Summary Statistics")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Products", len(updated_recommendations))
        
        with col2:
            increases = sum(1 for r in updated_recommendations if float(r['Hybrid Price'].replace('$', '')) > float(r['Base Price'].replace('$', '')))
            st.metric("Price Increases", increases)
        
        with col3:
            decreases = sum(1 for r in updated_recommendations if float(r['Hybrid Price'].replace('$', '')) < float(r['Base Price'].replace('$', '')))
            st.metric("Price Decreases", decreases)
        
        with col4:
            avg_change = sum((float(r['Hybrid Price'].replace('$', '')) - float(r['Base Price'].replace('$', ''))) / float(r['Base Price'].replace('$', '')) * 100 for r in updated_recommendations) / len(updated_recommendations)
            st.metric("Avg Change", f"{avg_change:+.1f}%")
        
        with col5:
            with_tags = sum(1 for r in updated_recommendations if r['Smart Tags'] != 'No tags')
            st.metric("Products w/ Tags", with_tags)
        
        st.info(f"💡 ML Weight: {ml_weight:.0%} (Rules: {(1-ml_weight):.0%}, ML: {ml_weight:.0%})")
        
        # Exit early - don't show the button
        return
    
    # Don't load until user clicks
    if st.button("Load Product Data", type="primary", use_container_width=True):
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Load data
            status_text.text("Loading product data...")
            progress_bar.progress(20)
            
            products_df = load_product_data()
            
            if products_df.empty:
                st.error(" No product data found")
                st.info("Please ensure ProductLibrary.xlsx exists with columns: SKU, Product_Name, Base_Price, Tier")
                return
            
            progress_bar.progress(40)
            status_text.text(f"Loaded {len(products_df)} products")
            
            # Step 2: Check ML engine
            progress_bar.progress(50)
            status_text.text("Checking ML engine...")
            
            engine, ml_available = get_ml_engine()
            
            if not ml_available:
                st.warning(" ML Engine not available - showing data only")
                progress_bar.progress(100)
                status_text.text("Complete!")
                
                # Show simple table
                st.dataframe(products_df.head(100), use_container_width=True, height=600)
                return
            
            progress_bar.progress(60)
            status_text.text("ML Engine ready")
            
            # Step 3: Generate recommendations (for all products)
            total_products = len(products_df)
            status_text.text(f"Generating recommendations for all {total_products} products...")
            progress_bar.progress(70)
            
            recommendations = []
            
            # Reset base calculations for fresh load
            st.session_state.base_calculations = []
            
            # Process all products
            subset = products_df
            
            # Get ML weight from slider (if exists, otherwise use default)
            ml_weight = st.session_state.get('ml_weight_slider', 0.5)
            
            for idx, (_, row) in enumerate(subset.iterrows()):
                
                # Update progress
                if idx % 10 == 0:  # Update every 10 products
                    progress = 70 + (idx / len(subset) * 25)
                    progress_bar.progress(int(progress))
                    status_text.text(f"Processing product {idx+1}/{len(subset)}...")
                
                try:
                    sku = str(row.get('SKU', ''))
                    product_name = str(row.get('Product_Name', 'Unknown'))[:30]
                    base_price = float(row.get('Base_Price', 0))
                    cost = float(row.get('cost', base_price * 0.70))
                    tier = str(row.get('Tier', 'Mid'))
                    category = str(row.get('Category', 'Other'))
                    lifecycle = str(row.get('Product_Lifecycle', 'Maturity'))
                    demand_index = float(row.get('demand_index', 1.0))
                    
                    # Get competitor data
                    competitor_avg = base_price
                    market_oos = False
                    if 'market_out_of_stock' in row.index:
                        market_oos = bool(row['market_out_of_stock'])
                    
                    # Get Rules price (ML weight = 0)
                    engine_rules, _ = get_ml_engine(0.0)
                    rec_rules = engine_rules.get_recommendation(
                        product_name=product_name,
                        base_price=base_price,
                        cost=cost,
                        tier=tier,
                        category=category,
                        lifecycle=lifecycle,
                        competitor_avg=competitor_avg,
                        market_oos=market_oos,
                        demand_index=demand_index
                    )
                    rules_price = rec_rules.get('recommended_price', base_price)
                    rules_adjustment = (rules_price - base_price) / base_price if base_price > 0 else 0
                    
                    # Get ML price (ML weight = 1)
                    engine_ml, _ = get_ml_engine(1.0)
                    rec_ml = engine_ml.get_recommendation(
                        product_name=product_name,
                        base_price=base_price,
                        cost=cost,
                        tier=tier,
                        category=category,
                        lifecycle=lifecycle,
                        competitor_avg=competitor_avg,
                        market_oos=market_oos,
                        demand_index=demand_index
                    )
                    ml_price = rec_ml.get('recommended_price', base_price)
                    ml_adjustment = (ml_price - base_price) / base_price if base_price > 0 else 0
                    
                    # Calculate Hybrid price using blending formula (matches app.py logic)
                    # Hybrid = (1 - ml_weight) * rules_adjustment + ml_weight * ml_adjustment
                    blended_adjustment = (1 - ml_weight) * rules_adjustment + ml_weight * ml_adjustment
                    hybrid_price = base_price * (1 + blended_adjustment)
                    
                    # Calculate margin based on hybrid price
                    margin_pct = ((hybrid_price - cost) / hybrid_price * 100) if hybrid_price > 0 else 0
                    
                    # Calculate deltas
                    hybrid_delta = ((hybrid_price - base_price) / base_price * 100) if base_price > 0 else 0
                    
                    # Generate smart tags
                    smart_tags = generate_smart_tags(
                        demand_index=demand_index,
                        price_change_pct=hybrid_delta,
                        margin_pct=margin_pct,
                        lifecycle=lifecycle,
                        market_out_of_stock=market_oos,
                        tier=tier,
                        base_price=base_price,
                        cost=cost
                    )
                    
                    # Default context values (can be customized)
                    season = "Normal"
                    time_of_day = "Peak"
                    end_of_month = "No"
                    
                    # Store base calculation for efficient recalculation
                    st.session_state.base_calculations.append({
                        'sku': sku,
                        'product_name': product_name,
                        'tier': tier,
                        'base_price': base_price,
                        'cost': cost,
                        'rules_price': rules_price,
                        'rules_adjustment': rules_adjustment,
                        'ml_price': ml_price,
                        'ml_adjustment': ml_adjustment,
                        'demand_index': demand_index,
                        'lifecycle': lifecycle,
                        'market_oos': market_oos,
                        'season': season,
                        'time_of_day': time_of_day,
                        'end_of_month': end_of_month
                    })
                    
                    recommendations.append({
                        'SKU': sku,
                        'Product': product_name,
                        'Tier': tier.upper(),
                        'Base Price': f"${base_price:.2f}",
                        'Rules Price': f"${rules_price:.2f}",
                        'ML Price': f"${ml_price:.2f}",
                        'Hybrid Price': f"${hybrid_price:.2f}",
                        'Season': season,
                        'Time of Day': time_of_day,
                        'End of Month': end_of_month,
                        'Smart Tags': smart_tags[:50] + '...' if len(smart_tags) > 50 else smart_tags,
                        'Demand': f"{demand_index:.2f}",
                        'Lifecycle': lifecycle
                    })
                    
                except Exception as e:
                    continue
            
            progress_bar.progress(95)
            status_text.text("Finalizing...")
            
            if recommendations:
                progress_bar.progress(100)
                status_text.text(" Complete!")
                
                # Store initial data in session state
                if 'all_products_df' not in st.session_state:
                    st.session_state.all_products_df = products_df
                    st.session_state.recommendations_cache = recommendations
                    st.session_state.current_batch = 1  # Already loaded first batch
                    st.session_state.last_ml_weight = ml_weight  # Store initial ML weight
                
                # Get all accumulated recommendations
                all_recs = st.session_state.get('recommendations_cache', recommendations)
                
                st.success(f" Generated {len(all_recs)} recommendations")
                
                # Show results
                st.dataframe(
                    pd.DataFrame(all_recs),
                    use_container_width=True,
                    height=600
                )
                
                # Enhanced Stats
                st.markdown("---")
                st.markdown("### Summary Statistics")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Total Products", len(all_recs))
                
                with col2:
                    # Count products with price increases
                    increases = sum(1 for r in all_recs if float(r['Hybrid Price'].replace('$', '')) > float(r['Base Price'].replace('$', '')))
                    st.metric("Price Increases", increases)
                
                with col3:
                    # Count products with price decreases
                    decreases = sum(1 for r in all_recs if float(r['Hybrid Price'].replace('$', '')) < float(r['Base Price'].replace('$', '')))
                    st.metric("Price Decreases", decreases)
                
                with col4:
                    # Average price change
                    avg_change = sum((float(r['Hybrid Price'].replace('$', '')) - float(r['Base Price'].replace('$', ''))) / float(r['Base Price'].replace('$', '')) * 100 for r in all_recs) / len(all_recs)
                    st.metric("Avg Change", f"{avg_change:+.1f}%")
                
                with col5:
                    # Count products with tags
                    with_tags = sum(1 for r in all_recs if r['Smart Tags'] != 'No tags')
                    st.metric("Products w/ Tags", with_tags)
                
                # Show completion message
                st.success(f" All {len(all_recs)} products loaded! ML Weight: {ml_weight:.0%} (Rules: {(1-ml_weight):.0%}, ML: {ml_weight:.0%})")
            else:
                st.error("❌ Failed to generate recommendations")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
            import traceback
            with st.expander(" Error Details"):
                st.code(traceback.format_exc())
    
    else:
        # Not loaded yet - show preview
        st.info(" Click 'Load Product Data' to see pricing recommendations for all products")
        

def load_next_batch(ml_weight, engine):
    """Load next 30 products incrementally"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        products_df = st.session_state.all_products_df
        current_batch = st.session_state.get('current_batch', 1)
        
        # Calculate batch range
        batch_size = 30
        start_idx = current_batch * batch_size
        end_idx = min(start_idx + batch_size, len(products_df))
        
        if start_idx >= len(products_df):
            st.warning("No more products to load")
            return
        
        subset = products_df.iloc[start_idx:end_idx]
        
        status_text.text(f"Loading products {start_idx + 1} to {end_idx}...")
        progress_bar.progress(20)
        
        new_recommendations = []
        
        for idx, (_, row) in enumerate(subset.iterrows()):
            
            # Update progress
            if idx % 5 == 0:
                progress = 20 + (idx / len(subset) * 70)
                progress_bar.progress(int(progress))
                status_text.text(f"Processing product {start_idx + idx + 1}/{len(products_df)}...")
            
            try:
                sku = str(row.get('SKU', ''))
                product_name = str(row.get('Product_Name', 'Unknown'))[:30]
                base_price = float(row.get('Base_Price', 0))
                cost = float(row.get('cost', base_price * 0.70))
                tier = str(row.get('Tier', 'Mid'))
                category = str(row.get('Category', 'Other'))
                lifecycle = str(row.get('Product_Lifecycle', 'Maturity'))
                demand_index = float(row.get('demand_index', 1.0))
                
                # Get competitor data
                competitor_avg = base_price
                market_oos = False
                if 'market_out_of_stock' in row.index:
                    market_oos = bool(row['market_out_of_stock'])
                
                # Get Rules price (ML weight = 0)
                engine_rules, _ = get_ml_engine(0.0)
                rec_rules = engine_rules.get_recommendation(
                    product_name=product_name,
                    base_price=base_price,
                    cost=cost,
                    tier=tier,
                    category=category,
                    lifecycle=lifecycle,
                    competitor_avg=competitor_avg,
                    market_oos=market_oos,
                    demand_index=demand_index
                )
                rules_price = rec_rules.get('recommended_price', base_price)
                
                # Get ML price (ML weight = 1)
                engine_ml, _ = get_ml_engine(1.0)
                rec_ml = engine_ml.get_recommendation(
                    product_name=product_name,
                    base_price=base_price,
                    cost=cost,
                    tier=tier,
                    category=category,
                    lifecycle=lifecycle,
                    competitor_avg=competitor_avg,
                    market_oos=market_oos,
                    demand_index=demand_index
                )
                ml_price = rec_ml.get('recommended_price', base_price)
                
                # Get Hybrid price (current ML weight)
                rec_hybrid = engine.get_recommendation(
                    product_name=product_name,
                    base_price=base_price,
                    cost=cost,
                    tier=tier,
                    category=category,
                    lifecycle=lifecycle,
                    competitor_avg=competitor_avg,
                    market_oos=market_oos,
                    demand_index=demand_index
                )
                hybrid_price = rec_hybrid.get('recommended_price', base_price)
                margin_pct = rec_hybrid.get('margin_pct', 0)
                
                # Calculate deltas
                hybrid_delta = ((hybrid_price - base_price) / base_price * 100) if base_price > 0 else 0
                
                # Generate smart tags
                smart_tags = generate_smart_tags(
                    demand_index=demand_index,
                    price_change_pct=hybrid_delta,
                    margin_pct=margin_pct,
                    lifecycle=lifecycle,
                    market_out_of_stock=market_oos,
                    tier=tier,
                    base_price=base_price,
                    cost=cost
                )
                
                # Default context values
                season = "Normal"
                time_of_day = "Peak"
                end_of_month = "No"
                
                new_recommendations.append({
                    'SKU': sku,
                    'Product': product_name,
                    'Tier': tier.upper(),
                    'Base Price': f"${base_price:.2f}",
                    'Rules Price': f"${rules_price:.2f}",
                    'ML Price': f"${ml_price:.2f}",
                    'Hybrid Price': f"${hybrid_price:.2f}",
                    'Season': season,
                    'Time of Day': time_of_day,
                    'End of Month': end_of_month,
                    'Smart Tags': smart_tags[:50] + '...' if len(smart_tags) > 50 else smart_tags,
                    'Demand': f"{demand_index:.2f}",
                    'Lifecycle': lifecycle
                })
                
            except Exception as e:
                print(f"Error processing product: {e}")
                continue
        
        progress_bar.progress(95)
        status_text.text("Finalizing...")
        
        if new_recommendations:
            # Add to cache
            st.session_state.recommendations_cache.extend(new_recommendations)
            st.session_state.current_batch += 1
            
            progress_bar.progress(100)
            status_text.text(f"Loaded {len(new_recommendations)} more products!")
            
            # Force rerun to update display
            st.rerun()
        else:
            st.error("Failed to load more products")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        with st.expander(" Error Details"):
            st.code(traceback.format_exc())


def show_single_product_tab():
    """Single product - fast and interactive"""
    
    st.markdown("### 🎯 Single Product Pricing")
    st.markdown("Calculate optimized pricing for one specific product")
    
    # Load data on demand
    try:
        products_df = load_product_data()
        
        if products_df.empty:
            st.warning("No product data available")
            return
        
        # Product selection
        sku_options = ["Select a product..."]
        for _, row in products_df.head(50).iterrows():  # Limit to 50 for dropdown speed
            sku = str(row['SKU'])
            name = str(row.get('Product_Name', 'Unknown'))[:40]
            sku_options.append(f"{sku} – {name}")
        
        selected = st.selectbox("Select Product", sku_options)
        
        if selected == "Select a product...":
            st.info(" Select a product to calculate pricing")
            return
        
        selected_sku = selected.split(" – ")[0]
        
        # Get product
        product_row = products_df[products_df['SKU'].astype(str) == selected_sku]
        
        if product_row.empty:
            st.error(f"Product {selected_sku} not found")
            return
        
        product_row = product_row.iloc[0]
        
        # Show product info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Product Information**")
            st.markdown(f"**SKU:** {selected_sku}")
            st.markdown(f"**Name:** {product_row.get('Product_Name', 'Unknown')}")
            st.markdown(f"**Category:** {product_row.get('Category', 'Other')}")
        
        with col2:
            st.markdown("**Current Metrics**")
            st.markdown(f"**Base Price:** ${float(product_row.get('Base_Price', 0)):.2f}")
            st.markdown(f"**Tier:** {product_row.get('Tier', 'Mid')}")
            st.markdown(f"**Lifecycle:** {product_row.get('Product_Lifecycle', 'Maturity')}")
        
        st.markdown("---")
        
        # Business context
        st.markdown("**Pricing Context**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            season = st.radio("Season", ["Normal", "Busy", "Slow"], index=0)
        
        with col2:
            time_of_day = st.radio("Time", ["Peak", "Off-Peak"], index=0)
        
        with col3:
            end_of_month = st.checkbox("End of Month", value=False)
        
        ml_weight = st.slider("ML Weight", 0.0, 1.0, 0.5, 0.05)
        
        # Calculate button
        if st.button("Calculate Price", type="primary", use_container_width=True):
            
            with st.spinner("Calculating optimal price..."):
                
                try:
                    # Get engine
                    engine, ml_available = get_ml_engine(ml_weight)
                    
                    if not ml_available:
                        st.error("ML Engine not available")
                        return
                    
                    # Product details
                    product_name = str(product_row.get('Product_Name', 'Unknown'))
                    base_price = float(product_row.get('Base_Price', 0))
                    cost = float(product_row.get('cost', base_price * 0.70))
                    tier = str(product_row.get('Tier', 'Mid'))
                    category = str(product_row.get('Category', 'Other'))
                    lifecycle = str(product_row.get('Product_Lifecycle', 'Maturity'))
                    demand_index = float(product_row.get('demand_index', 1.0))
                    
                    # Get recommendation
                    rec = engine.get_recommendation(
                        product_name=product_name,
                        base_price=base_price,
                        cost=cost,
                        tier=tier,
                        category=category,
                        lifecycle=lifecycle,
                        competitor_avg=base_price,
                        market_oos=False,
                        demand_index=demand_index
                    )
                    
                    hybrid_price = rec.get('recommended_price', base_price)
                    
                    # Apply business adjustments
                    adjustments = []
                    
                    if season == "Busy":
                        hybrid_price *= 1.10
                        adjustments.append("Season (Busy): +10%")
                    elif season == "Slow":
                        hybrid_price *= 0.90
                        adjustments.append("Season (Slow): -10%")
                    
                    if time_of_day == "Off-Peak":
                        hybrid_price *= 0.95
                        adjustments.append("Time (Off-Peak): -5%")
                    
                    if end_of_month:
                        hybrid_price *= 0.98
                        adjustments.append("End of Month: -2%")
                    
                    hybrid_delta = ((hybrid_price - base_price) / base_price * 100)
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("###  Pricing Results")
                    
                    # Price comparison
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Base Price",
                            f"${base_price:.2f}",
                            help="Current price"
                        )
                    
                    with col2:
                        st.metric(
                            "Recommended Price",
                            f"${hybrid_price:.2f}",
                            f"{hybrid_delta:+.1f}%",
                            delta_color="normal"
                        )
                    
                    with col3:
                        margin = ((hybrid_price - cost) / hybrid_price * 100) if hybrid_price > 0 else 0
                        st.metric(
                            "Margin",
                            f"{margin:.1f}%",
                            help=f"Cost: ${cost:.2f}"
                        )
                    
                    # Adjustments applied
                    if adjustments:
                        st.markdown("**Adjustments Applied:**")
                        for adj in adjustments:
                            st.markdown(f"- {adj}")
                    
                    # Context summary
                    with st.expander("Calculation Details"):
                        st.markdown(f"""
**Base Calculation:**
- Base Price: ${base_price:.2f}
- Cost: ${cost:.2f}
- ML Weight: {ml_weight:.0%}

**Context:**
- Season: {season}
- Time: {time_of_day}
- End of Month: {'Yes' if end_of_month else 'No'}

**Final Price:** ${hybrid_price:.2f} ({hybrid_delta:+.1f}%)
                        """)
                    
                    st.success("Price calculated successfully!")
                    
                except Exception as e:
                    st.error(f" Calculation Error: {str(e)}")
                    
                    import traceback
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")


# ===================================================================
# HELPER FUNCTIONS (Optimized for Speed)
# ===================================================================

def generate_smart_tags(
    demand_index,
    price_change_pct,
    margin_pct,
    lifecycle,
    market_out_of_stock=False,
    tier=None,
    base_price=None,
    cost=None
):
    """Generate smart tags with relaxed thresholds."""
    tags = []
    
    # Lifecycle (priority)
    lifecycle_lower = str(lifecycle).lower().strip()
    if lifecycle_lower in ['introduction', 'launch', 'new']:
        tags.append("New arrival")
    elif lifecycle_lower == 'growth':
        tags.append("Growing")
    elif lifecycle_lower == 'decline':
        tags.append("End-of-life")
    
    # Demand
    if demand_index is not None:
        if demand_index >= 1.3:
            tags.append("Very High Demand")
        elif demand_index >= 1.15:
            tags.append("High Demand")
        elif demand_index <= 0.75:
            tags.append("Low Demand")
    
    # Price changes (≥2% threshold)
    if price_change_pct is not None and abs(price_change_pct) >= 2:
        if price_change_pct >= 10:
            tags.append("↗ Large Increase")
        elif price_change_pct >= 3:
            tags.append("↗ Price Increase")
        elif price_change_pct <= -10:
            tags.append("↘ Large Discount")
        elif price_change_pct <= -3:
            tags.append("↘ Price Decrease")
    
    # Margin
    if margin_pct is not None:
        if margin_pct >= 35:
            tags.append("Exceptional Margin")
        elif margin_pct >= 28:
            tags.append("Premium Margin")
        elif margin_pct >= 18:
            tags.append("Healthy Margin")
        elif margin_pct <= 10:
            tags.append("Low Margin")
    
    # Competitive
    if market_out_of_stock:
        tags.append(" Competitor Out-of-Stock")
    
    # Tier
    if tier:
        tier_lower = str(tier).lower().strip()
        if tier_lower == 'premium':
            tags.append("Premium Tier")
    
    # Margin watch
    if base_price and cost and tier:
        tier_configs = {'low': 0.10, 'mid': 0.15, 'high': 0.20, 'premium': 0.25}
        tier_lower = str(tier).lower().strip()
        min_margin = tier_configs.get(tier_lower, 0.15)
        current_margin = (base_price - cost) / base_price if base_price > 0 else 0
        margin_buffer = current_margin - min_margin
        
        if 0 <= margin_buffer <= 0.02:
            tags.append(" Margin Watch")
    
    return ", ".join(tags) if tags else "No tags"


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_product_data():
    """Load product data with caching"""
    
    try:
        # Try data_loader first
        from data_loader import get_product_data
        return get_product_data()
    except:
        pass
    
    try:
        # Try direct Excel load
        df = pd.read_excel("ProductLibrary.xlsx", engine='openpyxl')
        return df
    except:
        return pd.DataFrame()


@st.cache_resource  # Cache engine instance
def get_ml_engine(ml_weight=0.5):
    """Get ML engine with caching"""
    
    try:
        from ml_engine import PricingEngine
        engine = PricingEngine(ml_weight=ml_weight)
        return engine, True
    except:
        return None, False


# ===================================================================
# END OF FILE
# ===================================================================