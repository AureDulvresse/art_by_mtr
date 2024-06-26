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
    success: (data) => {
      showToast("Succès", data.message, "bg-success text-white");
      $("#cart-items").html(data.cart_items_html);
    },
    error: (xhr, textStatus, error) => {
      showToast(
        "Erreur",
        "Erreur lors de l'ajout au panier",
        "bg-danger text-white"
      );
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
    success: (data) => {
      if (data.success) {
        showToast(
          "Succès",
          "Oeuvre supprimé du panier",
          "bg-success text-white"
        );

        $("#cart-items").html(data.cart_items_html);
        $("#cart-items-table").html(data.cart_items_table_html);
      } else {
        showToast(
          "Erreur",
          "Erreur lors de la suppression de l'article",
          "bg-danger text-white"
        );
      }
    },
    error: (xhr, textStatus, error) => {
      showToast(
        "Erreur",
        "Erreur lors de la suppression de l'article",
        "bg-danger text-white"
      );
      console.error(xhr.responseText, textStatus, error);
    },
  });
}

function deleteArtwork(artwork_id) {
  $.ajax({
    url: "/management/artworks/delete/",
    type: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    contentType: "application/json",
    data: JSON.stringify({ artwork_id: artwork_id }),
    success: function (data) {
      if (data.success) {
        showToast("Succès", "Oeuvre supprimée", "bg-success text-white");
        reloadTable("#artwork-table-body");
      } else {
        alert(data.message);
      }
    },
    error: (xhr, textStatus, error) => {
      showToast(
        "Erreur",
        "Erreur lors de la suppression de l'article",
        "bg-danger text-white"
      );
      console.error(xhr.responseText, textStatus, error);
    },
  });
}

function deletePost(post_id) {
   $.ajax({
     url: "/management/posts/delete/",
     type: "POST",
     headers: {
       "X-CSRFToken": getCookie("csrftoken"),
     },
     contentType: "application/json",
     data: JSON.stringify({ post_id: post_id }),
     success: function (data) {
       if (data.success) {
         showToast("Succès", "Evènement supprimé", "bg-success text-white");
         reloadTable("#post-table-body");
       } else {
         alert(data.message);
       }
     },
     error: (xhr, textStatus, error) => {
       showToast(
         "Erreur",
         "Erreur lors de la suppression de l'évènement",
         "bg-danger text-white"
       );
       console.error(xhr.responseText, textStatus, error);
     },
   });
}

function reloadTable(content_ref) {
  $.ajax({
    url: window.location.href,
    type: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
    success: function (data) {
      var parsedHTML = $.parseHTML(data);
      var newTableBody = $(parsedHTML).find(content_ref).html();
      $(content_ref).html(newTableBody);
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function showToast(title, message, className) {
  const toastId = "toast-" + Math.random().toString(36).substr(2, 9);
  const toastHTML = `
    <div id="${toastId}" class="toast ${className} wow animate__animated animate__fadeIn" data-wow-delay="0.5s" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">${title}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        ${message}
      </div>
    </div>
  `;

  $("#toast-container").append(toastHTML);
  const toastElement = new bootstrap.Toast(document.getElementById(toastId));
  toastElement.show();
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

  Alpine.data("artworkManager", () => ({
    deleteArtwork,
  }));

  Alpine.data("postManager", () => ({
    deletePost,
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
