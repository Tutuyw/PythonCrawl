from Crawler.Common_Def.common_request_url import request_url_json


class YouTube_Google_API:
    def __init__(self,api_key):
        self.api_url = 'https://www.googleapis.com/youtube/v3/'
        self.api_key = api_key
        self.headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

    def get_search(self,keyword,type,order):
        """
        :param keyword: 关键词
        :param type: video、channel、playlist
        :param order:date、rating、relevance、videoCount、title、viewCount
        :return:
        """
        search_url = f'{self.api_url}search?key={self.api_key}&q={keyword}&type={type}&order={order}&maxResults=50&part=snippet'
        response_data = request_url_json(search_url, self.headers)
        return response_data

    def get_playlists(self,channel_id):
        playlists_url = f'{self.api_url}playlists?key={self.api_key}&channelId={channel_id}&maxResults=50&part=snippet,contentDetails,id'
        response_data = request_url_json(playlists_url, self.headers)
        self.get_playlistItems(response_data)
        self.judge_nextPageToken(playlists_url, response_data, self.get_playlistItems)

    def get_playlistItems(self,response_data):
        for item in response_data['items']:
            playlistId = item['id']
            play_url = f'{self.api_url}playlistItems?key={self.api_key}&playlistId={playlistId}&maxResults=50&part=snippet,contentDetails,id'
            response_data = request_url_json(play_url, self.headers)
            self.get_videos(response_data)
        self.judge_nextPageToken(play_url,response_data,self.get_videos)

    def get_videos(self,response_data):
        for item in response_data['items']:
            videoId = item['contentDetails']['videoId']
            video_url = f'{self.api_url}videos?key={self.api_key}&id={videoId}&maxResults=50&part=snippet,statistics,contentDetails'
            response_data = request_url_json(video_url, self.headers)
            self.get_video_info(response_data)
        self.judge_nextPageToken(video_url, response_data, self.get_video_info)

    def judge_nextPageToken(self,now_url,response_data,func):
        try:
            if 'nextPageToken' in response_data.keys():
                nextPageToken = response_data['nextPageToken']
                nextPageToken_url = f'{now_url}&pageToken={nextPageToken}'
                response_data = request_url_json(nextPageToken_url, self.headers)
                func(response_data)
            else:
                print('没有下一页')
        except Exception as e:
            print('')

    def get_video_info(self,response_data):
        for item in response_data['items']:
            video_info = {}

    def get_channel(self,channel_id):
        channel_url = f'{self.api_url}channels?key={self.api_key}&id={channel_id}&maxResults=50&part=snippet,statistics,contentDetails'
        response_data = request_url_json(channel_url, self.headers)
        print(response_data)



