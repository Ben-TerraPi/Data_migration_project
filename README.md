# Data_migration_project

## Context

Ce projet a été réalisé dans le cadre de mon parcours de formation 'Data Engineer' avec OpenClassrooms.

Ce projet intitulé `Maintenez et documentez un système de stockage des données sécurisé et performant`, consiste en une migraion de données issue d'un fichier csv vers une base de donnée MongoDB en se servant d'un script python puis ...

---

## 📌 MongoDB (Local)

Ce projet utilise **MongoDB** comme base de données NoSQL.

### 🛠 Installations
1. **MongoDB Community Server** :
   - Télécharger depuis [le site officiel](https://www.mongodb.com/try/download/community).

2. **Outils** :
   - [MongoDB Compass](https://www.mongodb.com/products/compass).
   - [Extension MongoDB pour VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) (pour manipuler la base directement depuis l'éditeur).

### 🐍 Utilisation avec Python
1. **Installer `pymongo`** :
```sh
pip install pymongo
```

---

## Création de la BDD et de sa collection

Cette partie a été effectué directement avec l'interface MongoDB Compass.

- Une nouvelle connection a été ajouté en utilisant le port local par défaut:
```sh
mongodb://localhost:27017
```

- Une fois la connection établie la database `datasolutech` et la collection `healthcare_dataset`  ont été créé.

---

## Récupération du CSV source

Pour ce projet un dataset regroupant des données médicales provenant de kaggle a été utilié, [lien](https://www.kaggle.com/datasets/prasad22/healthcare-dataset/data?select=healthcare_dataset.csv).

Dans le fichier 'dataset/data_import.py' nous retrouvons un script sommaire pour télécharger le csv dans le même dossier.

---

## 📚 Ressources utiles

- [MongoDB University](https://learn.mongodb.com/) - Apprendre à utiliser MongoDB.
- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/) - Documentation pour utiliser MongoDB avec Python.