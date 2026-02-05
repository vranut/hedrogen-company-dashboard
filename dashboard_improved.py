import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from math import ceil

# --- Page Configuration ---
st.set_page_config(
    page_title="H2 Intelligence Hub",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #0f766e 0%, #14b8a6 50%, #2dd4bf 100%);
        --secondary-gradient: linear-gradient(135deg, #1e3a5f 0%, #0c4a6e 50%, #0369a1 100%);
        --accent-gradient: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        --dark-bg: #0f172a;
        --card-bg: rgba(255, 255, 255, 0.03);
        --border-color: rgba(255, 255, 255, 0.08);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --success: #10b981;
        --warning: #f59e0b;
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Global Background */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
    }
    
    p, span, div, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] label {
        color: var(--text-primary) !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: var(--text-secondary) !important;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(15, 118, 110, 0.15) 0%, rgba(20, 184, 166, 0.08) 100%);
        border: 1px solid rgba(20, 184, 166, 0.2);
        padding: 1.5rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(20, 184, 166, 0.15);
        border-color: rgba(20, 184, 166, 0.4);
    }
    
    div[data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: var(--success) !important;
        font-size: 0.9rem;
    }
    
    /* Company Cards */
    .company-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .company-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .company-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border-color: rgba(20, 184, 166, 0.3);
    }
    
    .company-card:hover::before {
        opacity: 1;
    }
    
    .company-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .company-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .tag-country {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
    }
    
    .tag-business {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    
    /* Search Box */
    .stTextInput input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #14b8a6 !important;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2) !important;
    }
    
    .stTextInput input::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(20, 184, 166, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(20, 184, 166, 0.4) !important;
    }
    
    /* Link Buttons */
    .stLinkButton > a {
        background: transparent !important;
        color: #14b8a6 !important;
        border: 2px solid #14b8a6 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stLinkButton > a:hover {
        background: rgba(20, 184, 166, 0.1) !important;
    }
    
    /* Company Card Container */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(20, 184, 166, 0.3) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(20, 184, 166, 0.2) !important;
        border: 1px solid rgba(20, 184, 166, 0.4) !important;
        border-radius: 8px !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--border-color) !important;
        margin: 2rem 0 !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        color: var(--text-secondary);
        border: 1px solid var(--border-color);
        padding: 0.5rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Container borders */
    [data-testid="stVerticalBlock"] > div:has(> [data-testid="stVerticalBlockBorderWrapper"]) {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* Checkbox */
    .stCheckbox label span {
        color: var(--text-primary) !important;
    }
    
    /* Caption */
    .stCaption {
        color: var(--text-secondary) !important;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    /* Pagination */
    .pagination-info {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    /* Logo placeholder */
    .logo-placeholder {
        width: 80px;
        height: 80px;
        background: linear-gradient(145deg, rgba(20, 184, 166, 0.2) 0%, rgba(14, 165, 233, 0.2) 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #14b8a6;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(20, 184, 166, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(20, 184, 166, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# --- Configuration ---
DATA_FILE = "FINAL_WEBSITE_DATA.csv"
IMG_FOLDER = "Final_Database_Images"
ITEMS_PER_PAGE = 8

# Column names
COL_COMPANY = 'Company Name'
COL_BUSINESS = 'Hydrogen-focused business'
COL_COUNTRY = 'Originator Country'
COL_INTRO = 'Basic introduction'
COL_WEBSITE = 'Website'
COL_CONTACT_TXT = 'Form of Contacts'
COL_NEWS_TEXT = 'News/Recent Outstanding Achievement/Applications and Project References'
COL_HIGHLIGHT_TEXT = 'Highlighted Info'
COL_INDUSTRY = 'Type of Industry'

# --- Helper Functions ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE).fillna("-")
    if COL_BUSINESS in df.columns:
        df[COL_BUSINESS] = df[COL_BUSINESS].astype(str).str.strip()
    if COL_COMPANY in df.columns:
        df[COL_COMPANY] = df[COL_COMPANY].astype(str).str.strip()
    return df

def get_images(img_string):
    if not img_string or img_string == "-" or pd.isna(img_string):
        return []
    return [os.path.join(IMG_FOLDER, img.strip()) for img in str(img_string).split(";") if img.strip()]

def shorten_text(text, max_len=100):
    text = str(text)
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text

def get_country_emoji(country):
    country_emojis = {
        'United States': '🇺🇸', 'Germany': '🇩🇪', 'Japan': '🇯🇵', 'China': '🇨🇳',
        'United Kingdom': '🇬🇧', 'France': '🇫🇷', 'Australia': '🇦🇺', 'Canada': '🇨🇦',
        'South Korea': '🇰🇷', 'Netherlands': '🇳🇱', 'Norway': '🇳🇴', 'Denmark': '🇩🇰',
        'Spain': '🇪🇸', 'Italy': '🇮🇹', 'India': '🇮🇳', 'Brazil': '🇧🇷',
        'Singapore': '🇸🇬', 'Thailand': '🇹🇭', 'Malaysia': '🇲🇾', 'Indonesia': '🇮🇩',
        'Saudi Arabia': '🇸🇦', 'UAE': '🇦🇪', 'Belgium': '🇧🇪', 'Sweden': '🇸🇪',
        'Switzerland': '🇨🇭', 'Austria': '🇦🇹', 'Poland': '🇵🇱', 'Finland': '🇫🇮'
    }
    return country_emojis.get(country, '🌐')

# --- Load Data ---
df = load_data()
if df is None:
    st.error(f"❌ ไม่พบไฟล์ {DATA_FILE}")
    st.stop()

# --- Initialize Session State ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">⚡</div>
            <h2 style="margin: 0; font-size: 1.5rem; color: #14b8a6;">H2 Intelligence</h2>
            <p style="color: #64748b; font-size: 0.85rem; margin-top: 0.3rem;">Hydrogen Market Database</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Search Box
    st.markdown("##### 🔍 Quick Search")
    search_query = st.text_input(
        "Search",
        placeholder="Search company name...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Business Filter
    st.markdown("##### 🏭 Business Sector")
    biz_options = sorted([x for x in df[COL_BUSINESS].unique() if x != "-" and x != "nan" and len(str(x)) > 2])
    all_biz = st.checkbox("Select All Sectors", value=True, key="all_biz")
    
    if all_biz:
        selected_biz = biz_options
    else:
        selected_biz = st.multiselect(
            "Choose sectors",
            biz_options,
            default=[],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # Country Filter
    st.markdown("##### 🌍 Country / Region")
    country_options = sorted([x for x in df[COL_COUNTRY].unique() if x != "-" and x != "nan" and x != "Unknown" and len(str(x)) > 1])
    all_country = st.checkbox("Select All Countries", value=True, key="all_country")
    
    if all_country:
        selected_country = country_options
    else:
        selected_country = st.multiselect(
            "Choose countries",
            country_options,
            default=[],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # Sort Options
    st.markdown("##### 📊 Sort By")
    sort_option = st.selectbox(
        "Sort",
        ["Company Name (A-Z)", "Company Name (Z-A)", "Country (A-Z)"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Reset Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state.current_page = 1
        st.rerun()

# --- Filter Data ---
filtered_df = df[
    (df[COL_BUSINESS].isin(selected_biz)) &
    (df[COL_COUNTRY].isin(selected_country))
]

# Apply search
if search_query:
    filtered_df = filtered_df[
        filtered_df[COL_COMPANY].str.lower().str.contains(search_query.lower(), na=False)
    ]
    st.session_state.current_page = 1

# Apply sorting
if sort_option == "Company Name (A-Z)":
    filtered_df = filtered_df.sort_values(COL_COMPANY)
elif sort_option == "Company Name (Z-A)":
    filtered_df = filtered_df.sort_values(COL_COMPANY, ascending=False)
elif sort_option == "Country (A-Z)":
    filtered_df = filtered_df.sort_values(COL_COUNTRY)

# --- Main Content ---
# Hero Section
st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <h1 class="hero-title">⚡ Hydrogen Market Intelligence</h1>
        <p class="hero-subtitle">Explore the global hydrogen economy with comprehensive company data</p>
    </div>
""", unsafe_allow_html=True)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Companies",
        value=f"{len(df):,}",
        delta="In Database"
    )

with col2:
    st.metric(
        label="Filtered Results",
        value=f"{len(filtered_df):,}",
        delta="Matching" if len(filtered_df) > 0 else "No match"
    )

with col3:
    st.metric(
        label="Business Sectors",
        value=f"{len(biz_options)}",
        delta="Categories"
    )

with col4:
    st.metric(
        label="Countries",
        value=f"{len(country_options)}",
        delta="Regions"
    )

st.markdown("---")

# --- Tabs for different views ---
tab1, tab2 = st.tabs(["📊 Analytics", "🏢 Companies"])

# --- Tab 1: Analytics ---
with tab1:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 🏭 Business Sectors")
        if not filtered_df.empty:
            biz_counts = filtered_df[COL_BUSINESS].value_counts().head(10).reset_index()
            biz_counts.columns = ['Sector', 'Count']
            
            # สร้างชื่อย่อที่อ่านง่าย
            short_names = {
                'Hydrogen Production Equipment Manaufacturers and its apparatus': 'H2 Equipment Mfg',
                'Hydrogen Production Equipment Manufacturers and its apparatus': 'H2 Equipment Mfg',
                'Conference Organizer/ Event Advertiser/Journalism/': 'Events & Media',
                'EPC and/or Engineering Services and Consulting Firms': 'EPC & Engineering',
                'Green Field of Energy/ Start-up/Innovative Technology/AI Technology': 'Green Tech & Startups',
                'Hydrogen Project Owners/Showcase/Reference/Business Portfolio': 'H2 Project Owners',
                'Renewable Energy Companies': 'Renewable Energy',
                'Government Agency/Representative/Policy Maker': 'Government',
                'Hydrogen Storage tank and other forms of Pressure Vessels': 'H2 Storage',
                'H2 Community/ Professional Association': 'H2 Associations',
                'H2 Business developer &  Investor': 'H2 Investors',
                'Academic or Research Institution': 'Research & Academia',
                'Offtaker or Terminal Ports or Maritime Logistic  or Refuelling Station': 'Maritime & Logistics',
                'Fuel Cell & Electric Vehicle': 'Fuel Cell & EV',
                'Energy Conservation Technology/ Energy Efficiency': 'Energy Efficiency',
            }
            
            biz_counts['Short'] = biz_counts['Sector'].apply(
                lambda x: short_names.get(x, x[:20] + '...' if len(str(x)) > 20 else x)
            )
            
            # ใช้ Horizontal Bar Chart แทน Pie Chart
            fig_biz = px.bar(
                biz_counts,
                x='Count',
                y='Short',
                orientation='h',
                text='Count',
                color='Count',
                color_continuous_scale='Teal'
            )
            fig_biz.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8', size=12),
                yaxis=dict(
                    autorange="reversed", 
                    gridcolor='rgba(255,255,255,0.05)',
                    title=""
                ),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)', 
                    showgrid=True,
                    title=""
                ),
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=400
            )
            fig_biz.update_traces(
                textposition='outside',
                textfont=dict(color='#94a3b8', size=11)
            )
            st.plotly_chart(fig_biz, use_container_width=True)
        else:
            st.info("No data to display")
    
    with col_chart2:
        st.markdown("### 🌍 Top 10 Countries")
        if not filtered_df.empty:
            country_counts = filtered_df[COL_COUNTRY].value_counts().head(10).reset_index()
            country_counts.columns = ['Country', 'Count']
            
            fig_country = px.bar(
                country_counts,
                x='Count',
                y='Country',
                orientation='h',
                text='Count',
                color='Count',
                color_continuous_scale='Teal'
            )
            fig_country.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                yaxis=dict(autorange="reversed", gridcolor='rgba(255,255,255,0.05)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', showgrid=True),
                coloraxis_showscale=False,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            fig_country.update_traces(
                textposition='outside',
                textfont=dict(color='#94a3b8')
            )
            st.plotly_chart(fig_country, use_container_width=True)
        else:
            st.info("No data to display")

# --- Tab 2: Companies ---
with tab2:
    if filtered_df.empty:
        st.warning("🔍 No companies found matching your criteria. Try adjusting the filters.")
    else:
        # Pagination
        total_items = len(filtered_df)
        total_pages = ceil(total_items / ITEMS_PER_PAGE)
        
        # Pagination controls
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <span class="pagination-info">Showing {min((st.session_state.current_page - 1) * ITEMS_PER_PAGE + 1, total_items)} - {min(st.session_state.current_page * ITEMS_PER_PAGE, total_items)} of {total_items} companies</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Page navigation
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
        
        with nav_col1:
            if st.button("⏮️ First", disabled=st.session_state.current_page == 1, use_container_width=True):
                st.session_state.current_page = 1
                st.rerun()
        
        with nav_col2:
            if st.button("◀️ Prev", disabled=st.session_state.current_page == 1, use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
        
        with nav_col3:
            st.markdown(f"<div style='text-align: center; padding: 0.5rem; color: #94a3b8;'>Page {st.session_state.current_page} of {total_pages}</div>", unsafe_allow_html=True)
        
        with nav_col4:
            if st.button("Next ▶️", disabled=st.session_state.current_page >= total_pages, use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
        
        with nav_col5:
            if st.button("Last ⏭️", disabled=st.session_state.current_page >= total_pages, use_container_width=True):
                st.session_state.current_page = total_pages
                st.rerun()
        
        st.markdown("---")
        
        # Display companies
        start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
        page_df = filtered_df.iloc[start_idx:end_idx]
        
        # Display companies - 1 per row, show all info
        for idx, (_, row) in enumerate(page_df.iterrows()):
            comp_name = str(row.get(COL_COMPANY, 'Unknown')).strip()
            website = row.get(COL_WEBSITE, '#')
            biz_type = row.get(COL_BUSINESS, '-')
            country = row.get(COL_COUNTRY, '-')
            intro = row.get(COL_INTRO, '-')
            contact = row.get(COL_CONTACT_TXT, '-')
            
            # Get logo
            img_logo = get_images(row.get('Img_Logo', ''))
            logo_path = img_logo[0] if img_logo and os.path.exists(img_logo[0]) else None
            
            with st.container(border=True):
                # Row 1: Logo + Company Info + Website Button
                col_logo, col_info, col_action = st.columns([1, 4, 1.5])
                
                with col_logo:
                    if logo_path:
                        st.image(logo_path, width=90)
                    else:
                        st.markdown(f"""
                            <div class="logo-placeholder">
                                {comp_name[0].upper() if comp_name else '?'}
                            </div>
                        """, unsafe_allow_html=True)
                
                with col_info:
                    st.markdown(f"### {comp_name}")
                    st.markdown(f"""
                        <span class="company-tag tag-country">{get_country_emoji(country)} {country}</span>
                        <span class="company-tag tag-business">{shorten_text(biz_type, 40)}</span>
                    """, unsafe_allow_html=True)
                    st.write(intro if intro != "-" else "No description available")
                
                with col_action:
                    if website and website != "-" and website != "#":
                        st.link_button("🌐 Website", website, use_container_width=True)
                    
                    st.markdown(f"**📞 Contact:**")
                    st.caption(shorten_text(contact, 80) if contact != "-" else "N/A")
                
                # Row 2: Gallery (if exists)
                img_news = get_images(row.get('Img_NewsProj', ''))
                img_high = get_images(row.get('Img_Highlight', ''))
                gallery = [img for img in (img_news + img_high) if os.path.exists(img)]
                
                if gallery:
                    st.markdown("**🖼️ Gallery**")
                    gallery_cols = st.columns(min(len(gallery), 5))
                    for g_idx, img in enumerate(gallery[:5]):
                        gallery_cols[g_idx].image(img, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748b;">
    <p style="margin-bottom: 0.5rem;">⚡ <strong>H2 Intelligence Hub</strong> — Hydrogen Market Database</p>
    <p style="font-size: 0.85rem;">Built with Streamlit • Data-driven insights for the hydrogen economy</p>
</div>
""", unsafe_allow_html=True)
