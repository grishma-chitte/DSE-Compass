/* =============================================
   DSE-Compass — Main Application Logic
   ============================================= */

// Compare list stored in localStorage
let compareList = JSON.parse(localStorage.getItem("dse_compare") || "[]");

function saveCompare() {
  localStorage.setItem("dse_compare", JSON.stringify(compareList));
  updateCompareBadges();
}

function updateCompareBadges() {
  document.querySelectorAll("[data-compare-count]").forEach(el => {
    el.textContent = compareList.length;
  });
}

/* ---------- Mobile Nav Toggle ---------- */
function initNav() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => links.classList.toggle("open"));
  }
}

/* ---------- Search & Filter Logic ---------- */
function getFilters() {
  return {
    name: (document.getElementById("filter-name")?.value || "").toLowerCase().trim(),
    district: document.getElementById("filter-district")?.value || "",
    type: document.getElementById("filter-type")?.value || "",
    branch: document.getElementById("filter-branch")?.value || "",
    minCutoff: parseFloat(document.getElementById("filter-min")?.value) || 0,
    maxCutoff: parseFloat(document.getElementById("filter-max")?.value) || 100,
    sort: document.getElementById("sort-by")?.value || "cutoff-desc"
  };
}

function filterColleges() {
  const f = getFilters();
  let results = COLLEGES.filter(c => {
    if (f.name && !c.name.toLowerCase().includes(f.name)) return false;
    if (f.district && c.district !== f.district) return false;
    if (f.type && c.type !== f.type) return false;
    if (f.branch && !c.branches.some(b => b.toLowerCase().includes(f.branch.toLowerCase()))) return false;
    if (c.cutoff < f.minCutoff || c.cutoff > f.maxCutoff) return false;
    return true;
  });

  // Sort
  results.sort((a, b) => {
    switch (f.sort) {
      case "cutoff-asc": return a.cutoff - b.cutoff;
      case "package-desc": return b.avgPackage - a.avgPackage;
      case "fees-asc": return a.fees - b.fees;
      case "name-asc": return a.name.localeCompare(b.name);
      default: return b.cutoff - a.cutoff; // cutoff-desc
    }
  });

  return results;
}

function renderCollegeCard(c) {
  const inCompare = compareList.includes(c.id);
  return `
    <article class="college-card" data-id="${c.id}">
      <div class="card-top">
        <h3><a href="details.html?id=${c.id}">${c.name}</a></h3>
        <span class="badge ${typeBadgeClass(c.type)}">${c.type}</span>
      </div>
      <div class="card-location">📍 ${c.district}</div>
      <div class="card-metrics">
        <div class="metric">
          <div class="val">${c.cutoff}%</div>
          <div class="key">Approx. Cutoff</div>
        </div>
        <div class="metric">
          <div class="val">${c.avgPackage} LPA</div>
          <div class="key">Avg Package</div>
        </div>
        <div class="metric">
          <div class="val">${formatFees(c.fees)}</div>
          <div class="key">Annual Fees</div>
        </div>
        <div class="metric">
          <div class="val">${c.placementPct}%</div>
          <div class="key">Placement</div>
        </div>
      </div>
      <div class="card-branches">
        ${c.branches.slice(0, 4).map(b => `<span class="branch-tag">${b}</span>`).join("")}
        ${c.branches.length > 4 ? `<span class="branch-tag">+${c.branches.length - 4}</span>` : ""}
      </div>
      <div class="card-actions">
        <a href="details.html?id=${c.id}" class="btn btn-sm btn-outline">View Details</a>
        <button class="btn btn-sm ${inCompare ? "btn-danger" : "btn-ghost"}" onclick="toggleCompare(${c.id})">
          ${inCompare ? "Remove" : "+ Compare"}
        </button>
      </div>
    </article>
  `;
}

function renderResults() {
  const grid = document.getElementById("college-grid");
  const countEl = document.getElementById("results-count");
  if (!grid) return;

  const results = filterColleges();
  if (countEl) countEl.textContent = `${results.length} college${results.length !== 1 ? "s" : ""} found`;

  if (results.length === 0) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="icon">🔍</div>
        <h3>No colleges found</h3>
        <p>Try adjusting your filters or search term.</p>
      </div>`;
    return;
  }

  grid.innerHTML = results.map(renderCollegeCard).join("");
}

function toggleCompare(id) {
  if (compareList.includes(id)) {
    compareList = compareList.filter(x => x !== id);
  } else {
    if (compareList.length >= 4) {
      alert("You can compare maximum 4 colleges. Remove one first.");
      return;
    }
    compareList.push(id);
  }
  saveCompare();
  renderResults();
}

function clearFilters() {
  const ids = ["filter-name", "filter-district", "filter-type", "filter-branch", "filter-min", "filter-max"];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = id.includes("min") ? "" : id.includes("max") ? "" : "";
  });
  if (document.getElementById("filter-min")) document.getElementById("filter-min").value = "50";
  if (document.getElementById("filter-max")) document.getElementById("filter-max").value = "100";
  renderResults();
}

function initSearchPage() {
  // Bind filter events
  ["filter-name", "filter-district", "filter-type", "filter-branch", "filter-min", "filter-max", "sort-by"].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", renderResults);
      el.addEventListener("change", renderResults);
    }
  });

  const clearBtn = document.getElementById("btn-clear-filters");
  if (clearBtn) clearBtn.addEventListener("click", clearFilters);

  renderResults();
}

/* ---------- Init ---------- */
document.addEventListener("DOMContentLoaded", () => {
  initNav();
  updateCompareBadges();

  // Page-specific init
  if (document.getElementById("college-grid")) {
    initSearchPage();
  }
});
