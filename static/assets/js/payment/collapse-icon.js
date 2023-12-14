const btnApro = document.getElementById('btnAprovedCard');
const btnAproIconDown = btnApro.querySelectorAll('#icon-down')[0]
const btnAproIconUp =  btnApro.querySelectorAll('#icon-up')[0]

const btnPend = document.getElementById('btnPendingCard');
const btnPendIconDown = btnPend.querySelectorAll('#icon-down')[0]
const btnPendIconUp =  btnPend.querySelectorAll('#icon-up')[0]

const btnDeni = document.getElementById('btnDeniedCard');
const btnDeniIconDown = btnDeni.querySelectorAll('#icon-down')[0]
const btnDeniIconUp =  btnDeni.querySelectorAll('#icon-up')[0]

const collapseApro = new bootstrap.Collapse(document.getElementById('aprovedCard'), { toggle: false });
const collapsePend = new bootstrap.Collapse(document.getElementById('pendingCard'), { toggle: false });
const collapseDeni = new bootstrap.Collapse(document.getElementById('deniedCard'), { toggle: false });


function btnSecIcons(down, up) {
    down.style.display = 'inline-block';
    up.style.display = 'none';
}

function btnMainIcons(down, up) {
    down.style.display = down.style.display === 'none' ? 'inline-block' : 'none';
    up.style.display = up.style.display === 'none' ? 'inline-block' : 'none';
}

btnApro.addEventListener('click', function() {
    btnSecIcons(btnPendIconDown, btnPendIconUp);
    collapsePend.hide();
    btnSecIcons(btnDeniIconDown, btnDeniIconUp);
    collapseDeni.hide();
    btnMainIcons(btnAproIconDown, btnAproIconUp);
    collapseApro.toggle();
    
});

btnPend.addEventListener('click', function() {
    btnSecIcons(btnAproIconDown, btnAproIconUp);
    collapseApro.hide();
    btnSecIcons(btnDeniIconDown, btnDeniIconUp);
    collapseDeni.hide();
    btnMainIcons(btnPendIconDown, btnPendIconUp);
    collapsePend.toggle();
});

btnDeni.addEventListener('click', function() {
    btnSecIcons(btnAproIconDown, btnAproIconUp);
    collapseApro.hide();
    btnSecIcons(btnPendIconDown, btnPendIconUp);
    collapsePend.hide();
    btnMainIcons(btnDeniIconDown, btnDeniIconUp);
    collapseDeni.toggle();
});