import requests

def getMetrics(trackId, headers):

  metrics = [0] * 9 
    
  ## get track audio features 
  getTrackFeaturesUrl = f'https://api.spotify.com/v1/audio-features/{trackId}'
  response = requests.get(getTrackFeaturesUrl, headers=headers)
  trackFeaturesObj = response.json()

  ## get track audio analysis 
  getTrackAnalysisUrl = f'https://api.spotify.com/v1/audio-analysis/{trackId}'
  response = requests.get(getTrackAnalysisUrl, headers=headers)
  trackAnalysisObj = response.json()

  ## update total metrics
  metrics[0] = trackFeaturesObj['energy']
  metrics[1] = trackFeaturesObj['loudness']
  metrics[2] = trackFeaturesObj['tempo']
  metrics[3] = trackFeaturesObj['valence']
  metrics[4] = trackFeaturesObj['danceability']

  ## average tatum intervals per minute - could be changed 
  metrics[5] = len(trackAnalysisObj['tatums'])/trackAnalysisObj['track']['duration']

  ## each song is seperated into "segments", each have their own timbre vectors 
  segments = trackAnalysisObj['segments']
  xAvg = 0
  yAvg = 0
  zAvg = 0
  for segment in segments:
    xAvg += segment['timbre'][0]
    yAvg += segment['timbre'][1]
    zAvg += segment['timbre'][2]

  xAvg /= len(segments)
  yAvg /= len(segments)
  zAvg /= len(segments)

  ## store each dimension of timbre as its own metric - could be changed 
  metrics[6] = xAvg
  metrics[7] = yAvg
  metrics[8] = zAvg

  return metrics
  