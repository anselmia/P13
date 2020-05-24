/*!
 * Start Bootstrap - Creative v6.0.0 (https://startbootstrap.com/themes/creative)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-creative/blob/master/LICENSE)
 */
(function ($) {
  "use strict"; // Start of use strict
  $(document).ready(function () {
    $('#smartwizard').smartWizard();
    var options = {
      justified: true,
      transition: {
        animation: "slide-horizontal"
      },
      theme: "arrows",
    };
    $('#smartwizard').smartWizard("setOptions", options);
  });

  $('#add_city_button').click(function () {
    $('#add_city').css('display', 'block');
  });

  $('.meteo_search').bind('click', function () {
    var search_text = $('#city_to_find').value;

    $.post('/get_meteo_data/' + search_text).done(function (INFO) {
      if (INFO.status == true) {
        $(widget).data('fsr', INFO);
        set_votes(widget);
      }
    });
  });
})(jQuery); // End of use strict