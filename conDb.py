from PIL import Image
import matplotlib.pyplot as plt
import os
import mysql.connector
import pandas as pd

# Connexion à la base de données MySQL
db_config = {
    "host": "localhost",    # Adresse du serveur MySQL
    "user": "root",         # Nom d'utilisateur
    "password": "AregTec",  # Mot de passe
    "database": "AregTec_Drupal"  # Nom de la base de données
}

# Créer la connexion et récupérer les données
def fetch_data_from_db():
    # Ouverture de la connexion
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # Exécuter la requête SQL pour récupérer les données
    query = "SELECT entite, x, y, relie_a, nom_image FROM entites"
    cursor.execute(query)
    # Récupérer les résultats
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Transformer les données en DataFrame
data = fetch_data_from_db()
df = pd.DataFrame(data, columns=["entite", "x", "y", "relie_a", "nom_image"])

# Création du dictionnaire pour les positions des entités
positions = {row["entite"]: (row["x"], row["y"]) for _, row in df.iterrows()}

# Dossier contenant les images
script_dir = os.path.dirname(os.path.abspath(_file_))
image_dir = os.path.join(script_dir, "Squelette _structures de base")

# Déterminer les limites du graphique
x_min, x_max = df['x'].min() - 10, df['x'].max() + 10
y_min, y_max = df['y'].min() - 10, df['y'].max() + 10

# Créer la figure
fig, ax = plt.subplots(figsize=(20, 12))

# Prétraiter les images pour éviter de recharger à chaque itération
image_cache = {}

# Placer les images
for _, row in df.iterrows():
    x, y = row['x'], row['y']
    image_path = os.path.join(image_dir, f"{row['nom_image']}.png")

    if os.path.exists(image_path):
        if row['nom_image'] not in image_cache:
            # Ouvrir et prétraiter l'image si elle n'est pas dans le cache
            img = Image.open(image_path).rotate(180).transpose(Image.FLIP_LEFT_RIGHT).convert("RGBA")
            img_width, img_height = img.size
            image_cache[row['nom_image']] = (img, img_width, img_height)

        img, img_width, img_height = image_cache[row['nom_image']]

        # Placer l'image sur le graphique sans redimensionner
        ax.imshow(img, extent=(x - img_width / 2, x + img_width / 2, y - img_height / 2, y + img_height / 2), zorder=1)
    else:
        print(f"Image non trouvée pour {row['nom_image']}")

# Définir les limites initiales des axes
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Inverser l'axe y pour correspondre aux coordonnées
ax.invert_yaxis()

# Configurer le graphique
ax.set_xlabel("x (en milliers)")
ax.set_ylabel("y (en milliers)")
ax.set_title("Graphique des entités avec images ajustées")
ax.grid(True, linestyle='--', alpha=0.6)

# Variables pour gérer le panning et le zoom ciblé
press = None  # Position initiale du clic
last_x = None
last_y = None

# Facteur de réduction pour le panning (réduire la sensibilité)
move_factor = 0.01
zoom_factor = 1.2  # Facteur de zoom

# Fonction pour zoomer/dézoomer avec la molette de la souris
def on_scroll(event):
    global x_min, x_max, y_min, y_max
    scale_factor = 1.2
    x_range = (x_max - x_min) * 0.5
    y_range = (y_max - y_min) * 0.5
    x_center, y_center = (x_max + x_min) / 2, (y_max + y_min) / 2

    if event.button == 'up':
        new_x_range = x_range / scale_factor
        new_y_range = y_range / scale_factor
    elif event.button == 'down':
        new_x_range = x_range * scale_factor
        new_y_range = y_range * scale_factor
    else:
        return

    ax.set_xlim([x_center - new_x_range, x_center + new_x_range])
    ax.set_ylim([y_center - new_y_range, y_center + new_y_range])
    fig.canvas.draw_idle()

# Fonction pour déplacer le graphique
def on_press(event):
    global press, last_x, last_y
    press = (event.x, event.y)
    last_x, last_y = event.xdata, event.ydata

def on_motion(event):
    global press, last_x, last_y
    if press is not None:
        dx = event.x - press[0]
        dy = event.y - press[1]
        dx *= move_factor
        dy *= move_factor
        dx = dx
        dy = -dy
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        x_range = (x_max - x_min)
        y_range = (y_max - y_min)
        ax.set_xlim([x_min - dx * (x_range / fig.get_figwidth()), x_max - dx * (x_range / fig.get_figwidth())])
        ax.set_ylim([y_min + dy * (y_range / fig.get_figheight()), y_max + dy * (y_range / fig.get_figheight())])
        fig.canvas.draw_idle()
        press = (event.x, event.y)

def on_release(event):
    global press
    press = None

# Fonction de zoom sur un point spécifique
def on_click(event):
    global x_min, x_max, y_min, y_max

    # Si on clique sur un des os (entités), on zoom sur cet os
    clicked_x, clicked_y = event.xdata, event.ydata
    zoom_range_x = (x_max - x_min) * 0.2  # Ajuster cette valeur pour définir le niveau de zoom
    zoom_range_y = (y_max - y_min) * 0.2

    # Appliquer un zoom centré sur le point cliqué
    ax.set_xlim([clicked_x - zoom_range_x, clicked_x + zoom_range_x])
    ax.set_ylim([clicked_y - zoom_range_y, clicked_y + zoom_range_y])

    fig.canvas.draw_idle()

# Connecter les événements de souris
fig.canvas.mpl_connect('scroll_event', on_scroll)
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('button_press_event', on_click)  # Ajouter l'événement de clic

# Afficher le graphique
plt.show()