# PricingIQ: AI-Driven Dynamic Pricing Engine

An intelligent pricing optimization system powered by machine learning algorithms and real-time analytics that helps businesses maximize revenue and maintain market competitiveness through automated price recommendations, competitor monitoring, and executive insights.

## Features

- **Executive Insights Dashboard**
- **Revenue Impact Forecast**
- **Revenue by Category**
- **Price Change Distribution**
- **Performance by Tier**
- **Elasticity Trend Analysis**
- **Competitive Intelligence**
- **Smart Pricing Engine**
- **Approval Workflow**
- **Alert System**

  
## Tools Used

### Core Technologies
* **Python 3.11** - Backend logic and ML model implementation
* **Streamlit** - Interactive web application framework for rapid deployment
* **Plotly** - Interactive data visualizations and charts
* **Pandas & NumPy** - Data manipulation and numerical computing
* **Hugging Face Spaces** - Cloud deployment and hosting platform

### Machine Learning Stack (Ready for Integration)
* **XGBoost/LightGBM** - Gradient boosting for price elasticity modeling
* **Prophet** - Time series forecasting for demand prediction
* **Statistical Models** - Margin optimization and revenue forecasting


## System Architecture

```mermaid
graph TB
    User[Business User] -->|Access| HF[Hugging Face Spaces]
    HF -->|Hosts| WebUI[PricingIQ Dashboard]
    WebUI --> Insights[ Insights Tab]
    WebUI --> Pricing[Pricing Engine Tab]
    WebUI --> Approvals[ Approvals Tab]
    WebUI --> Alerts[ Alerts Tab]
    
    Insights -->|Display| KPIs[4 Key Metrics]
    Insights -->|Visualize| Charts[6 Interactive Charts]
    Insights -->|Show| CompCards[Competitor Cards]
    
    Pricing -->|Show| ProductTable[Product Catalog - 301 Items]
    Pricing -->|Calculate| Optimizer[Price Optimizer]
    
    Approvals -->|Queue| PendingItems[Pending Changes]
    Approvals -->|Track| AuditLog[Decision History]
    
    Alerts -->|Monitor| Thresholds[Margin/Price Thresholds]
    Alerts -->|Notify| Actions[3 Active Alerts]
    
    Optimizer --> MLModel[ML Price Model]
    MLModel --> MockData[Mock Data Layer]
    CompCards --> MockData
    
    classDef user fill:#e1f5fe
    classDef platform fill:#ff9800
    classDef frontend fill:#f3e5f5
    classDef backend fill:#e8f5e8
    classDef ml fill:#fff3e0
    
    class User user
    class HF platform
    class WebUI,Insights,Pricing,Approvals,Alerts frontend
    class KPIs,Charts,ProductTable,CompCards backend
    class Optimizer,MLModel,MockData ml
```

## Complete Pricing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant D as PricingIQ Dashboard
    participant E as Pricing Engine
    participant M as ML Model
    participant DB as Data Store
    participant A as Alert System

    U->>D: Access Insights Tab
    D->>DB: Fetch Current Prices
    DB->>D: Return 301 Products
    D->>U: Display KPIs & Charts
    
    Note over E: Real-time Optimization
    E->>DB: Get Historical Sales
    DB->>E: Sales Data
    E->>DB: Fetch Competitor Prices
    DB->>E: 4 Competitor Datasets
    
    E->>M: Request 295 Price Recommendations
    Note over M: ML Processing
    M->>M: Calculate Elasticity
    M->>M: Analyze Tier Performance
    M->>M: Optimize Margins (29.3%)
    M->>E: Optimized Prices
    
    E->>DB: Store Recommendations
    E->>A: Check Thresholds
    
    alt 3 Alerts Triggered
        A->>U: Display Alert Badge
        A->>E: Flag for Review
    end
    
    E->>D: Update Dashboard
    D->>U: Show $143,466 Potential
    
    U->>D: Review & Approve
    D->>DB: Update Active Prices
    DB->>A: Log Audit Trail
    A->>U: Confirmation
```

## Deployment on Hugging Face Spaces

```mermaid
graph TB
    subgraph HF[🤗 Hugging Face Spaces]
        Space[CGPricing_Final Space]
        Runtime[Streamlit Runtime]
        Storage[Ephemeral Storage]
    end
    
    subgraph App[PricingIQ Application]
        Streamlit[Streamlit Dashboard]
        Insights[Insights Tab - 6 Charts]
        Pricing[Pricing Engine - 301 Products]
        Approvals[Approvals - 295 Pending]
        Alerts[Alerts - 3 Active]
    end
    
    subgraph Data[Data Layer]
        Mock[Mock Data - 301 Products]
        Competitors[4 Competitor Profiles]
        State[Session State]
    end
    
    Users[Business Users] -->|HTTPS| Space
    Space --> Runtime
    Runtime --> Streamlit
    Streamlit --> Insights
    Streamlit --> Pricing
    Streamlit --> Approvals
    Streamlit --> Alerts
    
    Insights --> Mock
    Insights --> Competitors
    Pricing --> Mock
    Approvals --> State
    
    classDef hf fill:#8B3A3A,color:#fff
    classDef app fill:#f3e5f5
    classDef data fill:#e8f5e8
    
    class Space,Runtime,Storage hf
    class Streamlit,Insights,Pricing,Approvals,Alerts app
    class Mock,Competitors,State data
```

### Project Structure

```
CGPricing_Final/
├── app.py                    # Main PricingIQ application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── tabs/
│   ├── insights.py          # Executive insights dashboard
│   ├── pricing_engine.py    # Pricing engine tab
│   ├── approvals.py         # Approvals workflow tab
│   ├── alerts.py            # Alert system tab
│   └── login.py             # Authentication module
├── data/
│   ├── mock_data.py         # Mock 301 products
│   ├── competitor_data.py   # 4 competitors data
│   └── elasticity_data.py   # Elasticity trends
├── utils/
│   ├── charts.py            # Plotly chart components
│   ├── kpi_cards.py         # KPI card widgets
│   └── helpers.py           # Helper functions
└── assets/
    └── logo.png             # PIQ logo
```
