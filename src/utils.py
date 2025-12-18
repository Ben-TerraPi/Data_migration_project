import kagglehub
from pymongo import MongoClient
import pandas as pd
import os
import logging


def import_data():
    # Téléchargement dans le cache par défaut
    path = kagglehub.dataset_download("prasad22/healthcare-dataset")

    # Création du dossier de destination à la racine du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(project_root, "dataset")
    os.makedirs(dataset_dir, exist_ok=True)

    # Copie du fichier
    for filename in os.listdir(path):
        src_file = os.path.join(path, filename)
        dst_file = os.path.join(dataset_dir, filename)
        
        with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
            dst.write(src.read())
        
        logging.info(f"Fichier copié: {filename}")

    logging.info(f"Dataset disponible dans: {dataset_dir}")


def connect_to_mongodb():
    """
    Connexion à MongoDB
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        logging.info("✅ Connexion MongoDB")
        return client
    except Exception as e:
        logging.error(f"❌ Erreur de connexion: {e}")
        return None
    

def load_csv_data(file_path):
    """
    Charge les données depuis un fichier CSV
    """
    try:
        if not os.path.exists(file_path):
            logging.error(f"❌ Fichier '{file_path}' introuvable")
            return None
        
        df = pd.read_csv(file_path)
        logging.info(f"✅ Fichier CSV chargé: {len(df)} lignes")
        return df
    except Exception as e:
        logging.error(f"❌ Erreur lors du chargement du CSV: {e}")
        return None


def migrate_data(collection, df):
    """
    Migre les données du DataFrame vers MongoDB
    """
    try:
        # df to dictionnaires pour insertion documents
        records = df.to_dict('records')
        
        # Insertion
        result = collection.insert_many(records)
        logging.info(f"✅ Migration réussie: {len(result.inserted_ids)} documents insérés")
        return True
    except Exception as e:
        logging.error(f"❌ Erreur lors de la migration: {e}")
        return False
