function addToCart(event) {
  const artworkId = $(event.target).data("artwork-id");
  const quantity = $("#quantity").val();

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
    data: JSON.stringify({ order_uuid: order_uuid }),
    success: (data) => {
      if (data.success) {
        showToast(
          "Succès",
          "Oeuvre supprimée du panier",
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
    success: (data) => {
      if (data.success) {
        showToast("Succès", "Oeuvre supprimée", "bg-success text-white");
        reloadTable("#artwork-table-body");
      } else {
        showToast("Erreur", data.message, "bg-danger text-white");
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
    success: (data) => {
      if (data.success) {
        showToast("Succès", "Evènement supprimé", "bg-success text-white");
        reloadTable("#post-table-body");
      } else {
        showToast("Erreur", data.message, "bg-danger text-white");
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
    success: (data) => {
      const parsedHTML = $.parseHTML(data);
      const newTableBody = $(parsedHTML).find(content_ref).html();
      $(content_ref).html(newTableBody);
    },
    error: (xhr, status, error) => {
      console.error("Error:", error);
    },
  });
}

function deleteItem(url, itemId, itemType) {
  $.ajax({
    url: url,
    type: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    contentType: "application/json",
    data: JSON.stringify({ [`${itemType}_id`]: itemId }),
    success: (data) => {
      if (data.success) {
        $(`li[data-id="${itemId}"]`).remove();
        showToast(
          "Succès",
          `${
            itemType.charAt(0).toUpperCase() + itemType.slice(1)
          } supprimé avec succès`,
          "bg-success text-white"
        );
        reloadTable(`#${itemType}-list`);
      } else {
        showToast("Erreur", data.message, "bg-danger text-white");
        console.log(data.message);
      }
    },
    error: (xhr, status, error) => {
      showToast(
        "Erreur",
        `Erreur lors de la suppression de l'${itemType}`,
        "bg-danger text-white"
      );
      console.log("Une erreur est survenue lors de la suppression", error);
    },
  });
}

function showToast(title, message, className) {
  const toastId = "toast-" + Math.random().toString(36).substr(2, 9);
  const toastHTML = `
    <div id="${toastId}" class="toast ${className}" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="3000">
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
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Initialisation d'Alpine.js
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

  Alpine.data("settingsHandler", () => ({
    deleteItem,
  }));
});

$(document).ready(function () {
  new WOW().init();
});
