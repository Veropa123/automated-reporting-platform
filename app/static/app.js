const fileInput = document.querySelector("#file-input");
const chooseFileButton = document.querySelector("#choose-file");
const useSampleButton = document.querySelector("#use-sample");
const dropZone = document.querySelector("#drop-zone");
const fileName = document.querySelector("#file-name");
const state = document.querySelector("#analysis-state");
const results = document.querySelector("#results");
const kpiGrid = document.querySelector("#kpi-grid");
const numericChart = document.querySelector("#numeric-chart");
const missingValues = document.querySelector("#missing-values");
const columnList = document.querySelector("#column-list");
const columnCount = document.querySelector("#column-count");
const downloadJsonButton = document.querySelector("#download-json");
const downloadExcelButton = document.querySelector("#download-excel");

let selectedFile = null;
let lastAnalysis = null;

chooseFileButton.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) setFile(fileInput.files[0]);
});

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragover");
  });
});

dropZone.addEventListener("drop", (event) => {
  if (event.dataTransfer.files.length) setFile(event.dataTransfer.files[0]);
});

useSampleButton.addEventListener("click", async () => {
  setStatus("Loading sample dataset...");
  try {
    const response = await fetch("/sample-data");
    if (!response.ok) throw new Error("Could not load sample data.");
    const blob = await response.blob();
    setFile(new File([blob], "sales.csv", { type: "text/csv" }));
  } catch (error) {
    setStatus(error.message, true);
  }
});

downloadJsonButton.addEventListener("click", () => {
  if (!lastAnalysis) return;
  const blob = new Blob([JSON.stringify(lastAnalysis, null, 2)], {
    type: "application/json",
  });
  downloadBlob(blob, "analysis-report.json");
});

downloadExcelButton.addEventListener("click", async () => {
  if (!selectedFile) return;

  setStatus("Generating Excel report...");
  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("/report/excel", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Could not generate the report.");
    }

    const blob = await response.blob();
    downloadBlob(blob, "automated-analysis-report.xlsx");
    setStatus("Excel report generated successfully.");
  } catch (error) {
    setStatus(error.message, true);
  }
});

async function setFile(file) {
  selectedFile = file;
  fileName.textContent = file.name;
  results.classList.add("hidden");
  lastAnalysis = null;
  await analyzeSelectedFile();
}

async function analyzeSelectedFile() {
  if (!selectedFile) return;

  setStatus("Analyzing dataset...");

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "The dataset could not be analyzed.");
    }

    lastAnalysis = payload;
    renderResults(payload);
    setStatus("Analysis completed successfully.");
  } catch (error) {
    setStatus(error.message, true);
  }
}

function renderResults(data) {
  renderKpis(data);
  renderNumericChart(data.numeric_summary);
  renderMissingValues(data.missing_values);
  renderColumns(data.column_names);
  results.classList.remove("hidden");
}

function renderKpis(data) {
  const completeness = data.rows ? (data.kpis.complete_rows / data.rows) * 100 : 0;
  const dynamicKpi = Object.entries(data.kpis).find(
    ([key]) => key.startsWith("total_") && key !== "total_rows"
  );

  const cards = [
    ["Rows", data.rows],
    ["Columns", data.columns],
    ["Complete rows", completeness.toFixed(1) + "%"],
    [
      dynamicKpi ? labelFromKey(dynamicKpi[0]) : "Numeric fields",
      dynamicKpi ? formatNumber(dynamicKpi[1]) : Object.keys(data.numeric_summary).length,
    ],
  ];

  kpiGrid.innerHTML = cards
    .map(([label, value]) =>
      '<div class="kpi-card"><div class="kpi-label">' +
      escapeHtml(String(label)) +
      '</div><div class="kpi-value">' +
      escapeHtml(String(value)) +
      "</div></div>"
    )
    .join("");
}

function renderNumericChart(summary) {
  const entries = Object.entries(summary);
  if (!entries.length) {
    numericChart.innerHTML = '<div class="good-state">No numeric columns detected.</div>';
    return;
  }

  const max = Math.max(...entries.map(([, metrics]) => Math.abs(metrics.mean)), 1);

  numericChart.innerHTML = entries
    .map(([column, metrics]) => {
      const width = Math.max((Math.abs(metrics.mean) / max) * 100, 2);
      return (
        '<div class="bar-row">' +
        '<div class="bar-label" title="' + escapeHtml(column) + '">' + escapeHtml(column) + '</div>' +
        '<div class="bar-track"><div class="bar-fill" style="width:' + width + '%"></div></div>' +
        '<div class="bar-value">' + formatNumber(metrics.mean) + '</div></div>'
      );
    })
    .join("");
}

function renderMissingValues(values) {
  const entries = Object.entries(values);

  if (!entries.length) {
    missingValues.innerHTML = '<div class="good-state">✓ No missing values detected.</div>';
    return;
  }

  missingValues.innerHTML = entries
    .map(([column, count]) =>
      '<div class="quality-row"><span>' + escapeHtml(column) +
      '</span><strong>' + count + ' missing</strong></div>'
    )
    .join("");
}

function renderColumns(columns) {
  columnCount.textContent = columns.length + " columns";
  columnList.innerHTML = columns
    .map((column) => '<span class="chip">' + escapeHtml(column) + '</span>')
    .join("");
}

function setStatus(message, isError = false) {
  state.textContent = message;
  state.classList.toggle("error", isError);
}

function labelFromKey(value) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (character) => character.toUpperCase());
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value);
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
