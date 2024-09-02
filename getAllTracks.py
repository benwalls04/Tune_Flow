import requests

def getAllTracks(playlist_id, headers):
    base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    
    tracks = []
    url = base_url

    while url:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        tracks.extend(response_data['items'])
        
        # Check if there is a next page
        url = response_data['next']

    return tracks