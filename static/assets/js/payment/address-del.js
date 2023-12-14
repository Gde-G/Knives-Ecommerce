const deleteButtons = document.querySelectorAll('.delete-address-btn');
deleteButtons.forEach(button => {
  button.addEventListener('click', function(event) {
    event.preventDefault();

    const addressId = this.dataset.addressId;
    console.log(addressId)
    $.ajax({
        url:"http://127.0.0.1:8000/checkout/".concat(OrderToken).concat("/shipping/del-address/").concat(addressId),
        success: function(data){
            console.log(data)
            if (data.result === 'success'){
                const parentContainer = document.getElementById(addressId);
                console.log(parentContainer);
                console.log('HEREE')
                parentContainer.remove()
            }else{

            }
        },
        error: function (xhr, status, error) {

        }
    })
  });
});