import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Streaming Wars Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# 2. Theme State Management
# ---------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# Color tokens
bg_color = "#09090b" if IS_DARK else "#ffffff"
bg_subtle = "#0c0c0f" if IS_DARK else "#f8fafc"
card_bg = "#111116" if IS_DARK else "#ffffff"
card_hover = "#181820" if IS_DARK else "#f1f5f9"
border_color = "#27272a" if IS_DARK else "#e2e8f0"
border_subtle = "#1e1e24" if IS_DARK else "#edf2f7"
text_color = "#fafafa" if IS_DARK else "#09090b"
text_muted = "#a1a1aa" if IS_DARK else "#64748b"
text_dim = "#71717a" if IS_DARK else "#94a3b8"
accent_color = "#3b82f6"
grid_color = "rgba(255,255,255,0.06)" if IS_DARK else "rgba(0,0,0,0.06)"

# Platform Brand Colors
PLATFORM_COLORS = {
    'Netflix': '#ef4444',
    'Amazon Prime Video': '#3b82f6',
    'Disney+': '#a855f7'
}

# ---------------------------------------------------------
# 3. Custom CSS Design System
# ---------------------------------------------------------
custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Hide Streamlit Default Chrome */
    header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton,
    div[data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}

    /* Base Typography & Background */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    .block-container {{
        padding: 1.25rem 2rem 3rem !important;
        max-width: 1440px !important;
    }}

    /* Metric Cards */
    .metric-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .metric-card:hover {{
        border-color: #3b82f6;
        background: {card_hover};
    }}
    .metric-label {{
        font-size: 0.75rem;
        color: {text_muted};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .metric-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {text_color};
        letter-spacing: -0.03em;
        margin: 0.3rem 0;
    }}
    .metric-subtitle {{
        font-size: 0.75rem;
        color: {text_dim};
        display: flex;
        align-items: center;
        gap: 5px;
    }}

    /* Chart Containers */
    .chart-wrap {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 1.25rem 1.25rem 0.6rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.2rem;
    }}
    .chart-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.8rem;
    }}
    .chart-title {{
        font-size: 0.95rem;
        font-weight: 600;
        color: {text_color};
        letter-spacing: -0.01em;
    }}
    .chart-subtitle {{
        font-size: 0.78rem;
        color: {text_muted};
        margin-top: 0.15rem;
    }}

    /* Insight Banner Box */
    .insight-box {{
        background: {card_bg};
        border-left: 4px solid #3b82f6;
        border-top: 1px solid {border_color};
        border-right: 1px solid {border_color};
        border-bottom: 1px solid {border_color};
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }}
    .insight-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .insight-text {{
        font-size: 0.83rem;
        color: {text_muted};
        line-height: 1.45;
    }}

    /* Header Bar */
    .header-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid {border_color};
    }}
    .brand-title {{
        font-size: 1.45rem;
        font-weight: 800;
        color: {text_color};
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .brand-badge {{
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }}

    /* Tabs Styling */
    button[data-baseweb="tab"] {{
        background: transparent !important;
        color: {text_muted} !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.55rem 1.1rem !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {text_color} !important;
        background: {card_bg} !important;
        border-color: {border_color} !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{
        display: none !important;
    }}
    [data-baseweb="tab-list"] {{
        gap: 6px !important;
        background: {bg_subtle} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 4px !important;
        margin-bottom: 1.5rem !important;
    }}

    /* Badges */
    .badge {{
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
    }}
    .badge-netflix {{ color: #ef4444; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); }}
    .badge-amazon {{ color: #3b82f6; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); }}
    .badge-disney {{ color: #a855f7; background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.3); }}
    .badge-size-large {{ color: #10b981; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); }}
    .badge-size-medium {{ color: #f59e0b; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-size-small {{ color: #64748b; background: rgba(100, 116, 139, 0.15); border: 1px solid rgba(100, 116, 139, 0.3); }}

    /* Selectboxes and Inputs */
    div[data-baseweb="select"] > div {{
        background-color: {card_bg} !important;
        border-color: {border_color} !important;
        border-radius: 8px !important;
        color: {text_color} !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Load Data & Feature Engineering
# ---------------------------------------------------------
@st.cache_data
def load_data():
    csv_path = "country_summary.csv"
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "country_summary.csv")
    
    df = pd.read_csv(csv_path)
    
    # Library Size Tiers matching notebook
    bins = [0, 100, 500, 10000]
    labels = ['Small (<100)', 'Medium (100-500)', 'Large (>500)']
    df['library_size'] = pd.cut(df['total_titles'], bins=bins, labels=labels)
    df['title_rank'] = df['total_titles'].rank(ascending=False, method='min').astype(int)
    df['imdb_rank'] = df['avg_imdb'].rank(ascending=False, method='min').astype(int)
    
    # Market catalog percentage of total global catalog
    total_global_titles = df['total_titles'].sum()
    df['catalog_share_pct'] = (df['total_titles'] / total_global_titles) * 100
    
    return df

df_raw = load_data()

# ---------------------------------------------------------
# 5. Header Component
# ---------------------------------------------------------
head_col1, head_col2 = st.columns([7, 2])
with head_col1:
    st.markdown(f"""
    <div class="header-bar">
        <div>
            <div class="brand-title">
                🎬 Streaming Wars Analytics
                <span class="brand-badge">24 Global Markets</span>
            </div>
            <div style="color: {text_muted}; font-size: 0.85rem; margin-top: 0.2rem;">
                Cross-national content library volume, platform dominance, and rating intelligence dashboard
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    btn_label = "☀️ Light Mode" if IS_DARK else "🌙 Dark Mode"
    if st.button(btn_label, use_container_width=True, on_click=toggle_theme):
        st.rerun()

# ---------------------------------------------------------
# 6. Global Filters Toolbar
# ---------------------------------------------------------
with st.container():
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([3, 2, 2, 2, 1.5])
    
    with f_col1:
        selected_countries = st.multiselect(
            "Filter Countries",
            options=sorted(df_raw['country'].unique()),
            default=[],
            placeholder="All 24 Countries..."
        )
    with f_col2:
        selected_size = st.selectbox(
            "Library Size Tier",
            options=["All Tiers", "Large (>500)", "Medium (100-500)", "Small (<100)"]
        )
    with f_col3:
        selected_platform = st.selectbox(
            "Leading Platform",
            options=["All Platforms"] + sorted(df_raw['top_platform'].unique().tolist())
        )
    with f_col4:
        min_rating = st.slider(
            "Min IMDb Rating",
            min_value=float(round(df_raw['avg_imdb'].min(), 2)),
            max_value=float(round(df_raw['avg_imdb'].max(), 2)),
            value=float(round(df_raw['avg_imdb'].min(), 2)),
            step=0.05
        )
    with f_col5:
        search_query = st.text_input("🔍 Search", placeholder="Country...")

# Apply Filters
df = df_raw.copy()
if selected_countries:
    df = df[df['country'].isin(selected_countries)]
if selected_size != "All Tiers":
    df = df[df['library_size'] == selected_size]
if selected_platform != "All Platforms":
    df = df[df['top_platform'] == selected_platform]
if min_rating > df_raw['avg_imdb'].min():
    df = df[df['avg_imdb'] >= min_rating]
if search_query:
    df = df[df['country'].str.contains(search_query.strip(), case=False)]

# ---------------------------------------------------------
# 7. Executive Metrics Banner
# ---------------------------------------------------------
total_countries = len(df)
total_titles = df['total_titles'].sum() if total_countries > 0 else 0
global_titles_sum = df_raw['total_titles'].sum()
catalog_coverage = (total_titles / global_titles_sum * 100) if global_titles_sum > 0 else 0
avg_imdb = df['avg_imdb'].mean() if total_countries > 0 else 0.0

top_vol_country = df.sort_values('total_titles', ascending=False).iloc[0] if total_countries > 0 else None
top_rating_country = df.sort_values('avg_imdb', ascending=False).iloc[0] if total_countries > 0 else None

dominant_platform_mode = df['top_platform'].mode()[0] if total_countries > 0 else "N/A"
dominant_platform_pct = (len(df[df['top_platform'] == dominant_platform_mode]) / total_countries * 100) if total_countries > 0 else 0

m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Scope</div>
        <div class="metric-value">{total_countries} <span style="font-size: 0.9rem; color: {text_muted}; font-weight: normal;">/ 24</span></div>
        <div class="metric-subtitle">Markets selected</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Titles</div>
        <div class="metric-value">{total_titles:,}</div>
        <div class="metric-subtitle">{catalog_coverage:.1f}% global catalog</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Mean IMDb</div>
        <div class="metric-value">{avg_imdb:.2f} <span style="font-size: 1rem;">⭐</span></div>
        <div class="metric-subtitle">Across active scope</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Leader Share</div>
        <div class="metric-value" style="font-size: 1.4rem;">{dominant_platform_mode}</div>
        <div class="metric-subtitle">{dominant_platform_pct:.1f}% market lead</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    top_vol_name = top_vol_country['country'] if top_vol_country is not None else "N/A"
    top_vol_cnt = f"{top_vol_country['total_titles']:,}" if top_vol_country is not None else "0"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Largest Market</div>
        <div class="metric-value" style="font-size: 1.35rem;">{top_vol_name}</div>
        <div class="metric-subtitle">{top_vol_cnt} titles</div>
    </div>
    """, unsafe_allow_html=True)

with m6:
    top_rtg_name = top_rating_country['country'] if top_rating_country is not None else "N/A"
    top_rtg_val = f"{top_rating_country['avg_imdb']:.2f} ⭐" if top_rating_country is not None else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Highest Rated</div>
        <div class="metric-value" style="font-size: 1.35rem;">{top_rtg_name}</div>
        <div class="metric-subtitle">{top_rtg_val} mean</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. Common Plotly Theme Config
# ---------------------------------------------------------
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color=text_muted, size=11),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(
        gridcolor=grid_color,
        zerolinecolor=grid_color,
        tickfont=dict(size=10, color=text_muted),
    ),
    yaxis=dict(
        gridcolor=grid_color,
        zerolinecolor=grid_color,
        tickfont=dict(size=10, color=text_muted),
    ),
)

# ---------------------------------------------------------
# 9. Multi-Tab Navigation Architecture
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Content Volume & Map",
    "👑 Platform & Genre Dominance",
    "🔬 Library Tiers & Statistics",
    "⚔️ Country Head-to-Head",
    "💡 Executive Insights",
    "📋 Interactive Data Explorer"
])

# =========================================================
# TAB 1: Content Volume & Geographic Distribution
# =========================================================
with tab1:
    # Row 1: Global Map
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-header">
            <div>
                <div class="chart-title">Global Streaming Catalog Map</div>
                <div class="chart-subtitle">Geographic visualization of available content library volume and top streaming services</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if len(df) > 0:
        fig_map = px.choropleth(
            df,
            locations="country",
            locationmode="country names",
            color="total_titles",
            hover_name="country",
            hover_data={
                "country": False,
                "total_titles": ":,",
                "avg_imdb": ":.2f",
                "top_platform": True,
                "top_genre": True,
            },
            color_continuous_scale="Viridis",
        )
        fig_map.update_geos(
            showcoastlines=True,
            coastlinecolor=border_color,
            showland=True,
            landcolor="#1c1917" if IS_DARK else "#f1f5f9",
            showocean=True,
            oceancolor="#09090b" if IS_DARK else "#e2e8f0",
            bgcolor="rgba(0,0,0,0)",
            projection_type="natural earth",
        )
        fig_map.update_layout(
            **PLOT_LAYOUT,
            height=430,
            coloraxis_colorbar=dict(
                title="Catalog Titles",
                thickness=14,
                len=0.7,
                tickfont=dict(color=text_muted, size=10)
            )
        )
        st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
    else:
        st.warning("No data matching current filters.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Row 2: Bar Chart & Scatter
    col_t1_1, col_t1_2 = st.columns([5, 5])
    
    with col_t1_1:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Content Volume by Country</div>
                    <div class="chart-subtitle">Total titles cataloged in each national streaming market</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df) > 0:
            df_sorted = df.sort_values('total_titles', ascending=True)
            fig_bar = px.bar(
                df_sorted,
                x='total_titles',
                y='country',
                orientation='h',
                color='total_titles',
                color_continuous_scale=['#1d4ed8', '#3b82f6', '#60a5fa', '#93c5fd'],
                hover_data={'avg_imdb': ':.2f', 'top_platform': True, 'total_titles': ':,'}
            )
            fig_bar.update_layout(**PLOT_LAYOUT, height=440, coloraxis_showscale=False)
            fig_bar.update_traces(hovertemplate="<b>%{y}</b><br>Titles: %{x:,}<br>IMDb: %{customdata[0]}")
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning("No data matching current filters.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_t1_2:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Library Size vs. Average IMDb Rating</div>
                    <div class="chart-subtitle">Evaluating whether larger catalog sizes dilute overall viewer quality</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df) > 0:
            fig_scatter = px.scatter(
                df,
                x='total_titles',
                y='avg_imdb',
                size='total_titles',
                color='top_platform',
                hover_name='country',
                color_discrete_map=PLATFORM_COLORS,
                size_max=36
            )
            fig_scatter.update_layout(**PLOT_LAYOUT, height=440)
            fig_scatter.update_xaxes(title="Total Titles (Log Scale)", type="log")
            fig_scatter.update_yaxes(title="Average IMDb Rating", range=[6.65, 7.00])
            st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning("No data matching current filters.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2: Platform & Genre Dominance
# =========================================================
with tab2:
    col_t2_1, col_t2_2 = st.columns([4, 6])
    
    with col_t2_1:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Market Dominance Share</div>
                    <div class="chart-subtitle">Proportion of surveyed countries where platform has largest catalog</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df) > 0:
            platform_counts = df['top_platform'].value_counts().reset_index()
            platform_counts.columns = ['platform', 'count']
            
            fig_pie = px.pie(
                platform_counts,
                names='platform',
                values='count',
                hole=0.55,
                color='platform',
                color_discrete_map=PLATFORM_COLORS
            )
            fig_pie.update_layout(**PLOT_LAYOUT, height=380, showlegend=True)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning("No data matching current filters.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_t2_2:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">IMDb Rating Distribution by Dominant Platform</div>
                    <div class="chart-subtitle">Country-level average IMDb ratings grouped by leading service</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df) > 0:
            fig_box = px.box(
                df,
                x='top_platform',
                y='avg_imdb',
                color='top_platform',
                points="all",
                hover_name='country',
                color_discrete_map=PLATFORM_COLORS
            )
            fig_box.update_layout(**PLOT_LAYOUT, height=380, showlegend=False)
            fig_box.update_xaxes(title="Leading Platform")
            fig_box.update_yaxes(title="Average IMDb Rating", range=[6.65, 7.00])
            st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning("No data matching current filters.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2: Platform Stats Breakdown Cards & Genre Insights
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    g_col1, g_col2, g_col3 = st.columns(3)
    
    # Platform group calculations from df_raw for context
    platform_summary = df_raw.groupby('top_platform').agg(
        countries_led=('country', 'count'),
        total_market_titles=('total_titles', 'sum'),
        mean_rating=('avg_imdb', 'mean')
    ).reset_index()

    for i, row in platform_summary.iterrows():
        p_name = row['top_platform']
        badge_cls = 'badge-netflix' if p_name == 'Netflix' else ('badge-amazon' if p_name == 'Amazon Prime Video' else 'badge-disney')
        col_target = g_col1 if i == 0 else (g_col2 if i == 1 else g_col3)
        with col_target:
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="badge {badge_cls}">{p_name}</span>
                    <span style="font-size: 0.78rem; color: {text_muted};">{row['countries_led']} Markets</span>
                </div>
                <div style="margin-top: 0.8rem;">
                    <div style="font-size: 1.35rem; font-weight: 700; color: {text_color};">{row['mean_rating']:.2f} ⭐</div>
                    <div style="font-size: 0.76rem; color: {text_dim};">Mean IMDb across dominant markets</div>
                </div>
                <div style="margin-top: 0.6rem; font-size: 0.78rem; color: {text_muted};">
                    Total Volume in Led Markets: <b>{row['total_market_titles']:,}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# TAB 3: Library Tiers & Statistical Analysis
# =========================================================
with tab3:
    col_t3_1, col_t3_2 = st.columns([5, 5])
    
    with col_t3_1:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Rating Spread by Library Size Tier</div>
                    <div class="chart-subtitle">Comparing Small (&lt;100), Medium (100-500), and Large (&gt;500) markets</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df) > 0:
            fig_tier_box = px.box(
                df,
                x='library_size',
                y='avg_imdb',
                color='library_size',
                color_discrete_sequence=['#64748b', '#f59e0b', '#10b981'],
                points="all",
                hover_name='country'
            )
            fig_tier_box.update_layout(**PLOT_LAYOUT, height=380, showlegend=False)
            fig_tier_box.update_xaxes(title="Library Size Category")
            fig_tier_box.update_yaxes(title="Average IMDb Rating", range=[6.65, 7.00])
            st.plotly_chart(fig_tier_box, use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning("No data matching current filters.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_t3_2:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Correlation Matrix (Volume vs. Rating)</div>
                    <div class="chart-subtitle">Pearson statistical correlation between total titles and average IMDb rating</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df) > 1:
            corr = df[['total_titles', 'avg_imdb']].corr()
            fig_heatmap = px.imshow(
                corr,
                text_auto=".3f",
                color_continuous_scale="Blues",
                x=['Total Titles', 'Avg IMDb Rating'],
                y=['Total Titles', 'Avg IMDb Rating']
            )
            fig_heatmap.update_layout(**PLOT_LAYOUT, height=380, coloraxis_showscale=False)
            st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Select at least 2 countries to calculate correlation matrix.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2: Sunburst / Treemap Distribution
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-header">
            <div>
                <div class="chart-title">Hierarchical Market Treemap</div>
                <div class="chart-subtitle">Library Tier &rarr; Leading Platform &rarr; Country Market Size</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if len(df) > 0:
        fig_treemap = px.treemap(
            df,
            path=['library_size', 'top_platform', 'country'],
            values='total_titles',
            color='avg_imdb',
            color_continuous_scale='Viridis',
            hover_data={'avg_imdb': ':.2f', 'total_titles': ':,'}
        )
        fig_treemap.update_layout(**PLOT_LAYOUT, height=420)
        st.plotly_chart(fig_treemap, use_container_width=True, config={"displayModeBar": False})
    else:
        st.warning("No data matching current filters.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 4: Country Head-to-Head Comparison
# =========================================================
with tab4:
    st.markdown("""
    <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.2rem;">Country Head-to-Head Benchmark</div>
    <div style="font-size: 0.8rem; color: #a1a1aa; margin-bottom: 1.2rem;">Select any two national markets to perform a side-by-side metric comparison.</div>
    """, unsafe_allow_html=True)
    
    h_col1, h_col2 = st.columns(2)
    all_countries_list = sorted(df_raw['country'].unique())
    
    with h_col1:
        country_a = st.selectbox("Select Country A", options=all_countries_list, index=all_countries_list.index("United States"))
    with h_col2:
        default_b_idx = all_countries_list.index("India") if "India" in all_countries_list else 1
        country_b = st.selectbox("Select Country B", options=all_countries_list, index=default_b_idx)
    
    row_a = df_raw[df_raw['country'] == country_a].iloc[0]
    row_b = df_raw[df_raw['country'] == country_b].iloc[0]
    
    comp_c1, comp_c2 = st.columns(2)
    
    with comp_c1:
        badge_a = 'badge-netflix' if row_a['top_platform'] == 'Netflix' else ('badge-amazon' if row_a['top_platform'] == 'Amazon Prime Video' else 'badge-disney')
        st.markdown(f"""
        <div class="metric-card" style="border-color: #3b82f6;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.25rem; font-weight: 700; color: {text_color};">{row_a['country']}</span>
                <span class="badge {badge_a}">{row_a['top_platform']}</span>
            </div>
            <div style="margin-top: 1rem; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div class="metric-label">Total Catalog Titles</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #60a5fa;">{row_a['total_titles']:,}</div>
                    <div style="font-size: 0.72rem; color: {text_dim};">Global Rank #{row_a['title_rank']}</div>
                </div>
                <div>
                    <div class="metric-label">Average IMDb Rating</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #34d399;">{row_a['avg_imdb']:.2f} ⭐</div>
                    <div style="font-size: 0.72rem; color: {text_dim};">Global Rank #{row_a['imdb_rank']}</div>
                </div>
            </div>
            <div style="margin-top: 0.9rem; padding-top: 0.8rem; border-top: 1px solid {border_subtle}; font-size: 0.8rem; color: {text_muted};">
                Library Size Tier: <b>{row_a['library_size']}</b> | Top Genre: <b>{row_a['top_genre']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with comp_c2:
        badge_b = 'badge-netflix' if row_b['top_platform'] == 'Netflix' else ('badge-amazon' if row_b['top_platform'] == 'Amazon Prime Video' else 'badge-disney')
        st.markdown(f"""
        <div class="metric-card" style="border-color: #a855f7;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.25rem; font-weight: 700; color: {text_color};">{row_b['country']}</span>
                <span class="badge {badge_b}">{row_b['top_platform']}</span>
            </div>
            <div style="margin-top: 1rem; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div class="metric-label">Total Catalog Titles</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #60a5fa;">{row_b['total_titles']:,}</div>
                    <div style="font-size: 0.72rem; color: {text_dim};">Global Rank #{row_b['title_rank']}</div>
                </div>
                <div>
                    <div class="metric-label">Average IMDb Rating</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #34d399;">{row_b['avg_imdb']:.2f} ⭐</div>
                    <div style="font-size: 0.72rem; color: {text_dim};">Global Rank #{row_b['imdb_rank']}</div>
                </div>
            </div>
            <div style="margin-top: 0.9rem; padding-top: 0.8rem; border-top: 1px solid {border_subtle}; font-size: 0.8rem; color: {text_muted};">
                Library Size Tier: <b>{row_b['library_size']}</b> | Top Genre: <b>{row_b['top_genre']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # Comparison Bar Chart
    comp_df = pd.DataFrame({
        'Metric': ['Total Titles (Normalized)', 'Avg IMDb Rating (x100)'],
        country_a: [row_a['total_titles'] / df_raw['total_titles'].max() * 100, row_a['avg_imdb'] * 14],
        country_b: [row_b['total_titles'] / df_raw['total_titles'].max() * 100, row_b['avg_imdb'] * 14]
    }).melt(id_vars='Metric', var_name='Country', value_name='Score')
    
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-header">
            <div>
                <div class="chart-title">Direct Comparison Profile</div>
                <div class="chart-subtitle">Relative volume index and rating benchmark</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    fig_comp = px.bar(
        comp_df,
        x='Metric',
        y='Score',
        color='Country',
        barmode='group',
        color_discrete_sequence=['#3b82f6', '#a855f7']
    )
    fig_comp.update_layout(**PLOT_LAYOUT, height=340)
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 5: Executive Insights & Key Findings
# =========================================================
with tab5:
    st.markdown("""
    <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.2rem;">Executive Strategic Insights & Findings</div>
    <div style="font-size: 0.8rem; color: #a1a1aa; margin-bottom: 1.2rem;">Key takeaways synthesized from global streaming catalog analysis across 24 countries.</div>
    """, unsafe_allow_html=True)
    
    # Finding 1
    top5_countries = df_raw.sort_values('total_titles', ascending=False).head(5)
    top5_sum = top5_countries['total_titles'].sum()
    top5_pct = (top5_sum / global_titles_sum) * 100
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">🌐 1. Extreme Market Concentration in Content Volume</div>
        <div class="insight-text">
            The top 5 streaming markets (<b>United States, India, United Kingdom, South Korea, and Japan</b>) account for 
            <b>{top5_sum:,} titles ({top5_pct:.1f}%)</b> of all content cataloged globally. The United States alone leads with 5,736 titles, 
            over 4x larger than the second largest market (India with 1,429 titles).
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Finding 2
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">👑 2. Platform Oligopoly & Regional Strongholds</div>
        <div class="insight-text">
            <b>Netflix</b> commands undisputed global dominance, leading the catalog volume in <b>20 out of 24 countries (83.3%)</b>. 
            However, <b>Amazon Prime Video</b> maintains leadership in key strategic markets including Brazil (301 titles), Denmark (71 titles), 
            and Israel (74 titles), while <b>Disney+</b> holds the dominant position in Indonesia (69 titles).
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Finding 3
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">⚖️ 3. Quality vs. Quantity Independence</div>
        <div class="insight-text">
            Average IMDb ratings remain exceptionally consistent globally, ranging narrowly between <b>6.70 (Argentina)</b> and <b>6.95 (Sweden)</b>. 
            Statistical correlation between catalog size and average rating is virtually flat (Pearson r &approx; -0.04), indicating that 
            massive library expansion does not strictly correlate with diluted perceived quality.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Finding 4
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎭 4. Genre Homogeneity with Notable Regional Outliers</div>
        <div class="insight-text">
            <b>Drama</b> is the primary genre in 23 out of 24 analyzed markets (95.8%), highlighting its universal appeal and high production volume. 
            <b>China</b> represents the sole exception in the dataset, where <b>Comedy</b> emerges as the leading genre category.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TAB 6: Interactive Data Explorer
# =========================================================
with tab6:
    d_col1, d_col2 = st.columns([8, 2])
    with d_col1:
        st.markdown("""
        <div style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.2rem;">Country Catalog Summary Table</div>
        <div style="font-size: 0.78rem; color: #a1a1aa; margin-bottom: 0.8rem;">Browse, sort, and export the filtered streaming analytics records.</div>
        """, unsafe_allow_html=True)
    
    with d_col2:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name="streaming_wars_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    if len(df) > 0:
        display_df = df.sort_values('total_titles', ascending=False)[
            ['country', 'total_titles', 'library_size', 'avg_imdb', 'title_rank', 'imdb_rank', 'top_platform', 'top_genre']
        ]
        st.dataframe(
            display_df,
            column_config={
                "country": st.column_config.TextColumn("Country", help="Country Name"),
                "total_titles": st.column_config.NumberColumn("Total Titles", format="%d"),
                "library_size": st.column_config.TextColumn("Library Tier"),
                "avg_imdb": st.column_config.NumberColumn("Avg IMDb Rating", format="%.2f ⭐"),
                "title_rank": st.column_config.NumberColumn("Volume Rank", format="#%d"),
                "imdb_rank": st.column_config.NumberColumn("Rating Rank", format="#%d"),
                "top_platform": st.column_config.TextColumn("Leading Platform"),
                "top_genre": st.column_config.TextColumn("Dominant Genre"),
            },
            use_container_width=True,
            hide_index=True,
        )
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### 📈 Summary Descriptive Statistics")
        st.dataframe(
            df[['total_titles', 'avg_imdb']].describe().T,
            use_container_width=True
        )
    else:
        st.warning("No records match your selected filter criteria.")
