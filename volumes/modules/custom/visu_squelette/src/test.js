(function ($, Drupal) {
  Drupal.behaviors.testBehavior = {
    attach: function (context, settings) {
      $('#test-button', context).once('testBehavior').click(function () {
        $('#test-container').text('Le bouton a été cliqué !');
      });
    }
  };
})(jQuery, Drupal);
