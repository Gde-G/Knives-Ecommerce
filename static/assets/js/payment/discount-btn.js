const discounBtn = document.getElementById('discount-btn');
const discounInput = document.getElementById('id_discount_code');

const formPayment = document.getElementById('chosen-payment');
const contInput = document.getElementById('cont-input')

discounBtn.addEventListener('click', function(){
    discounInput.style.display = discounInput.style.display === 'none' ? 'inline-block' : 'none';
});

const allInputsRadio = formPayment.querySelectorAll('input[name="payment_kind"]');


formPayment.addEventListener('submit', function(event){
    event.preventDefault();
    var code_name = discounInput.value
    const data = new FormData(formPayment);
    let valueInput = "";
    for (const entry of data) {
        if(entry[0] === 'payment_kind'){
            valueInput = entry[1]
        }
    }
    if (code_name != ''){
        $.ajax({
            url: "http://127.0.0.1:8000/discount-codes",
            data: { "code_name": code_name },
            dataType: 'json',
            success: function (data) {
    
                if (data.result === 'success'){
                    formPayment.submit();
                    
                } else{
                    var errorCode = document.getElementById('error-code');
                    if (errorCode === null){
                        var messageError = document.createElement('span');
                        messageError.classList.add('text-secondary');
                        messageError.setAttribute('id', 'error-code')
                        messageError.textContent = 'El codigo de descuento ingresado no existe!';
                        contInput.append(messageError)

                        discounInput.value = null;
                        formPayment.reset()
                        allInputsRadio.forEach(input => {
                          if (input.value === valueInput) {
                            input.checked = true;
                          } else{
                            input.checked = false;
                          }
                        });
                    }
                }
            },
            error: function (xhr, status, error) {

            }
        })
    }
    else{
        formPayment.submit();
    }
})