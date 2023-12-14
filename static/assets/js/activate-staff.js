const FormStaff = document.getElementById('staff-form')
const containerStaff = document.getElementsByClassName('staff-setup')[0]
FormStaff.addEventListener('submit', function(event){
    event.preventDefault()
    const formData = new FormData(FormStaff);

    $.ajax({
        url: 'http://127.0.0.1:8000/setup-staff/',
        method: 'post',
        headers: {
        'X-CSRFToken': getCookie('csrftoken'), 
        },
        data:{
            username: formData.get('username'),
            password: formData.get('password'),
            email: formData.get('email'),
        },
        success: function(result){
            if (result.status === 'success'){
                FormStaff.style.display = 'none'
                var sendIt = document.createElement('div');
                sendIt.classList.add('row');
                sendIt.classList.add('send-it');
                var colIcon = document.createElement('div');
                colIcon.classList.add('col-12');
                colIcon.classList.add('col-sm-3');
                colIcon.classList.add('col-md-2');
                colIcon.classList.add('text-center');
                var icon = document.createElement('i');
                icon.classList.add('fa-solid');
                icon.classList.add('fa-circle-check');
                var colText = document.createElement('div');
                colText.classList.add('col-12');
                colText.classList.add('col-sm-9');
                colText.classList.add('col-md-10');
                colText.classList.add('text-center');
                var row1 = document.createElement('div');
                row1.classList.add('row');
                row1.classList.add('w-100');
                row1.classList.add('text-center');
                var textRow1 = document.createElement('span');
                textRow1.textContent = "Le enviamos el mail a ".concat(result.email).concat("; con el link para que pueda activar su cuenta como Staff.");
                var row2 = document.createElement('div');
                row2.classList.add('row');
                row2.classList.add('w-100');
                row2.classList.add('text-center');
                var textRow2 = document.createElement('small');
                textRow2.classList.add('w-100');
                textRow2.classList.add('text-muted');
                textRow2.classList.add('mx-auto');
                textRow2.textContent = "Recuerde revisar la casilla de SPAM."

                sendIt.append(colIcon)
                colIcon.append(icon)
                sendIt.append(colText)
                colText.append(row1);
                row1.append(textRow1);
                colText.append(row2);
                row2.append(textRow2)

                containerStaff.append(sendIt)
                sendIt.offsetHeight;

                sendIt.classList.add('show');
            }else{

                const InputElem = document.getElementById('id_email') 
                const parentInput = InputElem.parentElement

                InputElem.classList.add('border-4');

                var errorElem = document.createElement('span');
                errorElem.classList.add('text-secondary');
                errorElem.classList.add('bg-white');
                errorElem.classList.add('px-2');


                var icon = document.createElement('i');
                icon.classList.add('fa-solid');
                icon.classList.add('fa-circle-xmark');
                icon.classList.add('me-2');

                errorElem.append(icon)

                var textElem = document.createElement('span');
                textElem.textContent = result.text

                errorElem.append(icon)
                errorElem.append(textElem)
                parentInput.append(errorElem)
            }
        },
        error: function (xhr, status, error) {

        }
    })
})
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}