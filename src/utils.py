import kagglehub
from pymongo import MongoClient
import pandas as pd
import os
import logging


def import_data():
    """
    Fonction pour importer le CSV depuis kaggle
    """
    # Téléchargement dans le cache par défaut
    path = kagglehub.dataset_download("prasad22/healthcare-dataset")

    # Création du dossier de destination à la racine du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(project_root, "dataset")
    os.makedirs(dataset_dir, exist_ok=True)

    # Copie du fichier avec vérification si déjà présent
    for filename in os.listdir(path):
        src_file = os.path.join(path, filename)
        dst_file = os.path.join(dataset_dir, filename)

        if os.path.exists(dst_file):
            logging.info(f"Fichier déjà présent, non copié : {filename}")
            continue
        
        with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
            dst.write(src.read())
        
        logging.info(f"Fichier copié: {filename}")

    logging.info(f"Dataset disponible dans: {dataset_dir}")


def load_csv_data(file_path):
    """
    Charge les données depuis un fichier CSV
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier '{file_path}' introuvable")
    df = pd.read_csv(file_path)
    logging.info(f"Fichier CSV chargé: {len(df)} lignes")
    return df


def normalize_df(df):
    """
    Normalise les noms et supprime les doublons
    """
    df["Name"] = df["Name"].str.title()
    df = df.drop_duplicates()
    logging.info(f"{len(df)} lignes après suppression des doublons")
    return df


def check_dataframe(df):
    """
    Vérifie l'intégrité du DataFrame avant migration.
    Retourne un dictionnaire avec colonnes, types, doublons, valeurs manquantes.
    """
    colonnes = df.columns.tolist()
    types = df.dtypes.astype(str).to_dict()
    doublons = df.duplicated().sum()
    manquantes = df.isnull().sum().to_dict()
    # Log colonnes et types
    for col in colonnes:
        logging.info(f"[DF] Colonne: {col} | Type: {types[col]}")
    result = {
        "colonnes": colonnes,
        "types": types,
        "doublons": doublons,
        "manquantes": manquantes
    }
    return result


def connect_to_mongodb():
    """
    Connexion à MongoDB
    """
    client = MongoClient('mongodb://localhost:27017/')
    logging.info("Connexion MongoDB")
    return client


def migrate_data(collection, df):
    """
    Migre les données du DataFrame vers MongoDB
    """
    # df to dictionnaires pour insertion documents
    records = df.to_dict('records')
    # Insertion
    result = collection.insert_many(records)
    logging.info(f"✅ Migration réussie: {len(result.inserted_ids)} documents insérés")
    return True


def check_collection(collection, colonnes_ref=None):
    """
    Vérifie l'intégrité de la collection MongoDB après migration.
    Retourne un dictionnaire avec colonnes, types, doublons, valeurs manquantes.
    colonnes_ref : liste de colonnes attendues (optionnel)
    """
    sample = collection.find_one() or {}
    colonnes = list(sample.keys())
    types = {k: type(v).__name__ for k, v in sample.items()}
    # Log colonnes et types MongoDB
    for col in colonnes:
        logging.info(f"[MongoDB] Colonne: {col} | Type: {types.get(col, 'N/A')}")

    if colonnes_ref is None:
        colonnes_ref = [c for c in colonnes if c != "_id"]

    # Valeurs manquantes
    manquantes = {
        col: collection.count_documents({col: {"$in": [None, ""]}})
        for col in colonnes_ref if col != "_id"
    }

    # Doublons sur toutes les colonnes (hors _id)
    group_id = {col: f"${col}" for col in colonnes_ref if col != "_id"}
    pipeline = [
        {"$group": {
            "_id": group_id,
            "count": {"$sum": 1}
        }},
        {"$match": {"count": {"$gt": 1}}}
    ]
    doublons = len(list(collection.aggregate(pipeline)))

    result = {
        "colonnes": colonnes,
        "types": types,
        "doublons": doublons,
        "manquantes": manquantes
    }
    return result


def test_compare(df_info, mongo_info):
    """
    Compare les résultats d'intégrité entre DataFrame et MongoDB.
    Affiche les différences principales.
    """
    colonnes_df = set(df_info["colonnes"])
    colonnes_mongo = set(mongo_info["colonnes"]) - {"_id"}
    total_missing_df = sum(df_info['manquantes'].get(col, 0) for col in df_info['colonnes'])
    total_missing_mongo = sum(mongo_info['manquantes'].get(col, 0) for col in df_info['colonnes'] if col in mongo_info['manquantes'])

    logging.info("=== Comparaison ===")
    logging.info(f"Doublons DF={df_info['doublons']}, MongoDB={mongo_info['doublons']}")
    logging.info(f"Colonnes identiques (hors _id) : {colonnes_df == colonnes_mongo}")
    logging.info(f"Valeurs manquantes DF={total_missing_df}, MongoDB={total_missing_mongo}")
