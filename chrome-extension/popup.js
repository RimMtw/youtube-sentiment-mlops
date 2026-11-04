const API = "http://127.0.0.1:8000";
const NOMS = { "1": "Positif", "0": "Neutre", "-1": "Négatif" };
let resultats = [];
let filtre = "all";

const $ = (id) => document.getElementById(id);

// Mode sombre / clair (mémorisé)
function appliquerTheme(sombre) {
  document.body.classList.toggle("sombre", sombre);
  $("theme").textContent = sombre ? "☀️" : "🌙";
  localStorage.setItem("sombre", sombre);
}
appliquerTheme(localStorage.getItem("sombre") === "true");
$("theme").onclick = () => appliquerTheme(!document.body.classList.contains("sombre"));

// Message de chargement ou d'erreur
function message(texte, erreur = false) {
  $("message").textContent = texte;
  $("message").className = erreur ? "erreur" : "";
}

// Analyse : extraction -> API -> affichage
$("analyser").onclick = async () => {
  message("Chargement...");
  $("resultats").hidden = true;
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const rep = await chrome.tabs.sendMessage(tab.id, { action: "getComments" });
    const comments = rep.comments.slice(0, 500);
    if (!comments.length) return message("Aucun commentaire visible. Faites défiler la page.", true);

    const r = await fetch(`${API}/predict_batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ comments }),
    });
    if (!r.ok) throw new Error(`erreur API (${r.status})`);
    const data = await r.json();

    resultats = data.predictions;
    afficherStats(data.stats);
    afficherListe();
    $("resultats").hidden = false;
    message(`${data.stats.total} commentaires analysés`);
  } catch (e) {
    message(`Erreur : ${e.message}. Vérifiez que l'API tourne et rechargez la page YouTube.`, true);
  }
};

// Statistiques globales (barres)
function afficherStats(s) {
  $("stats").innerHTML = ["1", "0", "-1"].map((k) => `
    <div class="ligne">
      <span>${NOMS[k]}</span>
      <div class="barre"><div class="rempli" data-k="${k}" style="width:${s.percentages[k]}%"></div></div>
      <span>${s.percentages[k]}% (${s.counts[k]})</span>
    </div>`).join("");
}

// Liste des commentaires (filtrée)
function afficherListe() {
  const ul = $("liste");
  ul.innerHTML = "";
  resultats
    .filter((p) => filtre === "all" || String(p.label) === filtre)
    .forEach((p) => {
      const li = document.createElement("li");
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.dataset.k = p.label;
      tag.textContent = NOMS[p.label] + (p.confidence != null ? ` · ${Math.round(p.confidence * 100)}%` : "");
      const texte = document.createElement("p");
      texte.textContent = p.comment;
      li.append(tag, texte);
      ul.append(li);
    });
}

// Filtres par sentiment
document.querySelectorAll("#filtres button").forEach((b) => {
  b.onclick = () => {
    filtre = b.dataset.f;
    document.querySelectorAll("#filtres button").forEach((x) => x.classList.toggle("actif", x === b));
    afficherListe();
  };
});

// Copier les résultats
$("copier").onclick = async () => {
  const texte = resultats.map((p) => `${NOMS[p.label]}\t${p.comment}`).join("\n");
  await navigator.clipboard.writeText(texte);
  message("Résultats copiés");
};

// Export CSV
$("exporter").onclick = () => {
  const csv = "label,comment\n" + resultats.map((p) => `${p.label},"${p.comment.replace(/"/g, '""')}"`).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
  a.download = "sentiments.csv";
  a.click();
};