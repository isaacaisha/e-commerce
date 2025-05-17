// /home/siisi/e-commerce/static/js/prod_carousel.js

//Carouse / Reverse-cycling Script
document.addEventListener("DOMContentLoaded", function () {
  const carouselEl = document.getElementById("carouselExampleIndicators");

  const carousel = new bootstrap.Carousel(carouselEl, {
    interval: false, // no auto-slide
    wrap: true,
  });

  let intervalId = setInterval(() => {
    carousel.prev();
  }, 3000);

  // Pause on hover
  carouselEl.addEventListener("mouseenter", () => {
    clearInterval(intervalId);
  });

  // Resume on mouse leave
  carouselEl.addEventListener("mouseleave", () => {
    intervalId = setInterval(() => {
      carousel.prev();
    }, 3000);
  });
});
