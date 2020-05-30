/*!
 * Start Bootstrap - Creative v6.0.0 (https://startbootstrap.com/themes/creative)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-creative/blob/master/LICENSE)
 */

(function ($) {

  "use strict"; // Start of use strict
  $(document).ready(function () {
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    startWizard();
    $(".roof-img").hide();
    $(".vertical_spacing").hide();
    $(".horizontal_spacing").hide();
    $(".vertical_overlapping").hide();
    $(".horizontal_overlapping").hide();
  });

  // SmartWizard  Functions
  //###################################################################

  function startWizard() {
    $('#smartwizard').smartWizard();
    var options = {
      justified: true,
      transition: {
        animation: "slide-horizontal"
      },
      theme: "arrows",
    };
    $('#smartwizard').smartWizard("setOptions", options);
    $('.tab-content').css('height', 'auto');
    $('*[id*=step]').each(function () {
      $(this).css('width', '100%');
    });
  };

  let isLastStepChecked = false;
  //Initialize the leaveStep event
  $("#smartwizard").on("leaveStep", function (e, anchorObject, stepIndex, stepDirection) {
    $('#smartwizard').smartWizard("loader", "show");
    if (!isLastStepChecked && (stepDirection == "forward")) {
      e.preventDefault();
      check_step_fail(stepIndex, stepDirection, function (resp) {
        if (resp["success"]) {
          // Clear Step 3
          if (stepIndex == 1) {
            context.clearRect(0, 0, canvas.width, canvas.height);
            $('.infos_implantation').hide();
          }
          $('#smartwizard').smartWizard("next");
        } else {
          isLastStepChecked = false;
        }

        // Update errors in forms
        check_forms_errors(resp);

      });
      isLastStepChecked = true;
      $('#smartwizard').smartWizard("loader", "hide");
      return stepDirection === "forward"
    } else {
      isLastStepChecked = false;
      $('#smartwizard').smartWizard("loader", "hide");
      return true;
    }
  });

  $('#smartwizard').on('showStep', function (e, anchorObject, stepIndex, stepDirection, stepPosition) {
    $('.tab-content').css('height', 'auto')
    $('*[id*=step').each(function () {
      $(this).css('width', '100%');
    });
  });

  function check_forms_errors(resp) {

    if ($(".form_validation_errors").length) {
      $(".is-invalid").removeClass("form-control is-invalid");
      $(".form_errors").empty();
    }

    if (resp != null && resp.errors) {
      var errors = resp.errors
      for (var name in errors) {
        for (var i in errors[name]) {
          // object message error django
          var $input = $("[name='" + name + "']");
          $input.addClass("form-control is-invalid");
          var next = $input.closest('.row').next();
          next.append("<p class ='form_validation_errors'>" + errors[name][i] + "</p>");
        }
      }
    }
  }

  function check_step_fail(stepIndex, stepDirection, callback) {
    var items = [];
    if (stepIndex == 0 && stepDirection == "forward") {
      $.ajax({
        data: $('.form_project').serialize(),
        type: "POST",
        url: '/valid_project/',
        success: function (response) {
          callback(response);
        }
      });
    } else if (stepIndex == 1 && stepDirection == "forward") {
      $.ajax({
        data: $('.form_roof').serialize(),
        type: "POST",
        url: '/valid_roof/',
        success: function (response) {
          callback(response);
        }
      });
    } else if (stepIndex == 2 && stepDirection == "forward") {
      $.ajax({
        data: $('.form_implantation').serialize(),
        type: "POST",
        url: '/valid_implantation/',
        success: function (response) {
          callback(response);
        }
      });
    }
  };

  // Project  Functions
  //###################################################################

  $('.localisation_search').bind('click', function () {
    var search_text = $('#city_to_find').val();

    $.post('/get_meteo_data/', {
      "search": search_text
    }).done(function (INFO) {
      if (INFO.status == true && Object.keys(INFO.localisation).length > 0) {
        $('.localisation').css('display', 'block');
        $('.find_city').val(INFO.localisation["city"]);
        $('.find_lat').val(INFO.localisation["lat"]);
        $('.find_lon').val(INFO.localisation["lon"]);
        $("#city_errors").html("");
      }
    });
  });

  $('#city-form').on('submit', function (event) {
    event.preventDefault();
    add_city($(this));
  });

  function add_city(form) {
    var items = [];
    $.ajax({
      data: form.serialize(),
      type: form.attr('method'),
      url: form.attr('action'),
      success: function (response) {
        if (response['success']) {
          $("#city_errors").html();
          $('#id_city_id').val('');
          $('#id_city_id').append('<option value="' + response["id"] + '">' + response["name"] + '</option>')
          $('#id_city_id option').filter(function () {
            return ($(this).text() == response["name"]);
          }).prop('selected', true);
          $('.localisation').css('display', 'none');
          $('#CityModal').hide();
          $('body').removeClass('modal-open');
          $('.modal-backdrop').remove();
        } else if (response['errors']) {
          response['errors'].forEach(function (item) {
            items.push(item);
          });
        }
      },
      complete: function () {
        if (items.length > 0) {
          $("#city_errors").html("<div class='alert alert-danger'>" +
            items.join("") + "</div>");
        } else {
          $("#city_errors").html("");
        }
      }
    }).done(check_forms_errors(resp));
  };

  $("#CityModal").on('hide.bs.modal', function () {
    $('#city_to_find').val('');
    $('.localisation').css('display', 'none');
    $("#city_errors").html("");
  });

  // Panel  Functions
  //###################################################################
  $('#panel-form').on('submit', function (event) {
    event.preventDefault();
    add_panel($(this));
  });

  function add_panel(form) {
    var items = [];
    $.ajax({
      data: form.serialize(),
      type: form.attr('method'),
      url: form.attr('action'),
      success: function (response) {
        if (response['success']) {
          $("#panel_errors").html();
          $('#id_panel_id').val('');
          $('#id_panel_id').append('<option value="' + response["id"] + '">' + response["model"] + '</option>')
          $('#id_panel_id option').filter(function () {
            return ($(this).text() == response["name"]);
          }).prop('selected', true);
          $('#PanelModal').hide();
          $('body').removeClass('modal-open');
          $('.modal-backdrop').remove();
        } else if (response['errors']) {
          response['errors'].forEach(function (item) {
            items.push(item);
          });
        }
      },
      complete: function () {
        if (items.length > 0) {
          $("#panel_errors").html("<div class='alert alert-danger'>" +
            items.join("") + "</div>");
        } else {
          $("#panel_errors").html("");
        }
      }
    })
  };

  $("#PanelModal").on('hide.bs.modal', function () {
    $("#panel_errors").html("");
    clear_panel_val();
  });

  function clear_panel_val() {
    $("[name='model']").val('');
    $("[name='manufacturer_id']").val('');
    $("[name='technology_id']").val('');
    $("[name='power']").val('');
    $("[name='tolerance']").val('');
    $("[name='radiation']").val('');
    $("[name='temperature']").val('');
    $("[name='short_circuit_current']").val('');
    $("[name='open_circuit_voltage']").val('');
    $("[name='temperature_factor_current']").val('');
    $("[name='temperature_factor_current_type']").val('');
    $("[name='temperature_factor_voltage']").val('');
    $("[name='temperature_factor_voltage_type']").val('');
    $("[name='temperature_factor_power']").val('');
    $("[name='temperature_factor_power_type']").val('');
    $("[name='mpp_current']").val('');
    $("[name='mpp_voltage']").val('');
    $("[name='voltage_max']").val('');
    $("[name='length']").val('');
    $("[name='width']").val('');
    $("[name='serial_cell_quantity']").val('');
    $("[name='parallel_cell_quantity']").val('');
    $("[name='cell_surface']").val('');
    $("[name='comment']").val('');
  };

  // Roof Functions
  //###################################################################

  $('#id_roof_type').on('change', function () {
    var type = $("#id_roof_type option:selected").text();
    if (type == "---------") {
      $(".roof-img").hide();
      $("[id=id_width]").hide();
      $("[id=id_bottom_length]").hide();
      $("[id=id_top_length]").hide();
      $("[id=id_height]").hide();
    } else {
      if (type == "trapèze") {
        $("[id=id_width]").hide();
        $("[id=id_bottom_length]").show();
        $("[id=id_top_length]").show();
        $("[id=id_height]").show();
      } else {
        $("[id=id_width]").show();
        $("[id=id_bottom_length]").show();
        $("[id=id_top_length]").hide();
        $("[id=id_height]").hide();
      }

      $("[id=id_width]").val(0);
      $("[id=id_bottom_length]").val(0);
      $("[id=id_top_length]").val(0);
      $("[id=id_height]").val(0);

      // Add correct roof src image
      var old_src = $('.roof').find('img').attr("src");
      var temp_split_left = old_src.split("_")[0];
      var temp_split_right = old_src.split("_")[1].split(".")[1];
      var new_src = temp_split_left + "_" + type + "." + temp_split_right
      $('.roof').find('img').attr("src", new_src);
      $('.roof-img').show();
    }
    check_forms_errors(null);
  });

  // Implantation Functions
  //###################################################################

  $('#id_panel_implantation').on('change', function () {
    var type = $("#id_panel_implantation option:selected").text();
    if (type == "---------" || type == "côte à côtes") {
      $(".vertical_spacing").hide();
      $(".horizontal_spacing").hide();
      $(".vertical_overlapping").hide();
      $(".horizontal_overlapping").hide();
    } else {
      if (type == "Espacés") {
        $(".vertical_spacing").show();
        $(".horizontal_spacing").show();
        $(".vertical_overlapping").hide();
        $(".horizontal_overlapping").hide();
      } else {
        $(".vertical_spacing").hide();
        $(".horizontal_spacing").hide();
        $(".vertical_overlapping").show();
        $(".horizontal_overlapping").show();
      }
    }
    check_forms_errors(null);
  });

  $('.draw').on('click', function (event) {
    $('.infos_implantation').hide();
    calculate_implantation();
  });

  // Canva  Functions
  //###################################################################

  // Store the canvas object into a variable
  var canvas = document.getElementById('myCanvas')
  var context = canvas.getContext('2d');

  // (function () {
  //   // resize the canvas to fill browser window dynamically
  //   window.addEventListener('resize', resizeCanvas, false);

  //   function resizeCanvas() {
  //     calculate_implantation();
  //   }
  //   resizeCanvas();
  // })();


  var original_datas = {};
  var scale;

  function calculate_implantation() {
    $('#smartwizard').smartWizard("loader", "show");

    var form_project = $('.form_project').serialize();
    var form_roof = $('.form_roof').serialize();
    var form_implantation = $('.form_implantation').serialize();

    var success = true;
    $.ajax({
      data: form_project,
      type: "POST",
      url: '/valid_project/',
    }).done(function (resp) {
      if (resp["success"]) {
        $.ajax({
          data: form_roof,
          type: "POST",
          url: '/valid_roof/',
        }).done(function (resp) {
          if (resp["success"]) {
            $.ajax({
              data: form_implantation,
              type: "POST",
              url: '/valid_implantation/'
            }).done(function (resp) {
              if (resp["success"]) {
                var datas = {};
                var split = form_project.split('&');
                split.forEach(function (item) {
                  datas[item.split('=')[0]] = item.split('=')[1];
                });
                split = form_roof.split('&');
                split.forEach(function (item) {
                  datas[item.split('=')[0]] = item.split('=')[1];
                });
                split = form_implantation.split('&');
                split.forEach(function (item) {
                  datas[item.split('=')[0]] = item.split('=')[1];
                });
                $.each(datas, function (i, o) {
                  var val = parseFloat(o);
                  if (!isNaN(val))
                    original_datas[i] = val;
                });
                $.ajax({
                  data: datas,
                  type: "POST",
                  url: '/calcul_implantation/',
                }).done(function (resp) {
                  if (resp["success"]) {
                    var datas = JSON.parse(resp["implantation_values"]);
                    draw(datas)
                  }
                  check_forms_errors(resp);
                })
              } else {
                check_forms_errors(resp);
              }
            })
          }
        })
      }
      $('#smartwizard').smartWizard("loader", "hide");
    })
  }

  function draw(datas) {
    canvas.width = $('#myCanvas').parent().width();
    canvas.height = canvas.width;
    context.clearRect(0, 0, canvas.width, canvas.height);

    scale_value(datas);
    draw_roof(datas);
    draw_panel(datas);
    set_infos(datas);
  }

  function scale_value(datas) {
    var canva_width = canvas.width;
    var canva_height = canvas.height;
    if (original_datas["bottom_length"] > original_datas["width"]) {
      scale = canva_width / original_datas["bottom_length"];
      if (original_datas["roof_type"] == 1)
        canvas.height = 50 + canva_width * (original_datas["width"] / original_datas["bottom_length"]);
      else if (original_datas["roof_type"] == 2)
        canvas.height = 50 + canva_width * (original_datas["height"] / original_datas["bottom_length"]);
      else
        canvas.height = 50 + canva_width * (datas["height"] / original_datas["bottom_length"]);
    } else {
      scale = canva_height / original_datas["width"];
      canvas.width = canva_height * (original_datas["bottom_length"] / original_datas["width"]);
    }

    var context = canvas.getContext('2d');
  }

  function draw_roof(datas) {
    if (original_datas["roof_type"] == 1) {
      context.beginPath();
      context.rect(0, 0, original_datas["bottom_length"] * scale, original_datas["width"] * scale);
    } else if (original_datas["roof_type"] == 2) {
      context.beginPath();
      context.moveTo(0, original_datas["height"] * scale);
      context.lineTo(original_datas["bottom_length"] * scale, original_datas["height"] * scale);
      context.lineTo((((original_datas["bottom_length"] - original_datas["top_length"]) / 2) + original_datas["top_length"]) * scale, 0);
      context.lineTo(((original_datas["bottom_length"] - original_datas["top_length"]) / 2) * scale, 0);
      context.closePath();
      // the outline
      context.lineWidth = 1;
      context.strokeStyle = '#666666';
      context.stroke();
    } else {
      context.beginPath();
      context.moveTo(0, datas["height"] * scale);
      context.lineTo(original_datas["bottom_length"] * scale, datas["height"] * scale);
      context.lineTo((original_datas["bottom_length"] * scale) / 2, 0);
      context.closePath();
    }
    context.lineWidth = 1;
    context.strokeStyle = '#666666';
    context.stroke();
  }

  function draw_panel(datas) {
    for (var i = 0; i < datas.panel.length; i++) {
      var panel = datas.panel[i]
      context.beginPath();

      context.fillStyle = 'blue';
      context.strokeStyle = 'black';
      context.rect(panel[0] * scale, panel[1] * scale, panel[2] * scale, panel[3] * scale);
      context.fill();

      context.lineWidth = 1;
      context.stroke();
    }
    for (var i = 0; i < datas.abergement.length; i++) {
      var abergement = datas.abergement[i]
      context.beginPath();

      context.fillStyle = 'grey';
      context.strokeStyle = 'black';
      context.rect(abergement[0] * scale, abergement[1] * scale, abergement[2] * scale, abergement[3] * scale);
      context.fill();

      context.lineWidth = 1;
      context.stroke();
    }
  }

  function set_infos(datas) {
    $('.bottom_length_value').text(original_datas["bottom_length"].toFixed(2));
    $('.height_value').text(datas["height"].toFixed(2));
    $('.top_length_value').text(original_datas["top_length"].toFixed(2));
    $('.surface_value').text(datas["surface"].toFixed(2));
    $('.top_rest_value').text(datas["top_rest"].toFixed(2));
    $('.bottom_rest_value').text(datas["bottom_rest"].toFixed(2));
    $('.left_rest_value').text(datas["left_rest"].toFixed(2));
    $('.right_rest_value').text(datas["right_rest"].toFixed(2));
    $('.tot_pan_value').text(datas["total_pan"]);
    $('.tot_pan_width_value').text(datas["nb_panel_width"]);
    $('.tot_pan_length_value').text(datas["nb_panel_length"]);
    $('.tot_pan_left_triangle_value').text(datas["nb_pan_left_triangle"]);
    $('.tot_pan_right_triangle_value').text(datas["nb_pan_right_triangle"]);
    $('.panel_length_value').text(datas["panel_length"].toFixed(2));
    $('.panel_width_value').text(datas["panel_width"].toFixed(2));
    $('.power_value').text(datas["power"].toFixed(2));

    $('.rectangle').hide();
    $('.trapeze').hide();
    $('.triangle').hide();

    if (original_datas["roof_type"] == 1)
      $('.rectangle').show();
    else if (original_datas["roof_type"] == 2)
      $('.trapeze').show();
    else
      $('.triangle').show();

    $('.infos_implantation').show();
  }

  //###################################################################
})(jQuery); // End of use strict