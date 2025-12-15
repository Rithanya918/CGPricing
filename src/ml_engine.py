"""
ML Pricing Engine - Embedded Gradient Boosting Model
Based on Copy_of_TJCODEwSmartTags_11_30_with_GB.ipynb

This file uses the EXACT pricing rules and model parameters from your notebook.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# TIER CONFIG (from your notebook - exact values)
# =============================================================================

@dataclass
class TierConfig:
    """Exact copy from your notebook."""
    name: str
    min_margin_pct: float      # e.g., 0.10 = 10%
    change_cap_pct: float      # per adjustment cap, e.g., 0.05 = 5%

# From your notebook: TIER_CONFIGS
TIER_CONFIGS: Dict[str, TierConfig] = {
    "low": TierConfig(name="low", min_margin_pct=0.10, change_cap_pct=0.10),
    "mid": TierConfig(name="mid", min_margin_pct=0.15, change_cap_pct=0.05),
    "high": TierConfig(name="high", min_margin_pct=0.20, change_cap_pct=0.07),
    "premium": TierConfig(name="premium", min_margin_pct=0.25, change_cap_pct=0.05),
}

# =============================================================================
# PRICING RULES (from your notebook - exact values)
# =============================================================================

@dataclass
class PricingRules:
    """Exact copy from your notebook PricingRules class."""
    # Global caps
    max_above_market_pct: float = 0.15    # +15% above market average
    global_change_cap_pct: float = 0.07   # ±7% per adjustment

    # Demand
    demand_up_min: float = 0.05   # when demand high
    demand_up_max: float = 0.10
    demand_down_max: float = 0.10 # max discount when demand low

    # Competition
    market_band_low_pct: float = -0.10   # -10% below avg
    market_band_high_pct: float = 0.15   # +15% above avg
    match_drop_fraction: float = 0.5     # match 50% of competitor drop
    out_of_stock_bump_min: float = 0.05
    out_of_stock_bump_max: float = 0.10

    # Time-based
    busy_season_up_min: float = 0.10
    busy_season_up_max: float = 0.15
    slow_season_down_min: float = 0.10
    slow_season_down_max: float = 0.20
    offpeak_discount_min: float = 0.02
    offpeak_discount_max: float = 0.03
    end_of_month_extra_discount: float = 0.05

    # Lifecycle
    launch_discount: float = 0.10
    growth_increase: float = 0.05
    maturity_adjustment: float = 0.00
    decline_discount: float = 0.20

DEFAULT_RULES = PricingRules()

# =============================================================================
# HELPER FUNCTIONS (from your notebook)
# =============================================================================

def _clamp(value: float, low: float, high: float) -> float:
    """From your notebook."""
    return max(low, min(high, value))

def _pct_change(old: float, new: float) -> float:
    """From your notebook."""
    if old == 0:
        return 0.0
    return (new - old) / old

# =============================================================================
# SMART TAGS (from your notebook SmartTag module)
# =============================================================================

class SmartTagEngine:
    """
    Generate smart tags for products based on various signals.
    Based on your notebook's SmartTag system.
    """
    
    TAG_DEFINITIONS = {
        "new_arrival": {"emoji": "🆕", "label": "New Arrival", "color": "#10B981"},
        "declining": {"emoji": "📉", "label": "Declining", "color": "#EF4444"},
        "competitor_oos": {"emoji": "🏆", "label": "Competitor Out-of-Stock", "color": "#3B82F6"},
        "high_demand": {"emoji": "🔥", "label": "High Demand", "color": "#F59E0B"},
        "margin_watch": {"emoji": "⚠️", "label": "Margin Watch", "color": "#EF4444"},
        "price_leader": {"emoji": "👑", "label": "Price Leader", "color": "#C4437C"},
    }
    
    @classmethod
    def generate_tags(cls, 
                      lifecycle: str,
                      demand_index: float,
                      margin_pct: float,
                      our_price: float,
                      competitor_avg: float,
                      tier: str,
                      market_oos: bool = False) -> List[Dict[str, str]]:
        """
        Generate appropriate tags for a product.
        Based on your notebook's tag logic.
        """
        tags = []
        
        # Lifecycle tags (from your notebook)
        if lifecycle and lifecycle.lower() == "launch":
            tags.append(cls.TAG_DEFINITIONS["new_arrival"])
        elif lifecycle and lifecycle.lower() == "decline":
            tags.append(cls.TAG_DEFINITIONS["declining"])
        
        # Competitor out of stock (from your notebook)
        if market_oos:
            tags.append(cls.TAG_DEFINITIONS["competitor_oos"])
        
        # Demand tags
        if demand_index > 1.2:
            tags.append(cls.TAG_DEFINITIONS["high_demand"])
        
        # Competitive position
        if competitor_avg > 0 and our_price < competitor_avg * 0.95:
            tags.append(cls.TAG_DEFINITIONS["price_leader"])
        
        # Margin warning (from your notebook - uses tier min margin)
        tier_config = TIER_CONFIGS.get(tier.lower(), TIER_CONFIGS["mid"])
        if margin_pct < tier_config.min_margin_pct * 100:
            tags.append(cls.TAG_DEFINITIONS["margin_watch"])
        
        return tags

# =============================================================================
# GRADIENT BOOSTING MODEL (from your notebook)
# =============================================================================

class GradientBoostingPricingModel:
    """
    Gradient Boosting model for price adjustment prediction.
    Uses EXACT training logic from your notebook's generate_training_data() 
    and train_pricing_model() functions.
    """
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_cols = []
        self.is_trained = False
        self.feature_importance = {}
    
    def _create_encoders(self):
        """Create label encoders for categorical variables."""
        self.encoders["tier"] = LabelEncoder()
        self.encoders["tier"].fit(["Low", "Mid", "High", "Premium"])
        
        self.encoders["category"] = LabelEncoder()
        self.encoders["category"].fit(["Chemicals", "Equipment", "Paper", "Other"])
        
        self.encoders["lifecycle"] = LabelEncoder()
        self.encoders["lifecycle"].fit(["Launch", "Growth", "Maturity", "Decline", "Clearance"])
    
    def _generate_training_data(self, n_samples: int = 2000) -> pd.DataFrame:
        """
        Generate synthetic training data based on YOUR pricing rules.
        This is the EXACT logic from your notebook's generate_training_data().
        """
        np.random.seed(42)
        
        training_data = []
        
        # Sample product characteristics
        tiers = ["Low", "Mid", "High"]
        categories = ["Chemicals", "Equipment", "Paper", "Other"]
        lifecycles = ["Launch", "Growth", "Maturity", "Decline"]
        
        for _ in range(n_samples):
            # Random product characteristics
            tier = np.random.choice(tiers)
            category = np.random.choice(categories)
            lifecycle = np.random.choice(lifecycles, p=[0.1, 0.2, 0.5, 0.2])
            
            # Price range based on tier
            if tier == "Low":
                base_price = np.random.uniform(1, 20)
            elif tier == "Mid":
                base_price = np.random.uniform(10, 100)
            else:
                base_price = np.random.uniform(50, 500)
            
            competitor_avg = base_price * np.random.uniform(0.85, 1.15)
            
            # FROM YOUR NOTEBOOK: Simulate scenarios
            demand_index = np.random.uniform(0.5, 1.5)
            season_factor = np.random.choice([0, 0.125, -0.15])  # From your notebook
            market_oos = np.random.choice([0, 1], p=[0.7, 0.3])  # From your notebook
            
            # FROM YOUR NOTEBOOK: Calculate adjustment based on YOUR rules
            adjustment = 0.0
            
            # Demand (from your PricingRules - exact values)
            if demand_index > 1.0:
                adjustment += (demand_index - 1.0) * 0.10  # demand_up_max from your notebook
            elif demand_index < 1.0:
                adjustment -= (1.0 - demand_index) * 0.10  # demand_down_max from your notebook
            
            # Lifecycle (from your PricingRules - exact values)
            if lifecycle.lower() == "launch":
                adjustment -= 0.10  # launch_discount from your notebook
            elif lifecycle.lower() == "growth":
                adjustment += 0.05  # growth_increase from your notebook
            elif lifecycle.lower() == "decline":
                adjustment -= 0.20  # decline_discount from your notebook
            
            # Season (from your notebook)
            adjustment += season_factor
            
            # Competitor out of stock (from your PricingRules - uses midpoint)
            if market_oos:
                adjustment += 0.075  # (out_of_stock_bump_min + out_of_stock_bump_max) / 2
            
            # Add noise (from your notebook)
            adjustment += np.random.normal(0, 0.02)
            
            # Clip adjustment (reasonable bounds)
            adjustment = np.clip(adjustment, -0.30, 0.25)
            
            price_vs_comp = base_price / competitor_avg if competitor_avg > 0 else 1.0
            
            training_data.append({
                "Base_Price": base_price,
                "tier_encoded": self.encoders["tier"].transform([tier])[0],
                "category_encoded": self.encoders["category"].transform([category])[0],
                "lifecycle_encoded": self.encoders["lifecycle"].transform([lifecycle])[0],
                "competitor_avg": competitor_avg,
                "price_vs_competitor": price_vs_comp,
                "market_oos": market_oos,
                "demand_index": demand_index,
                "target_adjustment": adjustment
            })
        
        return pd.DataFrame(training_data)
    
    def train(self, n_samples: int = 2000) -> Dict[str, float]:
        """
        Train the Gradient Boosting model.
        Uses EXACT model parameters from your notebook's train_pricing_model().
        """
        self._create_encoders()
        
        # Generate training data (using your rules)
        train_df = self._generate_training_data(n_samples)
        
        self.feature_cols = [
            "Base_Price", "tier_encoded", "category_encoded", "lifecycle_encoded",
            "competitor_avg", "price_vs_competitor", "market_oos", "demand_index"
        ]
        
        X = train_df[self.feature_cols]
        y = train_df["target_adjustment"]
        
        # FROM YOUR NOTEBOOK: Exact model parameters
        self.model = GradientBoostingRegressor(
            n_estimators=100,        # From your notebook
            learning_rate=0.1,       # From your notebook
            max_depth=4,             # From your notebook
            min_samples_split=10,    # From your notebook
            min_samples_leaf=5,      # From your notebook
            random_state=42          # From your notebook
        )
        self.model.fit(X, y)
        self.is_trained = True
        
        # Get feature importance
        self.feature_importance = dict(zip(self.feature_cols, self.model.feature_importances_))
        
        return self.feature_importance
    
    def predict_adjustment(self,
                          base_price: float,
                          tier: str,
                          category: str,
                          lifecycle: str,
                          competitor_avg: float,
                          market_oos: bool,
                          demand_index: float) -> float:
        """
        Predict the optimal price adjustment percentage.
        Based on your notebook's predict_ml_adjustment().
        """
        if not self.is_trained:
            self.train()
        
        # Encode categorical variables (with fallbacks like your notebook)
        try:
            tier_enc = self.encoders["tier"].transform([tier])[0]
        except:
            tier_enc = 1  # Default to Mid
        
        try:
            cat_enc = self.encoders["category"].transform([category])[0]
        except:
            cat_enc = 3  # Default to Other
        
        try:
            life_enc = self.encoders["lifecycle"].transform([lifecycle])[0]
        except:
            life_enc = 2  # Default to Maturity
        
        price_vs_comp = base_price / competitor_avg if competitor_avg > 0 else 1.0
        
        features = np.array([[
            base_price, tier_enc, cat_enc, life_enc,
            competitor_avg, price_vs_comp, int(market_oos), demand_index
        ]])
        
        return float(self.model.predict(features)[0])

# =============================================================================
# RULE-BASED PRICING (from your notebook's calculate_price logic)
# =============================================================================

def apply_demand_adjustment(price: float, demand_index: float, rules: PricingRules) -> float:
    """
    From your notebook's apply_demand_adjustment().
    """
    if demand_index is None:
        return price
    
    if demand_index > 1.0:
        intensity = _clamp(demand_index - 1.0, 0.0, 1.0)
        uplift_pct = rules.demand_up_min + intensity * (rules.demand_up_max - rules.demand_up_min)
        return price * (1 + uplift_pct)
    
    if demand_index < 1.0:
        intensity = _clamp(1.0 - demand_index, 0.0, 1.0)
        discount_pct = intensity * rules.demand_down_max
        return price * (1 - discount_pct)
    
    return price

def apply_lifecycle_adjustment(price: float, lifecycle: str, rules: PricingRules) -> float:
    """
    From your notebook's apply_lifecycle_adjustment().
    """
    if not lifecycle:
        return price
    
    lifecycle = lifecycle.lower()
    
    if lifecycle == "launch":
        return price * (1 - rules.launch_discount)
    elif lifecycle == "growth":
        return price * (1 + rules.growth_increase)
    elif lifecycle == "maturity":
        return price * (1 + rules.maturity_adjustment)
    elif lifecycle == "decline":
        return price * (1 - rules.decline_discount)
    
    return price

def apply_competition_adjustment(price: float, competitor_avg: float, market_oos: bool, rules: PricingRules) -> float:
    """
    From your notebook's apply_competition_adjustment().
    """
    if market_oos:
        bump = (rules.out_of_stock_bump_min + rules.out_of_stock_bump_max) / 2
        return price * (1 + bump)
    
    return price

def enforce_boundaries(price: float, cost: float, tier: str, rules: PricingRules) -> float:
    """
    From your notebook's enforce_boundaries().
    Ensures minimum margin per tier.
    """
    tier_config = TIER_CONFIGS.get(tier.lower(), TIER_CONFIGS["mid"])
    min_price = cost * (1 + tier_config.min_margin_pct)
    return max(price, min_price)

def calculate_rules_price(base_price: float, cost: float, tier: str, lifecycle: str,
                          demand_index: float, competitor_avg: float, market_oos: bool) -> float:
    """
    Calculate price using rule-based approach.
    Combines all your notebook's pricing functions.
    """
    rules = DEFAULT_RULES
    
    price = base_price
    price = apply_demand_adjustment(price, demand_index, rules)
    price = apply_lifecycle_adjustment(price, lifecycle, rules)
    price = apply_competition_adjustment(price, competitor_avg, market_oos, rules)
    price = enforce_boundaries(price, cost, tier, rules)
    
    return price

# =============================================================================
# UNIFIED PRICING ENGINE (combines ML + Rules like your notebook)
# =============================================================================

class PricingEngine:
    """
    Unified pricing engine combining:
    - Rule-based pricing (from your notebook)
    - Gradient Boosting ML model (from your notebook)
    - Smart tags (from your notebook)
    
    Uses ML_WEIGHT to blend (like your notebook's ML_WEIGHT = 0.5)
    """
    
    def __init__(self, ml_weight: float = 0.5):
        """
        Args:
            ml_weight: 0 = all rules, 1 = all ML, 0.5 = hybrid (your notebook default)
        """
        self.ml_weight = ml_weight
        self.ml_model = GradientBoostingPricingModel()
        self.ml_model.train(n_samples=2000)
        self.feature_importance = self.ml_model.feature_importance
    
    def get_recommendation(self,
                          product_name: str,
                          base_price: float,
                          cost: float,
                          tier: str,
                          category: str,
                          lifecycle: str,
                          competitor_avg: float,
                          market_oos: bool,
                          demand_index: float) -> Dict[str, Any]:
        """
        Get pricing recommendation using hybrid approach.
        This mirrors your notebook's ML pricing logic.
        """
        
        # 1. Rule-based price (from your notebook)
        rules_price = calculate_rules_price(
            base_price, cost, tier, lifecycle, demand_index, competitor_avg, market_oos
        )
        rules_adjustment = (rules_price - base_price) / base_price
        
        # 2. ML price (from your notebook)
        ml_adjustment = self.ml_model.predict_adjustment(
            base_price, tier, category, lifecycle, competitor_avg, market_oos, demand_index
        )
        ml_price = base_price * (1 + ml_adjustment)
        
        # 3. Hybrid price (from your notebook - blended_adjustment)
        blended_adjustment = (1 - self.ml_weight) * rules_adjustment + self.ml_weight * ml_adjustment
        hybrid_price = base_price * (1 + blended_adjustment)
        
        # 4. Enforce minimum margin (from your notebook)
        tier_config = TIER_CONFIGS.get(tier.lower(), TIER_CONFIGS["mid"])
        min_price = cost * (1 + tier_config.min_margin_pct)
        hybrid_price = max(hybrid_price, min_price)
        
        # 5. Calculate final margin
        margin_pct = ((hybrid_price - cost) / hybrid_price) * 100 if hybrid_price > 0 else 0
        
        # 6. Generate smart tags (from your notebook)
        smart_tags = SmartTagEngine.generate_tags(
            lifecycle=lifecycle,
            demand_index=demand_index,
            margin_pct=margin_pct,
            our_price=hybrid_price,
            competitor_avg=competitor_avg,
            tier=tier,
            market_oos=market_oos
        )
        
        # 7. Track what rules were applied
        rule_adjustments = {
            "demand_adj": demand_index != 1.0,
            "lifecycle_adj": lifecycle.lower() in ["launch", "growth", "decline"],
            "market_oos_adj": market_oos,
            "margin_floor_applied": hybrid_price == min_price,
        }
        
        return {
            "product_name": product_name,
            "recommended_price": round(hybrid_price, 2),
            "rules_price": round(rules_price, 2),
            "ml_price": round(ml_price, 2),
            "ml_adjustment_pct": round(ml_adjustment * 100, 1),
            "price_change_pct": round(((hybrid_price - base_price) / base_price) * 100, 1),
            "margin_pct": round(margin_pct, 1),
            "smart_tags": smart_tags,
            "tier": tier,
            "demand_index": demand_index,
            "competitor_avg": competitor_avg,
            "rule_adjustments": rule_adjustments,
        }

# =============================================================================
# SINGLETON FACTORY
# =============================================================================

_engine_instance = None

def get_pricing_engine(ml_weight: float = 0.5) -> PricingEngine:
    """Get or create the pricing engine singleton."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = PricingEngine(ml_weight=ml_weight)
    return _engine_instance
