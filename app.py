import streamlit as st
import plotly.express as px
import pandas as pd
from spotify_auth import SpotifyAuthenticator
from data_processor import SpotifyDataProcessor

st.title("Recent Rhythms Dashboard")
st.write("Your latest Spotify listening insights")

# Sidebar for controls
with st.sidebar:
    st.header("Dashboard Settings")

    # Theme selector
    theme = st.selectbox(
        "Choose a theme:",
        ["Default", "Dark Mode", "Spotify Green", "Neon Purple"]
    )

    # Export section
    st.header("Export Data")

# Apply theme colors
if theme == "Spotify Green":
    color_palette = ["#1DB954", "#191414", "#1ed760"]
    primary_color = "#1DB954"
elif theme == "Dark Mode":
    color_palette = ["#2E2E2E", "#404040", "#606060"]
    primary_color = "#404040"
elif theme == "Neon Purple":
    color_palette = ["#8A2BE2", "#9932CC", "#BA55D3"]
    primary_color = "#8A2BE2"
else:
    color_palette = None
    primary_color = None

# Create authenticator
auth = SpotifyAuthenticator()

# Check authentication status
if auth.is_authenticated():
    st.success("Connected to Spotify!")

    # Get the data
    client = auth.get_authenticated_client()
    processor = SpotifyDataProcessor(client)

    # Add a slider to let user choose how many tracks to show
    num_tracks = st.slider("Number of recent tracks to display:", 5, 50, 10)

    recent_tracks = processor.get_recently_played(limit=num_tracks)

    if recent_tracks:
        st.subheader(f"Your {len(recent_tracks)} Most Recent Tracks")

        # Display as a nice table
        df = processor.get_recently_played_df(limit=num_tracks)
        st.dataframe(df[['track_name', 'artist', 'popularity', 'played_at']])

        # Export buttons
        col1, col2 = st.columns(2)

        with col1:
            # Export raw data as CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download Track Data (CSV)",
                data=csv_data,
                file_name=f"spotify_tracks_{num_tracks}.csv",
                mime="text/csv"
            )

        with col2:
            # Export summary report
            stats = processor.get_listening_stats(limit=num_tracks)
            report = f"""Recent Rhythms Report
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

LISTENING STATISTICS:
- Total Tracks: {stats['total_tracks']}
- Unique Artists: {stats['unique_artists']}
- Top Artist: {stats['top_artist']}
- Average Popularity: {stats['avg_popularity']}

TOP TRACKS:
{df[['track_name', 'artist', 'popularity']].head().to_string(index=False)}
"""
            st.download_button(
                label="Download Summary Report (TXT)",
                data=report,
                file_name=f"spotify_report_{pd.Timestamp.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

        # Time-based analysis
        st.subheader("Listening Patterns Over Time")

        # Listening by hour
        hourly_counts = df.groupby('hour').size().reset_index(name='count')
        fig_hourly = px.bar(
            hourly_counts,
            x='hour',
            y='count',
            title='Listening Activity by Hour',
            labels={'hour': 'Hour of Day', 'count': 'Number of Tracks'},
            color_discrete_sequence=color_palette
        )
        st.plotly_chart(fig_hourly)

        # Listening by day of the week
        day_counts = df.groupby('day_of_week').size().reset_index(name='count')
        fig_days = px.bar(
            day_counts,
            x='day_of_week',
            y='count',
            title='Listening Activity by Day of Week',
            labels={'day_of_week': 'Day of Week', 'count': 'Number of Tracks'},
            color_discrete_sequence=color_palette
        )
        st.plotly_chart(fig_days)

        # Charts showing artist popularity
        st.subheader("Artist Popularity Analysis")

        # Create a bar chart of artist popularity
        fig_popularity = px.bar(
            df,
            x='artist',
            y='popularity',
            title='Track Popularity by Artist',
            labels={'popularity': 'Spotify Popularity Score', 'artist': 'Artist'},
            color_discrete_sequence=color_palette
        )
        fig_popularity.update_xaxes(tickangle=45)  # Rotate artist names for readability
        st.plotly_chart(fig_popularity)

        # Create a histogram of popularity distribution
        fig_hist = px.histogram(
            df,
            x='popularity',
            title='Distribution of Track Popularity Scores',
            labels={'popularity': 'Popularity Score', 'count': 'Number of Tracks'},
            color_discrete_sequence=color_palette
        )
        st.plotly_chart(fig_hist)

        # Listening to statistics
        st.subheader("Listening Statistics")

        if stats:
            # Create columns for a nice layout
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Tracks", stats['total_tracks'])

            with col2:
                st.metric("Unique Artists", stats['unique_artists'])

            with col3:
                st.metric("Top Artist", stats['top_artist'])

            with col4:
                st.metric("Avg Popularity", f"{stats['avg_popularity']}")

    else:
        st.error("No recent tracks found.")

else:
    # Show login flow
    st.warning("Please authenticate with Spotify to view your data")

    if st.button("Login with Spotify"):
        auth_url = auth.get_auth_url()
        st.write("Click this link to login:")
        st.write(auth_url)

        # Input for response URL
        response_url = st.text_input("Paste the redirect URL here after logging in:")

        if response_url:
            token = auth.get_token_from_url(response_url)
            if token:
                st.success("Login successful! Please refresh the page.")
            else:
                st.error("Login failed. Please try again.")