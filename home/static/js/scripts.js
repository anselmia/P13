/*!
 * Start Bootstrap - Creative v6.0.0 (https://startbootstrap.com/themes/creative)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-creative/blob/master/LICENSE)
 */
(function ($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  $(document).ready(function () {
    if ($("input[name='GoToProduct']").length > 0) {
      $('body, html').animate({
        scrollTop: $("#product").offset().top - 82
      }, 600);
    }
    $('.rate_widget').each(function (i) {
      var widget = this;
      var widget_id = $(widget).attr('id');

      $.post('/rating/' + parseInt(widget_id) + '/').done(function (INFO) {
        $(widget).data('fsr', INFO);
        set_votes(widget);
      });
    });
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function () {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function () {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });


  $('select.family').on('change', function (e) {
    var valueSelected = this.value;
    var url = window.location.origin + "/favorites/" + parseInt(valueSelected) + '/'
    window.location.href = url;
  });

  $('select.favori').on('change', function (e) {
    var valueSelected = this.value.split("/");
    var id_favori = valueSelected[0]
    var id_family = valueSelected[1]
    $.get('/save_favorites/' + parseInt(id_favori) + '/' + parseInt(id_family) + '/')
  });

  $('select.order_product').on('change', function (e) {
    var valueSelected = this.value;
    var url = window.location.origin + "/product/" + parseInt(valueSelected) + '/'
    window.location.href = url;
  });

  $('select.order_substitute').on('change', function (e) {
    var valueSelected = this.value;
    var product_id = $('select.order_substitute').attr("id");
    var url = window.location.origin + "/substitute/" + parseInt(product_id) + '/' + parseInt(valueSelected) + '/'
    window.location.href = url;
  });

  $('.ratings_stars').hover(
    // Handles the mouseover
    function () {
      $(this).prevAll().addBack().addClass('ratings_over');
      $(this).nextAll().removeClass('ratings_vote');
    },
    // Handles the mouseout
    function () {
      $(this).prevAll().addBack().removeClass('ratings_over');
      set_votes($(this).parent());
    }
  );

  $('.ratings_stars').bind('click', function () {
    var star = this;
    var widget = $(this).parent();
    var clicked_on = parseInt($(star).attr('class').split(' ')[0].split('_')[1]);
    var widget_id = widget.attr('id');

    $.post('/vote/' + parseInt(widget_id) + '/' + clicked_on + '/').done(function (INFO) {
      if (INFO.status == true) {
        $(widget).data('fsr', INFO);
        set_votes(widget);
      }
    });
  });
})(jQuery); // End of use strict

$('input[name="email"], input[name="username"]').keyup(function () {
  if ($(this).val()) {
    $("button[name='confirm_change']").removeAttr('disabled').removeClass("disabled");
  }
});

function addFamily(largeur, hauteur) {
  var popup = document.getElementById('popup'),
    bouton = document.createElement('button'),
    bouton2 = document.createElement('button');

  popup.innerHTML = "";

  popup.appendChild(document.createTextNode('Nom de la famille à ajouter :'));
  popup.appendChild(document.createElement('br'));
  var input = document.createElement("input");
  input.type = "text";
  popup.appendChild(input);
  $('input[type="text"]').addClass("family_name");
  popup.appendChild(document.createElement('br'));
  popup.appendChild(bouton);
  bouton.appendChild(document.createTextNode('Valider'));
  $('button').addClass("validate");
  popup.style.display = "";
  popup.appendChild(document.createElement('br'));
  popup.appendChild(bouton2);
  bouton2.appendChild(document.createTextNode('Annuler'));

  popup.style.left = (screen.height - hauteur) / 2;
  popup.style.top = (screen.width - largeur) / 2;

  $(function () {
    $('.name').keypress(function (e) {
      var keyCode = e.which;
      if (((keyCode >= 48 && keyCode <= 57) ||
          (keyCode >= 65 && keyCode <= 90) ||
          (keyCode >= 97 && keyCode <= 122)) &&
        keyCode != 8 && keyCode != 32) {} else {
        return false;
      }
    });
  });

  bouton.onclick = function () {
    popup.style.display = "none";
    var family = input.value
    var url = window.location.origin + "/save_family/" + family + '/'
    window.location.href = url;
  };
  bouton2.onclick = function () {
    popup.style.display = "none";
  };
}

function deleteFamily() {
  var selectedFamily = $('select.family option:selected').val();
  if (selectedFamily != 0 && selectedFamily != null) {
    var url = window.location.origin + '/delete_family/' + parseInt(selectedFamily) + '/'
    window.location.href = url;
  }
}

function set_votes(widget) {
  var avg = $(widget).data('fsr').whole_avg;
  var votes = $(widget).data('fsr').number_votes;
  var exact = $(widget).data('fsr').dec_avg;

  $(widget).find('.star_' + avg).prevAll().addBack().addClass('ratings_vote');
  $(widget).find('.star_' + avg).nextAll().removeClass('ratings_vote');
  $(widget).find('.total_votes').text(votes + ' votes ( ' + exact + ' )');
}