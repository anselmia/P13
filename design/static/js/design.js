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
          } else if (stepIndex == 2) {
            tot_pan = $('.tot_pan_value').text();
            $('#nav-Configuration2-tab').hide();
            $('#nav-Configuration3-tab').hide();
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
    if (stepIndex == 2)
      calculate_implantation();
    else if (stepIndex == 3) {
      $('.tot_panel_value').text(tot_pan);
      calculate_configuration();
    }
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
          var next = $input.closest('.row .tag_error').next();
          next.append("<p class ='form_validation_errors'>" + errors[name][i] + "</p>");
        }
      }
    }
  }

  function check_step_fail(stepIndex, stepDirection, callback) {
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
    } else if (stepIndex == 3 && stepDirection == "forward") {
      callback(valid_configuration());
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
      $(".roof_width").hide();
      $(".roof_bottom_length").hide();
      $(".roof_top_length").hide();
      $(".roof_height").hide();
    } else {
      if (type == "trapèze") {
        $(".roof_width").hide();
        $(".roof_bottom_length").show();
        $(".roof_top_length").show();
        $(".roof_height").show();
      } else {
        $(".roof_width").show();
        $(".roof_bottom_length").show();
        $(".roof_top_length").hide();
        $(".roof_height").hide();
      }

      $("#id_width").val(0);
      $("#id_bottom_length").val(0);
      $("id_top_length").val(0);
      $("#id_height").val(0);

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
  var original_datas = {};
  var scale;

  function calculate_implantation() {
    $('#smartwizard').smartWizard("loader", "show");

    var form_project = $('.form_project').serialize();
    var form_roof = $('.form_roof').serialize();
    var form_implantation = $('.form_implantation').serialize();

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

  // Configuration Functions
  //###################################################################
  var form_project = null,
    form_roof = null,
    form_implantation = null,
    form_config1 = null,
    form_config1_mpp1 = null,
    form_config1_mpp2 = null,
    form_config1_mpp3 = null,
    form_config2 = null,
    form_config2_mpp1 = null,
    form_config2_mpp2 = null,
    form_config2_mpp3 = null,
    form_config3 = null,
    form_config3_mpp1 = null,
    form_config3_mpp2 = null,
    form_config3_mpp3 = null;
  var tot_pan = 0;
  //###################################################################

  $('#add-tab').on('click', function (event) {
    event.preventDefault();
    $('.nav-tabs a.active').removeClass('active');
    if ($('#nav-Configuration2-tab').is(":hidden")) {
      $('#nav-Configuration2-tab').show();
      $('#nav-Configuration2-tab').trigger('click');

    } else if ($('#nav-Configuration3-tab').is(":hidden")) {
      $('#nav-Configuration3-tab').show();
      $('#add-tab').hide();

      $('#nav-Configuration3-tab').trigger('click');
    }
  });

  $('.get_config').on('click', function (event) {
    calculate_configuration();
  });

  $('[id*=close_config').on('click', function (event) {
    var id_config = $(this).attr('id').match(/\d+/)[0];
    $('#nav-Configuration' + id_config + '-tab').hide();
    $('nav-Configuration' + id_config).find('input[class=.config]').val(0);
    $('#nav-Configuration1-tab').trigger('click');
    $('#add-tab').show();
  });

  $('[id=id_inverter_id]').on('change', function () {
    var parent_row = $(this).closest('form').closest(".row.cn");
    $('#smartwizard').smartWizard("loader", "show");
    $.ajax({
      data: {
        "inverter_id": $(this).val()
      },
      type: "POST",
      url: '/inverter_data/',
    }).done(function (resp) {
      if (resp["success"]) {
        var datas = JSON.parse(resp["data"])[0]["fields"];
        parent_row.find('.inverter_power_value').text(datas["ac_power_nominal"])
        parent_row.find('.max_dc_voltage_value').text(datas["dc_voltage_max"])
        parent_row.find('.mpp_min_value').text(datas["mpp_voltage_min"])
        parent_row.find('.mpp_max_value').text(datas["mpp_voltage_max"])
        parent_row.find('.current_value').text(datas["dc_current_max"])
      }
      $('#smartwizard').smartWizard("loader", "hide");
    })
  });

  $('.config').change(function () {
    if ($.isNumeric($(this).val()) && $(this).val() > 0 && parseInt($(this).val()) != NaN)
      calculate_configuration();
    else {
      if ($(this).attr('id') == "id_inverter_quantity") {
        var parent_form_class = $(this).closest('form').attr('class').match(/\d+/)[0];
        for (var i = 1; i < 4; i++) {
          $('.inverter' + parent_form_class + '_mpp' + i).find('p[class*=_value]').text('');
        }
      } else {
        $(this).closest('[class*=inverter]').find('p[class*=_value]').text('');
      }
      $(this).val(0);
    }
  });

  function calculate_configuration() {
    $('#smartwizard').smartWizard("loader", "show");
    init_config_var();

    $.when(ajax_post_form('/valid_project/', form_project, function (resp) {
      if (resp.responseJSON["success"] || resp.responseJSON["pass"]) {
        ajax_post_form('/valid_roof/', form_roof, function (resp) {
          if (resp.responseJSON["success"] || resp.responseJSON["pass"]) {
            ajax_post_form('/valid_implantation/', form_implantation, function (resp) {
              if (resp.responseJSON["success"] || resp.responseJSON["pass"]) {

                var datas = set_config_datas();

                if (datas["configs"].length > 0) {
                  $.ajax({
                    data: {
                      'data': JSON.stringify(datas)
                    },
                    type: "POST",
                    url: '/calcul_configuration/',
                  }).done(function (resp) {
                    if (resp["success"]) {
                      var datas = JSON.parse(resp["configuration_values"]);
                      set_configurations_informations(datas);
                    }
                    check_forms_errors(resp);
                    $('#smartwizard').smartWizard("loader", "hide");
                  })
                } else
                  $('#smartwizard').smartWizard("loader", "hide");
              } else {
                check_forms_errors(resp);
                $('#smartwizard').smartWizard("loader", "hide");
              }
            });
          } else {
            check_forms_errors(resp);
            $('#smartwizard').smartWizard("loader", "hide");
          }
        });
      } else {
        check_forms_errors(resp);
        $('#smartwizard').smartWizard("loader", "hide");
      }
    }))
  }

  function init_config_var() {
    $('p[class*=_value]').css("color", "black")
    form_project = $('.form_project').serialize();
    form_roof = $('.form_roof').serialize();
    form_implantation = $('.form_implantation').serialize();

    form_config1 = $('.form_config.config_1').serialize();
    form_config1_mpp1 = $("div.inverter1_mpp1").find("form.form_mpp").serialize();
    if ($('.inverter1_mpp2').is(":visible"))
      form_config1_mpp2 = $("div.inverter1_mpp2").find("form.form_mpp").serialize();
    if ($('.inverter1_mpp3').is(":visible"))
      form_config1_mpp3 = $("div.inverter1_mpp3").find("form.form_mpp").serialize();

    if ($('#nav-Configuration2-tab').is(":visible")) {
      form_config2 = $('.form_config.config_2').serialize();
      form_config2_mpp1 = $("div.inverter2_mpp1").find("form.form_mpp").serialize();
      if ($('.inverter2_mpp2').is(":visible"))
        form_config2_mpp2 = $("div.inverter2_mpp2").find("form.form_mpp").serialize();
      if ($('.inverter2_mpp3').is(":visible"))
        form_config2_mpp3 = $("div.inverter2_mpp3").find("form.form_mpp").serialize();
    }

    if ($('#nav-Configuration3-tab').is(":visible")) {
      form_config3 = $('.form_config.config_3').serialize();
      form_config3_mpp1 = $("div.inverter3_mpp1").find("form.form_mpp").serialize();
      if ($('.inverter3_mpp2').is(":visible"))
        form_config3_mpp2 = $("div.inverter3_mpp2").find("form.form_mpp").serialize();
      if ($('.inverter3_mpp3').is(":visible"))
        form_config3_mpp3 = $("div.inverter3_mpp3").find("form.form_mpp").serialize();
    }
  }

  function set_config_datas() {
    var datas = {};
    datas["tot_panel"] = tot_pan;
    datas["panel_id"] = $('#id_panel_id option:selected').val();
    datas["configs"] = [];
    if (form_config1 != null && $("form.config_1").find("#id_inverter_quantity").val() > 0) {
      var form_data = data_out_of_serialized_form(form_config1);
      var config = new Config(form_data['inverter_id'], form_data['inverter_quantity'], 1);

      if (form_config1_mpp1 != null) {
        var form_data = data_out_of_serialized_form(form_config1_mpp1);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 1);
        if (mpp.serial > 0 && mpp.parallel > 0)
          config.mpps.push(mpp)
      }

      if (form_config1_mpp2 != null) {
        var form_data = data_out_of_serialized_form(form_config1_mpp2);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 2);
        if (mpp.serial > 0 && mpp.parallel > 0)
          config.mpps.push(mpp)
      }

      if (form_config1_mpp3 != null) {
        var form_data = data_out_of_serialized_form(form_config1_mpp3);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 3);
        if (mpp.serial > 0 && mpp.parallel > 0)
          config.mpps.push(mpp)
      }

      if (config.mpps.length > 0)
        datas["configs"].push(config);
    }

    if (form_config2 != null && $("form.config_2").find("#id_inverter_quantity").val() > 0) {
      var form_data = data_out_of_serialized_form(form_config2);
      var config = new Config(form_data['inverter_id'], form_data['inverter_quantity'], 2);

      if (form_config2_mpp1 != null) {
        var form_data = data_out_of_serialized_form(form_config2_mpp1);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 1);
        if (mpp.serial > 0 && mpp.parallel > 0)
          config.mpps.push(mpp)
      }

      if (form_config2_mpp2 != null) {
        var form_data = data_out_of_serialized_form(form_config2_mpp2);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 2);
        if (mpp.serial > 0 && mpp.parallel > 0)
          config.mpps.push(mpp)
      }

      if (form_config2_mpp3 != null) {
        var form_data = data_out_of_serialized_form(form_config2_mpp3);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 3);
        if (mpp.serial > 0 && mpp.parallel > 0)
          config.mpps.push(mpp)
      }
      if (config.mpps.length > 0)
        datas["configs"].push(config);
    }

    if (form_config3 != null && $("form.config_3").find("#id_inverter_quantity").val() > 0) {
      var form_data = data_out_of_serialized_form(form_config3);
      var config = new Config(form_data['inverter_id'], form_data['inverter_quantity'], 3);

      if (form_config3_mpp1 != null) {
        var form_data = data_out_of_serialized_form(form_config3_mpp1);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 1);
        config.mpps.push(mpp)
      }

      if (form_config3_mpp2 != null) {
        var form_data = data_out_of_serialized_form(form_config3_mpp2);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 2);
        config.mpps.push(mpp)
      }

      if (form_config3_mpp3 != null) {
        var form_data = data_out_of_serialized_form(form_config3_mpp3);
        var mpp = new Mpp(form_data['serial'], form_data['parallel'], 3);
        config.mpps.push(mpp)
      }
      if (config.mpps.length > 0)
        datas["configs"].push(config);
    }

    return datas;
  }

  function set_configurations_informations(datas) {
    $('.pac_tot_value').text(datas["tot_ac_nom_power"].toFixed(2))
    $('.tot_panel_value').text(datas["tot_installed_panel"]);
    $('.configured_panel_value').text(datas["tot_configured_panel"]);
    $('.p_dc_tot_value').text(datas["tot_power"].toFixed(2));
    $('.rest_panel_value').text(datas["rest_panel"]);

    for (var i = 0; i < datas["configs"].length; i++) {
      var config = datas["configs"][i];
      var index_config = config["index"].toString();

      $('.i_tot_max_value').text(config["icc_tot_at_70"].toFixed(1));
      $('.i_tot_max_value').css('color', 'green');
      $('.i_tot_min_value').text(config["icc_tot_at__10"].toFixed(1));
      $('.i_tot_min_value').css('color', 'green');
      $('.ratio_pn_value').text(config["power_ratio"].toFixed(1));
      $('.ratio_pn_value').css('color', 'green');

      for (var j = 0; j < config["mpps"].length; j++) {
        var mpp = config["mpps"][j];
        var index_mpp = mpp["index"].toString();
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".mpp_voltage_min_value").text(mpp["mpp_string_voltage_at_70"].toFixed(1));
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".mpp_voltage_min_value").css('color', 'green');
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".mpp_voltage_max_value").text(mpp["mpp_string_voltage_at__10"].toFixed(1));
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".mpp_voltage_max_value").css('color', 'green');
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".vco_voltage_min_value").text(mpp["vco_string_voltage_at_70"].toFixed(1));
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".vco_voltage_min_value").css('color', 'green')
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".vco_voltage_max_value").text(mpp["vco_string_voltage_at__10"].toFixed(1));
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".vco_voltage_max_value").css('color', 'green')
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".i_max_value").text(mpp["icc_at_70"].toFixed(1));
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".i_max_value").css('color', 'green')
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".i_min_value").text(mpp["icc_at__10"].toFixed(1));
        $('.inverter' + index_config + '_mpp' + index_mpp).find(".i_min_value").css('color', 'green')
      }

      var errors = config["errors"];
      for (var i = 0; i < errors.length; i++) {
        var error = errors[i]
        if (error.length == 2)
          $(error[0]).find(error[1]).css('color', 'red');
        else
          $(error).css('color', 'red');
      }
    }
  }

  function valid_configuration() {
    $('p[class*=_value]').css("color").each(function () {
      if ($(this).css('color') == 'red') {
        return {
          "errors": true
        };
      }
    });
    if ($('.rest_panel_value').val() == 0)
      return {
        "success": true
      }
    else
      return {
        "errors": true
      };
  }

  function reset_config_value(index) {
    // $('.inverter' + index + '_mpp' + i).find('p[class*=_value]').text('');
  }

  function Config(inverter_id, inverter_quantity, index) {
    this.index = index;
    this.inverter_id = inverter_id;
    this.inverter_quantity = inverter_quantity;
    this.mpps = [];
  }

  function Mpp(serial, parallel, index) {
    this.index = index;
    this.serial = serial;
    this.parallel = parallel;
  }

  // General Functions
  //###################################################################
  function repsonse_null() {
    this.responseJSON = {
      "pass": true
    };
  }

  function ajax_post_form(url, form, callback) {
    if (form == null)
      callback(new repsonse_null());
    else {
      $.ajax({
        type: 'POST',
        url: url,
        data: form,
        complete: function (response) {
          callback(response);
        }
      });
    }
  }

  function data_out_of_serialized_form(form) {
    var datas = {}
    var split = form.split('&');
    split.forEach(function (item) {
      datas[item.split('=')[0]] = item.split('=')[1];
    });

    return datas;
  }

})(jQuery); // End of use strict