const FormConfirm = document.getElementById('form-confirm')

const submitButtons = FormConfirm.querySelectorAll('.submitBtn');

submitButtons.forEach(function(button) {
  button.addEventListener('click', function(event) {
    event.preventDefault(); 
    const statusBtn = button.getAttribute('data-process')
    $.ajax({
        url: "http://127.0.0.1:8000/checkout/".concat(TokenOrder).concat("/process-payment"),
        data: {
            "status": statusBtn     
        },
        dataType: 'json',
        success: function (data) {

            if (data.return === 'success'){
                window.location.href = "http://127.0.0.1:8000/checkout/".concat(TokenOrder).concat("/finished-payment");
            } else {
                console.log('error')
            }
            
        },
        error: function (xhr, status, error) {}
    });
  });
});





