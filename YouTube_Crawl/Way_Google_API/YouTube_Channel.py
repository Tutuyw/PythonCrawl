from Crawler.Common_Def.common_request_url import request_url_json

api_key = 'AIzaSyDmU-iYzIEu73OU3Bie_xkVmIir-wAU23M'
api_url = 'https://www.googleapis.com/youtube/v3/'
headers = {
    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

def get_playlists(channel_id):
    # search_url = f'{api_url}search?key={api_key}&channelId={channel_id}&maxResults=5&part=snippet'
    channel_url = f'{api_url}channels?key={api_key}&id={channel_id}&part=snippet,contentDetails,statistics,topicDetails'
    playlists_url = f'{api_url}playlists?key={api_key}&channelId={channel_id}&maxResults=50&part=snippet,contentDetails,id'
    response_data = request_url_json(playlists_url, headers)
    print(response_data)
    get_play_id(response_data)

def get_play_id(response_data):
    playlist = response_data['items']
    for play in playlist:
        play_id = play['id']
        get_playlistItems(play_id)

def get_playlistItems(play_id):
    play_url = f'{api_url}playlistItems?key={api_key}&playlistId={play_id}&maxResults=50&part=snippet,contentDetails,id'
    response_data = request_url_json(play_url, headers)
    print(response_data)


get_playlists('UCoC47do520os_4DBMEFGg4A')