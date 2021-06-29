from sys import path
from .browser import ReinsOperator
from scrapy.http import HtmlResponse


def get_profile_path(file):
    f = open(file, 'r')
    path = f.read()
    f.close()

    # プロファイルパスとディレクトリにパスを分割する
    split_path = path.rsplit('\\', 1)
    profile_path = split_path[0]
    profile_dir = split_path[1]
    return profile_path, profile_dir


# profile_path = 'C:\\Users\\chigu\\AppData\\Local\\Google\\Chrome\\User Data'
# profile_dir = 'Profile 2'
profile_path, profile_dir = get_profile_path('profile.txt')
ID = '134038181206'
PW = 'ryoma0927'
URL = "https://system.reins.jp/login/main/KG/GKG001200"

reins = ReinsOperator(ID, PW, URL)
reins.open(profile_path, profile_dir)


class SeleniumMiddleware(object):

    def process_request(self, request, spider):
        if request.meta['next']:
            reins.load_next_page()
            return HtmlResponse(
                url=URL,
                body=reins.download(),
                encoding='utf-8')
        else:
            reins.login()
            reins.input_query(request.meta['query'])
            return HtmlResponse(
                url=URL,
                body=reins.download(),
                encoding='utf-8')
