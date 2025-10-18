// JS offres: ajout au panier en AJAX (sans CSS inline)
(function () {
  function getCsrfToken() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input && input.value) return input.value;
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : null;
  }

  function addToCart(offerId) {
    const btn = (typeof event !== 'undefined' && event.target) ? event.target : null;
    const previousLabel = btn ? btn.innerHTML : null;
    if (btn) { btn.disabled = true; btn.innerText = 'Ajout...'; }

    const csrftoken = getCsrfToken();
    if (!csrftoken) {
      alert('Erreur de sécurité: CSRF manquant. Veuillez recharger la page.');
      if (btn) { btn.disabled = false; btn.innerHTML = previousLabel; }
      return;
    }

    fetch('/panier/ajouter/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      },
      body: JSON.stringify({ offer_id: offerId, quantity: 1 })
    })
      .then(async (res) => {
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.message || `HTTP ${res.status}`);
        return data;
      })
      .then((data) => {
        updateCartCounter(data.cart_total);
        alert(data.message || 'Article ajouté au panier');
      })
      .catch((err) => {
        alert('Ajout au panier impossible: ' + err.message);
      })
      .finally(() => {
        if (btn) { btn.disabled = false; btn.innerHTML = previousLabel; }
      });
  }

  function updateCartCounter(count) {
    if (typeof count !== 'number') return;
    const el1 = document.getElementById('cart-counter');
    const el2 = document.getElementById('cart-counter-mobile');
    if (el1) el1.textContent = String(count);
    if (el2) el2.textContent = String(count);
  }

  window.addToCart = addToCart;
})();
