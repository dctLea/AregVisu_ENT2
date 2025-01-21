import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import pandas as pd
import os
import speech_recognition as sr

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

# Fonction pour gérer les requêtes texte
def handle_query(query):
    try:
        with mysql.connector.connect(**db_config) as conn:
            cursor = conn.cursor(dictionary=True)

            if "table" in query.lower():
                cursor.execute("SHOW TABLES")
                tables = [table[f'Tables_in_{db_config["database"]}'] for table in cursor.fetchall()]
                result_label.config(text=f"Tables disponibles : {', '.join(tables)}")

            elif "contenu de" in query.lower():
                table_name = query.lower().split("contenu de")[-1].strip()
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [col["Field"] for col in cursor.fetchall()]
                cursor.execute(f"SELECT * FROM {table_name}")
                results = cursor.fetchall()
                formatted_results = "\n".join([", ".join(str(row[col]) for col in columns) for row in results])
                result_label.config(text=f"Contenu de la table {table_name} :\n{formatted_results}")

            elif "coordonnées" in query.lower():
                cursor.execute("SELECT entite, x, y FROM entites")
                results = cursor.fetchall()
                formatted_results = "\n".join([f"{row['entite']} : ({row['x']}, {row['y']})" for row in results])
                result_label.config(text=f"Coordonnées des entités :\n{formatted_results}")

            else:
                result_label.config(text="Je ne comprends pas cette question.")

    except mysql.connector.Error as e:
        result_label.config(text=f"Erreur lors de l'interrogation : {e}")

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
    record_button = tk.Button(main_frame, text="Démarrer l'enregistrement", 
                               command=start_voice_recognition)
    record_button.pack()

# Fonction de reconnaissance vocale
def start_voice_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            result_label.config(text="Posez votre question...")
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language="fr-FR")
            result_label.config(text=f"Votre question : {query}")

            if "entités" in query.lower():
                handle_query("Quel est le contenu de la table entités ?")
            elif "coordonnées" in query.lower():
                handle_query("Quelles sont les coordonnées des entités ?")
            elif "table" in query.lower():
                handle_query("Quelles sont les tables disponibles ?")
            else:
                result_label.config(text="Désolé, je n'ai pas compris votre question.")

        except sr.UnknownValueError:
            result_label.config(text="Je n'ai pas compris. Essayez encore.")
        except sr.RequestError:
            result_label.config(text="Problème avec le service de reconnaissance vocale.")
        except Exception as e:
            result_label.config(text=f"Une erreur s'est produite : {str(e)}")

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