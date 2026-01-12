# TuneFlow

## What it does

TuneFlow is a Spotify playlist filtering application that uses machine learning to automatically filter songs from your existing playlists based on mood. The application trains a neural network on your mood-labeled playlists (Happy, Sad, Hype, Chill) and then uses that model to create new playlists containing only songs that match your desired mood.

## Tech Stack

- **Backend Framework**: Flask (Python)
- **Machine Learning**: PyTorch
- **Data Processing**: pandas, numpy
- **ML Utilities**: scikit-learn
- **API Integration**: Spotify Web API
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: OAuth 2.0 (Spotify)

## Architecture at a High Level

The application follows a client-server architecture with a machine learning pipeline:

1. **Web Application Layer**: Flask server handles HTTP requests, user sessions, and OAuth authentication with Spotify
2. **Authentication Flow**: Implements Spotify OAuth 2.0 to obtain user permissions and access tokens
3. **Data Collection**: Fetches playlist data and audio features (energy, loudness, tempo, valence, danceability) from Spotify API
4. **Training Pipeline**: 
   - Collects audio metrics from mood-labeled training playlists
   - Trains a feedforward neural network (2 hidden layers) to classify songs into 4 mood categories
   - Uses CrossEntropyLoss and Adam optimizer
5. **Prediction & Filtering**: Uses the trained model to filter songs from user's playlists based on selected mood
6. **Playlist Creation**: Creates new Spotify playlists with filtered songs

## How it's used

### Prerequisites
- Python 3.x
- Spotify Developer Account (for Client ID and Secret)
- Required Python packages (Flask, PyTorch, pandas, numpy, scikit-learn, requests, python-dotenv)

### Setup
1. Clone the repository
2. Create a `.env` file with your Spotify credentials:
   ```
   CLIENT_SECRET=your_spotify_client_secret
   SECRET_KEY=your_flask_secret_key
   ```
3. Update `CLIENT_ID` in `main.py` with your Spotify Client ID
4. Ensure you have training playlists named: "hype shit", "happy shit", "chill shit", "sad shit" in your Spotify account

### Running the Application
1. Start the Flask server:
   ```bash
   python main.py
   ```
2. Navigate to `http://localhost:8000` in your browser
3. Click "Login with Spotify" to authenticate
4. Fill out the form with:
   - **Old Playlist Name**: The exact name of the playlist you want to filter
   - **New Playlist Name**: The name for your new filtered playlist
   - **Mood**: Select one of Happy, Sad, Hype, or Chill
5. The application will:
   - Train the model on your mood-labeled playlists
   - Filter songs from your old playlist based on the selected mood
   - Create a new playlist with the filtered songs

### Note
The application runs locally and requires manual setup. It's not currently hosted, so you'll need to run it on your local machine with your own Spotify API credentials.

