
//const carousel = document.getElementById('carousel')
//const items = carousel.querySelectorAll('.carousel-item');
//let currentItem = 0;
//let isActive = true;
/*
function hideItem(direction, slideId, slides) {
  //slides[slideId].classList.add(direction);
  //slides[slideId].addEventListener('animationend', function() {
    //this.classList.remove('active', direction);
  //});
  for (slide of slides){
    slide.classList.remove('active');
  }
  slides[slideId].classList.remove('active', direction);
}

function showItem(direction, slideId, slides) {
  //slides[slideId].classList.add('next', direction);
  
  //slides[slideId].classList.remove('next', direction);
  slides[slideId].classList.add('active');

  /*
  slides[slideId].addEventListener('animationend', function() {
    this.classList.remove('next', direction);
    this.classList.add('active');
  });/
}

function setCurrentIndex(slideId, slides, carousel){
  carousel.dataset.activeSlide = slideId % slides.length;
  console.log(carousel.dataset.activeSlide = slideId % slides.length);
}

function move(hide, show, carouselId, direction){
  const carousel = document.getElementById(carouselId)
  const slides = carousel.querySelectorAll('.slide');
  const slideId = carousel.dataset.activeSlide;
  hideItem(hide, slideId, slides, carousel);
  showItem(show, slideId, slides, carousel);
  setCurrentIndex(slideId+direction, slides, carousel);
}

function moveRight(carouselId){
  move('to-left', 'from-right', carouselId, 1);
}

function moveLeft(carouselId){
  move('to-right', 'from-left', carouselId, -1);
}
*/

function moveRight(carouselId){
  const carousel = document.getElementById(carouselId)
  const slides = carousel.querySelectorAll('.slide');
  
  var slideId = +carousel.dataset.activeSlide+1;
  if (slideId >= slides.length){
    slideId = 0;
  }
  carousel.dataset.activeSlide = slideId;

  for (slide of slides){
    slide.classList.remove('active');
  }
  slides[slideId].classList.add('active');
}

function moveLeft(carouselId){
  const carousel = document.getElementById(carouselId)
  const slides = carousel.querySelectorAll('.slide');
  
  var slideId = +carousel.dataset.activeSlide-1;
  if (slideId < 0){
    slideId = slides.length-1;
  }
  carousel.dataset.activeSlide = slideId;

  for (slide of slides){
    slide.classList.remove('active');
  }
  slides[slideId].classList.add('active');
}