(function (Drupal, once) {
  Drupal.behaviors.testBehavior = {
    attach: function (context) {
      console.log("Script chargé !");

      once("testBehavior", "#test-button", context).forEach((element) => {
        console.log("Bouton détecté !");
        element.addEventListener("click", function () {
          console.log("Bouton cliqué !");
          document.getElementById("test-container").textContent =
            "Le bouton a été cliqué !";
        });
      });
    },
  };
})(Drupal, window.once);
