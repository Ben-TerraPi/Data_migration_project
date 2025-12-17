import kagglehub
import os

# Téléchargement dans le cache par défaut
path = kagglehub.dataset_download("prasad22/healthcare-dataset")
print("Dataset téléchargé dans:", path)

# Creation du dossier de destination à la racine du projet
project_root = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(project_root, "dataset")
os.makedirs(dataset_dir, exist_ok=True)

# Copie du fichier
for filename in os.listdir(path):
    src_file = os.path.join(path, filename)
    dst_file = os.path.join(dataset_dir, filename)
    
    with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
        dst.write(src.read())
    
    print(f"Fichier copié: {filename}")

print("Dataset disponible dans:", dataset_dir)