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

def main_run():
    client = None
    try:
        # 1. Récupération du CSV source
        logging.info("Téléchargement du CSV")
        import_data()

        # 2. Chargement du CSV dans un DataFrame
        csv_file = "dataset/healthcare_dataset.csv"  
        df = load_csv_data(csv_file)
        if df is None:
            logging.error("❌ Chargement du CSV échoué.")
            sys.exit(1)

        # 3. Nettoyage du DataFrame
        df = normalize_df(df)

        # 4. Contrôle du DataFrame avant migration
        df_info = check_dataframe(df)

        # 5. Création database et collection MongoDB 
        client = connect_to_mongodb()
        if not client:
            sys.exit(1)
        db = client['datasolutech']
        collection = db['healthcare_dataset']

        # Création d'un utilisateur lecture seule
        mongo_user = os.getenv("MONGO_USER", "user")
        mongo_user_pwd = os.getenv("MONGO_USER_PASSWORD", "user")
        db.command("createUser", mongo_user, pwd=mongo_user_pwd, roles=[{"role": "read", "db": "datasolutech"}])

        # 6. Vider la collection avant migration
        collection.delete_many({})

        # 7. Migration des données
        logging.info("Démarrage de la migration")
        migrate_data(collection, df)

        # 8. Contrôle de la collection après migration
        mongo_info = check_collection(collection, colonnes_ref=df.columns.tolist())

        # 9. Compare le dataframe et la collection
        test_compare(df_info, mongo_info)


    except Exception as e:
        logging.error(f"❌ Erreur du script: {e}")
        sys.exit(1)
    finally:
        try:
            # 10. Fermeture de la connection MongoDB
            client.close()
            logging.info("Connexion MongoDB fermée")
        except Exception:
            pass

if __name__ == "__main__":
    main_run()