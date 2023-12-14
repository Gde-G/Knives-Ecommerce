
let frontImg = document.querySelector('.images-prod-show img')

const imgs = document.querySelectorAll('.img-select a');
const imgBtns = [...imgs];

let imgId = 1;


imgBtns.forEach((imgItem) => {
    imgItem.addEventListener('click', (event) => {
        event.preventDefault();
        imgSrc = imgItem.querySelector('img').getAttribute('src');
        slideImage()
    });
});

function slideImage() {
    let oldSrc = frontImg.getAttribute('src')

    if (oldSrc != imgSrc) {
        frontImg.setAttribute('src', imgSrc)
    }
}


