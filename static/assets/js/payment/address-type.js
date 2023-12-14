// Display inputs if type is appartment

$(document).ready(function () {
    $('#apartment-flor').hide();
    $('#apartment-id').hide();

    $('#id_address_type').change(function () {
        if ($(this).val() == 'apartment') {
            $('#apartment-flor').show();
            $('#apartment-id').show();
        } else {
            $('#apartment-flor').hide();
            $('#apartment-id').hide();
        }
    });
});