function requesting_checkbox_pressed() {
    var $radiobuttongroup = $(this).parent().next().next().next()
    var $itemid = $(this).parent().parent().attr('id')
    if ($(this).prop("checked")) {
        $radiobuttongroup.show()
        var $radiobuttons = $radiobuttongroup.children()
        $radiobuttons.each(function (i) {
            var $radiobutton = $(this).children().get(0)
            if ($radiobutton.checked) {
                switch (parseInt($radiobutton.value)) {
                    case 1:
                        $("#" + $itemid + "_new").show();
                        break;
                    case 2:
                        $("#" + $itemid + "_existing").show();
                        break;
                }
            }
        })
    } else {
        $radiobuttongroup.hide()
        $("#" + $itemid + "_new").hide();
        $("#" + $itemid + "_existing").hide();
    }
}

function new_or_existing_radiobutton_pressed() {
    var $itemid = $(this).parent().parent().parent().attr('id')
    switch (parseInt($(this).prop("value"))) {
        case 1:
            $("#" + $itemid + "_new").show();
            $("#" + $itemid + "_existing").hide();
            break;
        case 2:
            $("#" + $itemid + "_new").hide();
            $("#" + $itemid + "_existing").show();
            break;
        case 3:
            $("#" + $itemid + "_new").hide();
            $("#" + $itemid + "_existing").hide();
            break;
    }
}

// credit from here on goes to rmed
// https://www.rmedgar.com/blog/dynamic-fields-flask-wtf/

function replaceTemplateIndex(value, index) {
    const ID_RE = /(custom_items-)_/
    return value.replace(ID_RE, '$1'+index);
}

function adjustIndices(removedIndex) {
    var $forms = $('.form-custom_item');

    $forms.each(function(i) {
        var $form = $(this);
        var index = parseInt($form.data('index'));
        var newIndex = index - 1;

        if (index < removedIndex) {
            // Skip
            return true;
        }

        // This will replace the original index with the new one
        // only if it is found in the format -num-, preventing
        // accidental replacing of fields that may have numbers
        // intheir names.
        var regex = new RegExp('(custom_items-)'+index);
        var repVal = '$1'+newIndex;

        // Change ID in form itself
        $form.attr('id', $form.attr('id').replace(index, newIndex));
        $form.data('index', newIndex);

        // Change IDs in form fields
        $form.find('label, input, select, textarea').each(function(j) {
            var $item = $(this);

            if ($item.is('label')) {
                // Update labels
                $item.attr('for', $item.attr('for').replace(regex, repVal));
                return;
            }

            // Update other fields
            $item.attr('id', $item.attr('id').replace(regex, repVal));
            $item.attr('name', $item.attr('name').replace(regex, repVal));
        });
    });
}

function remove_custom_entry() {
    var $removed_entry = $(this).closest('.form-custom_item');
    var removedIndex = parseInt($removed_entry.data('index'));

    $removed_entry.remove();

    // Update indices
    adjustIndices(removedIndex);
}

function add_custom_entry() {
    var $template_form = $("#custom_items-_")
    var $last_entry = $('.form-custom_item').last();
    console.log($last_entry);

    var new_index = 0;
    
    if ($last_entry.length > 0) {
        new_index = parseInt($last_entry.data('index')) + 1;
    }

    var $new_form = $template_form.clone()

    console.log("New Index: " + new_index)

    $new_form.attr('id', replaceTemplateIndex($new_form.attr('id'), new_index));
    $new_form.data('index', new_index)

    console.log("NewFormData Index: " + $new_form.data('index'))
    console.log("NewFormData ID: " + $new_form.data('id'))

    $new_form.find('label, input, select, textarea').each(function(idx) {
        var $item = $(this);

        if ($item.is('label')) {
            // Update labels
            $item.attr('for', replaceTemplateIndex($item.attr('for'), new_index));
            return;
        }

        // Update other fields
        $item.attr('id', replaceTemplateIndex($item.attr('id'), new_index));
        $item.attr('name', replaceTemplateIndex($item.attr('name'), new_index));
    });

    $("#custom_items-container").append($new_form);

    $new_form.addClass('form-custom_item');
    $new_form.removeClass('custom_items-template');

    $new_form.find('.remove-custom_item').click(remove_custom_entry);

    $new_form.show();
}

$(document).ready(function () {
    $(".form-requesting").click(requesting_checkbox_pressed);
    $(".form-new_or_existing").click(new_or_existing_radiobutton_pressed);
    $(".remove-custom_item").click(remove_custom_entry);
    $("#append").click(add_custom_entry);
});