// /home/siisi/e-commerce/static/js/prod_carousel.js

//Carouse / Reverse-cycling Script
document.addEventListener("DOMContentLoaded", function () {
  const carouselEl = document.getElementById("carouselExampleIndicators");

  // Manually initialize (no auto-slide unless we define it)
  const carousel = new bootstrap.Carousel(carouselEl, {
    interval: false, // disable Bootstrap's internal auto-slide
    wrap: true,
  });

  // Go backward every 5s
  setInterval(() => {
    carousel.prev();
  }, 3000);
});
