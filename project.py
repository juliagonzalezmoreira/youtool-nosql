import os
from dotenv import load_dotenv
from pymongo import MongoClient
from youtool import YouTube
from pprint import pprint

# Carrega variáveis do .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
API_KEYS = os.getenv("YOUTUBE_API_KEYS", "").split(",")

# Conecta ao MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['youtube_data']
videos_col = db['videos']
comments_col = db['comments']

# Inicializa youtool
yt = YouTube(API_KEYS)

# Canal Amelia Dimoldenberg
channel_url = "https://youtube.com/@AmeliaDimoldenberg"
channel_id = yt.channel_id_from_url(channel_url)
print(f"Channel ID: {channel_id}")

# Coleta vídeos e salva no Atlas
for video in yt.channel_videos(channel_id):
    info = next(yt.videos_infos([video["id"]]))
    video_doc = {
        "_id": info["id"],
        "title": info["title"],
        "description": info["description"],
        "likes": info.get("likes", 0),
        "comments_count": info.get("comments_count", 0)
    }
    videos_col.replace_one({"_id": info["id"]}, video_doc, upsert=True)

# Coleta comentários do primeiro vídeo
first_video_id = yt.channel_videos(channel_id).__next__()["id"]
print(f"Buscando comentários de: {first_video_id}")

for comment in yt.video_comments(first_video_id):
    comment_doc = {
        "_id": comment["id"],
        "video_id": first_video_id,
        "author": comment["author"],
        "text": comment["text"],
        "likes": comment.get("likes", 0)
    }
    comments_col.replace_one({"_id": comment["id"]}, comment_doc, upsert=True)

# Mostra o que foi salvo
print("Vídeos salvos no Atlas:")
for v in videos_col.find().limit(3):
    pprint(v)

print("Comentários salvos no Atlas:")
for c in comments_col.find().limit(3):
    pprint(c)
