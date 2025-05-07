// /home/siisi/e-commerce/static/js/base_product.js

// Check if button pressed
$(document).on("click", "#add-cart", function (e) {
  e.preventDefault();
  const url = $(this).data("url");
  const csrf = $(this).data("csrf");

  $.ajax({
    type: "POST",
    url: url,
    data: {
      product_id: $("#add-cart").val(),
      product_qty: $("#qty-cart option:selected").text(),
      csrfmiddlewaretoken: csrf,
      action: "post",
    },

    success: function (json) {
      //console.log(json)
      document.getElementById("cart_quantity").textContent = json.qty;
    },
    error: function (xhr, errmsg, err) {},
  });
});

// Update Quantity
$(document).on("click", ".update-cart", function (e) {
  e.preventDefault();
  // grab the product id
  const url = $(this).data("url");
  const csrf = $(this).data("csrf");
  const productid = $(this).data("index");

  $.ajax({
    type: "POST",
    url: url,
    data: {
      product_id: $(this).data("index"),
      product_qty: $("#select" + productid + " option:selected").text(),
      csrfmiddlewaretoken: csrf,
      action: "post",
    },

    success: function (json) {
      //console.log(json)
      //document.getElementById('cart_quantity').textContent = json.qty
      location.reload();
    },
    error: function (xhr, errmsg, err) {},
  });
});
