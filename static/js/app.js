const elementNavBar = document.querySelector('.nav');
const navMenu = document.querySelector('.nav__menu');


setTimeout(()=>{
    document.body.setAttribute('data-id','hide');
},2000);

$('.header__menu').click((e)=>{

    e.target.classList.toggle('header__menu--close');
    elementNavBar.classList.toggle('nav--show');

});

// $('.nav__parent').click((e)=>{
//
//     const subMenu = document.querySelector('.nav__submenu');
//     const img =  document.querySelector('.nav__parent--img');
//
//     // const parent = $(this);
//     // const subMenu = parent.next('.nav__submenu'); // Busca el hermano inmediato con esa clase
//     // const img = parent.find('.nav__parent--img'); // Encuentra la imagen dentro del span
//
//     //if(window.innerWidth < 980){
//
//         e.currentTarget.classList.toggle('active');
//         let lenght = subMenu.clientHeight == 0? subMenu.scrollHeight : 0;
//         subMenu.style.height = `${lenght}px`;
//         img.classList.toggle('rotate');
//
//     //}
//
// });

$('.nav__parent').click(function () {
    const $parent = $(this);
    const $subMenu = $parent.next('.nav__submenu');
    const $img = $parent.find('.nav__parent--img');

    $parent.toggleClass('active');
    const newHeight = $subMenu[0].scrollHeight;
    const currentHeight = $subMenu.height();
    $subMenu.height(currentHeight === 0 ? newHeight : 0);
    $img.toggleClass('rotate');
});

const carouselSlide = document.querySelector('.carousel-slide');
const images = document.querySelectorAll('.carousel-slide img');

let counter = 1;
const size = images[0].clientWidth;

function slide() {
    carouselSlide.style.transition = 'transform 1s ease-in-out';
    carouselSlide.style.transform = `translateX(${-size * counter}px)`;

    counter++;

    if (counter === images.length) {
        counter = 0;
    }
}

setInterval(slide, 3000);