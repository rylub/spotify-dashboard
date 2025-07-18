import pandas as pd


class SpotifyDataProcessor:
    def __init__(self, spotify_client):
        self.spotify = spotify_client

    def get_recently_played(self, limit=50):
        """
        Get recently played tracks from Spotify API

        Args:
            limit (int): Number of tracks to fetch (max 50 per API call)

        Returns:
            list: List of dictionaries containing track data, or empty list if error
        """
        # Validate limit parameter - Spotify API restricts recently played to max 50
        if limit > 50:
            print(f"Warning: Limit {limit} exceeds Spotify's max of 50. Setting to 50.")
            limit = 50
        elif limit < 1:
            print(f"Warning: Limit {limit} is too low. Setting to 1.")
            limit = 1

        # Initialize empty to store processed track data
        tracks_data = []

        # log what we are attempting to do
        print(f"Fetching {limit} recently played tracks from Spotify API...")

        try:
            # Make the api call to get recently played tracks
            results = self.spotify.current_user_recently_played(limit=limit)

            # check if api returns valid results
            if not results:
                print("Error: No data returned from spotify api")
                return tracks_data

            # check if user has any recent tracks
            if not results.get("items") or len(results['items']) == 0:
                print("No recent tracks found. User needs to play some music on Spotify first!")
                return tracks_data

            # log how many tracks we got
            print(f"Successfully retrieved {len(results['items'])} tracks")

            # Loop through each track in the results
            for item in results['items']:
                # Extract track and timing info from each item
                track = item['track']
                played_at = item['played_at']

                # Check if track has required data (handle missing data gracefully)
                if not track.get('name') or not track.get('artists'):
                    print(f"Warning: Skipping track with missing data")
                    continue

                # create a dictionary with the track data we want
                track_info = {
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'popularity': track.get('popularity', 0),
                    'played_at': played_at
                }

                tracks_data.append(track_info)

            # log successful processing
            print(f'Successfully processed {len(tracks_data)} tracks')
            return tracks_data

        except Exception as e:
            print(f"Error fetching recently played tracks: {e}")
            return tracks_data  # return an empty list on error

    def get_recently_played_df(self, limit=50):
        """Get recently played tracks as a pandas DF"""
        tracks_data = self.get_recently_played(limit)

        if not tracks_data:
            return pd.DataFrame()

        df = pd.DataFrame(tracks_data)

        # Convert played_at to datetime and add time-based columns
        df['played_at'] = pd.to_datetime(df['played_at'])
        df['hour'] = df['played_at'].dt.hour
        df['day_of_week'] = df['played_at'].dt.day_name()
        df['date'] = df['played_at'].dt.date

        return df

    def get_listening_stats(self, limit=50):
        """Get basic statistics about recently played tracks"""
        df = self.get_recently_played_df(limit)

        if df.empty:
            return {}

        stats = {
            'total_tracks': len(df),
            'unique_artists': df['artist'].nunique(),
            'top_artist': df['artist'].mode().iloc[0] if not df['artist'].mode().empty else 'Unknown',
            'avg_popularity': round(df['popularity'].mean(), 1)
        }

        return stats