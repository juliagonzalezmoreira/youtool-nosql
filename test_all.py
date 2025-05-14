import os
import pytest
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from youtool import YouTube

from project import (
    connect_mongo,
    load_config,
    ensure_indexes,
    fetch_and_store_channel,
    process_videos,
)

# --- Fixtures ---

@pytest.fixture(scope="module")
def config():
    load_dotenv()
    return load_config()

@pytest.fixture(scope="module")
def db(config):
    return connect_mongo(config["mongo_uri"], config["db_name"])

@pytest.fixture(scope="module")
def yt(config):
    return YouTube(config["api_keys"])

# --- Testes de Conexão e Configuração ---

def test_mongo_connection(db):
    collections = db.list_collection_names()
    assert isinstance(collections, list)

def test_env_config_loaded(config):
    assert "mongo_uri" in config
    assert "channel_url" in config
    assert "api_keys" in config
    assert isinstance(config["api_keys"], list)
    assert config["api_keys"][0]

# --- Testes de Estrutura do Banco ---

def test_indexes_exist(db):
    ensure_indexes(db)
    indexes = db.videos.index_information()
    assert any("video_id" in idx["key"][0] for idx in indexes.values())

# --- Testes de Funções Principais ---

def test_fetch_channel_returns_ids(yt, db, config):
    channel_id, playlist_id = fetch_and_store_channel(yt, db, config["channel_url"])
    assert channel_id and playlist_id
    channel_doc = db.channels.find_one({"channel_id": channel_id})
    assert channel_doc is not None

def test_process_videos_returns_ids(yt, db, config):
    _, playlist_id = fetch_and_store_channel(yt, db, config["channel_url"])
    since = config.get("since")
    since_dt = None
    if since:
        since_dt = datetime.datetime.fromisoformat(since.rstrip('Z') + '+00:00')
    vids = process_videos(yt, db, playlist_id, since_dt)
    assert isinstance(vids, list)
    assert len(vids) > 0
    doc = db.videos.find_one({"video_id": vids[0]})
    assert doc is not None
    assert "raw_metadata" in doc
