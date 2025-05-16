// /home/siisi/e-commerce/static/js/base_product.js

function showMessage(text, tag = "success") {
  const container = document.getElementById("message-container");
  const alert = document.createElement("div");
  alert.className = `alert alert-${tag} alert-dismissible fade show`;
  alert.role = "alert";
  alert.innerHTML = `
    ${text}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  container.prepend(alert);
}

$(function () {
  // ADD TO CART
  $(document).on("click", "#add-cart", function (e) {
    e.preventDefault();
    const btn = $(this);

    $.post(
      btn.data("url"),
      {
        action: "post",
        product_id: btn.val(),
        product_qty: $("#qty-cart").val(),
        csrfmiddlewaretoken: btn.data("csrf"),
      },
      function (json) {
        $("#cart_quantity").text(json.distinct_count);
        $("#cart_total_quantity").text(json.total_quantity);
        showMessage(json.message, "success");
      }
    );
  });

  // UPDATE QUANTITY IN CART SUMMARY
  $(document).on("click", ".update-cart", function (e) {
    e.preventDefault();
    const checkoutUrl = $("#cart-wrapper").data("checkout-url");
    const btn = $(this),
      pid = btn.data("index"),
      newQty = $(`#select${pid}`).val();

    $.post(
      btn.data("url"),
      {
        action: "post",
        product_id: pid,
        product_qty: newQty,
        csrfmiddlewaretoken: btn.data("csrf"),
      },
      function (json) {
        $("#cart_quantity").text(json.distinct_count);
        $("#cart_total_quantity").text(json.total_quantity);

        // 👇 Re-render the #cart-total without touching the data attribute
        $("#cart-total").html(
          `<h3>Total: $${json.cart_total}</h3>
           <a href="${checkoutUrl}" class="btn btn-success mt-2">Checkout</a>`
        );

        showMessage(json.message, "info");
      }
    );
  });

  // DELETE ITEM CARD
  $(document).on("click", ".delete-cart", function (e) {
    e.preventDefault();
    const checkoutUrl = $("#cart-wrapper").data("checkout-url"); // 👈 FIXED
    const btn = $(this),
      pid = btn.data("index");

    $.post(
      btn.data("url"),
      {
        action: "post",
        product_id: pid,
        csrfmiddlewaretoken: btn.data("csrf"),
      },
      function (json) {
        $("#cart_quantity").text(json.distinct_count);
        $("#cart_total_quantity").text(json.total_quantity);

        $("#cart-total").html(
          `<h3>Total: $${json.cart_total}</h3>
           <a href="${checkoutUrl}" class="btn btn-success mt-2">Checkout</a>`
        );

        $(`#cart-card-${pid}`).fadeOut(200, function () {
          $(this).remove();
        });

        showMessage(json.message, "warning");
      }
    );
  });
});
