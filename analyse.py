import requests
import config
import os
import errno
import pandas as pd

headers = {}

# Auth URL for time-limited tokens
AUTH_URL = 'https://accounts.spotify.com/api/token'

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

def get_spotify_token():
  auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': config.CLIENT_ID,
    'client_secret': config.CLIENT_SECRET,
  })
  auth_response_data = auth_response.json();
  access_token = auth_response_data['access_token']
  return(access_token)

def get_artist_info():
  # Soundgarden
  artist_id = '5xUf6j4upBrXZPg6AI4MRK'
  # pull all artists albums
  response = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                 headers=headers, 
                 params={'include_groups': 'album', 'limit': 50})
  artist_data = response.json()
  return artist_data

def get_album_tracks(albumdata):
  data = []
  albums = []

  # loop over albums and get all tracks
  for album in albumdata['items']:
    album_name = album['name']

    # skip over albums that have already been grabbed
    trim_name = album_name.split('(')[0].strip()
    if trim_name.upper() in albums:
      continue
    albums.append(trim_name.upper()) # use upper to standardize

    # display progress as processing continues
    print(album_name)

    # pull all tracks from this album
    r = requests.get(BASE_URL + 'albums/' + album['id'] + '/tracks', headers=headers)
    tracks = r.json()['items']

    for track in tracks:
      # get audio features (key, liveliness, danceability...)
      f = requests.get(BASE_URL + 'audio-features/' + track['id'], headers=headers)
      f = f.json()

    # combine with album info
    f.update({
      'track_name': track['name'],
      'album_name': album_name,
      'short_album_name': trim_name,
      'release_date': album['release_date'],
      'album_id': album['id']
    })

    data.append(f)

  return data

if __name__ == "__main__":
  access_token = get_spotify_token()
  headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
  }
  data = get_artist_info()
  albumdata = get_album_tracks(data)
  df = pd.DataFrame(albumdata)

  json_file = df.to_json(orient='records')
  filename = '/tmp/spotinfo/albumdata.json'

  # create directory if required
  if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

  #export JSON file
  with open(filename, 'w') as f:
    f.write(json_file)

  # # convert release_date to an actual date, and sort by it
  # df['release_date'] = pd.to_datetime(df['release_date'])
  # df = df.sort_values(by='release_date')

  # # Get rid of live album, remixes, vocal tracks, ...
  # df = df[~df['track_name'].str.contains('Live|Mix|Track')]

  # df.head()