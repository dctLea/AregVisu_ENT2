// Import des bibliothèques nécessaires
const mysql = require("mysql");
const fs = require("fs");
const path = require("path");
const { createCanvas, loadImage } = require("canvas"); // Pour le rendu des images

// Configuration de la base de données
const dbConfig = {
  host: "localhost",
  user: "root",
  password: "AregTec",
  database: "AregTec_Drupal",
};

// Connexion à la base de données et récupération des données
const connection = mysql.createConnection(dbConfig);

connection.connect((err) => {
  if (err) throw err;
  console.log("Connecté à la base de données !");

  const query = "SELECT entite, x, y, relie_a, nom_image FROM entites";
  connection.query(query, async (error, results) => {
    if (error) throw error;

    // Dossier des images
    const scriptDir = __dirname;
    const imageDir = path.join(scriptDir, "dimensions");

    // Calcul des limites des axes
    const xValues = results.map((row) => row.x);
    const yValues = results.map((row) => row.y);
    const xMin = Math.min(...xValues) - 10;
    const xMax = Math.max(...xValues) + 10;
    const yMin = Math.min(...yValues) - 10;
    const yMax = Math.max(...yValues) + 10;

    // Création du canvas
    const canvasWidth = 1600;
    const canvasHeight = 800;
    const canvas = createCanvas(canvasWidth, canvasHeight);
    const ctx = canvas.getContext("2d");

    // Dessiner les limites du graphe
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);
    ctx.strokeStyle = "black";
    ctx.strokeRect(0, 0, canvasWidth, canvasHeight);

    // Mise en cache des images
    const imageCache = {};

    // Placer les images
    for (const row of results) {
      const { x, y, nom_image } = row;
      const imagePath = path.join(imageDir, `resized_${nom_image}.png`);

      if (fs.existsSync(imagePath)) {
        if (!imageCache[nom_image]) {
          const img = await loadImage(imagePath);
          imageCache[nom_image] = img;
        }

        const img = imageCache[nom_image];
        const imgWidth = img.width / 2; // Ajuster la taille si nécessaire
        const imgHeight = img.height / 2;

        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(Math.PI); // Rotation de 180°
        ctx.scale(-1, 1); // Flip horizontal
        ctx.drawImage(img, -imgWidth / 2, -imgHeight / 2, imgWidth, imgHeight);
        ctx.restore();
      }
    }

    // Ajouter des axes
    ctx.strokeStyle = "grey";
    ctx.beginPath();
    ctx.moveTo(0, canvasHeight / 2);
    ctx.lineTo(canvasWidth, canvasHeight / 2);
    ctx.moveTo(canvasWidth / 2, 0);
    ctx.lineTo(canvasWidth / 2, canvasHeight);
    ctx.stroke();

    // Enregistrer l'image
    const outputPath = path.join(scriptDir, "output.png");
    const buffer = canvas.toBuffer("image/png");
    fs.writeFileSync(outputPath, buffer);
    console.log(`Graphique généré : ${outputPath}`);
  });

  connection.end();
});
