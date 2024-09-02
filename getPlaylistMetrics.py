import requests
from getAllTracks import getAllTracks

def getMetrics(playlist_id, headers):

  items = getAllTracks(playlist_id, headers)

  track_ids = []
  for item in items:
    track_ids.append(item['track']['id'])

  metrics = [[0] * 5 for _ in range(len(track_ids))]  
  count = 0

  while(count < len(track_ids)):
    track_ids_str = ''

    ## call the function in chunks of 100
    chunk = track_ids[count:min(count + 100, len(track_ids))]
    chunk_str = ','.join(chunk)
    track_ids_str += chunk_str
    
    ## get track audio features 
    getTrackFeaturesUrl = f'https://api.spotify.com/v1/audio-features?ids={track_ids_str}'
    response = requests.get(getTrackFeaturesUrl, headers=headers)
    resList = response.json()

    if response.status_code == 200:
      # Successful response
      resList = response.json()  # Parse JSON data from response
      print('API call successful. Data received:')
    elif response.status_code == 429:
        # Rate limit exceeded
        print('Limit Reached')
    else:
      # Handle errors
      print(f'Error occurred: HTTP status code {response.status_code}')


    ## update total metrics
    audioFeatures = resList['audio_features']
    for i in range(len(audioFeatures)):
      metrics[count + i][0] = audioFeatures[i]['energy']
      metrics[count + i][1] = audioFeatures[i]['loudness']
      metrics[count + i][2] = audioFeatures[i]['tempo']
      metrics[count + i][3] = audioFeatures[i]['valence']
      metrics[count + i][4] = audioFeatures[i]['danceability']

    count += 100

  return metrics
  