import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import base64
from data_utils import preprocess_dynamic, detect_columns
from model import simple_forecast

# Configure page
st.set_page_config(
    page_title="Market Maven - Sales Forecasting Platform",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with dark theme support
def load_custom_css():
    # Initialize theme in session state
    if 'dark_theme' not in st.session_state:
        st.session_state.dark_theme = False
    
    # Set theme colors based on current theme
    if st.session_state.dark_theme:
        theme_vars = {
            'bg_color': '#1a1a1a',
            'card_bg': '#2d2d2d',
            'text_color': '#ffffff',
            'text_secondary': '#cccccc',
            'border_color': '#444444',
            'shadow': 'rgba(0,0,0,0.5)'
        }
    else:
        theme_vars = {
            'bg_color': '#ffffff',
            'card_bg': '#ffffff',
            'text_color': '#262730',
            'text_secondary': '#6c757d',
            'border_color': '#e1e5e9',
            'shadow': 'rgba(0,0,0,0.08)'
        }
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles - Full page theming */
    .stApp {{
        background-color: {theme_vars['bg_color']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .main {{
        padding: 0rem 1rem;
        background-color: {theme_vars['bg_color']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {theme_vars['bg_color']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Force background for all containers */
    .block-container {{
        background-color: {theme_vars['bg_color']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .element-container {{
        background-color: transparent !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px {theme_vars['shadow']};
    }}
    
    .main-header h1 {{
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .main-header p {{
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }}
    
    /* Enhanced Card styling with premium hover effects */
    .metric-card {{
        background: {theme_vars['card_bg']};
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px {theme_vars['shadow']};
        border: 1px solid {theme_vars['border_color']};
        margin-bottom: 1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        color: {theme_vars['text_color']};
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }}
    
    .metric-card:before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #56ab2f);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px {theme_vars['shadow']};
        border-color: #667eea;
    }}
    
    .metric-card:hover:before {{
        transform: scaleX(1);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }}
    
    .metric-label {{
        font-size: 0.9rem;
        color: {theme_vars['text_secondary']};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Success/Error styling */
    .success-box {{
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }}
    
    .warning-box {{
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }}
    
    /* Enhanced Button styling with better hover effects */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button:before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #5a6fd8 0%, #6b4190 100%);
    }}
    
    .stButton > button:hover:before {{
        left: 100%;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }}
    
    /* Theme toggle button with mobile optimization */
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: {theme_vars['card_bg']};
        border: 1px solid {theme_vars['border_color']};
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 1.5rem;
        box-shadow: 0 4px 20px {theme_vars['shadow']};
        transition: all 0.2s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.1);
    }}
    
    /* Mobile theme toggle adjustments */
    @media (max-width: 768px) {{
        .theme-toggle {{
            width: 60px !important;
            height: 60px !important;
            font-size: 1.8rem !important;
            top: 10px !important;
            right: 10px !important;
        }}
    }}
    
    /* Touch-friendly adjustments for mobile */
    @media (max-width: 480px) {{
        .theme-toggle {{
            width: 55px !important;
            height: 55px !important;
            top: 8px !important;
            right: 8px !important;
        }}
    }}
    
    /* Enhanced Sidebar styling with responsive design */
    .css-1d391kg, .stSidebar {{
        background-color: {theme_vars['card_bg']} !important;
        border-right: 1px solid {theme_vars['border_color']} !important;
    }}
    
    .stSidebar > div {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {{
        .stSidebar {{
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }}
        
        .stSidebar .stSelectbox label {{
            font-size: 1.1rem !important;
            margin-bottom: 0.75rem !important;
        }}
        
        .stSidebar .stSelectbox > div > div {{
            padding: 1rem !important;
            font-size: 1rem !important;
            min-height: 48px !important;
        }}
        
        .main-header h1 {{
            font-size: 2rem !important;
        }}
        
        .metric-card {{
            margin-bottom: 1.5rem !important;
            padding: 1rem !important;
        }}
        
        .metric-value {{
            font-size: 1.8rem !important;
        }}
        
        .metric-label {{
            font-size: 0.9rem !important;
        }}
    }}
    
    @media (max-width: 480px) {{
        .main-header h1 {{
            font-size: 1.5rem !important;
        }}
        
        .main-header p {{
            font-size: 0.9rem !important;
        }}
        
        .stButton > button {{
            width: 100% !important;
            margin: 0.5rem 0 !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
        }}
        
        .stSelectbox > div > div {{
            min-height: 44px !important;
            font-size: 0.95rem !important;
        }}
        
        .chart-container {{
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }}
        
        /* Improve sidebar visibility on mobile */
        .css-9s5bis {{
            display: block !important;
            z-index: 999 !important;
        }}
        
        /* Make navigation more touch-friendly */
        .stSelectbox label {{
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #667eea !important;
            margin-bottom: 1rem !important;
        }}
        
        /* Ensure main content has proper spacing on mobile */
        .main .block-container {{
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        
        /* File uploader mobile optimization */
        .stFileUploader {{
            padding: 1.5rem !important;
        }}
        
        /* Mobile-friendly metric cards in columns */
        .stColumns {{
            gap: 1rem !important;
        }}
        
        /* Progress indicators */
        .stProgress {{
            margin: 1rem 0 !important;
        }}
    }}
    
    .stSidebar .stSelectbox {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    .stSidebar .stSelectbox > div > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border: 1px solid {theme_vars['border_color']} !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stSidebar .stSelectbox > div > div > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .stSelectbox > div > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border: 1px solid {theme_vars['border_color']} !important;
    }}
    
    .stSelectbox > div > div > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .stSelectbox [data-baseweb="select"] > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    /* Fix dropdown menu background */
    .stSelectbox [data-baseweb="popover"] {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    .stSelectbox [data-baseweb="menu"] {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    .stSelectbox [data-baseweb="menu"] ul {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    .stSelectbox [data-baseweb="menu"] li {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .stSelectbox [data-baseweb="menu"] li:hover {{
        background-color: {theme_vars['border_color']} !important;
    }}
    
    /* Additional selectbox styling for complete dark theme support */
    [data-testid="stSelectbox"] > div > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    [data-testid="stSelectbox"] [data-baseweb="select"] {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    .stSidebar .stSelectbox > div > div:hover {{
        border-color: #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-1px) !important;
    }}
    
    .stSidebar .stSelectbox label {{
        color: {theme_vars['text_color']} !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    .stSidebar .stMarkdown {{
        color: {theme_vars['text_color']} !important;
    }}
    
    .stSidebar .stMarkdown h3 {{
        color: #667eea !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #667eea !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1rem !important;
    }}
    
    .stSidebar .stMetric {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border: 1px solid {theme_vars['border_color']} !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        margin: 0.25rem 0 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stSidebar .stMetric:hover {{
        border-color: #667eea !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-2px) !important;
    }}
    
    .stSidebar .stMetric > div {{
        background-color: transparent !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Sidebar section divider */
    .stSidebar hr {{
        border-color: {theme_vars['border_color']} !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* Enhanced File uploader styling with premium effects */
    .stFileUploader {{
        background: {theme_vars['card_bg']};
        border: 2px dashed {theme_vars['border_color']};
        border-radius: 15px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .stFileUploader:before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.6s ease;
    }}
    
    .stFileUploader:hover {{
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }}
    
    .stFileUploader:hover:before {{
        left: 100%;
    }}
    
    /* Enhanced Progress bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 8px !important;
    }}
    
    /* Premium Chart container with hover effects */
    .chart-container {{
        background: {theme_vars['card_bg']};
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px {theme_vars['shadow']};
        margin-bottom: 2rem;
        border: 1px solid {theme_vars['border_color']};
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .chart-container:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px {theme_vars['shadow']};
        border-color: rgba(102, 126, 234, 0.3);
    }}
    
    /* Premium Loading Spinner */
    .stSpinner > div {{
        width: 60px !important;
        height: 60px !important;
        border: 4px solid {theme_vars['border_color']} !important;
        border-top: 4px solid #667eea !important;
        border-radius: 50% !important;
        animation: premium-spin 1s linear infinite !important;
    }}
    
    @keyframes premium-spin {{
        0% {{ 
            transform: rotate(0deg);
            border-top-color: #667eea;
        }}
        25% {{ 
            border-top-color: #764ba2;
        }}
        50% {{ 
            border-top-color: #56ab2f;
        }}
        75% {{ 
            border-top-color: #f093fb;
        }}
        100% {{ 
            transform: rotate(360deg);
            border-top-color: #667eea;
        }}
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Custom animations */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .animate-fade-in {{
        animation: fadeInUp 0.6s ease-out;
    }}
    
    /* Comprehensive Streamlit widget styling */
    .stSelectbox > div > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    .stSelectbox label {{
        color: {theme_vars['text_color']} !important;
    }}
    
    .stTextInput > div > div > input {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border: 2px solid {theme_vars['border_color']} !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextInput label {{
        color: {theme_vars['text_color']} !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    .stDataFrame {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px {theme_vars['shadow']} !important;
    }}
    
    .stDataFrame table {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .stDataFrame th {{
        background-color: {theme_vars['border_color']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .stDataFrame td {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    /* Number input styling */
    .stNumberInput > div > div > input {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    .stNumberInput label {{
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Slider styling */
    .stSlider > div > div > div {{
        background-color: {theme_vars['card_bg']} !important;
    }}
    
    .stSlider label {{
        color: {theme_vars['text_color']} !important;
    }}
    
    /* File uploader text */
    .stFileUploader label {{
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Markdown text */
    .stMarkdown {{
        color: {theme_vars['text_color']} !important;
    }}
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
        color: {theme_vars['text_color']} !important;
    }}
    
    .stMarkdown p {{
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Metric styling */
    .stMetric {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    .stMetric > div {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
    }}
    
    /* Download button */
    .stDownloadButton > button {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-color: {theme_vars['border_color']} !important;
    }}
    
    /* Columns */
    .stColumn {{
        background-color: transparent !important;
    }}
    
    /* Info/Warning/Success boxes - enhance for theme */
    .stInfo {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    .stWarning {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    
    .stSuccess {{
        background-color: {theme_vars['card_bg']} !important;
        color: {theme_vars['text_color']} !important;
        border-color: {theme_vars['border_color']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def display_header():
    # Theme toggle button
    theme_icon = "🌙" if not st.session_state.dark_theme else "☀️"
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button(theme_icon, key="theme_toggle", help="Toggle theme"):
            st.session_state.dark_theme = not st.session_state.dark_theme
            st.rerun()
    
    st.markdown("""
    <div class="main-header animate-fade-in">
        <h1>🏪 Market Maven</h1>
        <p>Professional Sales Forecasting & Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

def display_metric_card(title, value, subtitle=""):
    # Get theme-aware colors for subtitle
    subtitle_color = '#cccccc' if st.session_state.get('dark_theme', False) else '#6c757d'
    
    st.markdown(f"""
    <div class="metric-card animate-fade-in">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        {f'<div style="font-size: 0.8rem; color: {subtitle_color}; margin-top: 0.5rem;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_professional_chart(data, chart_type, title, x_col=None, y_col=None, color_col=None):
    """Create professional-looking charts with consistent styling"""
    
    # Get theme-aware colors
    theme_aware_bg = 'rgba(0,0,0,0)'
    if st.session_state.get('dark_theme', False):
        title_color = '#ffffff'
        grid_color = 'rgba(255,255,255,0.2)'
        line_color = 'rgba(255,255,255,0.3)'
    else:
        title_color = '#262730'
        grid_color = 'rgba(128,128,128,0.2)'
        line_color = 'rgba(128,128,128,0.3)'
    
    if chart_type == "line":
        fig = px.line(data, x=x_col, y=y_col, title=title,
                     color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'])
    elif chart_type == "bar":
        fig = px.bar(data, x=x_col, y=y_col, title=title,
                    color_discrete_sequence=['#667eea'])
    elif chart_type == "pie":
        fig = px.pie(data, values=y_col, names=x_col, title=title,
                    color_discrete_sequence=['#667eea', '#764ba2', '#56ab2f', '#f093fb', '#ff6b6b', '#4ecdc4'])
        
        # Fix text overlap in pie chart with better spacing
        fig.update_traces(
            textposition='outside',
            textinfo='percent+label',
            textfont_size=10,
            marker=dict(line=dict(color='#FFFFFF', width=2)),
            pull=[0.05 if i == 0 else 0 for i in range(len(data))]  # Pull out first slice slightly
        )
        
        # Adjust layout for better spacing and readability
        fig.update_layout(
            height=600,
            margin=dict(l=80, r=80, t=100, b=80),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.1,
                font=dict(size=10),
                itemwidth=30
            ),
            showlegend=True,
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
        
    elif chart_type == "scatter":
        fig = px.scatter(data, x=x_col, y=y_col, title=title,
                        color=color_col if color_col else None,
                        color_discrete_sequence=['#667eea', '#764ba2'])
    
    # Apply consistent styling
    fig.update_layout(
        font_family="Inter",
        title_font_size=18,
        title_font_color=title_color,
        title_x=0.5,
        plot_bgcolor=theme_aware_bg,
        paper_bgcolor=theme_aware_bg,
        font_color=title_color,
        showlegend=True
    )
    
    # Only update axes for non-pie charts
    if chart_type != "pie":
        fig.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(
            gridcolor=grid_color,
            gridwidth=1,
            zeroline=False,
            showline=True,
            linecolor=line_color
        )
        fig.update_yaxes(
            gridcolor=grid_color,
            gridwidth=1,
            zeroline=False,
            showline=True,
            linecolor=line_color
        )
    
    return fig

def main():
    load_custom_css()
    
    # Initialize session state
    if 'user_df' not in st.session_state:
        st.session_state.user_df = None
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    
    # Sidebar navigation with mobile enhancements
    with st.sidebar:
        # Mobile-friendly navigation hint
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #667eea;">
            <small>📱 <strong>Mobile Navigation:</strong> Select pages below</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Navigation")
        
        page = st.selectbox(
            "Choose a section",
            ["🏠 Home", "📁 Upload Data", "📈 Forecast", "💡 Insights", "📊 Analytics", "ℹ️ About"],
            index=0,
            help="Use this dropdown to navigate between different sections of the app"
        )
        
        st.markdown("---")
        
        if st.session_state.file_uploaded:
            st.markdown("### 📋 Data Summary")
            df = st.session_state.user_df
            st.metric("Total Records", len(df))
            st.metric("Columns", len(df.columns))
            if 'Total' in df.columns:
                st.metric("Avg Sales", f"${df['Total'].mean():.2f}")
    
    # Main content
    display_header()
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📁 Upload Data":
        show_upload_page()
    elif page == "📈 Forecast":
        show_forecast_page()
    elif page == "💡 Insights":
        show_insights_page()
    elif page == "📊 Analytics":
        show_analytics_page()
    elif page == "ℹ️ About":
        show_about_page()

def show_home_page():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_metric_card("AI-Powered", "Forecasting", "Advanced machine learning algorithms")
    
    with col2:
        display_metric_card("Real-time", "Analytics", "Live data processing and insights")
    
    with col3:
        display_metric_card("Professional", "Reports", "Export-ready visualizations")
    
    st.markdown("---")
    
    st.markdown("""
    ## 🚀 Welcome to Market Maven
    
    Market Maven is your comprehensive sales forecasting and analytics platform designed for modern businesses. 
    Our AI-powered system helps you make data-driven decisions with confidence.
    
    ### Key Features:
    - **📊 Advanced Analytics**: Deep insights into your sales patterns
    - **🔮 AI Forecasting**: Predict future sales with machine learning
    - **📱 Responsive Design**: Works seamlessly on all devices
    - **📈 Interactive Charts**: Beautiful, interactive visualizations
    - **💼 Professional Reports**: Export-ready business intelligence
    
    ### Getting Started:
    1. **Upload your data** using the sidebar navigation
    2. **Generate forecasts** to predict future sales
    3. **Explore insights** to understand your business better
    4. **View analytics** for comprehensive reporting
    
    Ready to transform your sales strategy? Start by uploading your data!
    """)

def show_upload_page():
    st.markdown("## 📁 Upload Your Sales Data")
    
    uploaded_file = st.file_uploader(
        "Choose your sales data file",
        type=['csv', 'xlsx'],
        help="Upload CSV or Excel files containing your sales data"
    )
    
    if uploaded_file is not None:
        try:
            # Show loading animation
            with st.spinner('Processing your data...'):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            
            st.markdown('<div class="success-box">✅ File uploaded successfully!</div>', 
                       unsafe_allow_html=True)
            
            # Store in session state
            st.session_state.user_df = df
            st.session_state.file_uploaded = True
            
            # Display data preview
            st.markdown("### 📋 Data Preview")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                display_metric_card("Rows", f"{len(df):,}")
            with col2:
                display_metric_card("Columns", f"{len(df.columns)}")
            with col3:
                if 'Total' in df.columns:
                    display_metric_card("Total Sales", f"${df['Total'].sum():,.2f}")
                else:
                    display_metric_card("Data Type", "Sales Data")
            with col4:
                display_metric_card("Status", "Ready")
            
            # Interactive data table
            st.markdown("### 🔍 Interactive Data Table")
            st.dataframe(
                df.head(100), 
                use_container_width=True,
                height=400
            )
            
            # Column analysis
            if len(df.columns) > 0:
                st.markdown("### 📊 Column Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    st.markdown(f"**Numeric Columns ({len(numeric_cols)}):**")
                    for col in numeric_cols[:10]:  # Show first 10
                        st.markdown(f"• {col}")
                
                with col2:
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    st.markdown(f"**Categorical Columns ({len(categorical_cols)}):**")
                    for col in categorical_cols[:10]:  # Show first 10
                        st.markdown(f"• {col}")
            
        except Exception as e:
            st.markdown(f'<div class="warning-box">❌ Error processing file: {str(e)}</div>', 
                       unsafe_allow_html=True)
    
    else:
        st.markdown("""
        ### 📝 Data Requirements
        
        Your data should include:
        - **Date/Time columns** for temporal analysis
        - **Sales/Revenue columns** for forecasting
        - **Product/Category columns** for segmentation
        - **Additional dimensions** for deeper insights
        
        **Supported formats:** CSV, Excel (.xlsx)
        """)

def show_forecast_page():
    if not st.session_state.file_uploaded:
        st.markdown('<div class="warning-box">⚠️ Please upload your data first!</div>', 
                   unsafe_allow_html=True)
        return
    
    st.markdown("## 📈 Sales Forecasting")
    
    df = st.session_state.user_df
    date_col, target_col, product_col, external_cols = detect_columns(df)
    
    if not target_col:
        st.markdown('<div class="warning-box">❌ Could not detect sales/target column. Please check your data.</div>', 
                   unsafe_allow_html=True)
        return
    
    # Forecast configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Forecast Settings")
        period_options = {
            'Next 7 days': 7,
            'Next 30 days': 30,
            'Next 90 days': 90,
            'Next 6 months': 180,
            'Custom period': 0
        }
        
        selected_period = st.selectbox(
            "Forecast Period",
            list(period_options.keys())
        )
        
        if selected_period == 'Custom period':
            custom_days = st.number_input(
                'Enter number of days',
                min_value=1,
                max_value=365,
                value=30
            )
            forecast_days = custom_days
        else:
            forecast_days = period_options[selected_period]
    
    with col2:
        st.markdown("### 📊 Model Settings")
        confidence_level = st.slider(
            "Confidence Level",
            min_value=80,
            max_value=99,
            value=95,
            help="Confidence interval for predictions"
        )
        
        smoothing = st.selectbox(
            "Smoothing Method",
            ["Moving Average", "Exponential", "Linear Trend"]
        )
    
    # Generate forecast button
    if st.button("🔮 Generate Forecast", type="primary"):
        with st.spinner('Generating forecast...'):
            try:
                # Preprocess data
                X, y, label_encoders, feature_cols = preprocess_dynamic(
                    df, date_col, target_col, product_col, external_cols
                )
                
                # Generate forecast
                forecast_data = simple_forecast(y, forecast_days, method=smoothing.lower())
                
                # Store forecast in session state
                st.session_state.forecast = forecast_data
                st.session_state.forecast_period = forecast_days
                st.session_state.target_col = target_col
                
                st.markdown('<div class="success-box">✅ Forecast generated successfully!</div>', 
                           unsafe_allow_html=True)
                
                # Display forecast results
                display_forecast_results(forecast_data, target_col, forecast_days)
                
            except Exception as e:
                st.markdown(f'<div class="warning-box">❌ Error generating forecast: {str(e)}</div>', 
                           unsafe_allow_html=True)

def display_forecast_results(forecast_data, target_col, forecast_days):
    st.markdown("## 📊 Forecast Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_metric_card("Forecast Period", f"{forecast_days} days")
    
    with col2:
        avg_forecast = np.mean(forecast_data)
        display_metric_card("Avg Daily Sales", f"${avg_forecast:.2f}")
    
    with col3:
        total_forecast = np.sum(forecast_data)
        display_metric_card("Total Forecast", f"${total_forecast:,.2f}")
    
    with col4:
        growth_rate = ((forecast_data[-1] / forecast_data[0]) - 1) * 100 if forecast_data[0] != 0 else 0
        display_metric_card("Growth Rate", f"{growth_rate:.1f}%")
    
    # Forecast chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'Day': range(1, len(forecast_data) + 1),
        'Forecast': forecast_data,
        'Upper_Bound': forecast_data * 1.1,
        'Lower_Bound': forecast_data * 0.9
    })
    
    # Create interactive chart
    fig = go.Figure()
    
    # Add forecast line
    fig.add_trace(go.Scatter(
        x=forecast_df['Day'],
        y=forecast_df['Forecast'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6)
    ))
    
    # Add confidence interval
    fig.add_trace(go.Scatter(
        x=forecast_df['Day'],
        y=forecast_df['Upper_Bound'],
        mode='lines',
        name='Upper Bound',
        line=dict(color='rgba(102, 126, 234, 0.3)', width=1),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_df['Day'],
        y=forecast_df['Lower_Bound'],
        mode='lines',
        name='Lower Bound',
        line=dict(color='rgba(102, 126, 234, 0.3)', width=1),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        showlegend=False
    ))
    
    # Get theme-aware colors for forecast chart
    if st.session_state.get('dark_theme', False):
        title_color = '#ffffff'
        grid_color = 'rgba(255,255,255,0.2)'
        line_color = 'rgba(255,255,255,0.3)'
    else:
        title_color = '#262730'
        grid_color = 'rgba(128,128,128,0.2)'
        line_color = 'rgba(128,128,128,0.3)'
    
    fig.update_layout(
        title=f"{target_col} Forecast - Next {forecast_days} Days",
        xaxis_title="Days",
        yaxis_title=f"{target_col} ($)",
        font_family="Inter",
        title_font_color=title_color,
        font_color=title_color,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(
        gridcolor=grid_color,
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor=line_color
    )
    fig.update_yaxes(
        gridcolor=grid_color,
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor=line_color
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download forecast
    csv_data = forecast_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Forecast Data",
        data=csv_data,
        file_name=f"forecast_{forecast_days}_days.csv",
        mime="text/csv",
        type="secondary"
    )

def show_insights_page():
    if not st.session_state.file_uploaded:
        st.markdown('<div class="warning-box">⚠️ Please upload your data first!</div>', 
                   unsafe_allow_html=True)
        return
    
    if 'forecast' not in st.session_state:
        st.markdown('<div class="warning-box">⚠️ Please generate a forecast first!</div>', 
                   unsafe_allow_html=True)
        return
    
    st.markdown("## 💡 Business Insights & Recommendations")
    
    df = st.session_state.user_df
    forecast_data = st.session_state.forecast
    target_col = st.session_state.target_col
    
    # Generate insights
    insights = generate_business_insights(df, forecast_data, target_col)
    
    # Display enhanced insights with Streamlit components
    for insight in insights:
        # Get theme-aware colors
        if st.session_state.get('dark_theme', False):
            priority_colors = {'Critical': '#ff4757', 'High': '#ff6348', 'Medium': '#ffa502', 'Low': '#7bed9f'}
        else:
            priority_colors = {'Critical': '#e74c3c', 'High': '#e67e22', 'Medium': '#f39c12', 'Low': '#27ae60'}
            
        priority = insight.get('priority', 'Medium')
        category = insight.get('category', 'General')
        priority_color = priority_colors.get(priority, '#667eea')
        
        # Create insight card using containers
        with st.container():
            # Header with badges
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {insight['title']}")
            with col2:
                st.markdown(f"""
                <div style="text-align: right;">
                    <span style="background: {priority_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-right: 0.5rem;">{priority}</span>
                    <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">{category}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Description
            st.markdown(insight['description'])
            
            # Recommendation in info box
            st.info(f"💡 **Recommendation:** {insight.get('recommendation', '')}")
            
            # Action items
            if 'action_items' in insight and insight['action_items']:
                st.markdown("**🎯 Action Items:**")
                for item in insight['action_items']:
                    st.markdown(f"• {item}")
            
            st.markdown("---")

def show_analytics_page():
    if not st.session_state.file_uploaded:
        st.markdown('<div class="warning-box">⚠️ Please upload your data first!</div>', 
                   unsafe_allow_html=True)
        return
    
    st.markdown("## 📊 Advanced Analytics Dashboard")
    
    df = st.session_state.user_df
    date_col, target_col, product_col, external_cols = detect_columns(df)
    
    # Analytics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df[target_col].sum() if target_col else 0
        display_metric_card("Total Sales", f"${total_sales:,.2f}")
    
    with col2:
        avg_sales = df[target_col].mean() if target_col else 0
        display_metric_card("Average Sale", f"${avg_sales:.2f}")
    
    with col3:
        num_transactions = len(df)
        display_metric_card("Transactions", f"{num_transactions:,}")
    
    with col4:
        if product_col and product_col in df.columns:
            unique_products = df[product_col].nunique()
            display_metric_card("Unique Products", f"{unique_products}")
    
    # Charts section
    st.markdown("### 📈 Performance Analytics")
    
    if product_col and product_col in df.columns and target_col:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top products by sales
            product_sales = df.groupby(product_col)[target_col].sum().sort_values(ascending=False).head(10)
            fig = create_professional_chart(
                pd.DataFrame({'Product': product_sales.index, 'Sales': product_sales.values}),
                'bar', 'Top 10 Products by Sales', 'Product', 'Sales'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sales distribution pie chart
            fig = create_professional_chart(
                pd.DataFrame({'Product': product_sales.head(5).index, 'Sales': product_sales.head(5).values}),
                'pie', 'Sales Distribution (Top 5)', 'Product', 'Sales'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Time series analysis
    if date_col and date_col in df.columns and target_col:
        st.markdown("### 📅 Time Series Analysis")
        
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        daily_sales = df.groupby(df[date_col].dt.date)[target_col].sum().reset_index()
        daily_sales.columns = ['Date', 'Sales']
        
        fig = create_professional_chart(
            daily_sales, 'line', 'Daily Sales Trend', 'Date', 'Sales'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_about_page():
    st.markdown("""
    ## ℹ️ About Market Maven
    
    Market Maven is a professional sales forecasting and analytics platform designed to help businesses 
    make data-driven decisions. Built with cutting-edge technology and modern design principles.
    
    ### 🛠️ Technology Stack
    - **Frontend**: Streamlit with custom CSS
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Plotly, Interactive Charts
    - **Machine Learning**: Scikit-learn
    - **Design**: Professional UI/UX with responsive layout
    
    ### 🚀 Features
    - AI-powered sales forecasting
    - Interactive data visualization
    - Business intelligence insights
    - Professional reporting
    - Mobile-responsive design
    - Export capabilities
    
    ### 📞 Support
    For questions or support, please contact our team at support@marketmaven.com
    
    ### 📄 Version
    Market Maven v2.0 - Professional Edition
    
    ---
    
    *Built with ❤️ for modern businesses*
    """)

def generate_business_insights(df, forecast_data, target_col):
    """Generate comprehensive business insights based on data and forecast"""
    insights = []
    
    # Forecast performance insight
    avg_forecast = np.mean(forecast_data)
    current_avg = df[target_col].mean() if target_col else 0
    
    if avg_forecast > current_avg * 1.1:
        insights.append({
            'title': '🚀 Strong Growth Potential',
            'description': f'Your forecast shows a {((avg_forecast/current_avg)-1)*100:.1f}% increase in average sales.',
            'recommendation': 'Increase inventory by 20-30%, expand marketing budget, consider new distribution channels.',
            'action_items': ['Secure additional suppliers', 'Boost digital marketing spend', 'Prepare for higher demand'],
            'priority': 'High',
            'category': 'Growth'
        })
    elif avg_forecast < current_avg * 0.9:
        insights.append({
            'title': '⚠️ Performance Alert',
            'description': f'Your forecast indicates a potential {((1-avg_forecast/current_avg)*100):.1f}% decline in sales.',
            'recommendation': 'Implement promotional campaigns, review pricing strategy, analyze market competition.',
            'action_items': ['Launch 15-20% discount campaign', 'Conduct competitor price analysis', 'Survey customer satisfaction'],
            'priority': 'Critical',
            'category': 'Risk Management'
        })
    else:
        insights.append({
            'title': '📈 Stable Performance',
            'description': 'Your sales forecast shows consistent performance with current trends.',
            'recommendation': 'Maintain current strategies while exploring optimization opportunities.',
            'action_items': ['Monitor market trends', 'Test new marketing channels', 'Optimize operational efficiency'],
            'priority': 'Medium',
            'category': 'Optimization'
        })
    
    # Product performance insights
    date_col, _, product_col, _ = detect_columns(df)
    
    if product_col and product_col in df.columns:
        product_sales = df.groupby(product_col)[target_col].sum().sort_values(ascending=False)
        top_product = product_sales.index[0]
        top_sales = product_sales.iloc[0]
        total_sales = product_sales.sum()
        top_percentage = (top_sales / total_sales) * 100
        
        insights.append({
            'title': '🏆 Top Performer Analysis',
            'description': f'"{top_product}" dominates with ${top_sales:,.2f} ({top_percentage:.1f}% of total sales).',
            'recommendation': 'Leverage this success by creating product bundles and cross-selling opportunities.',
            'action_items': ['Create premium bundles', 'Develop complementary products', 'Feature in marketing campaigns'],
            'priority': 'High',
            'category': 'Product Strategy'
        })
        
        # Low performers analysis
        if len(product_sales) > 3:
            bottom_performers = product_sales.tail(3)
            insights.append({
                'title': '📉 Underperforming Products',
                'description': f'Bottom 3 products contribute only ${bottom_performers.sum():,.2f} in sales.',
                'recommendation': 'Consider discontinuing or repositioning low-performing products.',
                'action_items': ['Analyze profit margins', 'Test promotional pricing', 'Consider product redesign'],
                'priority': 'Medium',
                'category': 'Product Strategy'
            })
    
    # Sales velocity insights
    if target_col:
        sales_std = df[target_col].std()
        sales_mean = df[target_col].mean()
        cv = sales_std / sales_mean if sales_mean > 0 else 0
        
        if cv > 0.5:
            insights.append({
                'title': '📊 High Sales Volatility',
                'description': f'Sales show high variability (CV: {cv:.2f}), indicating unstable patterns.',
                'recommendation': 'Implement demand smoothing strategies and improve forecasting accuracy.',
                'action_items': ['Introduce subscription models', 'Develop loyal customer programs', 'Stabilize pricing'],
                'priority': 'Medium',
                'category': 'Risk Management'
            })
    
    # Seasonal insights
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        monthly_sales = df.groupby(df[date_col].dt.month)[target_col].mean()
        
        if len(monthly_sales) > 1:
            best_month = monthly_sales.idxmax()
            worst_month = monthly_sales.idxmin()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            peak_performance = monthly_sales.max()
            low_performance = monthly_sales.min()
            seasonal_variance = ((peak_performance - low_performance) / low_performance) * 100
            
            insights.append({
                'title': '📅 Seasonal Intelligence',
                'description': f'{month_names[best_month-1]} peaks at ${peak_performance:,.0f}, {month_names[worst_month-1]} dips to ${low_performance:,.0f} ({seasonal_variance:.0f}% variance).',
                'recommendation': 'Optimize inventory and staffing based on seasonal patterns.',
                'action_items': ['Build peak-season inventory in advance', 'Plan promotional events for slow months', 'Adjust staffing schedules'],
                'priority': 'High',
                'category': 'Seasonal Strategy'
            })
    
    # Revenue concentration insights
    if target_col:
        revenue_data = df[target_col].sort_values(ascending=False)
        total_revenue = revenue_data.sum()
        top_20_percent_count = int(len(revenue_data) * 0.2)
        top_20_percent_revenue = revenue_data.head(top_20_percent_count).sum()
        concentration_ratio = (top_20_percent_revenue / total_revenue) * 100
        
        if concentration_ratio > 80:
            insights.append({
                'title': '⚡ Revenue Concentration Risk',
                'description': f'Top 20% of transactions generate {concentration_ratio:.1f}% of revenue.',
                'recommendation': 'Diversify revenue streams to reduce dependency on high-value transactions.',
                'action_items': ['Develop mid-tier products', 'Expand customer base', 'Create recurring revenue streams'],
                'priority': 'Medium',
                'category': 'Risk Management'
            })
    
    return insights

if __name__ == "__main__":
    main()
