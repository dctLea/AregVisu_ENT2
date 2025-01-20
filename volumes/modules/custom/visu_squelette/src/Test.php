<?php

namespace Drupal\visu_squelette;

class Test {
  public function getContent() {
	  
	// Chemin du script Python
    $scriptPath = DRUPAL_ROOT . '/modules/custom/visu_squelette/scripts/script.py';
	
	// Commande pour exécuter le script Python
    $command = escapeshellcmd("python3 $scriptPath");
    
	// Exécuter le script et capturer la sortie
    $output = shell_exec($command);
	
    // Retourner le contenu généré ou une confirmation
    return $output ? $output : 'Erreur lors de l\'exécution du script Python.';
  }
}
