/*!
 * Start Bootstrap - Creative v6.0.0 (https://startbootstrap.com/themes/creative)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-creative/blob/master/LICENSE)
 */

(function ($) {

  //#region Global Variable
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
  var id_site = 0,
    id_panel = 0;
  var roof_installed_power = 0,
    roof_installed_panel = 0;
  var configs, tot_configured_ac_power = 0;

  function set_global_variable(step_index) {
    if (step_index == 0) {
      id_site = $('#id_city_id').val();
      id_panel = $('#id_panel_id').val();
    } else if (step_index == 1) {
      orientation = $('#id_orientation').val();
      tilt = $('#id_tilt').val();
      roof_bottom_length = $('#id_bottom_length').val();
      roof_top_length = $('#id_top_length').val();
      roof_height = $('#id_height').val();
      roof_width = $('#id_width').val();
      roof_type = $('#id_roof_type_id').val();
    } else if (step_index == 2) {
      roof_installed_power = $('p.power_value').text();
      roof_installed_panel = $('p.tot_pan_value').text();
    } else if (step_index == 3) {
      tot_configured_ac_power = $('p.pac_tot_value').text();
    }
  }
  //#endregion

  "use strict"; // Start of use strict
  $(document).ready(function () {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    startWizard();
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
  };

  let isLastStepChecked = false;
  let moveForward = false;
  //Initialize the leaveStep event
  $("#smartwizard").on("leaveStep", function (e, anchorObject, stepIndex, stepDirection) {
    $('#smartwizard').smartWizard("loader", "show");
    if (!isLastStepChecked && (stepDirection == "forward")) {
      moveForward = false;
      e.preventDefault();
      check_step_fail(stepIndex, stepDirection, function (resp) {
        if (resp["success"]) {
          set_global_variable(stepIndex);
          moveForward = true;
          isLastStepChecked = true;
          $('#smartwizard').smartWizard("next");
        } else {
          isLastStepChecked = false;
        }
        // Update errors in forms
        check_forms_errors(resp);
      });
      isLastStepChecked = true;
      $('#smartwizard').smartWizard("loader", "hide");
      return stepDirection == "forward"
    } else {
      isLastStepChecked = false;
      $('#smartwizard').smartWizard("loader", "hide");
      return stepDirection == "backward" || moveForward;
    }
  });

  $('#smartwizard').on('showStep', function (e, anchorObject, stepIndex, stepDirection, stepPosition) {
    set_step_view();

    if (stepIndex == 1) {
      form_project = $('.form_project');
      init_roof();
    } else if (stepIndex == 2) {
      form_roof = $('.form_roof');
      init_implantation();
      calculate_implantation();
    } else if (stepIndex == 3) {
      form_implantation = $('.form_implantation');
      init_config();
      calculate_configuration();
    } else if (stepIndex == 4) {
      init_infos_prod();
      calculate_prod();
    }
  });

  function set_step_view() {
    $('.tab-content').css('height', 'auto')
    $('*[id*=step').each(function () {
      $(this).css('width', '100%');
    });
  }

  function check_forms_errors(resp, error_tag = "") {
    $(".is-invalid").removeClass("form-control is-invalid");
    $(".form_errors").empty();

    if (resp != null && resp.errors) {
      var errors = resp.errors
      for (var name in errors) {
        for (var i in errors[name]) {
          // object message error django
          var $input = $("[name='" + name + "']");
          if ($input.length == 0 && error_tag != "") {
            $('.form_errors' + error_tag).append("<p class ='form_validation_errors'>" + errors[name][i] + "</p>")
          } else {

            $input.addClass("form-control is-invalid");
            var next = $input.closest('.row .tag_error').next();
            next.append("<p class ='form_validation_errors'>" + errors[name][i] + "</p>");
          }
        }
      }
    }
  }

  function check_step_fail(stepIndex, stepDirection, callback) {
    if (stepIndex == 0 && stepDirection == "forward") {
      ajax_post('/valid_project/', $(".form_project").serialize(), function (resp) {
        callback(resp.responseJSON);
      });
    } else if (stepIndex == 1 && stepDirection == "forward") {
      ajax_post('/valid_roof/', $(".form_roof").serialize(), function (resp) {
        callback(resp.responseJSON);
      });
    } else if (stepIndex == 2 && stepDirection == "forward") {
      ajax_post('/valid_implantation/', $(".form_implantation").serialize(), function (resp) {
        callback(resp.responseJSON);
      });
    } else if (stepIndex == 3 && stepDirection == "forward") {
      var response = valid_configuration();
      callback(response);
    }
  };

  function get_form(step_index) {
    var form
    if (step_index == 0) {
      if (form_project != null)
        form = form_project.serialize();
      else
        form = $('.form_project').serialize();
    } else if (step_index == 1) {
      if (form_roof != null)
        form = form_roof.serialize();
      else
        form = $('.form_roof').serialize();
    } else if (step_index == 2) {
      if (form_implantation != null)
        form = form_implantation.serialize();
      else
        form = $('.form_implantation').serialize();
    }

    return form;
  }

  // Project  Functions
  //###################################################################

  $('.localisation_search').bind('click', function () {
    $('#smartwizard').smartWizard("loader", "show");
    var search_text = $('#city_to_find').val();

    $.post('/get_localisation_data/', {
      "search": search_text
    }).done(function (INFO) {
      if (INFO.status == true && Object.keys(INFO.loc).length > 0) {
        set_meteo_data(INFO);
      } else
        $('.city_no_result').text("Pas de données disponibles");
      $('#smartwizard').smartWizard("loader", "hide");
    });
  });

  function set_meteo_data(INFO) {
    $('.localisation').css('display', 'block');
    $('.find_city').val(INFO.loc["name"]);
    $('.find_lat').val(INFO.loc["lat"]);
    $('.find_lon').val(INFO.loc["lon"]);
  }

  $('#city-form').on('submit', function (event) {
    event.preventDefault();
    add_city($(this));
  });

  function add_city(form) {
    $('#smartwizard').smartWizard("loader", "show");
    ajax_post('/add_city/', form.serialize(), function (resp) {
      if (resp.responseJSON["success"]) {
        $("#city_errors").html();
        $('#id_city_id').val('');
        $('#id_city_id').append('<option value="' + resp.responseJSON["id"] + '">' + resp.responseJSON["name"] + '</option>')
        $('#id_city_id option').filter(function () {
          return ($(this).text() == resp.responseJSON["name"]);
        }).prop('selected', true);
        $('.localisation').css('display', 'none');
        $('#CityModal').hide();
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
      } else
        $('.localisation').css('display', 'none');
      check_forms_errors(resp.responseJSON, ".city_errors");
      $('#smartwizard').smartWizard("loader", "hide");
    });
  }

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
    ajax_post('/add_panel/', form.serialize(), function (resp) {
      if (resp.responseJSON["success"]) {
        $("#panel_errors").html();
        $('#id_panel_id').val('');
        $('#id_panel_id').append('<option value="' + resp.responseJSON["id"] + '">' + resp.responseJSON["model"] + '</option>')
        $('#id_panel_id option').filter(function () {
          return ($(this).text() == resp.responseJSON["name"]);
        }).prop('selected', true);
        $('#PanelModal').hide();
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
      }

      check_forms_errors(resp.responseJSON, ".panel_errors");
      $('#smartwizard').smartWizard("loader", "hide");
    });
  }

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

  // Panel  Functions
  //###################################################################
  $('#inverter-form').on('submit', function (event) {
    event.preventDefault();
    add_inverter($(this));
  });

  function add_inverter(form) {
    ajax_post('/add_inverter/', form.serialize(), function (resp) {
      if (resp.responseJSON["success"]) {
        $("#inverter_errors").html();
        $('#inverter_id_id').val('');
        $('#inverter_id_id').append('<option value="' + resp.responseJSON["id"] + '">' + resp.responseJSON["model"] + '</option>')
        $('#inverter_id_id option').filter(function () {
          return ($(this).text() == resp.responseJSON["name"]);
        }).prop('selected', true);
        $('#InverterModal').hide();
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
      }

      check_forms_errors(resp.responseJSON, ".inverter_errors");
      $('#smartwizard').smartWizard("loader", "hide");
    });
  }

  $("#InverterModal").on('hide.bs.modal', function () {
    $("#inverter_errors").html("");
    clear_inverter_val();
  });

  function clear_inverter_val() {
    $("[name='model']").val('');
    $("[name='manufacturer_id']").val('');
    $("[name='mpp_voltage_min']").val('');
    $("[name='mpp_voltage_max']").val('');
    $("[name='dc_voltage_max']").val('');
    $("[name='dc_current_max']").val('');
    $("[name='dc_power_max']").val('');
    $("[name='ac_power_nominal']").val('');
    $("[name='ac_power_max']").val('');
    $("[name='ac_current_max']").val('');
    $("[name='efficiency']").val('');
    $("[name='mpp_string_max']").val('');
    $("[name='mpp']").val('');
    $("[name='ac_cabling']").val('');
    $("[name='comment']").val('');
  };

  // Roof Functions
  //###################################################################

  $('#id_roof_type_id').on('change', function () {
    var type = $("#id_roof_type_id option:selected").text();
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

  function init_roof() {
    form_roof = $('.form_roof');
    $(".roof-img").hide();
    $(".vertical_spacing").hide();
    $(".horizontal_spacing").hide();
    $(".vertical_overlapping").hide();
    $(".horizontal_overlapping").hide();
  }

  // Implantation Functions
  //###################################################################
  function init_implantation() {
    form_implantation = $('.form_implantation');
    context.clearRect(0, 0, canvas.width, canvas.height);
    $('.infos_implantation').hide();
  }

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
    ajax_post('/valid_project/', get_form(0), function (resp) {
      if (resp.responseJSON["success"]) {
        ajax_post('/valid_roof/', get_form(1), function (resp) {
          if (resp.responseJSON["success"]) {
            ajax_post('/valid_implantation/', get_form(2), function (resp) {
              if (resp.responseJSON["success"]) {
                var datas = {};
                datas = data_out_of_serialized_form(get_form(0));
                datas = extend(datas, data_out_of_serialized_form(get_form(1)));
                datas = extend(datas, data_out_of_serialized_form(get_form(2)));
                $.each(datas, function (i, o) {
                  var val = parseFloat(o);
                  if (!isNaN(val))
                    original_datas[i] = val;
                });
                ajax_post('/calcul_implantation/', datas, function (resp) {
                  if (resp.responseJSON["success"]) {
                    var datas = JSON.parse(resp.responseJSON["implantation_values"]);
                    draw(datas)

                    check_forms_errors(resp.responseJSON);
                    $('#smartwizard').smartWizard("loader", "hide");
                  } else
                    check_forms_errors(resp.responseJSON);
                  $('#smartwizard').smartWizard("loader", "hide");
                });
              } else
                check_forms_errors(resp.responseJSON);
              $('#smartwizard').smartWizard("loader", "hide");
            });
          } else
            check_forms_errors(resp.responseJSON);
          $('#smartwizard').smartWizard("loader", "hide");
        });
      } else
        check_forms_errors(resp.responseJSON);
      $('#smartwizard').smartWizard("loader", "hide");
    });
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

    context = canvas.getContext('2d');
  }

  function draw_roof(datas) {
    if (original_datas["roof_type_id"] == 1) {
      context.beginPath();
      context.rect(0, 0, original_datas["bottom_length"] * scale, original_datas["width"] * scale);
    } else if (original_datas["roof_type_id"] == 2) {
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

  function init_config() {
    $('.save_prod').show();
    $('.index1').find('#id_index').val(1);
    $('.index2').find('#id_index').val(2);
    $('.index3').find('#id_index').val(3);
    tot_pan = $('.tot_pan_value').text();
    $('#nav-Configuration2-tab').hide();
    $('#nav-Configuration3-tab').hide();
    $('.tot_panel_value').text(tot_pan);
    $('.rest_panel_value').text(0);
    $('.rest_panel_value').text(tot_pan);
    $('.configured_panel_value').text(0);
    calculate_configuration();
  }

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
    $('#add-tab').show();
    $('nav-Configuration' + id_config).find('input[class=.config]').val(0);
    $('#nav-Configuration1-tab').trigger('click');
    $('#nav-Configuration1-tab').trigger('click');

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

    ajax_post('/valid_project/', get_form(0), function (resp) {
      if (resp.responseJSON["success"]) {
        ajax_post('/valid_roof/', get_form(1), function (resp) {
          if (resp.responseJSON["success"]) {
            ajax_post('/valid_implantation/', get_form(2), function (resp) {
              if (resp.responseJSON["success"]) {
                var datas = set_config_datas();
                if (datas["configs"].length > 0) {
                  datas = {
                    'data': JSON.stringify(datas)
                  };
                  ajax_post('/calcul_configuration/', datas, function (resp) {
                    if (resp.responseJSON["success"]) {
                      var datas = JSON.parse(resp.responseJSON["configuration_values"]);
                      set_configurations_informations(datas);
                    }
                    check_forms_errors(resp.responseJSON);
                    $('#smartwizard').smartWizard("loader", "hide");
                  });
                } else {
                  $('#smartwizard').smartWizard("loader", "hide");
                  check_forms_errors(resp.responseJSON);
                }
              } else {
                check_forms_errors(resp.responseJSON);
                $('#smartwizard').smartWizard("loader", "hide");
              }
            });
          } else {
            check_forms_errors(resp.responseJSON);
            $('#smartwizard').smartWizard("loader", "hide");
          }
        });
      } else {
        check_forms_errors(resp.responseJSON);
        $('#smartwizard').smartWizard("loader", "hide");
      }
    });
  }

  function init_config_var() {
    $('p[class*=_value]').css("color", "black");

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
    configs = datas["configs"]

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

      $('.i_tot_max_value' + index_config).text(config["icc_tot_at_70"].toFixed(1));
      $('.i_tot_max_value' + index_config).css('color', 'green');
      $('.i_tot_min_value' + index_config).text(config["icc_tot_at__10"].toFixed(1));
      $('.i_tot_min_value' + index_config).css('color', 'green');
      $('.ratio_pn_value' + index_config).text(config["power_ratio"].toFixed(1));
      $('.ratio_pn_value' + index_config).css('color', 'green');

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
    $('p[class*=_value]').each(function () {
      if ($(this).css('color') == 'red') {
        return {
          "errors": true
        };
      }
    });
    if (parseInt($('.rest_panel_value').text()) == 0)
      return {
        "success": true
      }
    else
      $('.rest_panel_value').css('color', 'red')
    return {
      "errors": true
    };
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

  // Production Functions
  //###################################################################
  function sync_ajax(datas) {
    for (var i = 0; i < datas.length; i++) {
      var result = doAjax('/' + datas[i][0] + '/', datas[i][1]);
      try {
        if (!result["success"])
          return false;
      } catch {
        return false;
      }
    }
    return true;
  }

  $('.save_prod').on('click', function (event) {
    var datas = [
      ["valid_project", get_form(0)],
      ["valid_roof", get_form(1)],
      ["valid_implantation", get_form(2)]
    ];

    datas = check_conf_and_mpp_form(datas);

    var validOk = sync_ajax(datas);

    if (validOk) {
      for (var i = 0; i < datas.length; i++) {
        datas[i][0] = datas[i][0].replace('valid', 'save');
      }
      var savedOk = sync_ajax(datas);
      if (savedOk) {
        $('p.save_project').text('Le projet a été sauvegardé !')
        $('.save_prod').hide();
      } else
        $('p.save_project').text('Erreur pendant la sauvegarde du projet !')
    }
  });

  function check_conf_and_mpp_form(datas) {
    Array.prototype.forEach.call($('.form_config'), form => {
      form = $(form);
      var id_conf = form.attr('id').match(/\d+/)[0];
      var config = configs.find(function (conf) {
        return conf.index == id_conf;
      });
      if (config != null) {
        datas.push(["valid_configuration", form.serialize()]);
        Array.prototype.forEach.call(form.closest("#nav-Configuration" + id_conf).find('.form_mpp'), mpp_form => {
          mpp_form = $(mpp_form);
          var id_mpp = mpp_form.attr('id').match(/\d+/)[0];
          var mpp = config.mpps.find(function (_mpp) {
            return _mpp.index == id_mpp;
          });
          if (mpp != null) {
            datas.push(["valid_mpp", mpp_form.serialize()]);
          }
        });
      }
    });
    return datas;
  }


  function init_infos_prod() {
    var datas = {
      "panel_id": id_panel,
      "config": configs,
      "site_id": id_site,
      "tot_pan": roof_installed_panel
    };

    datas = {
      'data': JSON.stringify(datas)
    };

    ajax_post('/production_data/', datas, function (resp) {
      if (resp.responseJSON["success"]) {
        show_init_config_infos(resp.responseJSON["infos"]);
      }
    });
  }

  function show_init_config_infos(datas) {
    $('p.save_project').text('');
    // Site Informations
    $('p.energy_site_name').text(datas["site_data"][0])
    $('p.energy_latitude').text(datas["site_data"][1])
    $('p.energy_longitude').text(datas["site_data"][2])
    // Solar panel Information
    $('p.energy_panel_model').text(datas["pv_data"][0])
    $('p.energy_panel_power').text(datas["pv_data"][1])
    $('p.energy_tot_panel').text(roof_installed_panel)
    $('p.energy_tot_panel_power').text(roof_installed_power)
    $('p.energy_tot_panel_surface').text(datas["pv_data"][2])

    if (datas["inverters_datas"].length > 0) {
      for (var i = 1; i < 4; i++) {
        var inverter = datas["inverters_datas"].find(function (element) {
          return element[0] == i - 1;
        });

        if (inverter != null) {
          $('.energy_inverter' + String(i)).show();
          $('p.energy_inverter_model' + String(i)).text(inverter[1])
          $('p.energy_inverter_power' + String(i)).text(inverter[2])

          var config = configs.find(function (conf) {
            return conf.index == i;
          });
          $('p.energy_inverter_quantity' + +String(i)).text(config.inverter_quantity)
          for (var mpp = 1; mpp < 4; mpp++) {
            var Mpp = config.mpps.find(function (find_mpp) {
              return find_mpp.index == mpp;
            });
            if (Mpp != null && Mpp.serial > 0) {
              $('.energy_inverter' + String(i) + '_MPP' + String(mpp)).show();
              $('p.energy_inverter' + String(i) + '_serial' + String(mpp)).text(Mpp.serial)
              $('p.energy_inverter' + String(i) + '_parallel' + String(mpp)).text(Mpp.serial)
            } else
              $('.energy_inverter' + String(i) + '_MPP' + String(mpp)).hide();
          }
        } else
          $('.energy_inverter' + String(i)).hide();
      }
    } else {
      $('.energy_inverter1').hide();
      $('.energy_inverter2').hide();
      $('.energy_inverter3').hide();
    }
  }

  function calculate_prod() {
    $('#smartwizard').smartWizard("loader", "show");
    var datas = {
      "panel_id": $('#id_panel_id').val(),
      "site_id": $('#id_city_id').val(),
      "orientation": $('#id_orientation').val(),
      "tilt": $('#id_tilt').val(),
      "tot_panel": $('.tot_panel_value').text()
    };

    datas = {
      'data': JSON.stringify(datas)
    };

    ajax_post('/calculate_production/', datas, function (resp) {
      if (resp.responseJSON["success"])
        set_info_prod(resp.responseJSON["datas"]);
      $('#smartwizard').smartWizard("loader", "hide");
    });
  }

  function set_info_prod(datas) {
    var month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    for (var i = 0; i < month.length; i++) {
      $('p.energy_prod_' + month[i]).text(datas["monthly_prod"][i]);
      $('p.energy_irrad_' + month[i]).text(datas["monthly_irrad"][i]);
    }
    $('p.energy_irrad_year').text(datas["yearly_irrad"]);
    $('p.energy_prod_year').text(datas["yearly_prod"]);
    $('p.energy_ratio_prod').text(datas["ratio"]);
  }

  // General Functions
  //###################################################################
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

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  function repsonse_null() {
    this.responseJSON = {
      "pass": true
    };
  }

  function ajax_post(url, form, callback) {
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

  function doAjax(url, data) {
    var resp
    $.ajax({
      async: false,
      url: url,
      type: 'POST',
      data: data,
      done: function (response) {
        return response;
      }
    }).done(function (response) {
      resp = response;
    });
    return resp;
  }

  function data_out_of_serialized_form(form) {
    var datas = {}
    var split = form.split('&');
    split.forEach(function (item) {
      datas[item.split('=')[0]] = item.split('=')[1];
    });

    return datas;
  }

  function extend(obj, src) {
    for (var key in src) {
      if (src.hasOwnProperty(key)) obj[key] = src[key];
    }
    return obj;
  }

})(jQuery); // End of use strict