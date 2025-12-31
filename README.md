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

Nous retrouvons dans le fichier `src/utils.py` les fonctions ci-dessous utilisées dans le script. Un logger est de plus configuré pour s'assurer du bon fonctionnement de ce script.

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

### 5. Création database et collection MongoDB

Une connection est ajouté et ouverte en utilisant le port local par défaut:

```sh
def connect_to_mongodb():
    """
    Connexion à MongoDB
    """
    client = MongoClient('mongodb://localhost:27017/')
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

### Schéma de la collection `healthcare_dataset`

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

### Exemple de document

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
---

## 📚 Ressources utiles

- [MongoDB University](https://learn.mongodb.com/) - Apprendre à utiliser MongoDB.
- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/) - Documentation pour utiliser MongoDB avec Python.