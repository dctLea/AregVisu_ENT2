import tkinter as tk
from tkinter import messagebox
from PIL import Image
import matplotlib.pyplot as plt
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

def fetch_data_from_db():
    global df
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        all_data = {}
        
        # Charger les données de chaque table
        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = [col[0] for col in cursor.fetchall()]
            cursor.execute(f"SELECT * FROM {table}")
            all_data[table] = pd.DataFrame(cursor.fetchall(), columns=columns)
        
        # Optionnel: Vous pouvez enregistrer ou utiliser "all_data" pour une analyse graphique ou autre traitement
        return all_data

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def handle_query(query):
    try:
        with mysql.connector.connect(**db_config) as conn:
            cursor = conn.cursor(dictionary=True)

            if "table" in query.lower():
                cursor.execute("SHOW TABLES")
                tables = [table[f'Tables_in_{db_config["database"]}'] for table in cursor.fetchall()]
                messagebox.showinfo("Résultat", f"Tables disponibles : {', '.join(tables)}")

            elif "contenu de" in query.lower():
                table_name = query.lower().split("contenu de")[-1].strip()
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [col["Field"] for col in cursor.fetchall()]
                cursor.execute(f"SELECT * FROM {table_name}")
                results = cursor.fetchall()
                formatted_results = "\n".join([", ".join(str(row[col]) for col in columns) for row in results])
                messagebox.showinfo("Résultat", f"Contenu de la table {table_name} :\n{formatted_results}")

            elif "coordonnées" in query.lower():
                cursor.execute("SELECT entite, x, y FROM entites")
                results = cursor.fetchall()
                formatted_results = "\n".join([f"{row['entite']} : ({row['x']}, {row['y']})" for row in results])
                messagebox.showinfo("Résultat", f"Coordonnées des entités :\n{formatted_results}")

            else:
                messagebox.showinfo("Résultat", "Je ne comprends pas cette question.")

    except mysql.connector.Error as e:
        messagebox.showerror("Erreur Base de Données", f"Erreur lors de l'interrogation : {e}")

def show_text_mode():
    clear_frame()
    text_label = tk.Label(main_frame, text="Mode Texte : Tapez votre question sur les entités ou la base de données", font=("Arial", 12))
    text_label.pack(pady=10)

    # Zone de saisie de texte
    question_entry = tk.Entry(main_frame, width=50)
    question_entry.pack(pady=10)

    # Bouton pour soumettre la question
    submit_button = tk.Button(main_frame, text="Soumettre", 
                              command=lambda: handle_query(question_entry.get()))
    submit_button.pack()

def show_graphic_mode():
    clear_frame()
    graphic_label = tk.Label(main_frame, text="Mode Graphique : Visualisation en cours", font=("Arial", 12))
    graphic_label.pack(pady=10)
    render_graphic()

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
    plt.show()

def show_vocal_mode():
    clear_frame()
    vocal_label = tk.Label(main_frame, text="Mode Vocal : Parlez pour poser une question", font=("Arial", 12))
    vocal_label.pack(pady=10)
    record_button = tk.Button(main_frame, text="Démarrer l'enregistrement", 
                               command=start_voice_recognition)
    record_button.pack()

def start_voice_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Reconnaissance Vocale", "Posez votre question...")
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language="fr-FR")
            messagebox.showinfo("Votre question", query)

            # Pré-défini des questions et des réponses
            if "entités" in query.lower():
                handle_query("Quel est le contenu de la table entités ?")
            elif "coordonnées" in query.lower():
                handle_query("Quelles sont les coordonnées des entités ?")
            elif "table" in query.lower():
                handle_query("Quelles sont les tables disponibles ?")
            else:
                messagebox.showinfo("Résultat", "Désolé, je n'ai pas compris votre question.")

        except sr.UnknownValueError:
            messagebox.showerror("Erreur", "Je n'ai pas compris. Essayez encore.")
        except sr.RequestError:
            messagebox.showerror("Erreur", "Problème avec le service de reconnaissance vocale.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

# Interface principale
root = tk.Tk()
root.title("Tableau de Bord d'Interrogation")
root.geometry("600x400")

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

# Charger les données de la base de données au démarrage
fetch_data_from_db()

# Démarrer l'application
root.mainloop()
