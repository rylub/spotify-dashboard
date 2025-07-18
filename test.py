from spotify_auth import SpotifyAuthenticator

auth = SpotifyAuthenticator()

if auth.is_authenticated():
    print("This user is logged in already")
else:
    url = auth.get_auth_url()
    print("Please visit this URL to log in")
    print(f"{url}")

    response_url = input("After logging in, paste the full redirect URL here:\n")

    token = auth.get_token_from_url(response_url)

    if token:
        print('login successful')
    else:
        print('login failed')

# Test creating the client
print("Testing Spotify client creation...")
client = auth.get_authenticated_client()

if client:
    print("Authentication test complete! Ready to fetch data.")

    #Test data fetching
    print("\nTesting data fetching...")
    from data_processor import SpotifyDataProcessor

    processor = SpotifyDataProcessor(client)
    tracks = processor.get_recently_played(limit=5)

    if tracks:
        print(f"Successfully fetched {len(tracks)} recent tracks!")
        print("Sample track:", tracks[0])
    else:
        print("No tracks returned")

else:
    print("Failed to create Spotify client")