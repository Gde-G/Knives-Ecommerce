$(function () {
    $(document).on("change", ".upload-img", function () {
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
                uploadFile.closest(".img-portada").find('.img-preview-portada').css("background-image", "url(" + this.result + ")");
                uploadFile.closest(".img-portada").find('.img-portada-border').css("display", "none");
            }
        }

    });
});

$(function () {
    $(document).on("change", ".upload-img-sec", function () {
        var uploadFile = $(this);
        console.log(this)
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
                uploadFile.closest(".img-secondary-each").find('.img-preview').css("background-image", "url(" + this.result + ")");
                uploadFile.closest(".img-secondary-each").find('.img-secondary-each-border').css("display", "none");

            }
        }

    });
});