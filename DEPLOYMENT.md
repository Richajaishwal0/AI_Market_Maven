# 🚀 Market Maven Deployment Guide

This guide covers deploying Market Maven locally and on Streamlit Community Cloud.

## 📋 Prerequisites

- Python 3.11 or higher
- Git (for cloning repository)
- GitHub account (for Streamlit Cloud deployment)

## 🏠 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/market-maven.git
cd market-maven
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv market-maven-env

# Activate virtual environment
# On Windows:
market-maven-env\Scripts\activate
# On macOS/Linux:
source market-maven-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements-local.txt
```

### 4. Run Locally
```bash
streamlit run app.py --server.port 5000
```

### 5. Access Application
Open your browser and navigate to: `http://localhost:5000`

## ☁️ Streamlit Community Cloud Deployment

### 1. Prepare Your Repository
Ensure your repository contains:
- `app.py` (main application file)
- `requirements-local.txt` (renamed to `requirements.txt` for deployment)
- `data_utils.py` (data processing utilities)
- `model.py` (machine learning models)
- All other necessary files

### 2. Create requirements.txt for Deployment
Copy the contents of `requirements-local.txt` to a new file called `requirements.txt`:
```bash
cp requirements-local.txt requirements.txt
```

### 3. Deploy on Streamlit Community Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit deployment"
   git push origin main
   ```

2. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Create New App**
   - Click "New app"
   - Select your repository
   - Choose branch (usually `main`)
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Configure Settings (if needed)**
   - Set Python version to 3.11
   - Ensure requirements.txt is properly configured

### 4. Access Your Deployed App
Your app will be available at: `https://your-app-name.streamlit.app`

## 🔧 Configuration Files

### requirements.txt Content
```
streamlit>=1.27.0
pandas>=2.0.3
numpy>=1.24.3
openpyxl>=3.1.2
scikit-learn>=1.3.0
joblib>=1.3.0
plotly>=5.15.0
python-dateutil>=2.8.2
pytz>=2023.3
```

### .streamlit/config.toml (Optional)
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

## 🐛 Troubleshooting

### Common Issues

**1. Module Not Found Error**
```bash
# Ensure all dependencies are installed
pip install -r requirements-local.txt

# Check virtual environment is activated
which python
```

**2. Port Already in Use**
```bash
# Use different port
streamlit run app.py --server.port 8501
```

**3. Deployment Failures**
- Check requirements.txt has correct package versions
- Ensure all imports are available in requirements.txt
- Verify Python version compatibility

**4. Memory Issues on Streamlit Cloud**
- Optimize data processing functions
- Use st.cache_data for expensive operations
- Consider data sampling for large datasets

## 🚀 Production Deployment Options

### 1. Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT --server.headless true" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 2. Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements-local.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.headless", "true"]
```

### 3. AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Configure load balancing and auto-scaling
- Set up HTTPS certificates

## 📝 Pre-Deployment Checklist

- [ ] All dependencies listed in requirements.txt
- [ ] Python version specified (3.11+)
- [ ] No hardcoded file paths
- [ ] Environment variables configured
- [ ] Error handling implemented
- [ ] Mobile responsiveness tested
- [ ] Performance optimized
- [ ] Security considerations addressed

## 🔒 Security Considerations

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Implement proper error handling
- Validate user inputs
- Use HTTPS in production

## 📊 Performance Optimization

- Use `st.cache_data` for expensive operations
- Implement lazy loading for large datasets
- Optimize chart rendering
- Minimize memory usage
- Use efficient data structures

## 🎯 Next Steps

After successful deployment:
1. Monitor application performance
2. Set up analytics tracking
3. Configure backup strategies
4. Plan for scaling requirements
5. Implement CI/CD pipeline

---

**Need Help?**
- Check [Streamlit Documentation](https://docs.streamlit.io)
- Visit [Streamlit Community Forum](https://discuss.streamlit.io)
- Review deployment logs for specific errors