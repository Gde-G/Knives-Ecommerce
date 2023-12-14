function password_show_hide(input, show_eye, hide_eye) {
    hide_eye.classList.remove("d-none");
    if (input.type === "password") {
        input.type = "text";
        show_eye.style.display = "none";
        hide_eye.style.display = "block";
    } else {
        input.type = "password";
        show_eye.style.display = "block";
        hide_eye.style.display = "none";
    }
};