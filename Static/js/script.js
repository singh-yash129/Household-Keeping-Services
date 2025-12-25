const container = document.getElementById('container');
const arrowBack = document.getElementById('backward');
const arrowForward = document.getElementById('forward'); 

arrowBack.addEventListener('click', () => {
  container.scrollBy({
    left: -300, 
    behavior: 'smooth'
  });
});

arrowForward.addEventListener('click', () => {
  container.scrollBy({
    left: 300, 
    behavior: 'smooth'
  });
});

function checkArrows() {
  arrowBack.classList.toggle('disabled', container.scrollLeft === 0);
  
  arrowForward.classList.toggle('disabled', container.scrollLeft + container.clientWidth >= container.scrollWidth);
}

container.addEventListener('scroll', checkArrows);
window.addEventListener('load', checkArrows);
