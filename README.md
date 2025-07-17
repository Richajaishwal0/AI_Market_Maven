# Market Maven - Sales Forecasting Platform

## Overview

Market Maven is an AI-powered sales forecasting and analytics platform built with Streamlit. It provides sales teams with automated data processing, machine learning-based forecasting, and interactive visualizations to analyze product performance and generate actionable business insights.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (January 2025)

### UI/UX Transformation - Complete
- **Professional Design Overhaul**: Modern card-based layouts with gradient headers and Inter font family
- **Comprehensive Dark Theme**: Full application theming including sidebar, dropdowns, charts, and all components
- **Premium Hover Effects**: Enhanced animations with shimmer effects, scaling, and smooth transitions
- **Chart Optimization**: Fixed text overlap issues in pie charts with improved spacing and positioning
- **Enhanced Insights**: Comprehensive business recommendations with priority levels, category tags, and actionable items
- **Responsive Design**: Mobile, tablet, and desktop compatible layouts
- **User Satisfaction**: Successfully completed transformation per user approval

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Styling**: Custom CSS with Inter font family, gradient backgrounds, and professional color schemes
- **Layout**: Wide layout with expandable sidebar navigation
- **Themes**: Dynamic light/dark theme toggle with theme-aware chart styling
- **Responsive Design**: Mobile, tablet, and desktop compatible layouts
- **Chart Optimization**: Fixed text overlap issues in pie charts with improved spacing and positioning

### Backend Architecture
- **Core Framework**: Python-based Streamlit application
- **Data Processing**: Pandas for data manipulation and NumPy for numerical operations
- **Machine Learning**: Scikit-learn with Random Forest and Linear Regression models
- **Visualization**: Plotly for interactive charts and graphs
- **File Handling**: Support for CSV and Excel file uploads

### Data Processing Pipeline
- **Automatic Column Detection**: Intelligent detection of date, target, product, and external factor columns
- **Dynamic Preprocessing**: Automated handling of categorical encoding, date parsing, and feature engineering
- **Data Validation**: Built-in data cleaning and validation processes

## Key Components

### 1. Data Upload and Processing (`data_utils.py`)
- **File Support**: CSV and Excel file formats
- **Column Detection**: Automatic identification of key columns (date, sales, product, external factors)
- **Preprocessing**: Label encoding for categorical variables, date handling, and feature preparation

### 2. Forecasting Engine (`model.py`)
- **Multiple Methods**: Moving average, exponential smoothing, and linear trend forecasting
- **Machine Learning**: Random Forest and Linear Regression models
- **Model Persistence**: Save and load trained models using joblib
- **Evaluation Metrics**: MAE, MSE, RMSE, and R² score calculations

### 3. User Interface (`app.py`)
- **Navigation**: Icon-based navigation with home, upload, forecast, suggestions, analytics, and about sections
- **Data Visualization**: Interactive Plotly charts for sales trends, product performance, and forecasting results
- **Professional Styling**: Custom CSS with gradients, shadows, and modern typography
- **Responsive Design**: Optimized for multiple screen sizes

### 4. Analytics and Insights
- **Product Performance**: Bar charts and pie charts showing sales distribution
- **Sales Trends**: Time series visualization with forecasting overlays
- **Business Suggestions**: Automated generation of actionable insights based on data analysis

## Data Flow

1. **Data Upload**: Users upload CSV/Excel files through Streamlit file uploader
2. **Column Detection**: System automatically identifies relevant columns (date, sales, product)
3. **Preprocessing**: Data is cleaned, encoded, and prepared for analysis
4. **Model Training**: Machine learning models are trained on historical data
5. **Forecasting**: Future sales predictions are generated using trained models
6. **Visualization**: Results are displayed through interactive charts and tables
7. **Insights Generation**: System provides actionable business recommendations
8. **Export**: Users can download forecasting results as CSV files

## External Dependencies

### Core Libraries
- **Streamlit (1.27.0)**: Web application framework
- **Pandas (2.0.3)**: Data manipulation and analysis
- **NumPy (1.24.3)**: Numerical computations
- **Scikit-learn**: Machine learning algorithms and preprocessing
- **Plotly**: Interactive data visualization

### Additional Libraries
- **OpenPyXL (3.1.2)**: Excel file reading support
- **Matplotlib (3.7.2)**: Static plotting (optional fallback)
- **Seaborn (0.12.2)**: Statistical data visualization (optional)
- **Joblib**: Model serialization and persistence

### System Requirements
- **Python**: 3.11
- **Build Tools**: python3-dev, build-essential

## Deployment Strategy

### Local Development
- **Setup**: Clone repository, install dependencies via requirements.txt
- **Launch**: Run `streamlit run app.py` for local development server
- **Port**: Default Streamlit port 8501

### Production Considerations
- **Environment**: Python 3.11 runtime specified
- **Dependencies**: All requirements pinned to specific versions for stability
- **Assets**: Static CSS and styling assets in dedicated assets folder
- **Error Handling**: Graceful fallbacks for optional plotting libraries

### File Structure
```
/
├── app.py                 # Main Streamlit application
├── data_utils.py         # Data processing utilities
├── model.py              # Machine learning models and forecasting
├── assets/
│   └── styles.css        # Additional styling and animations
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version specification
└── packages.txt         # System packages
```

### Performance Optimizations
- **Caching**: Streamlit's built-in caching for data processing and model training
- **Memory Management**: Efficient data handling for large datasets
- **Progressive Loading**: Lazy loading of visualization components
- **Error Recovery**: Robust error handling with user-friendly messages