from originals.model.prime.oropondb import oropondb
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

#class learning_model:
#ex)genre = "国内TV番組・ドラマ"
db = oropondb()
#ジャンルで絞り込めるようにする
results = db.get_story()
# result = []
# if genre != "":
#     for main.js in range(len(results)):
#         if results[main.js][0].find(genre) != -1:
#             result.append(results[main.js][1])
#
#     results = result

training = []

for i in range(len(results)):
    id = results[i][0]
    text = results[i][1]
    tagger = MeCab.Tagger("-Owakati")
    string_output = tagger.parse(text)
    list_output = string_output.split()
    # 各文書を表すTaggedDocumentクラスのインスタンスを作成
    sentence = TaggedDocument(words=list_output, tags=["doc" + str(id)])
    # 各TaggedDocumentをリストに格納
    training.append(sentence)

# モデル作成
model = Doc2Vec(documents=training,size=100,window=15,min_count=1,dm=0)

# モデル保存
model.save('doc2vec.model')

#モデル読み込み
model = Doc2Vec.load('doc2vec.model')

for i in range(len(results)):
    id = results[i][0]
    similar = model.docvecs.most_similar("doc" + str(id))
    similar_id = ""
    for j in range(len(similar)):
        similar_id = similar_id + similar[j][0][3:] + ","

    db.insert_similarity(id,similar_id[:-1])

db.close()