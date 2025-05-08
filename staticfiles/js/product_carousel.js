// /home/siisi/e-commerce/static/js/prod_carousel.js

//Carouse / Reverse-cycling Script
document.addEventListener("DOMContentLoaded", function () {
  var carouselEl = document.getElementById("carouselExampleIndicators");
  var carousel = new bootstrap.Carousel(carouselEl, {
    interval: 3000, // 3s between slides
    wrap: true,
  });
  // Call prev() every interval to go backwards
  setInterval(function () {
    carousel.prev();
  }, 3000);
});
