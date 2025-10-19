(function () {
  let scanner = null;
  let locked = false;

  function init() {
    const el = document.getElementById('qr-reader');
    if (!el) return;
    scanner = new Html5QrcodeScanner('qr-reader', { fps: 10, qrbox: { width: 250, height: 250 } }, false);
    scanner.render(onScanSuccess, onScanFailure);

    const manualBtn = document.getElementById('validateManualBtn');
    const manualInput = document.getElementById('manualKeyInput');
    if (manualBtn && manualInput) {
      manualBtn.addEventListener('click', function () {
        const v = manualInput.value.trim();
        if (v) validateTicket(v);
      });
    }
  }

  function onScanSuccess(decodedText) {
    if (locked) return;
    locked = true;
    try { if (scanner) scanner.clear(); } catch (e) {}
    validateTicket(decodedText);
  }

  function onScanFailure() { /* bruit normal, ne rien faire */ }

  function getCsrfToken() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input && input.value) return input.value;
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : null;
  }

  function validateTicket(finalKey) {
    const resultDiv = document.getElementById('validationResult');
    const csrftoken = getCsrfToken();

    fetch('/api/billets/valider/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken || ''
      },
      body: JSON.stringify({ final_key: finalKey })
    })
      .then(async (res) => {
        const data = await res.json().catch(() => ({}));
        return { ok: res.ok, data };
      })
      .then(({ ok, data }) => {
        if (!resultDiv) return;
        resultDiv.classList.remove('hidden');
        if (ok && data.success) {
          resultDiv.textContent = 'Billet validé: ' + (data.user_name || '');
        } else {
          resultDiv.textContent = 'Validation échouée: ' + (data.error || '');
        }
      })
      .catch((err) => {
        if (resultDiv) {
          resultDiv.classList.remove('hidden');
          resultDiv.textContent = 'Erreur: ' + err.message;
        }
      });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
