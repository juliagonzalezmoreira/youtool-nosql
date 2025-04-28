import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from pymongo import MongoClient  # type: ignore
from youtool import YouTube # type: ignore

load_dotenv()

def get_db(uri=None):
    """
    Conecta ao MongoDB Atlas usando a URI em MONGO_URI.
    """
    uri = uri or os.getenv("MONGO_URI")
    client = MongoClient(uri)
    return client['youtube_data']


def get_yt(api_keys=None):
    """
    Inicializa o cliente YouTube (youtool) com chaves em YOUTUBE_API_KEYS
    e disable_ipv6=True para maior compatibilidade.
    """
    keys = api_keys or os.getenv("YOUTUBE_API_KEYS", "").split(",")
    return YouTube(keys, disable_ipv6=True)


def fetch_and_store(channel_url, db=None, yt=None):
    """
    Extrai metadados de vídeos do canal e armazena na coleção 'videos'.
    Retorna o total de vídeos processados.
    """
    db = db or get_db()
    yt = yt or get_yt()
    channel_id = yt.channel_id_from_url(channel_url)
    videos_col = db['videos']

    total_videos = 0
    for v in yt.channel_videos(channel_id):
        info = next(yt.videos_infos([v['id']]))
        doc = {
            '_id': info['id'],
            'title': info['title'],
            'description': info['description'],
            'likes': info.get('likes', 0),
            'comments_count': info.get('comments_count', 0)
        }
        videos_col.replace_one({'_id': doc['_id']}, doc, upsert=True)
        total_videos += 1

    return total_videos


def fetch_and_store_comments(channel_url, db=None, yt=None):
    """
    Coleta comentários de todos os vídeos do canal e armazena na coleção 'comments'.
    Retorna o total de comentários processados.
    """
    db = db or get_db()
    yt = yt or get_yt()
    channel_id = yt.channel_id_from_url(channel_url)
    comments_col = db['comments']

    total_comments = 0
    for v in yt.channel_videos(channel_url):
        video_id = v['id']
        for c in yt.video_comments(video_id):
            doc = {
                '_id': c['id'],
                'video_id': video_id,
                'author': c.get('author'),
                'text': c.get('text'),
                'likes': c.get('likes', 0)
            }
            comments_col.replace_one({'_id': doc['_id']}, doc, upsert=True)
            total_comments += 1

    return total_comments


def fetch_and_store_transcriptions(channel_url, db=None, yt=None, path: str = 'transcriptions'):
    """
    Baixa transcrições em português para todos os vídeos do canal,
    salva arquivos em 'path' e registra status na coleção 'transcriptions'.
    Retorna o total de transcrições processadas.
    """
    db = db or get_db()
    yt = yt or get_yt()
    channel_id = yt.channel_id_from_url(channel_url)
    trans_col = db['transcriptions']

    Path(path).mkdir(parents=True, exist_ok=True)
    video_ids = [v['id'] for v in yt.channel_videos(channel_url)]
    total_trans = 0
    for result in yt.download_transcriptions(video_ids, language_code='pt', path=path):
        doc = {
            'video_id': result['video_id'],
            'status': result.get('status'),
            'filename': str(result.get('filename'))
        }
        trans_col.replace_one({'video_id': doc['video_id']}, doc, upsert=True)
        total_trans += 1

    return total_trans


def fetch_and_store_livechat(channel_url, db=None, yt=None):
    """
    Coleta mensagens de chat e superchat do primeiro vídeo do canal,
    armazena na coleção 'livechat' e retorna o total de mensagens.
    """
    db = db or get_db()
    yt = yt or get_yt()
    channel_id = yt.channel_id_from_url(channel_url)
    live_col = db['livechat']

    # Converte a lista em um iterador
    videos_iter = iter(yt.channel_videos(channel_url))
    try:
        first_vid = next(videos_iter)
    except StopIteration:
        return 0

    video_id = first_vid['id']
    total_msgs = 0
    for msg in yt.video_livechat(video_id):
        doc = {
            '_id': msg.get('id'),
            'video_id': video_id,
            'author': msg.get('author'),
            'text': msg.get('text'),
            'money_currency': msg.get('money_currency'),
            'money_amount': msg.get('money_amount')
        }
        live_col.replace_one({'_id': doc['_id']}, doc, upsert=True)
        total_msgs += 1

    return total_msgs

if __name__ == '__main__':
    URL = os.getenv('CHANNEL_URL', 'https://youtube.com/@AmeliaDimoldenberg')
    print(f"Vídeos armazenados: {fetch_and_store(URL)}")
    print(f"Comentários armazenados: {fetch_and_store_comments(URL)}")
    print(f"Transcrições processadas: {fetch_and_store_transcriptions(URL)}")
    print(f"Mensagens de chat armazenadas: {fetch_and_store_livechat(URL)}")
