import requests
import json


class NeteaseMusic:
    """
    网易云音乐
    """
    def __init__(self):
        self.base_url = 'http://musicapi.leanapp.cn'

    def get_music_list(self, keyword, limit, page, stype):
        """
        调用此接口,传入搜索关键词可以搜索该音乐/专辑/歌手/歌单/用户,关键词可以多个,以空格隔开,
        如"周杰伦 搁浅"(不需要登录),搜索获取的mp3url不能直接用,可通过/song/url接口传入歌曲id获取具体的播放链接
        :param keyword: 关键词
        :param limit: 返回数量 , 默认为 30
        :param page: 分页 , 如:(page-1)*30, 其中 30 为 limit 的值 , 默认为 0
        :param type: 搜索类型；默认为 1 即单曲 , 取值意义 : 1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单, 1002: 用户, 1004: MV,
                1006: 歌词, 1009: 电台, 1014: 视频, 1018:综合
        :return: 简化后的歌曲列表信息
        """
        url = self.base_url + '/search?keywords={}&limit={}&offset={}&type=1'.format(keyword, limit, (page-1)*limit, stype)
        response = requests.get(url=url)
        html = json.loads(response.text)
        song_list = html['result']['songs']
        simplified_song_list = []
        for song in song_list:
            simplified_song = {}
            simplified_song['id'] = song['id']
            simplified_song['name'] = song['name']

            artist_name = ''
            for artist in song['artists']:
                artist_name = artist_name + str(artist['name']) + '/'
            simplified_song['artist'] = artist_name[:-1]
            simplified_song['album'] = song['album']['name']
            simplified_song_list.append(simplified_song)

        return simplified_song_list

    def verify_music(self, music_id):
        """
        调用此接口,传入歌曲 id, 可获取音乐是否可用
        :param music_id:
        :return: { success: true, message: 'ok' } 或者 { success: false, message: '亲爱的,暂无版权' }
        """
        return json.loads(requests.get(self.base_url + '/check/music?id={}'.format(music_id)).text)

    def get_music(self, music_id):
        """
        根据歌曲Id获得歌曲链接
        :param music_id: 歌曲ID
        :return: 歌曲的URL
        """
        res = requests.get(self.base_url + '/music/url?id={}'.format(music_id))
        print('Service-get_music[res]:', res.url)
        data = json.loads(res.text)
        return data['code'], data['data'][0]['url']

    def get_music_info(self, music_id):
        """
        可获得歌曲详情(注意:歌曲封面现在需要通过专辑内容接口获取)
        :param music_id:
        :return: 歌曲信息
        """
        res = requests.get(self.base_url + '/song/detail?ids={}'.format(music_id))
        data = json.loads(res.text)
        return data['code'], data['songs'][0]


# url = NeteaseMusic().get_music_info('349892')
# print(url)
# # music_list = get_music_list('是想你的声音啊', 10, 2, 1)
# # for music in music_list:
# #     print(music)

