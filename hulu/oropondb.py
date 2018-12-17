import mysql.connector

class oropondb:

  def __init__(self):
    self.config = {
      'user': 'root',
      'password': 'oroshiterec0205',
      'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
      'database': 'oropon_db',
      'raise_on_warnings': True,
    }
    self.conn = mysql.connector.connect(**self.config)
    self.cursor = self.conn.cursor()

  def insert_scraping(self,title,released_t,duration,genre,tags,story,actors,directors,creators):
    cursor = self.cursor
    if tags == "":
      tags = None

    if directors == "":
      directors = None

    if creators == "":
      creators = None

    data = (title,released_t,duration,genre,tags,story,actors,directors,creators)
    query = "insert into t_h_item (title,released_t,duration,genre,tags,story,actors,directors,creators) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(query,data)

  def insert_similarity(self,id,similar_id):
    cursor = self.cursor
    data = (id,similar_id)
    query = "insert into t_h_similarity (id,similar_id) values(%s,%s);"
    cursor.execute(query,data)

  def insert_genre(self,genre):
    cursor = self.cursor
    query = "insert into t_h_itemmaster_g (genre) values(%s);"
    #変数1つの時もタプルに変換し、末尾にカンマが必要
    cursor.execute(query,genre)

  def insert_tags(self,tags):
    cursor = self.cursor
    query = 'insert into t_h_itemmaster_t (tags) values(%s);'
    cursor.execute(query,tags)

  def insert_review(self,user_id,rate,text,item_id,service):
    cursor = self.cursor
    data = (user_id, rate, text, item_id)
    query = 'insert into t_h_review (user_id,rate,text,item_id) values(%s,%s,%s,%s);'
    cursor.execute(query, data)
    last_insertid = cursor.lastrowid
    data = (user_id, rate, text, item_id, service, last_insertid)
    query = 'insert into t_review (user_id,rate,text,item_id,service,service_reviewid) values(%s,%s,%s,%s,%s,%s);'
    cursor.execute(query, data)

  def insert_user(self,name):
    cursor = self.cursor
    query = 'insert into t_user (name) values(%s);'
    cursor.execute(query, name)
    last_insertid = cursor.lastrowid
    return last_insertid

  def get_story(self):
    cursor = self.cursor
    query = "select id,story from t_h_item;"
    cursor.execute(query)
    return cursor.fetchall()

  def get_genre(self):
    cursor = self.cursor
    query = "select id,genre from t_h_itemmaster_g;"
    cursor.execute(query)
    return cursor.fetchall()

  def get_tag(self):
    cursor = self.cursor
    query = "select id,tags from t_h_itemmaster_t;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_item(self,id):
    cursor = self.cursor
    query = "select * from t_h_item where id=%s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_item_title(self,id):
    cursor = self.cursor
    query = "select id,title from t_h_item where id=%s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_items(self):
    cursor = self.cursor
    query = "select id,title,genre,channel,released_t from t_h_item;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_genre(self):
    cursor = self.cursor
    query = "select genre from t_h_item;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_tags(self):
    cursor = self.cursor
    query = "select tags from t_h_item;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_more_genre(self,genre):
    cursor = self.cursor
    query = "select id,title,genre,channel,released_t from t_h_item where "
    last = len(genre)
    for i in range(len(genre)):
      if i == last-1:
        add_query = "find_in_set('" + genre[i] + "', genre);"
        query = query + add_query
      else:
        add_query = "find_in_set('" + genre[i] + "', genre) or "
        query = query + add_query

    cursor.execute(query)
    return cursor.fetchall()

  def select_more_tag(self,tag,way):
    cursor = self.cursor
    query = "select id,title,genre,tags,released_t from t_h_item where "
    last = len(tag)
    for i in range(len(tag)):
      if i == last - 1:
        add_query = "find_in_set('" + tag[i] + "', tags);"
        query = query + add_query
      else:
        if way == "and":
          add_query = "find_in_set('" + tag[i] + "', tags) and "
          query = query + add_query
        else:
          add_query = "find_in_set('" + tag[i] + "', tags) or "
          query = query + add_query

    cursor.execute(query)
    return cursor.fetchall()

  def select_similarity(self,id):
    cursor = self.cursor
    query = "select id,similar_id from t_h_similarity where id=%s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_s_item(self,id):
    cursor = self.cursor
    query = "select id,title,genre,tags,released_t from t_h_item where id=%s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_new_item_list(self):
    cursor = self.cursor
    query = "select * from t_h_new_item order by created_t asc;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_reviews_count(self,id):
    cursor = self.cursor
    query = "select count(id),avg(rate) from t_h_review where item_id = %s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_reviews_avgrate(self,id):
    cursor = self.cursor
    query = "select avg(rate) from t_h_review where item_id = %s and rate != 0 ;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_reviews(self,id):
    cursor = self.cursor
    query = "select * from t_h_review where item_id=%s order by created_t desc limit 50;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def select_review_list(self):
    cursor = self.cursor
    query = "select * from t_h_review order by created_t desc limit 50;"
    cursor.execute(query, id)
    return cursor.fetchall()

  def select_users(self):
    cursor = self.cursor
    query = "select id,name from t_user order by created_t desc;"
    cursor.execute(query)
    return cursor.fetchall()

  def select_user(self,id):
    cursor = self.cursor
    query = "select id,name from t_user where id=%s;"
    cursor.execute(query,id)
    return cursor.fetchall()

  def check_user(self,name):
    cursor = self.cursor
    query = "select id,name from t_user where name=%s;"
    cursor.execute(query,name)
    return cursor.fetchall()

  def search_review(self,data):
    cursor = self.cursor
    if type(data) is not int:
      query = "select * from t_h_review inner join t_h_item on t_h_review.item_id = t_n_item.id where t_h_review.text LIKE '%" + data + "%' or t_h_item.title LIKE '%" + data + "%' order by t_h_review.created_t desc;"
    else:
      query = "select * from t_h_review where user_id LIKE '%" + str(data) + "%' order by created_t desc;"
    cursor.execute(query)
    return cursor.fetchall()

  def load_review(self,start,itemid):
      cursor = self.cursor
      data = (itemid,start)
      query = "select * from t_h_review where item_id=%s order by created_t desc limit 50 offset %s;"
      cursor.execute(query, data)
      return cursor.fetchall()

  def load_review_list(self,start):
      cursor = self.cursor
      query = "select * from t_h_review order by created_t desc limit 50 offset %s;"
      cursor.execute(query,start)
      return cursor.fetchall()

  def close(self):
      self.conn.commit()
      self.cursor.close()
      self.conn.close()