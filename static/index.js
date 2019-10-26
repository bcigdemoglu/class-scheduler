let current_slot_count = 1;
let selected_table = {};
let loading_count = 0;

function loading() {
  $("#loading").css('width','200');
  $("#loading").css('height','200');
  loading_count++;
}

function done_loading() {
  loading_count--;
  if (loading_count === 0) {
    $("#loading").css('height','0');
  }
}

async function disableOtherSlots(slot_count) {
  for (let sibling_slot = 0; sibling_slot < slot_count; sibling_slot++) {
    loading();
    console.log(`getting classes for slot ${slot_count} to disable`);
    $.getJSON('/get_classes/', {
      picked_slot: sibling_slot
    }, function(data) {
      $(`#slot${sibling_slot} > option`).each(function() {
        if (!data.CLASSES.includes(this.value)) {
          $(this).attr('disabled','disabled');
        }
      });
      done_loading()
    });
  } 
}

async function formSlot(class_names, slot_number, slot_count) {
  const slotId = `slot${slot_number}`;
  const selectOpts = {
    id: slotId,
    size: class_names.length,
    width: 200
    // multiple: true
  };
  const slot = $('<select />', selectOpts);
  for (const class_name of class_names) {
    const optionsOpts = {value: class_name, text: class_name};
      $('<option />', optionsOpts).appendTo(slot);
  }

  console.log("done with classes, adding listener to slot "+ slot_number);
  
  $(slot).change(function() {
    const class_name = $(`#${slotId} option:selected`).text();
    if (selected_table[class_name]) {
      // Do no run if already picked
      return;
    }
    $(`#${slotId} option:selected`).css("background-color", "lightgreen")
                                   .removeAttr("selected");
    // Processing
    $(slot).css('opacity', 0.3);
    loading();
    $.getJSON('/select_class/', {
      class_name,
      picked_slot: slot_number
    }, async function(data) {
      console.log(`selected class ${class_name}, getting classes for slots`);
      selected_table[class_name] = true;
      // Disable other slots based on selection
      await disableOtherSlots(slot_count);
      // Done process
      $(slot).css('opacity', 1);
      done_loading();
    });

  });

  const slotdiv = $("<div />", {class: "slotDiv"});
  $( "p" ).add( `<span>Slot ${slot_number + 1}\t\t</span>` ).appendTo(slotdiv);
  slot.appendTo(slotdiv);
  $("<br/>").appendTo(slotdiv);
  slotdiv.appendTo('body');
}

async function setupSlots(slot_count) {
  for (let slot_number = 0; slot_number < slot_count; slot_number++) {
    // Processing
    loading();
    console.log("getting classes for slot "+ slot_number);
    $.getJSON('/get_classes/', {
      picked_slot: slot_number
    }, async function(data) {
      console.log("done gettin classes, forming up slot "+ slot_number);
      await formSlot(data.CLASSES, slot_number, slot_count);
      done_loading();
    });
  }
}

$(function () {

  $('a#load_excel').bind('click', function() {
    // Processing
    $("#excel_form").css('opacity', 0.3);
    loading();
    const excel_data = $('[name="excel_data"]').val();
    current_slot_count = $('[name="slot_count"]').val();
    // const excel_data = 'Physics\tChemistry\tBusiness\nPhysics\tChemistry\tEcon\nPhysics\tCS\tEcon\nChemistry\tBiology\tEcon'
    // current_slot_count = 5

    console.log("loading excel");
    $.getJSON('/load_excel/', {
      excel_data,
      slot_count: current_slot_count,
    }, async function() {
      console.log("loaded excel, setting up slots");
      await setupSlots(current_slot_count);
      // Done process
      done_loading();
      $("#excel_form").css('opacity', 0.7);
      $('a#load_excel').remove();
    });
    return false;
  });
  
  $('a#reset_schedule').bind('click', function() {
    $("select").css('opacity', 0.3);
    loading();
    $.getJSON('/reset_schedule/', {}, async function() {
      // Cleanup
      selected_table = {};
      $(".slotDiv").remove();
      const slot_count = $('input[name="slot_count"]').val();
      await setupSlots(slot_count);
      // Done process
      done_loading();
    });
    return false;
  });
});