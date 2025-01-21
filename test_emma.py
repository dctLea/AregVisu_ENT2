import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import pandas as pd
import os
import difflib

# Configuration de la base de données
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "AregTec",
    "database": "AregTec_Drupal"
}

# Initialisation des données globales
df = None
image_positions = []

# Fonction pour récupérer les données de la base de données
def fetch_data_from_db():
    global df
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT entite, x, y, relie_a, nom_image FROM entites")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["entite", "x", "y", "relie_a", "nom_image"])

# Fonction pour nettoyer le cadre principal
def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def get_entities_from_db():
    """
    Récupère les noms d'entités uniques depuis la table `entites`.
    """
    try:
        with mysql.connector.connect(**db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT entite FROM entites")
            entities = [row[0] for row in cursor.fetchall()]
            return entities
    except mysql.connector.Error as e:
        messagebox.showerror("Erreur Base de Données", f"Erreur lors de l'accès aux entités : {e}")
        return []

def find_closest_entity(user_input, entity_list):
    """
    Recherche l'entité la plus proche dans la liste (gestion des fautes et majuscules).
    """
    matches = difflib.get_close_matches(user_input, entity_list, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Fonction pour gérer les requêtes texte
def handle_query(query):
    """
    Recherche l'entité correspondant à une question utilisateur.
    """
    try:
        # Charger les mots-clés dynamiquement
        entity_list = get_entities_from_db()

        # Identifier le mot-clé le plus proche dans la requête
        words = query.split()
        detected_entity = None

        for word in words:
            closest_match = find_closest_entity(word.lower(), [e.lower() for e in entity_list])
            if closest_match:
                detected_entity = closest_match
                break

        if detected_entity:
            # Rechercher l'entité dans la base de données
            with mysql.connector.connect(**db_config) as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT x, y, relie_a, nom_image FROM entites WHERE LOWER(entite) = %s", (detected_entity,))
                result = cursor.fetchone()

                if result:
                    x, y, relie_a, nom_image = result["x"], result["y"], result["relie_a"], result["nom_image"]
                    messagebox.showinfo(
                        "Résultat",
                        f"Entité trouvée : {detected_entity.capitalize()}\nCoordonnées : ({x}, {y})\nRelie à : {relie_a}"
                    )
                    highlight_entity_on_canvas(detected_entity, x, y, relie_a, nom_image)
                else:
                    messagebox.showinfo("Résultat", f"L'entité '{detected_entity}' n'a pas été trouvée dans la base.")
        else:
            messagebox.showinfo("Résultat", "Aucune entité correspondante trouvée dans votre question.")

    except mysql.connector.Error as e:
        messagebox.showerror("Erreur Base de Données", f"Erreur lors de l'interrogation : {e}")


# Mode texte
def show_text_mode():
    clear_frame()
    text_label = tk.Label(main_frame, text="Mode Texte : Tapez votre question sur les entités ou la base de données", font=("Arial", 12))
    text_label.pack(pady=10)

    question_entry = tk.Entry(main_frame, width=50)
    question_entry.pack(pady=10)

    submit_button = tk.Button(main_frame, text="Soumettre", 
                              command=lambda: handle_query(question_entry.get()))
    submit_button.pack()


def highlight_entity_on_canvas(entity_name, x, y, relie_a, image_name):
    """
    Affiche une entité sur un graphique Matplotlib avec surbrillance.
    """
    fig, ax = plt.subplots()

    # Exemple de visualisation avec des coordonnées
    ax.scatter([x], [y], c='red', s=200, label=f"Entité : {entity_name}")
    ax.annotate(entity_name, (x, y), textcoords="offset points", xytext=(10, 10), ha='center', fontsize=10)
    
    # Ajouter des détails
    if relie_a:
        ax.text(x, y - 10, f"Relie à : {relie_a}", fontsize=8, color='blue')
    
    plt.title(f"Surbrillance de {entity_name}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.legend()
    plt.show()


# Mode graphique
def show_graphic_mode():
    clear_frame()
    graphic_label = tk.Label(main_frame, text="Mode Graphique : Interagissez avec le graphe", font=("Arial", 12))
    graphic_label.pack(pady=10)
    render_graphic()

# Fonction pour afficher le graphique interactif
def render_graphic():
    global df, image_positions

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, "dimensions")
    x_min, x_max = df['x'].min() - 10, df['x'].max() + 10
    y_min, y_max = df['y'].min() - 10, df['y'].max() + 10

    fig, ax = plt.subplots(figsize=(12, 8))
    image_cache = {}

    image_positions.clear()
    for _, row in df.iterrows():
        x, y = row['x'], row['y']
        image_path = os.path.join(image_dir, f"resized_{row['nom_image']}.png")
        if os.path.exists(image_path):
            if row['nom_image'] not in image_cache:
                img = Image.open(image_path).rotate(180).transpose(Image.FLIP_LEFT_RIGHT).convert("RGBA")
                image_cache[row['nom_image']] = img
            img = image_cache[row['nom_image']]
            img_width, img_height = img.size
            ax.imshow(img, extent=(x - img_width / 2, x + img_width / 2, y - img_height / 2, y + img_height / 2))
            image_positions.append((x - img_width / 2, x + img_width / 2, y - img_height / 2, y + img_height / 2, row))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.invert_yaxis()
    ax.set_title("Graphique des entités avec images")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Ajout des événements interactifs
    def on_zoom(event):
        base_scale = 1.1
        if event.button == 'up':  # Molette vers l'avant
            scale_factor = base_scale
        elif event.button == 'down':  # Molette vers l'arrière
            scale_factor = 1 / base_scale
        else:  # Aucun zoom
            return

        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        xdata = event.xdata  # Coordonnée x sous le curseur
        ydata = event.ydata  # Coordonnée y sous le curseur

        # Calcul des nouvelles limites
        new_xlim = [
            xdata - (xdata - cur_xlim[0]) / scale_factor,
            xdata + (cur_xlim[1] - xdata) / scale_factor,
        ]
        new_ylim = [
            ydata - (ydata - cur_ylim[0]) / scale_factor,
            ydata + (cur_ylim[1] - ydata) / scale_factor,
        ]

        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        canvas.draw()

    def on_pan(event):
        if event.button != 1:  # Se déplace uniquement avec clic gauche
            return

        if not hasattr(on_pan, "press_event"):
            on_pan.press_event = None

        if event.name == 'button_press_event':
            on_pan.press_event = event
        elif event.name == 'motion_notify_event' and on_pan.press_event is not None:
            dx = event.xdata - on_pan.press_event.xdata
            dy = event.ydata - on_pan.press_event.ydata
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            ax.set_xlim([cur_xlim[0] - dx, cur_xlim[1] - dx])
            ax.set_ylim([cur_ylim[0] - dy, cur_ylim[1] - dy])
            canvas.draw()
            on_pan.press_event = event  # Mise à jour de l'événement
        elif event.name == 'button_release_event':
            on_pan.press_event = None

    canvas.mpl_connect("scroll_event", on_zoom)
    canvas.mpl_connect("button_press_event", on_pan)
    canvas.mpl_connect("motion_notify_event", on_pan)
    canvas.mpl_connect("button_release_event", on_pan)


# Mode vocal
def show_vocal_mode():
    clear_frame()
    vocal_label = tk.Label(main_frame, text="Mode Vocal : Parlez pour poser une question", font=("Arial", 12))
    vocal_label.pack(pady=10)
    record_button = tk.Button(main_frame, text="Démarrer l'enregistrement")
    record_button.pack()

# Fonction de reconnaissance vocale

# Interface principale
root = tk.Tk()
root.title("Tableau de Bord d'Interrogation")
root.geometry("800x600")

# Titre
title_label = tk.Label(root, text="Tableau de Bord d'Interrogation", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Boutons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

text_button = tk.Button(button_frame, text="Mode Texte", command=show_text_mode, width=15, bg="lightgreen")
text_button.grid(row=0, column=0, padx=10)

graphic_button = tk.Button(button_frame, text="Mode Graphique", command=show_graphic_mode, width=15, bg="lightblue")
graphic_button.grid(row=0, column=1, padx=10)

vocal_button = tk.Button(button_frame, text="Mode Vocal", command=show_vocal_mode, width=15, bg="lightcoral")
vocal_button.grid(row=0, column=2, padx=10)

# Zone principale
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Zone de résultat
result_label = tk.Label(root, text="", font=("Arial", 12), fg="darkblue")
result_label.pack(pady=10)

# Charger les données de la base de données au démarrage
fetch_data_from_db()

# Afficher le graphe par défaut
show_graphic_mode()

# Démarrer l'application
root.mainloop()