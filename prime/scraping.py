import requests
from lxml.html import fromstring
from originals.model.prime.oropondb import oropondb

class scraping:

    def __init__(self):
        self.url = "https://www.netflix.com/jp/originals"
        self.template = "https://www.netflix.com"
        # dbインスタンス作成
        self.db = oropondb()

    def scraping(self):
        # 一覧画面
        r1 = requests.get(self.url)
        # html取得
        root1 = fromstring(r1.text)
        self.items = root1.xpath("//div[@class='original-title']")
        # 詳細画面リンク
        items_link = root1.xpath("//a[@class='original-title-link']")

        for i in range(len(self.items)):
            item_link = self.template + items_link[i].attrib['href']
            # 詳細画面
            r2 = requests.get(item_link)
            root2 = fromstring(r2.text)

            # タイトル
            title = root2.xpath("//h1[@class='show-title']")[0].text

            # 公開日
            released_t = root2.xpath("//span[@class='year']")[0].text

            # 上映時間
            duration = root2.xpath("//span[@class='duration']")[0].text
            if duration == None:
                # シーズン
                duration = root2.xpath("//span[@class='test_dur_str']")[0].text

            # ジャンル
            genre = root2.xpath("//span[@class='genre-list']")[0].text
            genre = genre.translate(str.maketrans({u"\xa0": u"", "、": ","}))

            # タグ
            taglist = root2.xpath("//div[@class='moods more-details-content']")
            tags = ""
            if len(taglist) > 0:
                tags = taglist[0].text
                tags = tags.translate(str.maketrans({" ": "", "、": ","}))

            # あらすじ
            story = root2.xpath("//p[@class='synopsis']")[0].text

            # 主演
            actorslist = root2.xpath("//span[@class='actors-list']")
            if len(actorslist) > 0:
                actors = actorslist[0].text
                actors = actors.translate(str.maketrans({u"\xa0": u"", "、": ","}))

            # 監督
            directorslist = root2.xpath("//span[@class='director-name more-details-content']")
            directors = ""
            if len(directorslist) > 0:
                directors = directorslist[0].text
                directors = directors.translate(str.maketrans({u"\xa0": u"", "、": ","}))

            # クリエイター
            creatorslist = root2.xpath("//span[@class='director-name more-details-content']")
            creators = ""
            if len(creatorslist) > 0:
                creators = creatorslist[0].text
                creators = creators.translate(str.maketrans({u"\xa0": u"", "、": ","}))

            self.db.insert_scraping(title,released_t,duration,genre,tags,story,actors,directors,creators)

        self.db.close()

    def add_itemmaster_g(self):
        db = oropondb()
        genres = db.select_genre()

        genre = []
        for i in range(len(genres)):
            genres_list = genres[i][0].split(",")
            for j in range(len(genres_list)):
                if genre.count(genres_list[j]) == 0:
                    genre.append(genres_list[j])

        for i in range(len(genre)):
            genre_list = []
            genre_list.append(genre[i])
            db.insert_genre(tuple(genre_list))

        db.close()
        #ア\ufeffジ\ufeffア\ufeffT\ufeffV\ufeff番\ufeff組\ufeff・ド\ufeffラ\ufeffマ 17

    def add_itemmaster_t(self):
        db = oropondb()
        tags = db.select_tags()
        tag = []
        for i in range(len(tags)):
            if tags[i][0] == None:
                continue
            tags_list = tags[i][0].split(",")
            for j in range(len(tags_list)):
                if tag.count(tags_list[j]) == 0:
                    tag.append(tags_list[j])

        for i in range(len(tag)):
            tag_list = []
            tag_list.append(tag[i])
            db.insert_tags(tuple(tag_list))

        db.close()
