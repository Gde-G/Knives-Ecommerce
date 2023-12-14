$(document).ready(function() {
    var countrySelected = $("#id_country");
    var phoneInput = $("#id_phone_number");
    const country_code = document.getElementById('country_code');
    countrySelected.change(function () {
        var countryId = $(this).val();

        $.ajax({
            url: "http://127.0.0.1:8000/get-phone-code",
            data: { "country_id": countryId },
            dataType: 'json',
            success: function (data) {
                //Clean the default or previuslly choosen option in regions input 
                phoneInput.empty();
                
                //Add the options tag for each regios that we get
                $('#id_phone_number').prop('disabled', false);

                phoneInput.val(data.code_phone);
            },
            error: function (xhr, status, error) {

            }
        })
    });
})