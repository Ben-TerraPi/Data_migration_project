import os
import sys
import logging
from utils import import_data, connect_to_mongodb, load_csv_data, migrate_data


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
    # Import du CSV
    logging.info("Téléchargement du CSV")
    import_data()

    # Connexion à MongoDB
    logging.info("Démarrage de la migration")
    client = connect_to_mongodb()
    if not client:
        sys.exit(1)
    
    try:
        # Sélection de la base et collection
        db = client['datasolutech']
        collection = db['healthcare_dataset']

        # Chargement du fichier CSV
        csv_file = "dataset/healthcare_dataset.csv"  
        df = load_csv_data(csv_file)
        if df is None:
            logging.error("❌ Chargement du CSV échoué.")
            sys.exit(1)
        
        # Migration des données
        migrate_data(collection, df)
        
        logging.info("✅ Migration terminée avec succès!")
        
    except Exception as e:
        logging.error(f"❌ Erreur migration: {e}")
    finally:
        # Fermeture de la connexion
        client.close()
        logging.info("Connexion MongoDB fermée")