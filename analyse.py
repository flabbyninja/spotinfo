import requests
import config

# Auth URL for time-limited tokens
AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_spotify_token():
  auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': config.CLIENT_ID,
    'client_secret': config.CLIENT_SECRET,
  })
  auth_response_data = auth_response.json();
  access_token = auth_response_data['access_token']
  return(access_token)

if __name__ == "__main__":
  access_token = get_spotify_token()
  headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}