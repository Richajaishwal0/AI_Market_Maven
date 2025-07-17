# 🏪 Market Maven - AI-Powered Sales Forecasting Platform

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/Streamlit-1.27.0-red" alt="Streamlit 1.27.0" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/Version-2.0-purple" alt="Version 2.0" />
</div>

Market Maven is a professional AI-powered sales forecasting and analytics platform built with Streamlit. It provides businesses with automated data processing, machine learning-based forecasting, and interactive visualizations to analyze product performance and generate actionable business insights.

## ✨ Key Features

### 🎨 **Modern Professional UI**

- **Dark/Light Theme Toggle**: Seamless switching between themes with full component theming
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Premium Animations**: Smooth hover effects, transitions, and interactive elements
- **Card-Based Layout**: Clean, organized interface with gradient headers

### 🤖 **AI-Powered Forecasting**

- **Multiple Algorithms**: Moving average, exponential smoothing, linear trend, and ML models
- **Machine Learning**: Random Forest and Linear Regression implementations
- **Automated Column Detection**: Intelligent identification of date, sales, and product columns
- **Model Persistence**: Save and load trained models for consistent predictions

### 📊 **Advanced Analytics**

- **Interactive Charts**: Plotly-powered visualizations with theme-aware styling
- **Performance Metrics**: MAE, MSE, RMSE, and R² score evaluations
- **Product Analysis**: Top performers, sales distribution, and trend analysis
- **Time Series Visualization**: Daily, monthly, and seasonal pattern recognition

### 💡 **Business Intelligence**

- **Comprehensive Insights**: 7+ types of business recommendations
- **Priority Levels**: Critical, High, Medium, Low risk assessments
- **Action Items**: Specific, actionable recommendations for each insight
- **Category Classification**: Growth, Risk Management, Product Strategy insights

### 📱 **Mobile-Optimized**

- **Touch-Friendly Interface**: Larger buttons and improved navigation
- **Responsive Charts**: Optimized chart sizing and spacing for mobile
- **Sidebar Navigation**: Clear mobile navigation with helpful hints
- **Optimized Performance**: Fast loading and smooth interactions

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/market-maven.git
cd market-maven
```

2. **Install dependencies**

```bash
pip install -r requirements-local.txt
```

3. **Run the application**

```bash
streamlit run app.py --server.port 5000
```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📋 Requirements

### Core Dependencies

- `streamlit>=1.27.0` - Web application framework
- `pandas>=2.0.3` - Data manipulation and analysis
- `numpy>=1.24.3` - Numerical computations
- `scikit-learn` - Machine learning algorithms
- `plotly` - Interactive data visualization
- `openpyxl>=3.1.2` - Excel file support

### System Requirements

- **Python**: 3.11+
- **Memory**: 2GB RAM minimum
- **Storage**: 100MB free space
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

## 🎯 Usage Guide

### 1. **Data Upload**

- Navigate to the "📁 Upload Data" section
- Upload CSV or Excel files containing sales data
- System automatically detects date, sales, and product columns
- Preview and validate your data before processing

### 2. **Forecasting**

- Go to "📈 Forecast" section
- Select forecasting method (Moving Average, Exponential, Linear Trend, ML Models)
- Choose forecast period (days/weeks/months)
- Generate predictions with confidence intervals
- Download forecast results as CSV

### 3. **Business Insights**

- Visit "💡 Insights" section after generating forecasts
- Review AI-generated business recommendations
- Analyze priority levels and action items
- Implement suggested strategies for growth

### 4. **Analytics Dashboard**

- Access "📊 Analytics" for comprehensive analysis
- View performance metrics and KPIs
- Analyze product performance and sales trends
- Export charts and reports

## 🏗️ Architecture

### **Frontend Architecture**

- **Framework**: Streamlit with custom CSS styling
- **Theme System**: Dynamic light/dark mode with full component theming
- **Responsive Design**: Mobile-first approach with breakpoints
- **Animations**: CSS transitions and hover effects

### **Backend Architecture**

- **Data Processing**: Pandas and NumPy for data manipulation
- **Machine Learning**: Scikit-learn for predictive modeling
- **Visualization**: Plotly for interactive charts
- **File Handling**: Support for CSV and Excel formats

### **Data Processing Pipeline**

1. **File Upload** → **Column Detection** → **Data Validation**
2. **Preprocessing** → **Feature Engineering** → **Model Training**
3. **Forecasting** → **Visualization** → **Insights Generation**
4. **Export** → **Reporting** → **Business Recommendations**

## 🔧 Configuration

### Streamlit Configuration

The app uses the following configuration in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Environment Variables

No environment variables are required for basic functionality. The app runs with default settings.

## 🎨 Customization

### Theme Customization

- Modify CSS variables in `app.py` for custom colors
- Update gradient definitions for different brand colors
- Customize animation timings and effects

### Adding New Forecasting Methods

1. Create new method in `model.py`
2. Add UI controls in forecast page
3. Update method selection logic
4. Test with sample data

### Custom Insights

1. Extend `generate_business_insights()` function
2. Add new insight categories and priorities
3. Update display logic for new insight types

## 🚀 Deployment

Check it out on [Website](https://aimarketmaven-e3jb3tzwvnayambyswzuqn.streamlit.app/)

### Local Development

```bash
streamlit run app.py --server.port 8501
```

### Production Deployment

1. **Replit**: Deploy directly on Replit platform
2. **Heroku**: Use provided `requirements.txt` and `runtime.txt`
3. **Docker**: Create container with Python 3.11 base image
4. **Cloud Platforms**: Deploy on AWS, GCP, or Azure

## 📊 Sample Data Format

Your data should include the following columns:

- **Date Column**: Date/timestamp for time series analysis
- **Sales Column**: Numerical sales values
- **Product Column**: Product categories or names (optional)
- **Additional Columns**: Any relevant business metrics

Example CSV format:

```csv
Date,Product,Sales,Quantity,Total
2024-01-01,Electronics,150.50,5,752.50
2024-01-02,Clothing,89.99,3,269.97
2024-01-03,Electronics,200.00,2,400.00
```

## 🔍 Troubleshooting

### Common Issues

**1. Data Upload Problems**

- Ensure file format is CSV or Excel
- Check for proper column headers
- Verify date formats are recognized

**2. Forecasting Errors**

- Confirm sufficient historical data (minimum 10 records)
- Check for missing values in key columns
- Ensure numerical data types for sales columns

**3. Chart Display Issues**

- Refresh the page if charts don't load
- Check browser console for JavaScript errors
- Ensure stable internet connection for Plotly

**4. Mobile Navigation**

- Use sidebar dropdown for page navigation
- Ensure JavaScript is enabled
- Try refreshing if sidebar doesn't appear

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation for changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing framework
- **Plotly** for interactive visualizations
- **Scikit-learn** for machine learning capabilities
- **Community Contributors** for feedback and suggestions
