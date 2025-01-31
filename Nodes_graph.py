import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd


# Détails de la connexion (ajuste ces informations)
host = "localhost"         # L'hôte de ta base de données, souvent localhost
user = "root"              # Ton nom d'utilisateur MySQL (par exemple "root")
password = "AregTec"  # Ton mot de passe MySQL
database = "AregTec_Drupal"   # Le nom de ta base de données

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
)

# Vérifier si la connexion est réussie
if conn.is_connected():
    print("Connexion réussie à la base de données")

# Créer un curseur pour exécuter des requêtes SQL
cursor = conn.cursor(dictionary=True)

# Exemple : Sélectionner toutes les entités de la table
query = "SELECT entite AS entité, X, Y, relie_a AS `relié à` FROM entites;"
cursor.execute(query)

# Récupérer les résultats
data = cursor.fetchall()

# Convertir les données en DataFrame
df = pd.DataFrame(data)

# Créer un dictionnaire pour mémoriser les coordonnées des entités
positions = {row['entité']: (row['X'], row['Y']) for _, row in df.iterrows()}

# Créer la figure et les axes
plt.figure(figsize=(12, 8))

# Tracer les points
for _, row in df.iterrows():
    x, y = row['X'], row['Y']
    plt.scatter(x, y, color='blue', zorder=5)
    plt.text(x, y, row['entité'], fontsize=8, ha='right', zorder=10)

# Tracer les liaisons
for _, row in df.iterrows():
    if row['relié à'] in positions:
        x1, y1 = positions[row['entité']]
        x2, y2 = positions[row['relié à']]
        plt.plot([x1, x2], [y1, y2], color='black', linewidth=0.8, zorder=1)

# Inverser l'axe Y pour corriger l'inversion
plt.gca().invert_yaxis()

# Configurer le graphique
plt.xlabel("X (en milliers)")
plt.ylabel("Y (en milliers)")
plt.title("Graphique des entités et liaisons")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()


# Fermer la connexion et le curseur
cursor.close()
conn.close()
