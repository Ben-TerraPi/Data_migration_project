import sys
import pytest
import os
import logging
import main


def make_mock_df():
    class DummyDF:
        class Columns(list):
            def tolist(self):
                return list(self)
        columns = Columns(['Name', 'Age'])
        def __getitem__(self, key): return [1, 2]
        def __setitem__(self, key, value): pass
        def drop_duplicates(self): return self
        def to_dict(self, orient): return [{'Name': 'Alice', 'Age': 30}]
        def __len__(self): return 1
    return DummyDF()


class DummyCollection:
    def insert_many(self, records): 
        class Result: inserted_ids = [1]
        return Result()
    def delete_many(self, query): pass
    def find_one(self): return {'Name': 'Alice', 'Age': 30}
    def aggregate(self, pipeline): return []
    def count_documents(self, query): return 0


class DummyDB:
    def __getitem__(self, name): return DummyCollection()
    def command(self, *args, **kwargs): pass


class DummyClient:
    def __getitem__(self, name): return DummyDB()
    def close(self): pass


@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    monkeypatch.setattr(main, "import_data", lambda: None)
    monkeypatch.setattr(main, "load_csv_data", lambda path: make_mock_df())
    monkeypatch.setattr(main, "normalize_df", lambda df: df)
    monkeypatch.setattr(main, "check_dataframe", lambda df: {
        "colonnes": ['Name', 'Age'],
        "types": {'Name': 'str', 'Age': 'int'},
        "doublons": 0,
        "manquantes": {'Name': 0, 'Age': 0}
    })
    monkeypatch.setattr(main, "connect_to_mongodb", lambda: DummyClient())
    monkeypatch.setattr(main, "migrate_data", lambda collection, df: True)
    monkeypatch.setattr(main, "check_collection", lambda collection, colonnes_ref=None: {
        "colonnes": ['Name', 'Age', '_id'],
        "types": {'Name': 'str', 'Age': 'int', '_id': 'ObjectId'},
        "doublons": 0,
        "manquantes": {'Name': 0, 'Age': 0}
    })
    monkeypatch.setattr(main, "test_compare", lambda df_info, mongo_info: None)
    monkeypatch.setattr(logging, "info", lambda *a, **k: None)
    monkeypatch.setattr(logging, "error", lambda *a, **k: None)
    monkeypatch.setattr(os, "makedirs", lambda *a, **k: None)
    monkeypatch.setattr(os.path, "dirname", lambda path: "root")
    monkeypatch.setattr(os.path, "abspath", lambda path: "root")
    monkeypatch.setattr(os.path, "join", lambda *a: "/".join(a))
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    monkeypatch.setattr(logging, "basicConfig", lambda **kwargs: None)


def test_main_success(monkeypatch):
    ''' 
    vérifie que le script s'exécute sans erreur quand tout est simulé correctement
    '''
    monkeypatch.setattr(sys, "exit", lambda code=0: (_ for _ in ()).throw(SystemExit(code)))
    try:
        main.main_run()
    except SystemExit as e:
        assert e.code != 1


def test_main_error(monkeypatch):
    '''
    vérifie que le script gère bien une exception et quitte avec un code d'erreur.
    '''
    monkeypatch.setattr(main, "import_data", lambda: (_ for _ in ()).throw(Exception("fail")))
    monkeypatch.setattr(sys, "exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    try:
        main.main_run()
    except SystemExit as e:
        assert e.code == 1