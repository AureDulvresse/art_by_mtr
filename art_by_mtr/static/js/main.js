$(document).ready(function () {
  // Utilisation de jQuery pour l'initialisation de WOW.js
  new WOW().init();

  // Fonction pour ajouter au panier avec jQuery Ajax
  function addToCart(event) {
    const artworkId = event.target.getAttribute("data-artwork-id");

    $.ajax({
      url: '{% url "store:add-to-cart" %}',
      type: "POST",
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
      },
      contentType: "application/json",
      data: JSON.stringify({
        artwork_id: artworkId,
        quantity: 1,
      }),
      success: function (data) {
        alert(data.message);
      },
      error: function () {
        alert("Erreur lors de l'ajout au panier");
      },
    });
  }

  // Ajouter un événement click sur le bouton d'ajout au panier
  $(".btn-add-to-cart").on("click", function () {
    var artworkId = $(this).data("artwork-id");
    addToCart(artworkId);
  });
});
