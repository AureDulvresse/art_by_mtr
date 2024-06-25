function addToCart(event) {
  const artworkId = $(event.target).data("artwork-id");
  const quantity = document.getElementById("quantity").value;

  $.ajax({
    url: "/store/cart/add-to-cart/",
    type: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    contentType: "application/json",
    data: JSON.stringify({
      artwork_id: artworkId,
      quantity: quantity,
    }),
    success: function (data) {
      showToast("Succès", data.message, "bg-success");
      $("#cart-items").html(data.cart_items_html);
    },
    error: function (xhr, textStatus, error) {
      showToast("Erreur", "Erreur lors de l'ajout au panier", "bg-danger");
      console.error(xhr.responseText, textStatus, error);
    },
  });
}

function removeFromCart(order_uuid) {
  $.ajax({
    url: "/store/cart/remove-from-cart/",
    type: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    contentType: "application/json",
    data: JSON.stringify({
      order_uuid: order_uuid,
    }),
    success: function (data) {
      if (data.success) {
        showToast("Succès", "Article supprimé du panier", "bg-success");
        $("#cart-items").html(data.cart_items_html);
      } else {
        showToast(
          "Erreur",
          "Erreur lors de la suppression de l'article",
          "bg-danger"
        );
      }
    },
    error: function (xhr, textStatus, error) {
      showToast(
        "Erreur",
        "Erreur lors de la suppression de l'article",
        "bg-danger"
      );
      console.error(xhr.responseText, textStatus, error);
    },
  });
}

function showToast(title, message, toastClass) {
  const toastContainer = document.getElementById("toast-container");
  const toastId = `toast-${Date.now()}`;
  const toastHtml = `
    <div id="${toastId}" class="toast ${toastClass} text-white" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">${title}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        ${message}
      </div>
    </div>
  `;
  toastContainer.insertAdjacentHTML("beforeend", toastHtml);

  const toastElement = document.getElementById(toastId);
  const bootstrapToast = new bootstrap.Toast(toastElement);
  bootstrapToast.show();

  // Remove toast element after it's hidden
  toastElement.addEventListener("hidden.bs.toast", () => {
    toastElement.remove();
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Recherche du jeton CSRF par son nom
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function stripePayment() {
  return {
    stripe: null,
    initStripe() {
      this.stripe = Stripe("{{ stripe_public_key }}");
    },
    checkout() {
      $.ajax({
        url: "/stripe/create-checkout-session/",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          // any additional data you want to send to the server
        }),
        success: (response) => {
          if (response.id) {
            this.stripe
              .redirectToCheckout({ sessionId: response.id })
              .then((result) => {
                if (result.error) {
                  showToast("Erreur", result.error.message, "bg-danger");
                }
              });
          } else {
            console.error("Error:", response);
          }
        },
        error: (xhr, status, error) => {
          console.error("Error:", error);
        },
      });
    },
  };
}

// Initier Alpine.js
document.addEventListener("alpine:init", () => {
  Alpine.data("cartHandler", () => ({
    addToCart,
    removeFromCart,
  }));
  Alpine.data("stripePayment", () => ({
    stripePayment,
  }));
});

// Utilisation avec jQuery pour la gestion de l'événement
$(document).ready(function () {
  // Utilisation de jQuery pour l'initialisation de WOW.js
  new WOW().init();
});
