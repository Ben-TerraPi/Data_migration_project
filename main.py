import sys
from utils import connect_to_mongodb, load_csv_data, migrate_data


def main():
    print("Démarrage de la migration")
    
    # Connexion à MongoDB
    client = connect_to_mongodb()
    if not client:
        sys.exit(1)
    
    try:
        # Sélection de la base et collection (créées via l'interface Compass)
        db = client['datasolutech']
        collection = db['healthcare_dataset']

        # Chargement du fichier CSV
        csv_file = "dataset/healthcare_dataset.csv"  
        df = load_csv_data(csv_file)
        if df is None:
            sys.exit(1)
        
        # Migration des données
        migrate_data(collection, df)
        
        print("✅ Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur migration: {e}")
    finally:
        # Fermeture de la connexion
        client.close()


if __name__ == "__main__":
    main()