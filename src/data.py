"""
Data module for the pricing dashboard
Contains all mock data for charts and tables
"""

# Revenue data for the forecast chart
revenue_data = [
    {'month': 'Jan', 'current': 52000, 'optimized': 54600, 'profit': 11200},
    {'month': 'Feb', 'current': 55000, 'optimized': 58300, 'profit': 12800},
    {'month': 'Mar', 'current': 58000, 'optimized': 62100, 'profit': 14100},
    {'month': 'Apr', 'current': 61000, 'optimized': 66800, 'profit': 15600},
    {'month': 'May', 'current': 64000, 'optimized': 70200, 'profit': 16800},
    {'month': 'Jun', 'current': 67340, 'optimized': 75600, 'profit': 18200},
]

# Competitor data
competitor_data = [
    {
        'name': 'Budget Janitorial',
        'avgPrice': 8.25,
        'marketShare': 28,
        'position': 'Below'
    },
    {
        'name': 'All-Brite Sales',
        'avgPrice': 9.10,
        'marketShare': 22,
        'position': 'Above'
    },
    {
        'name': 'CleanALL Supply',
        'avgPrice': 7.85,
        'marketShare': 18,
        'position': 'Below'
    },
    {
        'name': 'Staples',
        'avgPrice': 12.50,
        'marketShare': 15,
        'position': 'Above'
    },
    {
        'name': 'C&G Services',
        'avgPrice': 8.75,
        'marketShare': 17,
        'position': 'Optimal'
    }
]

# Price elasticity data by tier
elasticity_data = [
    {'tier': 'Low', 'elasticity': -1.8},
    {'tier': 'Mid', 'elasticity': -1.2},
    {'tier': 'High', 'elasticity': -0.9},
    {'tier': 'Premium', 'elasticity': -0.6}
]

# Mock pricing data for products
mock_pricing_data = [
    {
        'product': 'Lysol Disinfecting Spray',
        'category': 'Cleaning',
        'tier': 'Mid',
        'currentPrice': 8.99,
        'optimizedPrice': 9.49,
        'competitor': 9.29,
        'change': 5.6,
        'margin': 22.4,
        'demand': 'High',
        'status': 'pending'
    },
    {
        'product': 'Purell Hand Sanitizer',
        'category': 'Hygiene',
        'tier': 'High',
        'currentPrice': 12.99,
        'optimizedPrice': 11.99,
        'competitor': 12.49,
        'change': -7.7,
        'margin': 28.3,
        'demand': 'Very High',
        'status': 'pending'
    },
    {
        'product': 'Clorox Disinfecting Wipes',
        'category': 'Cleaning',
        'tier': 'Mid',
        'currentPrice': 7.49,
        'optimizedPrice': 7.99,
        'competitor': 7.79,
        'change': 6.7,
        'margin': 19.8,
        'demand': 'High',
        'status': 'review'
    },
    {
        'product': 'Bounty Paper Towels',
        'category': 'Paper Products',
        'tier': 'Mid',
        'currentPrice': 24.99,
        'optimizedPrice': 23.99,
        'competitor': 25.49,
        'change': -4.0,
        'margin': 15.2,
        'demand': 'Medium',
        'status': 'approved'
    },
    {
        'product': 'Charmin Ultra Soft',
        'category': 'Paper Products',
        'tier': 'High',
        'currentPrice': 28.99,
        'optimizedPrice': 27.99,
        'competitor': 29.99,
        'change': -3.4,
        'margin': 18.6,
        'demand': 'High',
        'status': 'pending'
    },
    {
        'product': 'Tide Laundry Detergent',
        'category': 'Laundry',
        'tier': 'High',
        'currentPrice': 19.99,
        'optimizedPrice': 21.49,
        'competitor': 20.99,
        'change': 7.5,
        'margin': 24.7,
        'demand': 'Very High',
        'status': 'review'
    },
    {
        'product': 'Febreze Air Freshener',
        'category': 'Air Care',
        'tier': 'Mid',
        'currentPrice': 5.99,
        'optimizedPrice': 6.29,
        'competitor': 6.49,
        'change': 5.0,
        'margin': 21.3,
        'demand': 'Medium',
        'status': 'approved'
    },
    {
        'product': 'Glad Trash Bags',
        'category': 'Household',
        'tier': 'Low',
        'currentPrice': 12.49,
        'optimizedPrice': 11.99,
        'competitor': 13.29,
        'change': -4.0,
        'margin': 16.8,
        'demand': 'High',
        'status': 'pending'
    },
    {
        'product': 'Swiffer WetJet Pads',
        'category': 'Cleaning',
        'tier': 'Mid',
        'currentPrice': 14.99,
        'optimizedPrice': 15.49,
        'competitor': 15.99,
        'change': 3.3,
        'margin': 23.1,
        'demand': 'Medium',
        'status': 'approved'
    },
    {
        'product': 'Kleenex Facial Tissue',
        'category': 'Paper Products',
        'tier': 'Low',
        'currentPrice': 3.99,
        'optimizedPrice': 4.29,
        'competitor': 4.49,
        'change': 7.5,
        'margin': 19.5,
        'demand': 'High',
        'status': 'review'
    }
]

# Alerts data
alerts_data = [
    {
        'id': 1,
        'type': 'critical',
        'message': 'Paper Towels margin below threshold (15.2% vs 18% target)',
        'time': '5 minutes ago',
        'severity': 'High'
    },
    {
        'id': 2,
        'type': 'warning',
        'message': 'Competitor B decreased price on Clorox Wipes by 8%',
        'time': '1 hour ago',
        'severity': 'Medium'
    },
    {
        'id': 3,
        'type': 'info',
        'message': 'High demand detected for cleaning supplies category',
        'time': '2 hours ago',
        'severity': 'Low'
    },
    {
        'id': 4,
        'type': 'success',
        'message': 'Successfully optimized pricing for 15 products',
        'time': '3 hours ago',
        'severity': 'Low'
    }
]

# Category performance data
category_performance = [
    {
        'category': 'Cleaning',
        'revenue': 145200,
        'margin': 21.8,
        'products': 28,
        'growth': 12.3
    },
    {
        'category': 'Paper Products',
        'revenue': 98600,
        'margin': 17.2,
        'products': 18,
        'growth': 8.7
    },
    {
        'category': 'Hygiene',
        'revenue': 87300,
        'margin': 24.5,
        'products': 22,
        'growth': 15.2
    },
    {
        'category': 'Laundry',
        'revenue': 76400,
        'margin': 23.1,
        'products': 16,
        'growth': 10.8
    },
    {
        'category': 'Air Care',
        'revenue': 45200,
        'margin': 20.4,
        'products': 12,
        'growth': 6.5
    },
    {
        'category': 'Household',
        'revenue': 38900,
        'margin': 18.9,
        'products': 7,
        'growth': 4.2
    }
]

# Demand forecast data (default/demo data)
default_forecast = {
    'success': True,
    'forecast': {
        'category': 'Cleaning Supplies',
        'expected_increase': '+25%',
        'timeframe': '3-5 days',
        'confidence': '87%',
        'reasoning': 'Based on seasonal patterns, regional health trends, and historical sales data',
        'recommendation': 'Consider increasing inventory for Cleaning Supplies category and preparing for price optimization to maximize revenue during demand surge.'
    }
}

# Historical price changes
price_change_history = [
    {'date': '2024-11-22', 'product': 'Lysol Spray', 'old_price': 8.49, 'new_price': 8.99, 'change': 5.9},
    {'date': '2024-11-21', 'product': 'Purell Sanitizer', 'old_price': 13.49, 'new_price': 12.99, 'change': -3.7},
    {'date': '2024-11-20', 'product': 'Clorox Wipes', 'old_price': 7.99, 'new_price': 7.49, 'change': -6.3},
    {'date': '2024-11-19', 'product': 'Paper Towels', 'old_price': 23.99, 'new_price': 24.99, 'change': 4.2},
]

# Approval statistics
approval_stats = {
    'pending': 8,
    'approved_this_month': 45,
    'rejected_this_month': 3,
    'success_rate': 93.8,
    'avg_approval_time': '4.2 hours',
    'high_priority': 3,
    'medium_priority': 4,
    'low_priority': 1
}