# Recent Rhythms Dashboard

A Spotify listening analytics dashboard that provides insights into your recent music listening habits. Built with Python, Streamlit, and the Spotify Web API.

## Features

- **Authentication**: Secure OAuth integration with Spotify
- **Recent Tracks**: View your last 50 recently played tracks
- **Interactive Charts**: 
  - Artist popularity analysis
  - Listening patterns by hour and day of week
  - Popularity score distribution
- **Customizable Themes**: Choose from Default, Dark Mode, Spotify Green, or Neon Purple
- **Data Export**: Download your listening data as CSV or summary report
- **Real-time Statistics**: Track count, unique artists, top artist, and average popularity

## Screenshots

![Dashboard Overview](screenshot.png)
*Main dashboard showing recent tracks and analytics*

## Installation

### Prerequisites

- Python 3.8 or higher
- Spotify account
- Spotify Developer App (for API credentials)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ryanlubell/spotify-dashboard.git
   cd spotify-dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Spotify API credentials**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Note your Client ID and Client Secret
   - Set redirect URI to: `http://localhost:8888/callback`

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

## Usage

1. **Start the dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Authenticate with Spotify**
   - Click "Login with Spotify" 
   - Complete the OAuth flow
   - Return to the dashboard

3. **Explore your data**
   - Adjust the number of tracks with the slider
   - Switch between different themes
   - Export your data for further analysis

## Project Structure

```
spotify-dashboard/
├── app.py                 # Main Streamlit application
├── spotify_auth.py        # Spotify authentication handler
├── data_processor.py      # Data fetching and processing
├── main.py               # Command-line interface
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## API Endpoints Used

- `current_user_recently_played` - Fetches recently played tracks
- Requires scopes: `user-read-recently-played`, `user-top-read`, `user-read-private`

## Technical Details

### Built With

- **Streamlit** - Web application framework
- **Spotipy** - Spotify Web API wrapper
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation and analysis
- **Python-dotenv** - Environment variable management

### Data Processing

The application fetches recent tracks and enriches them with:
- Timestamp parsing (hour, day of week, date)
- Popularity scoring
- Artist frequency analysis
- Statistical summaries

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Limitations

- Spotify API limits recently played tracks to the last 50 songs
- Requires active Spotify usage for meaningful data
- OAuth tokens expire and require re-authentication

## Future Enhancements

- [ ] Historical data storage
- [ ] Playlist analysis
- [ ] Music recommendation engine
- [ ] Social sharing features
- [ ] Mobile-responsive design
- [ ] Deployment to cloud platforms

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Spotify Web API for providing music data
- Streamlit community for the excellent framework
- Plotly for beautiful interactive charts

## Troubleshooting

### Common Issues

**Authentication Error**: Ensure your redirect URI in Spotify Developer Dashboard exactly matches `http://localhost:8888/callback`

**No Recent Tracks**: Play some music on Spotify and wait a few minutes before trying again

**Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

**Token Expired**: Delete the `.cache` file and re-authenticate

## Contact

Ryan Lubell - lubellryan@gmail.com  
Portfolio: https://www.notion.so/Ryan-Lubell-QA-Data-Python-Portfolio-2310281aa0dd8019a6b3d202b7990f00