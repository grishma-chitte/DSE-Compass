/* =============================================
   DSE-Compass — Compare Page Logic
   ============================================= */

function renderComparePage() {
  const container = document.getElementById("compare-content");
  const empty = document.getElementById("compare-empty");
  const chips = document.getElementById("compare-chips");

  if (!container) return;

  const selected = COLLEGES.filter(c => compareList.includes(c.id));

  // Chips
  if (chips) {
    if (selected.length === 0) {
      chips.innerHTML = `<span style="color:var(--text-muted);font-size:0.9rem;">No colleges selected yet.</span>`;
    } else {
      chips.innerHTML = selected.map(c => `
        <div class="compare-chip">
          ${c.name.split("(")[0].trim()}
          <button onclick="removeFromCompare(${c.id})" title="Remove">×</button>
        </div>
      `).join("");
    }
  }

  if (selected.length < 2) {
    container.innerHTML = "";
    if (empty) empty.style.display = "block";
    return;
  }

  if (empty) empty.style.display = "none";

  const metrics = [
    { key: "district", label: "Location" },
    { key: "type", label: "College Type" },
    { key: "cutoff", label: "Approx. Cutoff", suffix: "%" },
    { key: "avgPackage", label: "Avg Package", suffix: " LPA" },
    { key: "placementPct", label: "Placement Rate", suffix: "%" },
    { key: "fees", label: "Annual Fees", format: formatFees },
    { key: "trend", label: "Cutoff Trend (3 yrs)", format: v => v.map(x => x + "%").join(" → ") },
    { key: "branches", label: "Branches", format: v => v.join(", ") },
    { key: "description", label: "Overview" }
  ];

  let html = `<div class="compare-table-wrap"><table class="compare-table"><thead><tr><th>Metric</th>`;
  selected.forEach(c => {
    html += `<th>${c.name.split("(")[0].trim()}</th>`;
  });
  html += `</tr></thead><tbody>`;

  metrics.forEach(m => {
    html += `<tr><td>${m.label}</td>`;
    selected.forEach(c => {
      let val = c[m.key];
      if (m.format) val = m.format(val);
      else if (m.suffix) val = val + m.suffix;
      html += `<td>${val}</td>`;
    });
    html += `</tr>`;
  });

  html += `</tbody></table></div>`;
  html += `<div style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap;">
    <button class="btn btn-outline" onclick="clearCompare()">Clear All</button>
    <a href="search.html" class="btn btn-primary">Add More Colleges</a>
  </div>`;

  container.innerHTML = html;
}

function removeFromCompare(id) {
  compareList = compareList.filter(x => x !== id);
  saveCompare();
  renderComparePage();
}

function clearCompare() {
  compareList = [];
  saveCompare();
  renderComparePage();
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("compare-content")) {
    renderComparePage();
  }
});
