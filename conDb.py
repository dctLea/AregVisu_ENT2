from PIL import Image
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import os

# Connexion à la base de données
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "AregTec",
    "database": "AregTec_Drupal"
}

# Connexion à la base de données avec gestion de la connexion
with mysql.connector.connect(**db_config) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT entite, x, y, relie_a, nom_image FROM entites")
    data = cursor.fetchall()

# Transformer les résultats en DataFrame
df = pd.DataFrame(data, columns=["entite", "x", "y", "relie_a", "nom_image"])

# Dossier des images
script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, "dimensions")

# Calculer les limites des axes
x_min, x_max = df['x'].min() - 10, df['x'].max() + 10
y_min, y_max = df['y'].min() - 10, df['y'].max() + 10

# Créer la figure
fig, ax = plt.subplots(figsize=(20, 12))

# Cache des images pour éviter les rechargements répétés
image_cache = {}

# Placer les images avec transformations
for _, row in df.iterrows():
    x, y = row['x'], row['y']
    image_path = os.path.join(image_dir, f"resized_{row['nom_image']}.png")

    if os.path.exists(image_path):
        if row['nom_image'] not in image_cache:
            img = Image.open(image_path)
            img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT).convert("RGBA")
            image_cache[row['nom_image']] = img
        img = image_cache[row['nom_image']]

        img_width, img_height = img.size
        ax.imshow(img, extent=(x - img_width / 2, x + img_width / 2, y - img_height / 2, y + img_height / 2), zorder=1)

# Définir les limites des axes
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Inverser l'axe y
ax.invert_yaxis()

# Configurer le graphique
ax.set_xlabel("x (en milliers)")
ax.set_ylabel("y (en milliers)")
ax.set_title("Graphique des entités avec images ajustées")
ax.grid(True, linestyle='--', alpha=0.6)

# Variables pour gérer le panning
press = None  # Position initiale du clic
last_x = None
last_y = None
move_factor = 0.01  # Sensibilité du mouvement 

# Fonction de zoom avec molette de la souris
def on_scroll(event):
    scale_factor = 1.2  # Facteur de zoom : > 1 pour zoom avant, < 1 pour zoom arrière
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    x_range = (x_max - x_min) * 0.5
    y_range = (y_max - y_min) * 0.5
    
    # Obtenir la position du curseur dans les coordonnées des axes
    mouse_x, mouse_y = ax.transData.inverted().transform([event.x, event.y])
    
    x_center = mouse_x
    y_center = mouse_y

    # Zoom avant
    if event.button == 'up':
        new_x_range = x_range / scale_factor
        new_y_range = y_range / scale_factor
    # Zoom arrière
    elif event.button == 'down':
        new_x_range = x_range * scale_factor
        new_y_range = y_range * scale_factor
    else:
        return

    ax.set_xlim([x_center - new_x_range, x_center + new_x_range])
    ax.set_ylim([y_center - new_y_range, y_center + new_y_range])
    fig.canvas.draw_idle()

# Fonction pour déplacer le graphique (panning)
def on_press(event):
    global press, last_x, last_y
    press = (event.x, event.y)
    last_x, last_y = event.xdata, event.ydata

def on_motion(event):
    global press, last_x, last_y
    if press is not None:
        dx = event.x - press[0]
        dy = event.y - press[1]
        
        # Appliquer le facteur de réduction pour le panning
        dx *= move_factor
        dy *= move_factor
        
        # Inverser les directions des mouvements (pour la droite-gauche et haut-bas)
        dx = dx 
        dy = -dy  
        
        # Calculer le déplacement en coordonnées des données
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        x_range = (x_max - x_min)
        y_range = (y_max - y_min)
        
        # Calculer les nouveaux bords
        ax.set_xlim([x_min - dx * (x_range / fig.get_figwidth()), x_max - dx * (x_range / fig.get_figwidth())])
        ax.set_ylim([y_min + dy * (y_range / fig.get_figheight()), y_max + dy * (y_range / fig.get_figheight())])
        
        fig.canvas.draw_idle()
        press = (event.x, event.y)

def on_release(event):
    global press
    press = None

# Connecter les événements de souris
fig.canvas.mpl_connect('scroll_event', on_scroll)
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Afficher le graphique
plt.show()
