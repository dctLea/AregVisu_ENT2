import cv2
import mysql.connector
from datetime import datetime
from jinja2 import Template

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AregTec",  # Remplace par ton mot de passe
    database="AregTec_Drupal"
)
cursor = conn.cursor()

# Charger les entités depuis la table 'entites'
cursor.execute("SELECT nom_image, x, y FROM entites")
entites = cursor.fetchall()

# Afficher les entités pour déboguer
print("Entités récupérées depuis la base de données:")
for entite in entites:
    print(f"Image: {entite[0]}, Coordonnées: ({entite[1]}, {entite[2]})")

# Référence du squelette
squelette_path = 'C:/DrupalDocker/squelette chien.png'
img_squelette = cv2.imread(squelette_path, cv2.IMREAD_COLOR)
if img_squelette is None:
    print("Erreur : Image de squelette introuvable.")
    exit()

# Paramètres et initialisation
threshold = 25  # Augmenter légèrement le seuil pour capturer plus de zones autour de l'os
output_html_path = 'C:/Projet/AregVisu_ENT2/resultats_comparaison.html'
resultats = []

# Comparaison des images
image_dir = 'C:/DrupalDocker/Squelette _structures de base/'

# Fonction pour afficher les informations au clic sur l'image
def afficher_info(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Vérifier si l'événement est un clic gauche
        print(f"Clic détecté à: ({x}, {y})")  # Affichage des coordonnées du clic
        # Parcourir les entités et vérifier si le clic est dans la zone de l'os
        for entite in entites:
            nom_image = entite[0]
            # Vérifier si le clic est proche des coordonnées de l'entité
            if entite[1] - threshold <= x <= entite[1] + threshold and entite[2] - threshold <= y <= entite[2] + threshold:
                # Afficher le nom et les coordonnées de l'os
                info_text = f"Nom de l'os : {nom_image}, Coordonnées : ({entite[1]}, {entite[2]})"
                print(info_text)  # Affichage dans la console
                
                # Ajouter à la liste des résultats pour affichage dans le tableau HTML
                resultats.append({
                    "image_name": nom_image,
                    "coordonnees": f"({entite[1]}, {entite[2]})",
                    "date_comparaison": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # Afficher les informations sur l'image
                img_with_text = img_squelette.copy()  # Faire une copie pour ne pas altérer l'image originale
                cv2.putText(img_with_text, info_text, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.imshow("Squelette", img_with_text)  # Affichage avec texte
                break  # Sortir de la boucle dès que l'entité correspondante est trouvée

# Afficher l'image et attendre un clic
cv2.imshow("Squelette", img_squelette)
cv2.setMouseCallback("Squelette", afficher_info)

cv2.waitKey(0)  # Attendre que l'utilisateur appuie sur une touche pour fermer la fenêtre
cv2.destroyAllWindows()

# Vérification de la liste des résultats après les clics
if resultats:
    print("Résultats capturés :")
    for resultat in resultats:
        print(resultat)
else:
    print("Aucun clic effectué ou les résultats ne sont pas capturés.")


# Générer un fichier HTML avec Jinja2
template_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Résultats des Clics sur l'Image</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: center; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h1>Informations des Os Cliqués</h1>
    <table>
        <thead>
            <tr>
                <th>Nom de l'os</th>
                <th>Coordonnées</th>
                <th>Date du Clic</th>
            </tr>
        </thead>
        <tbody>
            {% for resultat in resultats %}
            <tr>
                <td>{{ resultat.image_name }}</td>
                <td>{{ resultat.coordonnees }}</td>
                <td>{{ resultat.date_comparaison }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

template = Template(template_html)
html_output = template.render(resultats=resultats)

# Sauvegarder le fichier HTML
if resultats:
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Résultats enregistrés dans : {output_html_path}")
else:
    print("Aucun clic effectué, donc aucun fichier HTML généré.")
