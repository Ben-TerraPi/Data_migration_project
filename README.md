## Context

Ce projet a été réalisé dans le cadre de mon parcours de formation 'Data Engineer' avec OpenClassrooms.

Titre du projet :

`Maintenez et documentez un système de stockage des données sécurisé et performant`

Ce projet consiste à :

- Extraire et nettoyer un jeu de données médicales au format CSV (issu de Kaggle).
- Migrer ces données vers une base de données **MongoDB** à l’aide d’un script **Python**, en garantissant la performance et la sécurité du stockage.
- Containeriser l’application avec **Docker** pour faciliter son déploiement et sa scalabilité.

---

# Extraction et migration vers MongoDB

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

## Fonctionnement par étape du script `src/main.py`

Nous retrouvons dans le fichier `src/utils.py` toutes les fonctions utilisées à chaque étapes du script. 
Un logger est de plus configuré pour s'assurer du bon déroulement de ce script.

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

### 2. Chargement du CSV dans un DataFrame

Pour manipuler les données avant leur migration.

### 3. Nettoyage du DataFrame

Un nettoyage est effectué pour corriger la « casse irrégulière » des noms et la suppression des doublons.

### 4. Contrôle du DataFrame avant migration

Ici la fonction `check_dataframe` va servir à afficher dans les logs le nom et le type des différentes colonnes. Et dans un deuxième temps elle sera utilisé pour comparer les données après migration.

`df_info = check_dataframe(df)`

### 5. Création database et collection MongoDB

Une connection est ajouté et ouverte en utilisant le port local par défaut:

```sh
def connect_to_mongodb():
    """
    Connexion à MongoDB
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    logging.info("Connexion MongoDB")
    return client
```

Avec MongoDB, nous n’avons pas besoin d’initialiser la base de données ou la collection en amont.
MongoDB cré automatiquement la base `datasolutech` et la collection `healthcare_dataset` lors de la première insertion de documents si elles n’existent pas déjà.

```sh
client = connect_to_mongodb()
if not client:
    sys.exit(1)
db = client['datasolutech']
collection = db['healthcare_dataset']
```

#### Schéma de la collection `healthcare_dataset`

| Champ                | Type      | Description                        |
|----------------------|-----------|------------------------------------|
| _id                  | ObjectId  | Identifiant unique MongoDB         |
| Name                 | string    | Nom du patient                     |
| Age                  | int       | Âge                                |
| Gender               | string    | Sexe                               |
| Blood Type           | string    | Groupe sanguin                     |
| Medical Condition    | string    | Pathologie principale              |
| Date of Admission    | string    | Date d'admission (YYYY-MM-DD)      |
| Doctor               | string    | Médecin référent                   |
| Hospital             | string    | Hôpital                            |
| Insurance Provider   | string    | Assurance                          |
| Billing Amount       | float     | Montant facturé                    |
| Room Number          | int       | Numéro de chambre                  |
| Admission Type       | string    | Type d'admission                   |
| Discharge Date       | string    | Date de sortie (YYYY-MM-DD)        |
| Medication           | string    | Médication principale              |
| Test Results         | string    | Résultat des tests                 |

#### Exemple de document

```sh
{
  "_id": "ObjectId('...')",
  "Name": "Elizabeth Jackson",
  "Age": 30,
  "Gender": "Female",
  "Blood Type": "B-",
  "Medical Condition": "Cancer",
  "Date of Admission": "2024-01-31",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.28,
  "Room Number": 328,
  "Admission Type": "Urgent",
  "Discharge Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
```

### 6. Vider la collection avant migration

Cette étape avec la commande `.delete_many({})` de la librairie pymongo est une sécurité pour éviter les doublons si le script est exécuté plusieurs fois.

### 7. Migration des données

La migration des données est effectuée avec cette fonction:

```sh
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
```

### 8. Contrôle de la collection après migration

Dans le même principe que l'étape 4 la fonction `check_collection` vérifie l'intégrité de la collection MongoDB après migration. Elle retourne un dictionnaire avec colonnes, types, doublons, valeurs manquantes qui sera affiché dans les logs.

`mongo_info = check_collection(collection, colonnes_ref=df.columns.tolist())`

### 9. Compare le dataframe et la collection

Grâce à la fonction `test_compare` nous reprenons les informations de l'étape 4 et 8 pour comparaison, les résultats sont synthétisés dans les logs.

### 10. Fermeture de la connection MongoDB

Utilisation de la méthode `.close()` de la librairie pymongo.

---

# Conteneurisation avec Docker

## Fonctionnement

**Docker** permet d’exécuter l'application dans un environnement isolé, appelé « conteneur », qui contient tout ce dont elle a besoin (Python, dépendances, code…).

**Docker Compose** permet de lancer plusieurs conteneurs qui communiquent ensemble (ici : un pour MongoDB, un pour le script Python).

## Structure des fichiers importants

- **Dockerfile** : décrit comment construire l’image de l'application Python.
- **docker-compose.yml** : décrit comment lancer les différents conteneurs (MongoDB + application).
- **requirements.txt** : liste les librairies Python à installer dans le conteneur.
- **main.py** : Le script python de l'application

## Utilisation de l'application

### Installation de Docker 🐳

[Docker Desktop](https://www.docker.com/products/docker-desktop/) (windows/mac)
[Docker Engine](https://docs.docker.com/engine/install/) (Linux)

### Cloner le projet depuis Github

```sh
git clone https://github.com/Ben-TerraPi/Data_migration_project.git
cd Data_migration_project
```

### Lancer les conteneurs avec Docker Compose

```sh
docker-compose up --build
```

### Arrêter et nettoyer Docker

```sh
docker-compose down
```

---

# Base de données MongoDB

Pour cette partie du projet, deux utilisateurs avec des rôles distincts sont créés.

1. Administrateur avec tous les droits :

l'utilisateur `root` est créé automatiquement par MongoDB grâce aux variables d’environnement dans le `docker-compose.yml`.

Connexion avec ce rôle:

```sh
mongodb://root:root@localhost:27018
```

2. Utilisateur en lecture seule :

L'utilisateur `user` est créé dans le script avec un rôle limité.

```sh
# Création d'un utilisateur lecture seule
mongo_user = os.getenv("MONGO_USER", "user")
mongo_user_pwd = os.getenv("MONGO_USER_PASSWORD", "user")
db.command("createUser", mongo_user, pwd=mongo_user_pwd, roles=[{"role": "read", "db": "datasolutech"}])
```

Connexion avec ce rôle:

```sh
mongodb://user:user@localhost:27018/datasolutech
```

## ⚠️ Hashage des mots de passe ⚠️

A des fins pédagogiques des mots de passes simples sont en clair sur ce projet mais une bonne pratique est d'utiliser des variables d'environnement avec un fichier `.env` non versionné en l'ajoutant au fichier `.gitignore`.

---

# 📚 Ressources utiles

- [MongoDB University](https://learn.mongodb.com/) - Apprendre à utiliser MongoDB.
- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/) - Documentation pour utiliser MongoDB avec Python.
- [Docker Compose - Guide officiel](https://docs.docker.com/compose/)
- [Formation OpenClassrooms - Docker](https://openclassrooms.com/fr/courses/8431896-optimisez-votre-deploiement-en-creant-des-conteneurs-avec-docker)