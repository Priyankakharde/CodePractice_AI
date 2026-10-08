from pathlib import Path
from turtle import right
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CodePractice AI",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
# ============================================================
# CSS
# ============================================================

st.markdown(r"""
<style>

.stApp{
    background:radial-gradient(
        circle at 72% 0%,
        rgba(20,61,105,.18),
        transparent 28%
    ),#050b14;
    color:#e8f1ff
}

[data-testid="stAppViewContainer"]{
    background:#050b14
}

[data-testid="stHeader"]{
    background:transparent
}

[data-testid="stToolbar"]{
    visibility:hidden;
    height:0
}

footer{
    visibility:hidden
}

.block-container{
    max-width:1480px;
    padding:18px 26px 28px
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"]{
    width:285px !important;
    min-width:285px !important;
    max-width:285px !important;
    background:#071426 !important;
    border-right:1px solid #132840 !important;
}

section[data-testid="stSidebar"] > div{
    width:285px !important;
    min-width:285px !important;
    max-width:285px !important;
    background:#071426 !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{
    width:285px !important;
    background:#071426 !important;
}

/* ============================================================
   FORCE SIDEBAR OPEN
   ============================================================ */

section[data-testid="stSidebar"]{
    transform:translateX(0) !important;
    visibility:visible !important;
    opacity:1 !important;
}

section[data-testid="stSidebar"][aria-expanded="false"]{
    transform:translateX(0) !important;
    visibility:visible !important;
    opacity:1 !important;
    width:285px !important;
    min-width:285px !important;
    max-width:285px !important;
}

section[data-testid="stSidebar"][aria-expanded="false"] > div{
    width:285px !important;
    visibility:visible !important;
    opacity:1 !important;
}

/* Sidebar inner area */
section[data-testid="stSidebar"] > div:first-child{
    padding:18px 16px !important;
}

/* Sidebar collapse / expand button */
[data-testid="stSidebarCollapseButton"]{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
}

[data-testid="stSidebarCollapseButton"] button{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    color:#f8fafc !important;
    background:#1e293b !important;
    border:1px solid #475569 !important;
    border-radius:8px !important;
    width:34px !important;
    height:34px !important;
}

[data-testid="stSidebarCollapseButton"] button:hover{
    background:#334155 !important;
}

[data-testid="stSidebarCollapseButton"] svg{
    color:#f8fafc !important;
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

.brand{
    display:flex;
    align-items:center;
    gap:10px;
    padding:4px
}

.brand-code{
    color:#43a7ff;
    font-size:28px;
    font-weight:900;
    line-height:1
}

.brand-name{
    color:#f4f8ff;
    font-size:20px;
    font-weight:800;
    line-height:1.05
}

.brand-name span{
    color:#3198ff
}

.brand-tagline{
    color:#6f87a6;
    font-size:9px;
    margin-left:38px
}

.sidebar-divider{
    height:1px;
    background:#172b43;
    margin:19px 0 18px
}

.sidebar-section-title{
    color:#7189a7;
    font-size:9px;
    font-weight:800;
    letter-spacing:.7px;
    text-transform:uppercase;
    margin:0 0 8px 4px
}


/* ============================================================
   SIDEBAR NOTE
   ============================================================ */

.sidebar-note{
    border:1px solid #1a304a;
    border-radius:10px;
    background:#081626;
    padding:15px 14px 13px;
    margin:22px 2px 0
}

.sidebar-note-text{
    color:#9bb0ca;
    font-size:10px;
    line-height:1.5
}

.sidebar-note-line{
    width:27px;
    height:3px;
    background:#318dff;
    border-radius:10px;
    margin-top:9px
}


/* ============================================================
   SIDEBAR BUTTONS
   ============================================================ */

section[data-testid="stSidebar"] .stButton > button{
    width:100%;
    min-height:37px;
    border:1px solid transparent;
    border-radius:8px;
    background:transparent;
    color:#aabbd0;
    text-align:left;
    font-size:12px;
    font-weight:500;
    padding:7px 10px;
    margin:2px 0
}

section[data-testid="stSidebar"] .stButton > button:hover{
    background:#0d2138;
    border-color:#17385c;
    color:#fff
}


/* ============================================================
   TOP BAR
   ============================================================ */

.topbar{
    display:flex;
    align-items:center;
    gap:18px;
    margin-bottom:20px
}

.search-box{
    flex:1;
    max-width:620px;
    height:39px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    border:1px solid #203a58;
    border-radius:8px;
    background:#0b1a2c;
    padding:0 13px
}

.search-left{
    color:#7590af;
    font-size:10px
}

.search-shortcut{
    color:#6681a3;
    font-size:9px
}

.top-spacer{
    flex:1
}

.notification{
    position:relative;
    color:#a8bad1;
    font-size:19px;
    width:28px;
    text-align:center
}

.notification-dot{
    position:absolute;
    width:6px;
    height:6px;
    border-radius:50%;
    background:#ff5964;
    top:1px;
    right:3px
}

.profile{
    display:flex;
    align-items:center;
    gap:8px
}

.avatar{
    width:29px;
    height:29px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#277ef1;
    color:#fff;
    font-size:12px;
    font-weight:800
}

.profile-name{
    color:#f0f5fc;
    font-size:10px;
    font-weight:700
}

.profile-sub{
    color:#7890ad;
    font-size:8px;
    margin-top:2px
}

.profile-arrow{
    color:#718aa8;
    font-size:12px;
    margin-left:2px
}


/* ============================================================
   HERO
   ============================================================ */

.hero-row{
    display:flex;
    justify-content:space-between;
    align-items:flex-end;
    margin-bottom:16px
}

.hero-title{
    color:#f4f7fc;
    font-size:23px;
    font-weight:800;
    line-height:1.2;
    margin-bottom:5px
}

.hero-subtitle{
    color:#7189a7;
    font-size:11px
}

.hero-quote{
    color:#879bb5;
    font-size:11px;
    font-weight:500;
    padding-bottom:3px
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin:17px 0 9px
}

.section-title{
    color:#eaf1fb;
    font-size:14px;
    font-weight:800
}

.section-link{
    color:#3196ff;
    font-size:10px;
    font-weight:600
}


/* ============================================================
   SUBJECT CARDS
   ============================================================ */

.subject-card{
    position:relative;
    min-height:136px;
    border-radius:9px;
    border:1px solid #183553;
    overflow:hidden;
    padding:18px
}

.python-card{
    background:
        radial-gradient(
            circle at 12% 112%,
            rgba(21,88,177,.44),
            transparent 37%
        ),
        linear-gradient(135deg,#102744,#0c1c31)
}

.postgres-card{
    background:
        radial-gradient(
            circle at 15% 115%,
            rgba(0,136,102,.42),
            transparent 38%
        ),
        linear-gradient(135deg,#10312f,#0a2527);
    border-color:#154b47
}

.wave{
    position:absolute;
    left:-6%;
    right:-6%;
    bottom:-38px;
    height:76px;
    border-radius:50%;
    background:rgba(22,90,181,.24);
    transform:rotate(-2deg)
}

.postgres-card .wave{
    background:rgba(0,151,117,.23);
    transform:rotate(2deg)
}

.subject-content{
    position:relative;
    z-index:2
}

.subject-icon{
    font-size:32px;
    line-height:1;
    margin-bottom:5px
}

.subject-title{
    color:#f3f7ff;
    font-size:16px;
    font-weight:800
}

.subject-text{
    color:#a2b4ca;
    font-size:9px;
    line-height:1.45;
    max-width:270px;
    margin-top:5px
}

.subject-arrow{
    position:absolute;
    right:13px;
    top:13px;
    width:25px;
    height:25px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(42,128,229,.18);
    color:#4ea7ff;
    font-size:12px
}

.postgres-card .subject-arrow{
    background:rgba(0,184,144,.14);
    color:#32d6b1
}


/* ============================================================
   SUBJECT BUTTONS
   ============================================================ */

.subject-button .stButton > button{
    margin-top:7px;
    min-height:30px;
    border-radius:6px;
    font-size:10px;
    font-weight:700;
    padding:4px 12px;
    color:#fff
}

.subject-blue .stButton > button{
    background:#2b83f6;
    border:1px solid #4092ff
}

.subject-green .stButton > button{
    background:#06ad78;
    border:1px solid #12c88e
}


/* ============================================================
   CONTINUE LEARNING
   ============================================================ */

.continue-panel{
    border:1px solid #142b46;
    border-radius:9px;
    background:#091626;
    padding:8px
}

.learning-row{
    display:flex;
    align-items:center;
    gap:10px;
    min-height:46px;
    border:1px solid #172d47;
    border-radius:8px;
    background:#0b192a;
    padding:7px 9px;
    margin:4px 0
}

.learning-icon{
    width:32px;
    height:32px;
    border-radius:50%;
    background:#122a46;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:18px;
    flex-shrink:0
}

.learning-name{
    color:#edf3fb;
    font-size:10px;
    font-weight:700
}

.learning-sub{
    color:#7289a5;
    font-size:8px;
    margin-top:2px
}

.learning-info{
    width:128px;
    flex-shrink:0
}

.progress-track{
    flex:1;
    height:5px;
    background:#1c3046;
    border-radius:10px;
    overflow:hidden
}

.progress-blue{
    height:100%;
    background:#328fff;
    border-radius:10px
}

.progress-green{
    height:100%;
    background:#22c997;
    border-radius:10px
}

.progress-value{
    color:#8ea3bd;
    font-size:9px;
    width:30px;
    text-align:right
}

.continue-blue .stButton > button,
.continue-green .stButton > button{
    min-height:27px;
    border-radius:6px;
    font-size:9px;
    font-weight:700;
    padding:3px 11px;
    color:#fff
}

.continue-blue .stButton > button{
    background:#2d84f6;
    border:1px solid #3d91ff
}

.continue-green .stButton > button{
    background:#06ae78;
    border:1px solid #10c78d
}


/* ============================================================
   RIGHT SIDE CARDS
   ============================================================ */

.side-card{
    border:1px solid #18314d;
    border-radius:9px;
    background:#091827;
    padding:12px;
    margin-bottom:11px
}

.side-title{
    color:#edf4fc;
    font-size:11px;
    font-weight:800;
    margin-bottom:7px
}

.donut-wrap{
    display:flex;
    justify-content:center;
    margin:2px 0 7px
}

.donut{
    width:82px;
    height:82px;
    border-radius:50%;
    background:
        conic-gradient(
            #2f8cff 0deg 126deg,
            #20cda0 126deg 180deg,
            #1c3148 180deg 360deg
        );
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative
}

.donut:after{
    content:"";
    width:63px;
    height:63px;
    border-radius:50%;
    background:#091827;
    position:absolute
}

.donut-value{
    position:relative;
    z-index:2;
    color:#fff;
    font-size:16px;
    font-weight:800
}

.donut-caption{
    color:#7087a2;
    text-align:center;
    font-size:7px;
    margin-bottom:8px
}

.mini-progress{
    padding:7px 8px;
    border-radius:7px;
    background:#0c1b2c;
    margin-top:5px
}

.mini-top{
    display:flex;
    justify-content:space-between;
    color:#b0bfd1;
    font-size:8px;
    margin-bottom:5px
}

.mini-track{
    height:4px;
    background:#1a2d42;
    border-radius:8px;
    overflow:hidden
}


/* ============================================================
   STREAK
   ============================================================ */

.streak-card{
    border:1px solid #5a3421;
    border-radius:9px;
    background:
        radial-gradient(
            circle at 0% 50%,
            rgba(255,126,37,.18),
            transparent 52%
        ),
        #211711;
    padding:13px;
    min-height:74px;
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:11px
}

.streak-icon{
    font-size:27px
}

.streak-number{
    color:#fff;
    font-size:24px;
    font-weight:800;
    line-height:1
}

.streak-label{
    color:#a9978c;
    font-size:8px;
    margin-top:4px
}

.streak-arrow{
    margin-left:auto;
    color:#e7a04f;
    font-size:17px
}


/* ============================================================
   QUICK LINKS
   ============================================================ */

.quick-item{
    display:flex;
    align-items:center;
    gap:8px;
    padding:8px 0;
    border-top:1px solid #172c43;
    color:#a8b9ce;
    font-size:9px
}

.quick-item:first-of-type{
    border-top:0
}

.quick-icon{
    width:18px;
    text-align:center;
    font-size:14px
}

.quick-arrow{
    margin-left:auto;
    color:#8298b1
}


/* ============================================================
   RECOMMENDED
   ============================================================ */

.recommend-card{
    border:1px solid #172e48;
    border-radius:8px;
    background:#0a192a;
    padding:12px;
    min-height:96px
}

.recommend-top{
    display:flex;
    gap:9px
}

.recommend-icon{
    width:35px;
    height:35px;
    border-radius:50%;
    background:#122a45;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    flex-shrink:0
}

.recommend-title{
    color:#edf3fa;
    font-size:10px;
    font-weight:800
}

.recommend-text{
    color:#7e94ad;
    font-size:8px;
    line-height:1.4;
    margin-top:4px
}

.recommend-bottom{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-top:9px
}

.badge-blue,
.badge-green{
    border-radius:20px;
    padding:3px 8px;
    font-size:7px
}

.badge-blue{
    background:#102f55;
    color:#5eaaff
}

.badge-green{
    background:#0d4034;
    color:#4de1b5
}

.start-link{
    color:#3d9aff;
    font-size:9px;
    font-weight:700
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media(max-width:1050px){

    .block-container{
        padding-left:16px;
        padding-right:16px
    }

    .hero-title{
        font-size:20px
    }

    .learning-info{
        width:105px
    }

}

@media(max-width:800px){

    .topbar{
        flex-wrap:wrap
    }

    .search-box{
        max-width:none;
        width:100%;
        order:1
    }

    .top-spacer{
        display:none
    }

    .profile{
        margin-left:auto
    }

    .hero-row{
        align-items:flex-start;
        gap:10px
    }

    .hero-quote{
        display:none
    }

    .learning-info{
        width:105px
    }

}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DASHBOARD PAGE
# ============================================================

def render_dashboard():
    # ========================================================
    # WELCOME
    # ========================================================
    st.markdown("""
        <div class="hero-row">
            <div><div class="hero-title">Welcome back, Priyanka! 👋</div><div class="hero-subtitle">Continue learning and practice to build your skills.</div></div>
            <div class="hero-quote">“Code. Practice. Improve.”</div>
        </div>
        """, unsafe_allow_html=True)
    
    # SUBJECT CARDS
    py_col, sql_col = st.columns(2, gap="small")
    with py_col:
        st.markdown("""
        <div class="subject-card python-card"><div class="wave"></div><div class="subject-content">
            <div class="subject-icon">🐍</div><div class="subject-title">Python</div>
            <div class="subject-text">Learn Python from basics to advanced<br>with examples and hands-on practice.</div>
            <div class="subject-arrow">→</div>
        </div></div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="subject-button subject-blue">', unsafe_allow_html=True)
        if st.button("Start Learning →", key="start_python", use_container_width=True):
            st.switch_page("python_learning.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with sql_col:
        st.markdown("""
        <div class="subject-card postgres-card"><div class="wave"></div><div class="subject-content">
            <div class="subject-icon">🐘</div><div class="subject-title">PostgreSQL</div>
            <div class="subject-text">Learn SQL with PostgreSQL and<br>practice real queries.</div>
            <div class="subject-arrow">→</div>
        </div></div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="subject-button subject-green">', unsafe_allow_html=True)
        if st.button("Start Learning →", key="start_postgres", use_container_width=True):
            st.switch_page("postgres_learning.py")
        st.markdown('</div>', unsafe_allow_html=True)    


    # CONTINUE LEARNING
    st.markdown(
        '<div class="section-title-row"><div class="section-title">Continue Learning</div><div class="section-link">View All →</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="continue-panel">',
        unsafe_allow_html=True,
    ) 

    # ------------------------------------------------------------
    # GET AUTOMATIC COURSE PROGRESS
    # ------------------------------------------------------------

    import os
    import psycopg2
    from dotenv import load_dotenv

    load_dotenv()

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=os.getenv("DB_NAME", "codepractice"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            l.subject,
            COUNT(l.id) AS total_lessons,
            COUNT(
                CASE
                    WHEN p.completed = TRUE THEN 1
                END
            ) AS completed_lessons
        FROM lessons l
        LEFT JOIN progress p
            ON p.lesson_id = l.id
            AND p.user_id = (
                SELECT id
                FROM users
                WHERE email = %s
                LIMIT 1
            )
        GROUP BY l.subject;
        """,
        ("priyanka@codepractice.local",),
    )

    course_progress = cursor.fetchall()

    cursor.close()
    connection.close()

    python_total = 0
    python_completed = 0

    postgres_total = 0
    postgres_completed = 0

    for subject, total, completed in course_progress:

        if subject == "Python":
            python_total = total
            python_completed = completed

        elif subject == "PostgreSQL":
            postgres_total = total
            postgres_completed = completed


    python_percentage = (
        round((python_completed / python_total) * 100)
        if python_total > 0
        else 0
    )

    postgres_percentage = (
        round((postgres_completed / postgres_total) * 100)
        if postgres_total > 0
        else 0
    )

    # ------------------------------------------------------------
    # PYTHON
    # ------------------------------------------------------------

    c1, c2, c3 = st.columns([1.55, 2.3, .62], gap="small")

    with c1:
        st.markdown(
            '<div class="learning-row"><div class="learning-icon">🐍</div><div><div class="learning-name">Python Output</div><div class="learning-sub">Print Text</div></div></div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-top:20px"><div class="progress-track"><div class="progress-blue" style="width:{python_percentage}%"></div></div><div class="progress-value">{python_percentage}%</div></div>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            '<div class="continue-blue">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Continue",
            key="continue_python",
            use_container_width=True,
        ):
            st.switch_page("python_learning.py")

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------
    # POSTGRESQL
    # ------------------------------------------------------------

    c1, c2, c3 = st.columns([1.55, 2.3, .62], gap="small")

    with c1:
        st.markdown(
            '<div class="learning-row"><div class="learning-icon">🐘</div><div><div class="learning-name">SELECT Statement</div><div class="learning-sub">Basic Queries</div></div></div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-top:20px"><div class="progress-track"><div class="progress-green" style="width:{postgres_percentage}%"></div></div><div class="progress-value">{postgres_percentage}%</div></div>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            '<div class="continue-green">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Continue",
            key="continue_postgres",
            use_container_width=True,
        ):
            st.switch_page("postgres_learning.py")

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )

    # ============================================================
    # RECOMMENDED
    # ============================================================

    st.markdown(
        '<div class="section-title-row">'
        '<div class="section-title">Recommended for You</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    r1, r2 = st.columns(2, gap="small")

    # ============================================================
    # PYTHON RECOMMENDATION
    # ============================================================

    with r1:

        st.markdown(
            '<div class="recommend-card">'
            '<div class="recommend-top">'
            '<div class="recommend-icon">🐍</div>'
            '<div>'
            '<div class="recommend-title">Python</div>'
            '<div class="recommend-text">'
            'Improve Your Python Skills'
            '</div>'
            '</div>'
            '</div>'
            '<div class="recommend-bottom">'
            '<span class="badge-blue">Beginner</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Practice →",
            key="recommended_python",
            use_container_width=True,
        ):
            st.switch_page("recommended_python.py")        

    # ============================================================
    # POSTGRESQL RECOMMENDATION
    # ============================================================

    with r2:

        st.markdown(
            '<div class="recommend-card">'
            '<div class="recommend-top">'
            '<div class="recommend-icon">🐘</div>'
            '<div>'
            '<div class="recommend-title">PostgreSQL</div>'
            '<div class="recommend-text">'
            'Improve Your PostgreSQL Skills'
            '</div>'
            '</div>'
            '</div>'
            '<div class="recommend-bottom">'
            '<span class="badge-green">Beginner</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Practice →",
            key="recommended_postgres",
            use_container_width=True,
        ):
            st.switch_page("recommended_postgres.py")        


    # ============================================================
    # FOOTER
    # ============================================================

    st.markdown(
        '<div style="text-align:center;'
        'color:#4d637e;'
        'font-size:8px;'
        'margin-top:18px;'
        'padding-top:10px;'
        'border-top:1px solid #12263d">'
        'CodePractice AI • Learn. Practice. Grow.'
        '</div>',
        unsafe_allow_html=True,
    )
    
# ============================================================
# NATIVE STREAMLIT NAVIGATION
# ============================================================

dashboard_page = st.Page(
    render_dashboard,
    title="Dashboard",
    icon="🏠",
    default=True,
)

python_page = st.Page(
    "python_learning.py",
    title="Python",
    icon="🐍",
)

postgres_page = st.Page(
    "postgres_learning.py",
    title="PostgreSQL",
    icon="🐘",
)

progress_page = st.Page(
    "my_progress.py",
    title="My Progress",
    icon="📊",
)

bookmarks_page = st.Page(
    "bookmarks.py",
    title="Bookmarks",
    icon="🔖",
)

settings_page = st.Page(
    "settings.py",
    title="Settings",
    icon="⚙️",
)

# ============================================================
# RECOMMENDED PRACTICE PAGES
# ============================================================

recommended_python_page = st.Page(
    "recommended_python.py",
    title="Python Practice",
)

recommended_postgres_page = st.Page(
    "recommended_postgres.py",
    title="PostgreSQL Practice",
)

# Keep the Dashboard page available to other pages
st.session_state["dashboard_page"] = dashboard_page

# ============================================================
# NAVIGATION
# ============================================================

nav = st.navigation(
    [
        dashboard_page,
        python_page,
        postgres_page,
        progress_page,
        bookmarks_page,
        settings_page,
        recommended_python_page,
        recommended_postgres_page,
    ],
    position="hidden",
)
# ============================================================
# SIDEBAR
# ============================================================

if nav == dashboard_page:

    with st.sidebar:

        st.markdown("""
        <div class="brand">
            <div class="brand-code">&lt;/&gt;</div>
            <div>
                <div class="brand-name">
                    Code<span>Practice</span>
                </div>
            </div>
        </div>

        <div class="brand-tagline">
            Learn. Practice. Grow.
        </div>

        <div class="sidebar-divider"></div>

        <div class="sidebar-section-title">
            Navigation
        </div>
        """, unsafe_allow_html=True)

        # Dashboard
        if st.button(
            "🏠   Dashboard",
            key="side_dashboard",
            use_container_width=True,
        ):
            st.rerun()

        # Python
        if st.button(
            "🐍   Python",
            key="side_python",
            use_container_width=True,
        ):
            st.switch_page(python_page)

        # PostgreSQL
        if st.button(
            "🐘   PostgreSQL",
            key="side_postgres",
            use_container_width=True,
        ):
            st.switch_page(postgres_page)

        st.markdown(
            '<div class="sidebar-divider"></div>',
            unsafe_allow_html=True,
        )

        # My Progress
        if st.button(
            "📊   My Progress",
            key="side_progress",
            use_container_width=True,
        ):
            st.switch_page(progress_page)

        # Bookmarks
        if st.button(
            "🔖   Bookmarks",
            key="side_bookmarks",
            use_container_width=True,
        ):
            st.switch_page(bookmarks_page)

        # Settings
        if st.button(
            "⚙️   Settings",
            key="side_settings",
            use_container_width=True,
        ):
            st.switch_page(settings_page)

        # Bottom quote
        st.markdown("""
        <div class="sidebar-note">
            <div class="sidebar-note-text">
                “Small steps<br>
                every day lead<br>
                to big results.”
            </div>
            <div class="sidebar-note-line"></div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# RUN
# ============================================================

nav.run()