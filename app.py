import streamlit as st

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="infosteam — Most Played Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Game data ────────────────────────────────────────────
GAMES = [
    {
        "rank": 1,
        "title": "GTA V Legacy",
        "players": "156,631",
        "peak": "292,000",
        "image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=480&q=80",
        "change": "+12.4%",
        "up": True,
    },
    {
        "rank": 2,
        "title": "Counter-Strike 2",
        "players": "142,218",
        "peak": "1,802,853",
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=480&q=80",
        "change": "+8.1%",
        "up": True,
    },
    {
        "rank": 3,
        "title": "Dota 2",
        "players": "98,432",
        "peak": "1,295,114",
        "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=480&q=80",
        "change": "-3.2%",
        "up": False,
    },
    {
        "rank": 4,
        "title": "PUBG: Battlegrounds",
        "players": "87,204",
        "peak": "3,257,248",
        "image": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=480&q=80",
        "change": "+5.7%",
        "up": True,
    },
    {
        "rank": 5,
        "title": "Apex Legends",
        "players": "74,519",
        "peak": "614,082",
        "image": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=480&q=80",
        "change": "+2.9%",
        "up": True,
    },
    {
        "rank": 6,
        "title": "Elden Ring",
        "players": "68,917",
        "peak": "953,426",
        "image": "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=480&q=80",
        "change": "-1.5%",
        "up": False,
    },
    {
        "rank": 7,
        "title": "Rust",
        "players": "56,631",
        "peak": "245,396",
        "image": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=480&q=80",
        "change": "+4.2%",
        "up": True,
    },
    {
        "rank": 8,
        "title": "Cyberpunk 2077",
        "players": "45,203",
        "peak": "1,054,388",
        "image": "https://images.unsplash.com/photo-1614294149010-950b698f72c0?w=480&q=80",
        "change": "+6.8%",
        "up": True,
    },
    {
        "rank": 9,
        "title": "Baldur's Gate 3",
        "players": "38,891",
        "peak": "875,343",
        "image": "https://images.unsplash.com/photo-1560419015-7c427e8ae5ba?w=480&q=80",
        "change": "-2.1%",
        "up": False,
    },
    {
        "rank": 10,
        "title": "Team Fortress 2",
        "players": "31,704",
        "peak": "253,997",
        "image": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=480&q=80",
        "change": "+1.3%",
        "up": True,
    },
]

# ── CSS styles ───────────────────────────────────────────
st.markdown(
    """
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* Global overrides */
.stApp {
    background: #0f172a !important;
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0;
}

/* Hide Streamlit default elements */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── Navbar ── */
.navbar {
    position: fixed;
    top: 0; left: 0; width: 100%;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2.5rem;
    background: rgba(15,23,42,0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.navbar-logo {
    font-size: 1.5rem; font-weight: 800; letter-spacing: -0.5px;
    background: linear-gradient(135deg,#60a5fa,#a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.navbar-links { display: flex; gap: 2rem; list-style: none; margin: 0; padding: 0; }
.navbar-links li a {
    font-size: 0.9rem; font-weight: 500; color: #94a3b8;
    text-decoration: none; transition: color 0.3s;
}
.navbar-links li a:hover { color: #f1f5f9; }
.btn-install {
    padding: 0.5rem 1.25rem; border-radius: 8px; border: none;
    background: linear-gradient(135deg,#3b82f6,#8b5cf6);
    color: #fff; font-family: 'Inter', sans-serif; font-size: 0.85rem;
    font-weight: 600; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s;
}
.btn-install:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99,102,241,0.4);
}

/* ── Hero ── */
.hero {
    position: relative; width: 100%; min-height: 480px;
    display: flex; align-items: flex-end; overflow: hidden;
    margin-top: 56px;
}
.hero-bg {
    position: absolute; inset: 0;
    background: url('https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1600&q=80') center/cover no-repeat;
    filter: brightness(0.55) saturate(1.2);
}
.hero-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to bottom,
        rgba(15,23,42,0.3) 0%,
        rgba(15,23,42,0.7) 60%,
        #0f172a 100%);
}
.hero-content {
    position: relative; z-index: 2;
    padding: 3rem 2.5rem 2.5rem; max-width: 700px;
}
.hero-badge {
    display: inline-block; padding: 0.3rem 0.85rem; border-radius: 20px;
    background: rgba(251,191,36,0.15); color: #fbbf24;
    font-size: 0.75rem; font-weight: 600; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 1rem;
}
.hero-title {
    font-size: 3.5rem; font-weight: 900; line-height: 1.1;
    letter-spacing: -1.5px; margin-bottom: 0.75rem;
    background: linear-gradient(135deg,#f1f5f9,#94a3b8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle { font-size: 1.25rem; font-weight: 500; color: #94a3b8; }

/* ── Stats Bar ── */
.stats-bar {
    display: flex; gap: 2rem; padding: 1.5rem 2.5rem;
    margin: 0 2.5rem 2rem;
    background: rgba(30,41,59,0.6);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
}
.stat-item { display: flex; flex-direction: column; gap: 0.25rem; }
.stat-value { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; }
.stat-value.green { color: #34d399; }
.stat-value.blue  { color: #60a5fa; }
.stat-value.amber { color: #fbbf24; }
.stat-label { font-size: 0.8rem; color: #64748b; font-weight: 500; }

/* ── Section ── */
.section-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.5rem; padding: 0 2.5rem;
}
.section-title { font-size: 1.5rem; font-weight: 700; color: #f1f5f9; }

/* ── Game Cards ── */
.games-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1.5rem; padding: 0 2.5rem;
}
.game-card {
    background: #1e293b; border-radius: 16px; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.04);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    animation: fadeInUp 0.5s ease forwards; opacity: 0;
}
.game-card:nth-child(1)  { animation-delay: 0.05s; }
.game-card:nth-child(2)  { animation-delay: 0.10s; }
.game-card:nth-child(3)  { animation-delay: 0.15s; }
.game-card:nth-child(4)  { animation-delay: 0.20s; }
.game-card:nth-child(5)  { animation-delay: 0.25s; }
.game-card:nth-child(6)  { animation-delay: 0.30s; }
.game-card:nth-child(7)  { animation-delay: 0.35s; }
.game-card:nth-child(8)  { animation-delay: 0.40s; }
.game-card:nth-child(9)  { animation-delay: 0.45s; }
.game-card:nth-child(10) { animation-delay: 0.50s; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.game-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 8px 32px rgba(99,102,241,0.2),
                0 0 0 1px rgba(99,102,241,0.15);
}
.game-card-img {
    position: relative; width: 100%; height: 160px; overflow: hidden;
}
.game-card-img img {
    width: 100%; height: 100%; object-fit: cover;
    transition: transform 0.4s ease;
}
.game-card:hover .game-card-img img { transform: scale(1.08); }
.rank-badge {
    position: absolute; top: 10px; left: 10px;
    background: rgba(15,23,42,0.8); backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    color: #fbbf24; font-size: 0.7rem; font-weight: 700;
    padding: 0.2rem 0.55rem; border-radius: 6px;
    border: 1px solid rgba(251,191,36,0.2);
}
.game-card-body { padding: 1rem 1.15rem; }
.game-card-title {
    font-size: 1rem; font-weight: 700; color: #f1f5f9;
    margin-bottom: 0.65rem; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.game-card-stats {
    display: flex; justify-content: space-between; align-items: center;
}
.game-card-players { display: flex; align-items: center; gap: 0.4rem; }
.pulse-dot {
    width: 8px; height: 8px; border-radius: 50%; background: #34d399;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; box-shadow: 0 0 0 0 rgba(52,211,153,0.5); }
    50%     { opacity: 0.7; box-shadow: 0 0 0 6px rgba(52,211,153,0); }
}
.player-count { font-size: 0.85rem; font-weight: 600; color: #34d399; }
.peak-count { font-size: 0.75rem; color: #64748b; font-weight: 500; }

/* ── Trending ── */
.trending-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem; padding: 0 2.5rem;
}
.trending-item {
    display: flex; align-items: center; gap: 1rem; padding: 1rem;
    background: rgba(30,41,59,0.5); backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.04); border-radius: 12px;
    transition: background 0.3s, transform 0.3s; cursor: pointer;
}
.trending-item:hover { background: rgba(30,41,59,0.8); transform: translateX(4px); }
.trending-rank { font-size: 1.25rem; font-weight: 800; color: #475569; min-width: 28px; }
.trending-img { width: 48px; height: 48px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }
.trending-info { flex: 1; }
.trending-name { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; }
.trending-players { font-size: 0.78rem; color: #64748b; }
.trending-change { font-size: 0.8rem; font-weight: 600; padding: 0.2rem 0.5rem; border-radius: 6px; }
.trending-change.up { color: #34d399; background: rgba(52,211,153,0.1); }
.trending-change.down { color: #f87171; background: rgba(248,113,113,0.1); }

/* ── Footer ── */
.footer {
    text-align: center; padding: 2.5rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    color: #475569; font-size: 0.8rem;
}
.footer span {
    background: linear-gradient(135deg,#60a5fa,#a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-weight: 700;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .navbar { padding: 0.85rem 1.25rem; }
    .navbar-links { display: none; }
    .hero-title { font-size: 2.25rem; }
    .hero-content { padding: 2rem 1.25rem; }
    .hero { min-height: 360px; }
    .stats-bar { margin: 0 1.25rem 1.5rem; padding: 1rem 1.25rem; gap: 1.25rem; flex-wrap: wrap; }
    .stat-value { font-size: 1.15rem; }
    .section-header { padding: 0 1.25rem; }
    .games-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; padding: 0 1.25rem; }
    .game-card-img { height: 120px; }
    .trending-grid { grid-template-columns: 1fr; padding: 0 1.25rem; }
}
@media (max-width: 480px) {
    .hero-title { font-size: 1.75rem; }
    .hero-subtitle { font-size: 1rem; }
    .games-grid { grid-template-columns: 1fr 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Navbar ───────────────────────────────────────────────
st.markdown(
    """
<nav class="navbar">
    <div class="navbar-logo">infosteam</div>
    <ul class="navbar-links">
        <li><a href="#">Store</a></li>
        <li><a href="#">Community</a></li>
        <li><a href="#">Library</a></li>
        <li><a href="#">News</a></li>
    </ul>
    <button class="btn-install">Install Client</button>
</nav>
""",
    unsafe_allow_html=True,
)

# ── Hero ─────────────────────────────────────────────────
st.markdown(
    """
<section class="hero">
    <div class="hero-bg"></div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <span class="hero-badge">Live Now</span>
        <h1 class="hero-title">infosteam</h1>
        <p class="hero-subtitle">Most Played Games</p>
    </div>
</section>
""",
    unsafe_allow_html=True,
)

# ── Stats Bar ────────────────────────────────────────────
st.markdown(
    """
<div class="stats-bar">
    <div class="stat-item">
        <span class="stat-value green">33,648,102</span>
        <span class="stat-label">Players Online</span>
    </div>
    <div class="stat-item">
        <span class="stat-value blue">10,241,891</span>
        <span class="stat-label">In-Game Now</span>
    </div>
    <div class="stat-item">
        <span class="stat-value amber">142,387</span>
        <span class="stat-label">Games Available</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ── Most Played Games ────────────────────────────────────
st.markdown(
    """
<div class="section-header">
    <h2 class="section-title">Most Played Games &rarr;</h2>
</div>
""",
    unsafe_allow_html=True,
)

# Build game cards HTML
cards_html = '<div class="games-grid">'
for game in GAMES:
    cards_html += f"""
    <div class="game-card">
        <div class="game-card-img">
            <img src="{game['image']}" alt="{game['title']}" />
            <span class="rank-badge">#{game['rank']}</span>
        </div>
        <div class="game-card-body">
            <div class="game-card-title">{game['title']}</div>
            <div class="game-card-stats">
                <div class="game-card-players">
                    <span class="pulse-dot"></span>
                    <span class="player-count">{game['players']}</span>
                </div>
                <span class="peak-count">Peak: {game['peak']}</span>
            </div>
        </div>
    </div>"""
cards_html += "</div>"

st.markdown(cards_html, unsafe_allow_html=True)

# ── Trending Now ─────────────────────────────────────────
st.markdown(
    """
<div class="section-header" style="margin-top: 2rem;">
    <h2 class="section-title">Trending Now &rarr;</h2>
</div>
""",
    unsafe_allow_html=True,
)

trending_html = '<div class="trending-grid">'
for game in GAMES[:6]:
    change_class = "up" if game["up"] else "down"
    trending_html += f"""
    <div class="trending-item">
        <span class="trending-rank">{game['rank']}</span>
        <img class="trending-img" src="{game['image']}" alt="{game['title']}" />
        <div class="trending-info">
            <div class="trending-name">{game['title']}</div>
            <div class="trending-players">{game['players']} playing</div>
        </div>
        <span class="trending-change {change_class}">{game['change']}</span>
    </div>"""
trending_html += "</div>"

st.markdown(trending_html, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────
st.markdown(
    """
<footer class="footer">
    <p>&copy; 2026 <span>infosteam</span>. All rights reserved. Not affiliated with Valve Corporation.</p>
</footer>
""",
    unsafe_allow_html=True,
)
