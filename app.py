import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# ---------- Page config ----------
st.set_page_config(
    page_title="infosteam - Most Played Games",
    page_icon="🎮",
    layout="wide",
)

# ---------- Constants ----------
DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.csv")
TOP_N = 10

os.makedirs(DATA_DIR, exist_ok=True)


# ---------- Steam API functions ----------

@st.cache_data(ttl=300)  # refresh every 5 min
def get_top_games():
    """Fetch the most played games from Steam (no API key needed)."""
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()["response"]["ranks"][:TOP_N]


@st.cache_data(ttl=86400)  # cache 24h (names don't change)
def get_game_name(appid):
    """Get game name from Steam Store API."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data[str(appid)]["success"]:
            return data[str(appid)]["data"]["name"]
    except Exception:
        pass
    return f"App {appid}"


@st.cache_data(ttl=300)  # refresh every 5 min
def get_current_players(appid):
    """Get current player count for a game."""
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
    try:
        resp = requests.get(url, params={"appid": appid}, timeout=10)
        return resp.json()["response"]["player_count"]
    except Exception:
        return 0


def get_game_image(appid):
    """Header image URL for a Steam game (no API call needed)."""
    return f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"


# ---------- History / snapshot functions ----------

def save_daily_snapshot(df):
    """Save today's player data so we can show 7-day trends."""
    today = datetime.now().strftime("%Y-%m-%d")
    snapshot = df[["name", "current_players", "peak_players"]].copy()
    snapshot["date"] = today

    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
        if today in history["date"].values:
            return  # already saved today
        history = pd.concat([history, snapshot], ignore_index=True)
    else:
        history = snapshot

    # keep only last 30 days
    history["date"] = pd.to_datetime(history["date"])
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
    history = history[history["date"] >= cutoff]
    history["date"] = history["date"].dt.strftime("%Y-%m-%d")
    history.to_csv(HISTORY_FILE, index=False)


def load_history():
    """Load saved snapshots for trend charts."""
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame()


# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")

    source = st.radio("Data source:", ["🌐 Steam API (live)", "📁 Upload CSV"])

    uploaded_file = None
    if source == "📁 Upload CSV":
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"],
            help="Must have columns: name, current_players, peak_players",
        )
        st.caption("Format: `name, current_players, peak_players`")

    st.divider()

    if st.button("🔄 Refresh data"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.caption("Data refreshes automatically every 5 min.")
    st.caption("A daily snapshot is saved for trends.")


# ---------- Page header ----------
st.title("🎮 infosteam")
st.caption("Most Played Games on Steam — Real-time data")


# ---------- Load data ----------
df = None

if source == "📁 Upload CSV" and uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {"name", "current_players", "peak_players"}
        if not required_cols.issubset(df.columns):
            st.error(f"❌ CSV must have columns: {required_cols}")
            df = None
        else:
            st.success(f"✅ Loaded {len(df)} games from CSV")
    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")

elif source == "🌐 Steam API (live)":
    with st.spinner("Loading live data from Steam..."):
        try:
            top_games = get_top_games()
            rows = []
            for game in top_games:
                appid = game["appid"]
                rows.append({
                    "rank": game["rank"],
                    "name": get_game_name(appid),
                    "current_players": get_current_players(appid),
                    "peak_players": game["peak_in_game"],
                    "last_week_rank": game.get("last_week_rank", game["rank"]),
                    "image": get_game_image(appid),
                })
            df = pd.DataFrame(rows)
        except Exception as e:
            st.error(f"❌ Could not connect to Steam API: {e}")


# ---------- Display data ----------
if df is not None and not df.empty:
    # save snapshot for trends (only from API, not from uploaded CSV)
    if source == "🌐 Steam API (live)":
        save_daily_snapshot(df)

    # summary metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("🟢 Players Online", f"{df['current_players'].sum():,}")
    c2.metric("🎮 Games Tracked", len(df))
    c3.metric("🏆 Most Played", df.iloc[0]["name"])

    st.divider()

    # tabs
    tab1, tab2, tab3 = st.tabs(["📊 Rankings", "📈 7-Day Trend", "📋 Data Table"])

    # ---- Tab 1: game cards ----
    with tab1:
        for row_start in range(0, len(df), 5):
            cols = st.columns(5)
            for i, col in enumerate(cols):
                idx = row_start + i
                if idx >= len(df):
                    break
                game = df.iloc[idx]
                with col:
                    # game image
                    if "image" in game and pd.notna(game["image"]):
                        st.image(game["image"], use_container_width=True)

                    # rank + name
                    rank = int(game.get("rank", idx + 1))
                    st.markdown(f"**#{rank} {game['name']}**")

                    # current players
                    st.metric("Players now", f"{game['current_players']:,}")
                    st.caption(f"Peak: {game['peak_players']:,}")

    # ---- Tab 2: trend chart ----
    with tab2:
        st.subheader("📈 Player Trends — Last 7 Days")
        history = load_history()

        if not history.empty and len(history["date"].unique()) > 1:
            all_games = sorted(history["name"].unique().tolist())
            selected = st.multiselect(
                "Select games to compare:",
                all_games,
                default=all_games[:5],
            )
            if selected:
                filtered = history[history["name"].isin(selected)]
                chart_data = filtered.pivot_table(
                    index="date",
                    columns="name",
                    values="current_players",
                    aggfunc="first",
                )
                st.line_chart(chart_data)
            else:
                st.info("Select at least one game above.")
        else:
            st.info(
                "📊 Trend data will appear after 2+ days of snapshots. "
                "The app saves one snapshot per day automatically."
            )

        # bar chart of current data
        st.subheader("📊 Current Players Comparison")
        bar_data = df.set_index("name")[["current_players"]].sort_values(
            "current_players", ascending=True
        )
        st.bar_chart(bar_data)

    # ---- Tab 3: data table ----
    with tab3:
        st.subheader("📋 Complete Data")
        show_cols = [
            c for c in ["rank", "name", "current_players", "peak_players", "last_week_rank"]
            if c in df.columns
        ]
        st.dataframe(df[show_cols], use_container_width=True, hide_index=True)

        # download button
        csv_data = df[show_cols].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"infosteam_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

else:
    if source == "📁 Upload CSV":
        st.info("👆 Upload a CSV file from the sidebar to see your data.")
    else:
        st.warning("No data available. Check your internet connection.")


# ---------- Footer ----------
st.divider()
st.caption("© 2026 infosteam — Data from Steam Web API")
