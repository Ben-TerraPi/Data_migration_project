from pymongo import MongoClient
import pandas as pd
import os


def connect_to_mongodb():
    """
    Établit la connexion à MongoDB
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        # Test de la connexion
        client.admin.command('ping')
        print("✅ Connexion à MongoDB réussie")
        return client
    except Exception as e:
        print(f"❌ Erreur de connexion à MongoDB: {e}")
        return None


def load_csv_data(file_path):
    """
    Charge les données depuis un fichier CSV
    """
    try:
        if not os.path.exists(file_path):
            print(f"❌ Fichier '{file_path}' introuvable")
            return None
        
        df = pd.read_csv(file_path)
        print(f"✅ Fichier CSV chargé: {len(df)} lignes")
        return df
    except Exception as e:
        print(f"❌ Erreur lors du chargement du CSV: {e}")
        return None


def migrate_data(collection, df):
    """
    Migre les données du DataFrame vers MongoDB
    """
    try:
        # Convertir le DataFrame en liste de dictionnaires
        records = df.to_dict('records')
        
        # Insérer les données
        result = collection.insert_many(records)
        print(f"✅ Migration réussie: {len(result.inserted_ids)} documents insérés")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        return False