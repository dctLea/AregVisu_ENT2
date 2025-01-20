<?php

namespace Drupal\visu_squelette\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\visu_squelette\Test; // Import de la classe Test

class VisuSqueletteController extends ControllerBase {
  public function test() {
    // Instanciation de la classe Test
    $testInstance = new Test();
    // Appel de la méthode getContent
    $content = $testInstance->getContent();

    return [
      '#markup' => $content,
    ];
  }
}
