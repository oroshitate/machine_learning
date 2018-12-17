import sys,io
sys.path.append("Applications/MAMP/htdocs/netflix/oropondb")
from netflix.oropondb import oropondb
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

# class machine_learning:
# def machine_learning(self):
# training = []
# for i in range(len(stories)):
#     id = stories[i][0]
#     text = stories[i][1]
#     tagger = MeCab.Tagger("-Owakati")
#     string_output = tagger.parse(text)
#     list_output = string_output.split()
#     # 各文書を表すTaggedDocumentクラスのインスタンスを作成
#     sentence = TaggedDocument(words=list_output, tags=["doc" + str(id)])
#     # 各TaggedDocumentをリストに格納
#     training.append(sentence)

# モデル作成
# model = Doc2Vec(documents=training,size=100,window=15,min_count=1,alpha=0.0025,min_alpha=0.000001,dm=0)

# モデル保存
# model.save('doc2vec.model')

#モデル読み込み
# model = Doc2Vec.load('doc2vec.model')
#
# for i in range(len(stories)):
#     id = stories[i][0]
#     similar = model.docvecs.most_similar("doc" + str(id))
#     similar_id = ""
#     for j in range(len(similar)):
#         similar_id = similar_id + similar[j][0][3:] + ","
#     db.insert_similarity(id,similar_id[:-1])
#
# db.close()