import os
from PIL import Image

def resize_single_image():
    # Dossiers source et destination
    source_folder = "C:/Users/pimpr/OneDrive/Desktop/Cours_Fac_GPhy/M2/Projet Annuel AREG TeC/Dockers_Fichiers/app/images"  # Remplace par le chemin du dossier source
    destination_folder = "C:/Users/pimpr/OneDrive/Desktop/Cours_Fac_GPhy/M2/Projet Annuel AREG TeC/Dockers_Fichiers/app/dimensions"  # Remplace par le dossier de sortie

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Lister les fichiers images dans le dossier source
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    # Vérifier qu'il y a des images
    if not files:
        print("Aucune image trouvée dans le dossier source.")
        return

    print("Images disponibles :")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    # Demander à l'utilisateur de sélectionner une image
    while True:
        try:
            choice = int(input("Entrez le numéro de l'image à redimensionner : "))
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                break
            else:
                print(f"Veuillez entrer un nombre entre 1 et {len(files)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Demander le facteur de redimensionnement
    while True:
        try:
            factor = float(input("Entrez un facteur de redimensionnement (ex: 0.5 pour réduire de moitié) : "))
            if factor > 0:
                break
            else:
                print("Le facteur doit être supérieur à 0.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Chemins pour les fichiers source et destination
    source_path = os.path.join(source_folder, selected_file)
    destination_path = os.path.join(destination_folder, f"resized_{selected_file}")

    # Redimensionner et sauvegarder l'image
    try:
        with Image.open(source_path) as img:
            new_width = int(img.width * factor)
            new_height = int(img.height * factor)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            resized_img.save(destination_path)
            print(f"✅ Image redimensionnée enregistrée : {destination_path}")
    except Exception as e:
        print(f"❌ Erreur avec l'image {selected_file} : {e}")

if __name__ == "__main__":
    resize_single_image()
