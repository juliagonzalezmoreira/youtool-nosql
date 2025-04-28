import os
import sys
import pytest  # type: ignore
import mongomock # type: ignore
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv  # type: ignore

# Ajusta path para importar etl.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import etl

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

@pytest.fixture(autouse=True)
def env(monkeypatch):
    # Configura variáveis de ambiente de teste
    monkeypatch.setenv("MONGO_URI", os.getenv("MONGO_URI"))
    monkeypatch.setenv("YOUTUBE_API_KEYS", os.getenv("YOUTUBE_API_KEYS"))

@pytest.fixture
def fake_db():
    return mongomock.MongoClient()['youtube_data']

@pytest.fixture
def fake_yt():
    yt = MagicMock()
    yt.channel_id_from_url.return_value = "chan123"
    yt.channel_videos.return_value = [{"id": "v1"}, {"id": "v2"}]

    def infos(ids):
        for vid in ids:
            yield {"id": vid, "title": f"Title {vid}", "description": f"Desc {vid}", "likes": 10, "comments_count": 5}
    yt.videos_infos.side_effect = infos

    def comments(video_id):
        yield {"id": f"c1_{video_id}", "author": "UserA", "text": "Hello", "likes": 1}
        yield {"id": f"c2_{video_id}", "author": "UserB", "text": "World", "likes": 2}
    yt.video_comments.side_effect = comments

    def transcriptions(video_ids, language_code, path):
        for vid in video_ids:
            yield {"video_id": vid, "status": "done", "filename": f"{path}/{vid}.txt"}
    yt.download_transcriptions.side_effect = transcriptions

    def livechat(video_id):
        yield {"id": "lc1", "author": "UserA", "text": "Chat!", "money_currency": None, "money_amount": None}
        yield {"id": "sc1", "author": "UserC", "text": "Superchat!", "money_currency": "USD", "money_amount": 5.0}
    yt.video_livechat.side_effect = livechat

    return yt

@patch('etl.MongoClient')
def test_get_db(mock_mc, monkeypatch):
    mock_client = mongomock.MongoClient()
    mock_mc.return_value = mock_client
    monkeypatch.setenv("MONGO_URI", os.getenv("MONGO_URI"))

    db = etl.get_db()
    mock_mc.assert_called_once_with(os.getenv("MONGO_URI"))
    assert db == mock_client['youtube_data']

@patch('etl.YouTube')
def test_get_yt(mock_youtube, monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEYS", os.getenv("YOUTUBE_API_KEYS").strip())

    yt_client = etl.get_yt()
    mock_youtube.assert_called_once_with(os.getenv("YOUTUBE_API_KEYS").split(','), disable_ipv6=True)
    assert yt_client == mock_youtube.return_value


def test_fetch_and_store(monkeypatch, fake_db, fake_yt):
    monkeypatch.setattr(etl, "get_db", lambda uri=None: fake_db)
    monkeypatch.setattr(etl, "get_yt", lambda keys=None: fake_yt)

    count = etl.fetch_and_store(os.getenv("CHANNEL_URL"), db=fake_db, yt=fake_yt)
    assert count == 2
    docs = list(fake_db['videos'].find())
    assert len(docs) == 2
    ids = {d['_id'] for d in docs}
    assert ids == {"v1", "v2"}


def test_fetch_and_store_comments(monkeypatch, fake_db, fake_yt):
    monkeypatch.setattr(etl, "get_db", lambda uri=None: fake_db)
    monkeypatch.setattr(etl, "get_yt", lambda keys=None: fake_yt)

    total = etl.fetch_and_store_comments(os.getenv("CHANNEL_URL"), db=fake_db, yt=fake_yt)
    assert total == 4
    docs = list(fake_db['comments'].find())
    assert len(docs) == 4
    assert any(d['author'] == 'UserA' for d in docs)
    assert any(d['text'] == 'World' for d in docs)


def test_fetch_and_store_transcriptions(monkeypatch, fake_db, fake_yt, tmp_path):
    monkeypatch.setattr(etl, "get_db", lambda uri=None: fake_db)
    monkeypatch.setattr(etl, "get_yt", lambda keys=None: fake_yt)

    count = etl.fetch_and_store_transcriptions(os.getenv("CHANNEL_URL"), db=fake_db, yt=fake_yt, path=str(tmp_path))
    assert count == 2
    docs = list(fake_db['transcriptions'].find())
    assert len(docs) == 2
    for d in docs:
        assert d['status'] == 'done'
        assert d['filename'].endswith('.txt')


def test_fetch_and_store_livechat(monkeypatch, fake_db, fake_yt):
    monkeypatch.setattr(etl, "get_db", lambda uri=None: fake_db)
    monkeypatch.setattr(etl, "get_yt", lambda keys=None: fake_yt)

    count = etl.fetch_and_store_livechat(os.getenv("CHANNEL_URL"), db=fake_db, yt=fake_yt)
    assert count == 2
    docs = list(fake_db['livechat'].find())
    assert len(docs) == 2
    sc = next(d for d in docs if d['money_amount'] is not None)
    assert sc['money_currency'] == 'USD'
    assert sc['money_amount'] == 5.0
