# Data_migration_project

## Context

Ce projet a été réalisé dans le cadre de mon parcours de formation 'Data Engineer' avec OpenClassrooms.

Ce projet intitulé `Maintenez et documentez un système de stockage des données sécurisé et performant`, consiste en une migraion de données issue d'un fichier csv vers une base de donnée MongoDB en se servant d'un script python puis ...

---

## 🛠 Installations

### 🍃 MongoDB (Local)

Ce projet utilise **MongoDB** comme base de données NoSQL.

**MongoDB Community Server** :
   - Télécharger depuis [le site officiel](https://www.mongodb.com/try/download/community).

**Outils** :
   - [MongoDB Compass](https://www.mongodb.com/products/compass).
   - [Extension MongoDB pour VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) (pour manipuler la base directement depuis l'éditeur).

### 🐍 Utilisation avec Python
```sh
pip install pymongo
```

---

## Fonctionnement par étape du script `src/main.py`

Nous retrouvons dans le fichier `src/utils.py` les principales fonctions utilisées dans le script.

### 1. Récupération du CSV source

Pour ce projet un dataset regroupant des données médicales provenant de kaggle a été utilié, [lien](https://www.kaggle.com/datasets/prasad22/healthcare-dataset/data?select=healthcare_dataset.csv).

```sh
def import_data():
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
```

### 2. Création de la BDD MongoDB

Une connection est ajouté et ouverte en utilisant le port local par défaut:

```sh
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
```

---

## 📚 Ressources utiles

- [MongoDB University](https://learn.mongodb.com/) - Apprendre à utiliser MongoDB.
- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/) - Documentation pour utiliser MongoDB avec Python.