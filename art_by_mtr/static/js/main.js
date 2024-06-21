// Fonction pour ajouter au panier avec jQuery Ajax
function addToCart(event) {
  const artworkId = $(event.target).data("artwork-id");
  const quantity = document.getElementById("quantity");

  $.ajax({
    url: "/store/cart/add-to-cart/",
    type: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    contentType: "application/json",
    data: JSON.stringify({
      artwork_id: artworkId,
      quantity: quantity.value,
    }),
    success: function (data) {
      Toastify({
        text: data.message,
        duration: 3000,
        close: true,
        gravity: "top",
        backgroundColor: "#2ecc71",
      }).showToast();
    },
    error: function (xhr, textStatus, error) {
      Toastify({
        text: "Erreur lors de l'ajout au panier",
        duration: 3000,
        close: true,
        gravity: "top",
        backgroundColor: "#e74c3c",
      }).showToast();
      console.error(xhr.responseText, textStatus, error);
    },
  });
}

function removeFromCart(orderUuid) {
  $.ajax({
    url: "/store/cart/remove-from-cart/",
    type: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    contentType: "application/json",
    data: JSON.stringify({
      order_uuid: orderUuid,
    }),
    success: function (data) {
      if (data.success) {
        Toastify({
          text: "Article supprimé du panier",
          duration: 3000,
          close: true,
          gravity: "top",
          backgroundColor: "#2ecc71",
        }).showToast();
        location.reload();
      } else {
        Toastify({
          text: "Erreur lors de la suppression de l'article",
          duration: 3000,
          close: true,
          gravity: "top",
          backgroundColor: "#e74c3c",
        }).showToast();
      }
    },
    error: function (xhr, textStatus, error) {
      Toastify({
        text: "Erreur lors de la suppression de l'article",
        duration: 3000,
        close: true,
        gravity: "top",
        backgroundColor: "#e74c3c",
      }).showToast();
      console.error(xhr.responseText, textStatus, error);
    },
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
                  alert(result.error.message);
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
