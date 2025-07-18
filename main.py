from spotify_auth import SpotifyAuthenticator
from data_processor import SpotifyDataProcessor


def main():
    # Step 1: Create the auth object
    auth = SpotifyAuthenticator()

    # Step 2: Check if already authenticated
    if not auth.is_authenticated():
        print("Need to authenticate with Spotify...")

        # Get the Spotify login URL
        auth_url = auth.get_auth_url()
        print("Go to this URL and log in:")
        print(auth_url)

        # After logging in, paste the redirected URL
        response_url = input("\nPaste the full redirected URL after logging in:\n")

        # Try to get the token
        token = auth.get_token_from_url(response_url)

        if not token:
            print("FAILED: Could not get token.")
            return

        print("SUCCESS: Authentication complete!")
    else:
        print("Already authenticated!")

    # Step 3: Get authenticated client and fetch data
    client = auth.get_authenticated_client()

    if client:
        processor = SpotifyDataProcessor(client)
        recent_tracks = processor.get_recently_played(limit=10)

        if recent_tracks:
            print(f"\nYour {len(recent_tracks)} most recent tracks:")
            for track in recent_tracks:
                print(f"{track['track_name']} - {track['artist']} (popularity: {track['popularity']})")
        else:
            print("No tracks to show.")
    else:
        print("Authentication failed.")


if __name__ == "__main__":
    main()