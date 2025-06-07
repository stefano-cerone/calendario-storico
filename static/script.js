window.onload = function () {
  const giornoSelect = document.getElementById("giorno");
  const meseSelect = document.getElementById("mese");
  const risultatiDiv = document.getElementById("risultati");

  const nomiMesi = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"
  ];

  // Popola i menu giorno e mese
  for (let i = 1; i <= 31; i++) {
    const opt = document.createElement("option");
    opt.value = i;
    opt.text = i;
    giornoSelect.appendChild(opt);
  }

  for (let i = 0; i < 12; i++) {
    const opt = document.createElement("option");
    opt.value = i + 1;
    opt.text = nomiMesi[i];
    meseSelect.appendChild(opt);
  }

  window.cercaEventi = function () {
    const giorno = giornoSelect.value;
    const mese = meseSelect.value;

    risultatiDiv.innerHTML = `<h2>Eventi del ${giorno} ${nomiMesi[mese - 1]}</h2>`;

fetch(`/api/events?giorno=${giorno}&mese=${mese}`)

      .then(res => res.json())
      .then(data => {
        let eventi = data;

        // Applica filtro per anno se attivo
        const annoMin = parseInt(document.getElementById("anno-min")?.value);
        const annoMax = parseInt(document.getElementById("anno-max")?.value);

        if (annoMin || annoMax) {
          eventi = eventi.filter(ev => {
            if (annoMin && ev.anno < annoMin) return false;
            if (annoMax && ev.anno > annoMax) return false;
            return true;
          });
        }

        if (eventi.length === 0) {
          risultatiDiv.innerHTML += "<p>Nessun evento trovato.</p>";
        } else {
eventi.forEach(ev => {
  const eventoDiv = document.createElement("div");
  eventoDiv.className = "evento";
  eventoDiv.innerHTML = `
    <h3>${ev.titolo} (${ev.anno})</h3>
    <p><strong>${ev.anni_fa} anni fa</strong></p>
  `;
  eventoDiv.addEventListener("click", () => apriPopup(ev));
  risultatiDiv.appendChild(eventoDiv);
});

        }
      })
      .catch(err => {
        risultatiDiv.innerHTML += "<p style='color:red;'>Errore di connessione al server.</p>";
        console.error(err);
      });
  };
};

function apriPopup(ev) {
  const msg = encodeURIComponent(`${ev.titolo} (${ev.anno}) - ${ev.anni_fa} anni fa\nScopri di più su https://calendario-storico.onrender.com/}`);
  const whatsapp = `https://wa.me/?text=${msg}`;
  const contenuto = `
    <h2>${ev.titolo} (${ev.anno})</h2>
    <p><strong>${ev.anni_fa} anni fa</strong></p>
    <p>${ev.descrizione}</p>
    <img src="${ev.immagine_url}" alt="" style="max-width:100%; border-radius:10px; margin-top:10px;">
    <p><a href="${ev.link}" target="_blank">🔗 Approfondisci su Wikipedia</a></p>
    <p><a href="${whatsapp}" target="_blank" style="background:#25D366; color:white; padding:10px; border-radius:6px; text-decoration:none;">📤 Condividi su WhatsApp</a></p>
  `;
  document.getElementById("popup-contenuto").innerHTML = contenuto;
  document.getElementById("popup").style.display = "flex";
}

function chiudiPopup() {
  document.getElementById("popup").style.display = "none";
}


// Mostra/nasconde i dettagli
function toggleDettagli(elem) {
  const dettagli = elem.querySelector('.dettagli-evento');
  dettagli.style.display = (dettagli.style.display === 'block') ? 'none' : 'block';
}

// Mostra/nasconde il box del filtro anno
function toggleFiltroAnno() {
  const box = document.getElementById("box-filtro-anno");
  box.style.display = (box.style.display === "block") ? "none" : "block";
}

// Applica filtro richiamando la ricerca
function applicaFiltro() {
  if (typeof cercaEventi === "function") {
    cercaEventi();
  }
}
