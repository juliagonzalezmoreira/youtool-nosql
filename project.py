import os
from pprint import pprint
from pymongo import MongoClient
from youtool import YouTube
from youtool.utils import simplify_vtt
from dotenv import load_dotenv
import datetime

def load_config(env_path='.env'):
    load_dotenv(env_path)
    config = {
        'api_keys': os.getenv('YOUTUBE_API_KEYS', '').split(','),
        'channel_url': os.getenv('CHANNEL_URL'),
        'mongo_uri': os.getenv('MONGO_URI'),
        'db_name': os.getenv('DB_NAME'),
        'since': os.getenv('SINCE'),
        'transcription_lang': os.getenv('TRANSCRIPTION_LANG', 'en'),
        'transcription_dir': os.getenv('TRANSCRIPTION_DIR', './transcricoes')
    }
    missing = [k for k in ['api_keys', 'channel_url'] if not config[k] or (k == 'api_keys' and not any(config['api_keys']))]
    if missing:
        raise EnvironmentError(f"Missing required config(s) in .env: {', '.join(missing)}")
    config['api_keys'] = [k.strip() for k in config['api_keys'] if k.strip()]
    return config


def connect_mongo(uri: str, db_name: str):
    client = MongoClient(uri)
    return client[db_name]


def ensure_indexes(db):
    db.channels.create_index('channel_id', unique=True)
    db.videos.create_index('video_id', unique=True)
    db.comments.create_index([('video_id', 1), ('comment_id', 1)], unique=True)
    db.transcriptions.create_index('video_id', unique=True)
    db.livechats.create_index('video_id', unique=True)
    db.superchats.create_index('video_id', unique=True)


def fetch_and_store_channel(yt: YouTube, db, channel_url: str):
    channel_id = yt.channel_id_from_url(channel_url)
    info = list(yt.channels_infos([channel_id]))[0]
    record = {
        'channel_id': channel_id,
        'title': info.get('title'),
        'description': info.get('description'),
        'custom_url': info.get('custom_url'),
        'thumbnails': info.get('thumbnails'),
        'stats': info.get('statistics'),
    }
    db.channels.update_one({'channel_id': channel_id}, {'$set': record}, upsert=True)
    return channel_id, info.get('playlist_id')


def process_videos(yt: YouTube, db, playlist_id: str, since=None):
    video_ids, total = [], 0
    for v in yt.playlist_videos(playlist_id):
        total += 1
        pub = v.get('published_at')
        if since and pub and pub < since:
            continue
        vid = v['id']
        video_ids.append(vid)
        db.videos.update_one(
            {'video_id': vid},
            {'$set': {'video_id': vid, 'raw_metadata': v}},
            upsert=True
        )
    print(f"Coletados {len(video_ids)}/{total} vídeos")
    return video_ids


def store_comments(yt: YouTube, db, video_ids):
    for vid in video_ids:
        for c in yt.video_comments(vid):
            cid = c.get('comment_id') or c.get('id')
            if not cid:
                continue
            rec = {
                'video_id': vid,
                'comment_id': cid,
                'author': c.get('author_display_name'),
                'text': c.get('text_display') or c.get('text_original'),
                'published_at': c.get('published_at')
            }
            db.comments.update_one(
                {'video_id': vid, 'comment_id': cid},
                {'$set': rec},
                upsert=True
            )
        print(f"Comentários salvos para vídeo {vid}")


def store_transcriptions(yt: YouTube, db, video_ids, lang, out_dir):
    try:
        import yt_dlp  # noqa
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Para baixar transcrições, instale: pip install yt-dlp")
    try:
        import webvtt  # noqa
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Para processar VTT, instale: pip install webvtt-py")
    os.makedirs(out_dir, exist_ok=True)
    for vid in video_ids:
        for status in yt.download_transcriptions(videos_ids=[vid], language_code=lang, path=out_dir, batch_size=1):
            print(status)
        path = os.path.join(out_dir, f"{vid}.{lang}.vtt")
        with open(path, encoding='utf-8') as f:
            simple = simplify_vtt(f.read())
        db.transcriptions.update_one(
            {'video_id': vid},
            {'$set': {'video_id': vid, 'transcription': simple}},
            upsert=True
        )
        print(f"Transcrição salva para vídeo {vid}")


def store_chats(yt: YouTube, db, video_ids):
    for vid in video_ids:
        # Live chat
        if hasattr(yt, 'livechat'):
            chats = list(yt.livechat(vid))
            db.livechats.update_one(
                {'video_id': vid},
                {'$set': {'video_id': vid, 'live_chat': chats}},
                upsert=True
            )
            print(f"Live chats salvos para vídeo {vid}")
        else:
            print(f"Live chat não suportado pelo Youtool para vídeo {vid}")

        # Superchat
        if hasattr(yt, 'superchat'):
            scs = list(yt.superchat(vid))
            db.superchats.update_one(
                {'video_id': vid},
                {'$set': {'video_id': vid, 'superchat': scs}},
                upsert=True
            )
            print(f"Superchats salvos para vídeo {vid}")
        else:
            print(f"Superchat não suportado pelo Youtool para vídeo {vid}")



def main():
    cfg = load_config()
    since_dt = None
    if cfg['since']:
        val = cfg['since'].rstrip('Z')
        try:
            since_dt = datetime.datetime.fromisoformat(val + '+00:00')
        except Exception:
            raise ValueError("Formato inválido em SINCE no .env. Use ISO8601, ex: 2024-01-01T00:00:00Z")

    yt = YouTube(cfg['api_keys'])
    db = connect_mongo(cfg['mongo_uri'], cfg['db_name'])
    ensure_indexes(db)

    channel_id, playlist_id = fetch_and_store_channel(yt, db, cfg['channel_url'])
    vids = process_videos(yt, db, playlist_id, since_dt)
    limited_vids = vids[:10] # Limitar a 10 vídeos para teste
    store_comments(yt, db, limited_vids)
    store_transcriptions(yt, db, limited_vids, cfg['transcription_lang'], cfg['transcription_dir'])
    store_chats(yt, db, limited_vids)
    print(f"Pront! Operação executada para {len(limited_vids)} vídeos.")

if __name__ == '__main__':
    main()
