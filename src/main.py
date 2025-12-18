import os
import sys
import logging
from utils import import_data, load_csv_data, normalize_df, check_dataframe, connect_to_mongodb, migrate_data, check_collection, test_compare


# Création du dossier logs à la racine si besoin
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)
log_file_path = os.path.join(logs_dir, "migration.log")


# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    try:
        # Récupération du CSV source
        logging.info("Téléchargement du CSV")
        import_data()

        # Chargement du CSV dans un DataFrame
        csv_file = "dataset/healthcare_dataset.csv"  
        df = load_csv_data(csv_file)
        if df is None:
            logging.error("❌ Chargement du CSV échoué.")
            sys.exit(1)

        # Nettoyage du DataFrame
        df = normalize_df(df)

        # Contrôle du DataFrame avant migration
        df_info = check_dataframe(df)

        # Création database et collection MongoDB 
        client = connect_to_mongodb()
        if not client:
            sys.exit(1)
        db = client['datasolutech']
        collection = db['healthcare_dataset']

        # Vider la collection avant migration
        collection.delete_many({})

        # Migration des données
        logging.info("Démarrage de la migration")
        migrate_data(collection, df)

        # Contrôle de la collection après migration
        mongo_info = check_collection(collection, colonnes_ref=df.columns.tolist())

        # Compare le dataframe et la collection
        test_compare(df_info, mongo_info)


    except Exception as e:
        logging.error(f"❌ Erreur du script: {e}")
        sys.exit(1)
    finally:
        try:
            client.close()
            logging.info("Connexion MongoDB fermée")
        except Exception:
            pass