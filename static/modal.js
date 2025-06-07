
// Crea dinamicamente il contenitore modale se non esiste
if (!document.getElementById("eventoModal")) {
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.id = "eventoModal";
  overlay.innerHTML = `
    <div class="modal-content">
      <span class="modal-close" onclick="chiudiModal()">&times;</span>
      <div id="modalDettagli"></div>
    </div>
  `;
  document.body.appendChild(overlay);
}

// Mostra il popup con i dettagli dell'evento
function mostraModal(ev) {
  const messaggio = encodeURIComponent(`${ev.titolo} (${ev.anno}) - ${ev.anni_fa} anni fa\n${ev.link}`);
  const whatsappLink = `https://wa.me/?text=${messaggio}`;

  const html = `
    <h2>${ev.titolo} (${ev.anno})</h2>
    <p><strong>${ev.anni_fa} anni fa</strong></p>
    <p>${ev.descrizione}</p>
    <img src="${ev.immagine_url}" alt="immagine evento" style="max-width:100%; border-radius:8px; margin-top:10px;">
    <p><a href="${ev.link}" target="_blank">🔗 Approfondisci su Wikipedia</a></p>
    <p><a href="${whatsappLink}" target="_blank" style="background:#25D366; color:white; padding:10px; border-radius:6px; text-decoration:none;">
      📤 Condividi su WhatsApp
    </a></p>
  `;
  document.getElementById("modalDettagli").innerHTML = html;
  document.getElementById("eventoModal").style.display = "flex";
}

// Chiude il popup
function chiudiModal() {
  document.getElementById("eventoModal").style.display = "none";
}
