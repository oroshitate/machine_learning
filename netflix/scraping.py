import requests
from lxml.html import fromstring
from netflix.oropondb import oropondb

class scraping:

    def __init__(self):
        self.url = "https://www.netflix.com/jp/originals"
        self.template = "https://www.netflix.com"
        # dbインスタンス作成
        self.db = oropondb()

    def add_item(self):
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
            genre_list = []
            genre1 = root2.xpath("//span[@class='genre-list']")[0].text
            genre2_list = root2.xpath("//a[@class='title-hero-genre-list']")
            if len(genre2_list) > 0:
                for i in range(len(genre2_list)):
                    genre2 = genre2_list[i].text
                    genre2 = genre2.translate(str.maketrans({u"\xa0": u""}))
                    genre_list.append(genre2)

                genre1_list = root2.xpath("//span[@class='genre-list']/text()")
                for i in range(len(genre1_list)):
                    genre1_text = genre1_list[i]
                    if genre1_text == "、"+u"\xa0":
                        continue
                    genre1_text = genre1_text.translate(str.maketrans({u"\xa0": u""}))
                    if genre1_text[0:1] == "、":
                        genre1_text = genre1_text[1:]
                    if genre1_text[-1:] == "、":
                        genre1_text = genre1_text[:-1]

                    genre1 = genre1_text.translate(str.maketrans({u"\xa0": u"", "、": ","}))
                    genre_list.append(genre1)

                genre = ",".join(genre_list)
                if genre[-1:] == ",":
                    genre = genre[:-1]

            else:
                genre = genre1.translate(str.maketrans({u"\xa0": u"", "、": ","}))
                if genre[-1:] == ",":
                    genre = genre[:-1]

            # タグ
            taglist = root2.xpath("//div[@class='moods more-details-content']")
            tags = ""
            if len(taglist) > 0:
                tags = taglist[0].text
                tags = tags.translate(str.maketrans({" ": "", "、": ","}))
                if (tags[-1:] == ","):
                    tags = tags[:-1]

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

            print(title)
            print(genre)

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
        tags = db.select_tag()
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
            db.insert_tag(tuple(tag_list))

        db.close()