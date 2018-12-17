import mysql.connector

class oropondb:

  def __init__(self):
    self.config = {
      'user': 'root',
      'password': 'oroshiterec0205',
      'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
      'database': 'app_db',
      'raise_on_warnings': True,
    }
    self.conn = mysql.connector.connect(**self.config)
    self.cursor = self.conn.cursor()

  def insert_scraping(self,title,released_t,duration,genre,tag,story,actors,directors,creators):
    cursor = self.cursor
    if tag == "":
      tag = None

    if directors == "":
      directors = None

    if creators == "":
      creators = None

    data = (title,released_t,duration,genre,tag,story,actors,directors,creators)
    query = "insert into netflix_items (title,released_t,duration,genre,tag,story,actors,directors,creators) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(query,data)

  def insert_similarity(self,id,similar_id):
    cursor = self.cursor
    data = (id,similar_id)
    query = "insert into netflix_similarity (id,similar_id) values(%s,%s);"
    cursor.execute(query,data)

  def insert_genre(self,genre):
    cursor = self.cursor
    query = "insert into netflix_gitemmasters (genre) values(%s);"
    #変数1つの時もタプルに変換し、末尾にカンマが必要
    cursor.execute(query,genre)

  def insert_tag(self,tag):
    cursor = self.cursor
    query = 'insert into netflix_titemmasters (tag) values(%s);'
    cursor.execute(query,tag)

  def select_item(self,id):
    cursor = self.cursor
    query = "select * from netflix_items where id=%s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_items(self):
    cursor = self.cursor
    query = "select id,title,genre,tag,released_t from netflix_items;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_genre(self):
    cursor = self.cursor
    query = "select genre from netflix_items;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_tag(self):
    cursor = self.cursor
    query = "select tag from netflix_items;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_story(self):
    cursor = self.cursor
    query = "select id,story from netflix_items;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_new_item_list(self):
    cursor = self.cursor
    query = "select id,title,duration,category,format,released_t from netflix_new_items order by created_t asc;"
    cursor.execute(query)
    return cursor.fetchall()


  def close(self):
      self.conn.commit()
      self.cursor.close()
      self.conn.close()
