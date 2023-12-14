function createBootstrapAlert(message, alertType) {

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${alertType} alert-dismissible fade show`;
    alertDiv.role = 'alert';

    alertDiv.textContent = message;

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close';
    closeButton.classList.add('bg-primary');
    closeButton.setAttribute('data-bs-dismiss', 'alert');
    closeButton.setAttribute('aria-label', 'Close');

    alertDiv.appendChild(closeButton);

    const container = document.getElementById('alertContainer');
    container.appendChild(alertDiv);
}

const CategoryModal = new bootstrap.Modal(document.getElementById('addCategory'));
const CreateCategoryForm = document.getElementById("create-category"); 

const HandleModal = new bootstrap.Modal(document.getElementById('addHandle'));
const CreateHandleForm = document.getElementById("create-handle"); 

const DiscountModal = new bootstrap.Modal(document.getElementById('addDisCode'));
const CreateDiscountForm = document.getElementById("create-discount"); 

CreateCategoryForm.addEventListener('submit', function(event){
    event.preventDefault()
    let csrfToken = CreateCategoryForm.querySelector('input[name="csrfmiddlewaretoken"]').value
    
    let nameCate = CreateCategoryForm.querySelector('input[name="name"]').value
    let descriptionCate = CreateCategoryForm.querySelector('textarea[name="description"]').textContent
    
    $.ajax({
        url: '/add-category/', 
        type: 'POST', 
        data: {
            'name': nameCate,
            'description': descriptionCate    
        }, 
        headers: {
        
            "X-CSRFToken": csrfToken
        },
        success: function(result) {
            CategoryModal.hide()
            if (result.status === 'success'){
                createBootstrapAlert(result.message, 'success')
                CreateCategoryForm.reset()
            } else{
                createBootstrapAlert(result.message, 'danger')
                CreateCategoryForm.reset()
            }
        },
        error: function(xhr, status, error) {
            CategoryModal.hide()
        }
    });    
})

CreateHandleForm.addEventListener('submit', function(event){
    event.preventDefault()
    let csrfToken = CreateHandleForm.querySelector('input[name="csrfmiddlewaretoken"]').value
    let materialHand = CreateHandleForm.querySelector('input[name="material"]').value

     $.ajax({
      url: '/add-handle/', 
      type: 'POST',
      data: {
        'material': materialHand
      }, 
      headers: {
        "X-CSRFToken": csrfToken
      },
      success: function(result) {
        HandleModal.hide()
        if (result.status === 'success'){
            createBootstrapAlert(result.material.concat(' se a creado exitosamente!'), 'success')
            CreateHandleForm.reset()
        } else { 
            CreateHandleForm.reset()
            createBootstrapAlert(result.message, 'danger')
        }
        
      },
      error: function(xhr, status, error) {
        CategoryModal.hide()
      }
    });
})

CreateDiscountForm.addEventListener('submit', function(event){
    event.preventDefault()
    let csrfToken = CreateDiscountForm.querySelector('input[name="csrfmiddlewaretoken"]').value
    let code = CreateDiscountForm.querySelector('input[name="code"]').value
    let kind = CreateDiscountForm.querySelector('input[name="discount_kind"]').value
    let discount = CreateDiscountForm.querySelector('input[name="discount"]').value
    let enabledFrom = CreateDiscountForm.querySelector('input[name="enabled_from"]').value
    let enabledTo = CreateDiscountForm.querySelector('input[name="enabled_to"]').value

    $.ajax({
        url: '/add-dis-code/', 
        type: 'POST', 
        data: {
            'code': code,
            'discount_kind': kind,
            'discount': discount,
            'enabled_from': enabledFrom,
            'enabled_to': enabledTo
        }, 
        headers: {
        
            "X-CSRFToken": csrfToken
        },
        success: function(result) {
            DiscountModal.hide()
            if (result.status === 'success'){
                createBootstrapAlert(result.message, 'success')
                CreateDiscountForm.reset()
            } else {
                CreateDiscountForm.reset()
                createBootstrapAlert(result.message, 'danger')
            }
        
        },
        error: function(xhr, status, error) {
        
        }
    });
})