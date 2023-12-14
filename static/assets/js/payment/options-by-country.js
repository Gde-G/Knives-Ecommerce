// Options by Country
$(document).ready(function () {
    // Get the country input
    var countrySelected = $('#id_country');
    //Get the region input 
    var regionSelected = $('#id_region');
    //Get the city input
    var citySelected = $('#id_city');
    //Get phone number input-group-text

    //Event on the change of the country input
    countrySelected.change(function () {

        //Get the value of the country that be select
        var countryId = $(this).val()


        //AJAX request to get the regions query result 
        $.ajax({
            url: "http://127.0.0.1:8000/get-regions",
            data: { "country_id": countryId },
            dataType: 'json',
            success: function (data) {
                //Clean the default or previuslly choosen option in regions input 
                regionSelected.empty();
                console.log(regionSelected.firstChild ===undefined)
                //Add the options tag for each regios that we get
                $.each(data, function (key, value) {
                    regionSelected.append($('<option></option>').attr('value', key).text(value))
                });
                // Change the disabled attr
                $('#id_region').prop('disabled', false);
                var regionId = $('#id_region').val()

                $.ajax({
                    url: "http://127.0.0.1:8000/get-cities",
                    data: { "region_id": regionId },
                    dataType: 'json',
                    success: function (data) {
                    //Clean the default or previuslly choosen option in regions input 
                        citySelected.empty();
                        $('#id_city').prop('disabled', false);
                        //Add the options tag for each regios that we get
                        $.each(data, function (key, value) {
                            citySelected.append($('<option></option>').attr('value', key).text(value))
                        });

                    },
                    error: function (xhr, status, error) {

                    }
                });
            },
            error: function (xhr, status, error) {

            }
        });
    });
    //Event on the change of the country input
    regionSelected.change(function () {

        //Get the value of the country that be select
        var regionId = $(this).val()
        //AJAX request to get the regions query result 
        $.ajax({
            url: "http://127.0.0.1:8000/get-cities",
            data: { "region_id": regionId },
            dataType: 'json',
            success: function (data) {
                //Clean the default or previuslly choosen option in regions input 
                citySelected.empty();
                $('#id_city').prop('disabled', false);
                //Add the options tag for each regios that we get
                $.each(data, function (key, value) {
                    citySelected.append($('<option></option>').attr('value', key).text(value))
                });
                // Change the disabled attr

            },
            error: function (xhr, status, error) {

            }
        });
    });
});

