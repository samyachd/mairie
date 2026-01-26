// Mets ici l'URL de ton backend (ex: "http://localhost:3000")
const API_BASE_URL = "http://localhost:3000";

// --- State ---
const state = {
  items: [],
  search: "",
  editingId: null,
};

// --- DOM ---
const $ = (sel) => document.querySelector(sel);

const searchInput = $("#searchInput");
const form = $("#productForm");
const nameInput = $("#nameInput");
const qtyInput = $("#qtyInput");
const priceInput = $("#priceInput");

const formTitle = $("#formTitle");
const submitBtn = $("#submitBtn");
const cancelEditBtn = $("#cancelEditBtn");
const messageEl = $("#message");
const tbody = $("#productsTbody");

// --- API ---
async function apiGetItems() {
  const res = await fetch(`${API_BASE_URL}/items`);
  if (!res.ok) throw new Error(`GET /items a échoué (${res.status})`);
  return res.json();
}

async function apiCreateItem(payload) {
  const res = await fetch(`${API_BASE_URL}/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`POST /items a échoué (${res.status})`);
  return res.json();
}

async function apiUpdateItem(id, payload) {
  const res = await fetch(`${API_BASE_URL}/items/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`PUT /items/${id} a échoué (${res.status})`);
  return res.json();
}

async function apiDeleteItem(id) {
  const res = await fetch(`${API_BASE_URL}/items/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`DELETE /items/${id} a échoué (${res.status})`);
}

// --- Utils ---
function setMessage(text, type = "") {
  messageEl.textContent = text;
  messageEl.className = `message ${type}`.trim();
}

function clearForm() {
  form.reset();
  qtyInput.value = "0";
  priceInput.value = "";
}

function enterEditMode(item) {
  state.editingId = item.id;
  formTitle.textContent = "Modifier le produit";
  submitBtn.textContent = "Enregistrer";
  cancelEditBtn.classList.remove("hidden");

  nameInput.value = item.name ?? "";
  qtyInput.value = String(item.quantity ?? 0);
  priceInput.value = item.price == null ? "" : String(item.price);
}

function exitEditMode() {
  state.editingId = null;
  formTitle.textContent = "Ajouter un produit";
  submitBtn.textContent = "Ajouter";
  cancelEditBtn.classList.add("hidden");
  clearForm();
}

// --- Render ---
function getFilteredItems() {
  const s = state.search.trim().toLowerCase();
  if (!s) return state.items;
  return state.items.filter((it) => (it.name ?? "").toLowerCase().includes(s));
}

function render() {
  const items = getFilteredItems();

  tbody.innerHTML = items
    .map((it) => {
      const price = it.price == null ? "-" : `${Number(it.price).toFixed(2)} €`;
      return `
        <tr data-id="${it.id}">
          <td>${escapeHtml(it.name ?? "")}</td>
          <td>${Number(it.quantity ?? 0)}</td>
          <td>${price}</td>
          <td>
            <button class="secondary" data-action="edit">Modifier</button>
            <button class="danger" data-action="delete">Supprimer</button>
          </td>
        </tr>
      `;
    })
    .join("");

  if (items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4">Aucun produit</td></tr>`;
  }
}

function escapeHtml(str) {
  return str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

// --- Events ---
searchInput.addEventListener("input", (e) => {
  state.search = e.target.value;
  render();
});

cancelEditBtn.addEventListener("click", () => {
  setMessage("");
  exitEditMode();
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  setMessage("");

  const payload = {
    name: nameInput.value.trim(),
    quantity: Number(qtyInput.value),
    price: priceInput.value === "" ? null : Number(priceInput.value),
  };

  // Validation simple côté frontend
  if (payload.name.length < 2) return setMessage("Nom trop court.", "err");
  if (!Number.isFinite(payload.quantity) || payload.quantity < 0)
    return setMessage("Quantité invalide.", "err");
  if (payload.price != null && (!Number.isFinite(payload.price) || payload.price < 0))
    return setMessage("Prix invalide.", "err");

  try {
    if (state.editingId == null) {
      const created = await apiCreateItem(payload);
      state.items.unshift(created);
      setMessage("Produit ajouté.", "ok");
      clearForm();
    } else {
      const updated = await apiUpdateItem(state.editingId, payload);
      state.items = state.items.map((it) => (it.id === state.editingId ? updated : it));
      setMessage("Produit modifié.", "ok");
      exitEditMode();
    }
    render();
  } catch (err) {
    setMessage(err.message ?? "Erreur inconnue.", "err");
  }
});

// Event delegation pour les boutons du tableau
tbody.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const tr = e.target.closest("tr");
  const id = tr?.getAttribute("data-id");
  if (!id) return;

  const item = state.items.find((it) => String(it.id) === String(id));
  const action = btn.getAttribute("data-action");

  if (action === "edit" && item) {
    setMessage("");
    enterEditMode(item);
    return;
  }

  if (action === "delete") {
    const ok = confirm("Supprimer ce produit ?");
    if (!ok) return;

    try {
      await apiDeleteItem(id);
      state.items = state.items.filter((it) => String(it.id) !== String(id));
      if (String(state.editingId) === String(id)) exitEditMode();
      setMessage("Produit supprimé.", "ok");
      render();
    } catch (err) {
      setMessage(err.message ?? "Erreur inconnue.", "err");
    }
  }
});

// --- Init ---
async function init() {
  try {
    clearForm();
    setMessage("Chargement...");
    state.items = await apiGetItems();
    setMessage("");
    render();
  } catch (err) {
    setMessage(
      `Impossible de charger les produits. Vérifie API_BASE_URL et ton backend. (${err.message})`,
      "err"
    );
  }
}

init();
