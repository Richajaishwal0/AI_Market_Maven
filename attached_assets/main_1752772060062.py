import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

# Try to import matplotlib and seaborn with error handling
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    st.error("⚠️ Warning: matplotlib or seaborn not available. Some visualizations may not work.")
    PLOTTING_AVAILABLE = False

# --- Icon-only navigation and theme switching ---
NAV_ICONS = [
    ("🏠", "home", "Home"),
    ("📁", "upload", "Upload Data"),
    ("📊", "forecast", "Forecast"),
    ("💡", "suggestions", "Suggestions"),
    ("📈", "analytics", "Analytics"),
    ("ℹ️", "about", "About")
]
THEME_ICONS = {"light": "🌞", "dark": "🌙"}

# --- Theme CSS variables ---
THEME_CSS = {
    "light": {
        "--bg": "#f5f6fa",
        "--fg": "#181c27",
        "--primary": "#2d8cff",
        "--secondary": "#1c5db6",
        "--card": "#fff",
        "--hover": "#e6f0ff"
    },
    "dark": {
        "--bg": "#181c27",
        "--fg": "#f5f6fa",
        "--primary": "#2d8cff",
        "--secondary": "#1c5db6",
        "--card": "#232946",
        "--hover": "#223a5f"
    }
}

# --- Set theme and inject CSS ---
def set_theme():
    theme = st.session_state.get('theme', 'light')
    css_vars = THEME_CSS[theme]
    css = f":root {{ {' '.join([f'{k}: {v};' for k,v in css_vars.items()])} }}"
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown('''<style>
        body, .stApp { background: var(--bg) !important; color: var(--fg) !important; }
        .stButton>button, .stSelectbox>div>div, .stFileUploader>div>div {background: var(--card) !important; color: var(--fg) !important;}
        .stButton>button:hover {background: var(--primary) !important; color: #fff !important;}
        .stDataFrame, .stTable {background: var(--card) !important; color: var(--fg) !important;}
        .nav-bar {display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 2rem;}
        .nav-icon {font-size: 1.7rem; padding: 0.5rem 0.9rem; border-radius: 8px; background: none; border: none; cursor: pointer; transition: background 0.2s, color 0.2s; outline: none; margin: 0 0.1rem;}
        .nav-icon.selected {background: var(--primary); color: #fff;}
        .nav-icon:hover {background: var(--hover); color: var(--primary);}
        .theme-icon {font-size: 1.5rem; margin-left: 1.5rem; cursor: pointer; border-radius: 50%; padding: 0.3rem 0.5rem; background: var(--card); border: 1px solid var(--primary); transition: background 0.2s, color 0.2s;}
        .theme-icon:hover {background: var(--primary); color: #fff;}
        .stSelectbox>div>div {border-radius: 8px;}
    </style>''', unsafe_allow_html=True)

# --- Top Navigation Bar (functional) ---
def top_navigation():
    if 'nav' not in st.session_state:
        st.session_state['nav'] = 'home'
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'
    nav_cols = st.columns(len(NAV_ICONS) + 1, gap="small")
    for i, (icon, key, _) in enumerate(NAV_ICONS):
        if nav_cols[i].button(icon, key=f"nav_{key}", help=key, use_container_width=True):
            st.session_state['nav'] = key
            st.rerun()
        # No extra markdown for highlighting; only the button is shown
    # Theme switcher icon
    theme_icon = THEME_ICONS[st.session_state['theme']]
    if nav_cols[-1].button(theme_icon, key="theme_switch", help="Switch theme", use_container_width=True):
        st.session_state['theme'] = 'dark' if st.session_state['theme'] == 'light' else 'light'
        st.rerun()

# --- Helper functions ---
def preprocess_dynamic(df, date_col, target_col, product_col, external_cols):
    df = df.copy()
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['Year'] = df[date_col].dt.year
        df['Month'] = df[date_col].dt.month
        df['DayOfWeek'] = df[date_col].dt.dayofweek
    
    # Simple preprocessing without LabelEncoder
    label_encoders = {}
    for col in df.select_dtypes(include='object').columns:
        if col not in [target_col, date_col] + external_cols and not col.lower().endswith('id'):
            # Convert categorical to numeric using pandas factorize
            df[col], _ = pd.factorize(df[col])
            label_encoders[col] = None  # Keep for compatibility
    
    feature_cols = [c for c in df.columns if c != target_col and c != date_col and not c.lower().endswith('id')]
    feature_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c])]
    df = df.fillna(0)
    X = df[feature_cols]
    y = df[target_col] if target_col else None
    return X, y, label_encoders, feature_cols

def detect_columns(df):
    date_col = None
    for col in df.columns:
        if 'date' in col.lower():
            date_col = col
            break
    target_col = None
    for col in df.columns:
        if 'sales' in col.lower() or 'total' in col.lower() or 'profit' in col.lower():
            target_col = col
            break
    product_col = None
    for col in df.columns:
        if 'product' in col.lower() or 'item' in col.lower():
            product_col = col
            break
    external_cols = [col for col in df.columns if any(x in col.lower() for x in ['weather', 'event', 'crisis', 'season'])]
    return date_col, target_col, product_col, external_cols

# --- Main App ---
def main():
    st.set_page_config(page_title='Salesman AI Forecast', layout='wide')
    set_theme()
    top_navigation()
    nav = st.session_state.get('nav', 'home')

    if nav == 'home':
        st.markdown('<h1 style="text-align:center;">🛒</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;">Welcome! Upload your sales data, select a forecast period, and get actionable suggestions to maximize your profit. Use the navigation bar above to get started.</p>', unsafe_allow_html=True)
        st.image('https://cdn-icons-png.flaticon.com/512/1170/1170678.png', width=120)
        st.markdown('---')
        st.info('Tip: Use the navigation bar above to switch between features.')

    elif nav == 'upload':
        st.header('📁 Upload Your Sales Dataset')
        uploaded_file = st.file_uploader('Upload CSV or Excel', type=['csv', 'xlsx'], accept_multiple_files=False)
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success('✅ File uploaded!')
            st.dataframe(df.head(20))
            st.session_state['user_df'] = df
            st.session_state['file_uploaded'] = True
        else:
            st.info('Please upload your sales dataset to proceed.')

    elif nav == 'forecast':
        if not (st.session_state.get('file_uploaded') and st.session_state.get('user_df') is not None):
            st.warning('Please upload your dataset first in the "Upload Data" section.')
            return
        st.header('📊 Forecast')
        df = st.session_state['user_df']
        date_col, target_col, product_col, external_cols = detect_columns(df)
        if not target_col:
            st.error('Could not detect a target column (e.g., sales, total, profit). Please check your data.')
            return
        X, y, label_encoders, feature_cols = preprocess_dynamic(df, date_col, target_col, product_col, external_cols)
        st.markdown('**Select forecast period:**')
        period = st.selectbox('Prediction period', ['Next 7 days', 'Next 30 days', 'Next 90 days', 'Custom...'])
        if period == 'Custom...':
            custom_days = st.number_input('Enter number of days to forecast:', min_value=1, max_value=365, value=30)
            n = min(custom_days, len(X))
        else:
            period_map = {'Next 7 days': 7, 'Next 30 days': 30, 'Next 90 days': 90}
            n = min(period_map[period], len(X))
        
        # Simple statistical forecasting using pandas rolling mean
        if y is not None and len(y) > 0:
            # Use rolling mean for forecasting
            if len(y) >= n:
                y_pred = y.rolling(window=min(n, len(y)//2)).mean().iloc[-n:].fillna(y.mean())
            else:
                # If not enough data, use the mean
                y_pred = np.full(n, y.mean())
        else:
            y_pred = np.zeros(n)  # Fallback if no target column

        st.markdown('**Forecasted Sales/Profit:**')
        chart_df = pd.DataFrame({'Forecast': y_pred})
        st.line_chart(chart_df.reset_index(drop=True))
        st.markdown(f'**Average predicted {target_col}:** :blue[{np.mean(y_pred):.2f}]')
        # Download forecast
        csv = io.StringIO()
        pd.DataFrame({'Forecast': y_pred}).to_csv(csv, index=False)
        st.download_button('Download Forecast as CSV', csv.getvalue(), file_name='forecast.csv', mime='text/csv')
        # Save for use in suggestions/analytics
        st.session_state['model'] = None # No model saved
        st.session_state['label_encoders'] = label_encoders
        st.session_state['feature_cols'] = feature_cols
        st.session_state['target_col'] = target_col
        st.session_state['forecast'] = y_pred
        st.session_state['forecast_period'] = n

    elif nav == 'suggestions':
        if not (st.session_state.get('file_uploaded') and st.session_state.get('user_df') is not None):
            st.warning('Please upload your dataset first in the "Upload Data" section.')
            return
        st.header('💡 Suggestions & Sales Insights')
        if 'forecast' not in st.session_state:
            st.warning('Please run a forecast first.')
            return
        df = st.session_state['user_df']
        y_pred = st.session_state['forecast']
        target_col = st.session_state['target_col']
        date_col, _, product_col, _ = detect_columns(df)
        st.markdown(f'**Your average predicted {target_col} is:** :blue[{np.mean(y_pred):.2f}]')
        suggestions = []
        if product_col and product_col in df.columns:
            product_sales = df.groupby(product_col)[target_col].sum().sort_values(ascending=False)
            top_products = product_sales.head(3)
            if len(top_products) > 0:
                suggestions.append('🏆 **Top 3 products expected to generate highest future sales:**')
                for i, (product, total) in enumerate(top_products.items(), 1):
                    suggestions.append(f'   {i}. **{product}** — Current total: ${total:,.2f}')
                suggestions.append('')
        if product_col and product_col in df.columns:
            avg_product_sales = df.groupby(product_col)[target_col].mean().sort_values(ascending=False)
            high_performers = avg_product_sales.head(3)
            if len(high_performers) > 0:
                suggestions.append('📦 **Recommended inventory focus based on predicted sales:**')
                for i, (product, avg_sales) in enumerate(high_performers.items(), 1):
                    suggestions.append(f'   {i}. **{product}** — Average {target_col}: ${avg_sales:,.2f}')
                suggestions.append('')
        if date_col and date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            monthly_sales = df.groupby(df[date_col].dt.to_period('M'))[target_col].sum()
            if len(monthly_sales) > 1:
                recent_trend = monthly_sales.iloc[-1] - monthly_sales.iloc[-2]
                if recent_trend > 0:
                    suggestions.append(f'📈 **Sales trend:** Your {target_col} is trending upward (+${recent_trend:,.2f} vs previous month)')
                else:
                    suggestions.append(f'📉 **Sales trend:** Your {target_col} is trending downward (${recent_trend:,.2f} vs previous month)')
                suggestions.append('')
        forecast_avg = np.mean(y_pred)
        current_avg = df[target_col].mean()
        if forecast_avg > current_avg * 1.1:
            suggestions.append(f'🚀 **Growth opportunity:** Your forecast shows {((forecast_avg/current_avg)-1)*100:.1f}% growth potential.')
        elif forecast_avg < current_avg * 0.9:
            suggestions.append(f'⚠️ **Attention needed:** Your forecast shows a potential decline of {((1-forecast_avg/current_avg)*100):.1f}%.')
        else:
            suggestions.append('📊 **Stable outlook:** Your forecast shows consistent performance.')
        for suggestion in suggestions:
            st.markdown(suggestion)
        st.info('💡 These insights are based on your historical data and AI-powered sales forecasts.')

    elif nav == 'analytics':
        if not (st.session_state.get('file_uploaded') and st.session_state.get('user_df') is not None):
            st.warning('Please upload your dataset first in the "Upload Data" section.')
            return
        st.header('📈 Visual Analytics')
        if 'forecast' not in st.session_state:
            st.warning('Please run a forecast first.')
            return
        df = st.session_state['user_df']
        y_pred = st.session_state['forecast']
        target_col = st.session_state['target_col']
        date_col, _, product_col, _ = detect_columns(df)
        st.markdown('**Forecasted Total Sales per Product**')
        if product_col and product_col in df.columns:
            forecast_avg = np.mean(y_pred)
            total_forecast = forecast_avg * len(y_pred)
            product_sales = df.groupby(product_col)[target_col].sum()
            total_historical = product_sales.sum()
            forecasted_product_sales = {product: total_forecast * (product_sales[product] / total_historical) for product in product_sales.index}
            forecast_df = pd.DataFrame(list(forecasted_product_sales.items()), columns=['Product', 'Forecasted Sales'])
            forecast_df = forecast_df.sort_values('Forecasted Sales', ascending=False)
            st.markdown('**Bar Chart: Forecasted Sales by Product**')
            st.bar_chart(forecast_df.set_index('Product'))
            if PLOTTING_AVAILABLE:
                st.markdown('**Pie Chart: Product Sales Share (Forecasted)**')
                fig, ax = plt.subplots(figsize=(10, 8))
                forecast_df.plot.pie(y='Forecasted Sales', labels=forecast_df['Product'], autopct='%1.1f%%', ax=ax, legend=False)
                ax.set_ylabel('')
                st.pyplot(fig)
            else:
                st.markdown('**Product Sales Share (Forecasted)**')
                st.dataframe(forecast_df)
                st.info('📊 Pie chart not available. Showing data table instead.')
            st.markdown('**Forecast Summary:**')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Forecasted Sales", f"${total_forecast:,.2f}")
            with col2:
                st.metric("Average per Period", f"${forecast_avg:,.2f}")
            with col3:
                top_product = forecast_df.iloc[0]['Product']
                top_sales = forecast_df.iloc[0]['Forecasted Sales']
                st.metric("Top Product", f"{top_product}\n${top_sales:,.2f}")
        else:
            st.info('No product column detected. Please ensure your data has a product or item column for product-level analytics.')
        st.info('💡 These charts show which products are expected to drive the most sales in the forecast period, helping you focus your sales strategy.')

    elif nav == 'about':
        st.header('ℹ️ About & Help')
        st.markdown('''
        **Salesman AI Forecast** is a professional, interactive platform for sales forecasting and business suggestions.
        - Upload your sales data (CSV/Excel)
        - Select a forecast period and see predictions
        - Get actionable, AI-powered suggestions
        - Explore interactive analytics
        
        **Contact:** your.email@example.com
        ''')
        st.success('Thank you for using Salesman AI Forecast!')

if __name__ == '__main__':
    main() 