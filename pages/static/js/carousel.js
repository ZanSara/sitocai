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