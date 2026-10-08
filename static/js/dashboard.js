// // (() => {
// //     "use strict";

// //     const getJSON = (id) => {
// //         const element = document.getElementById(id);
// //         if (!element) return {labels: [], values: []};
// //         try { return JSON.parse(element.textContent || "{}"); }
// //         catch (_) { return {labels: [], values: []}; }
// //     };

// //     const cabang = getJSON("chartCabangData");
// //     const pasar = getJSON("chartPasarData");
// //     const distribusi = getJSON("chartDistribusiData");
// //     const tren = getJSON("chartTrenData");

// //     const rupiah = (value) => "Rp " + Number(value || 0).toLocaleString("id-ID");
// //     const short = (value) => {
// //         const n = Number(value || 0);
// //         if (Math.abs(n) >= 1e9) return (n / 1e9).toFixed(1) + " M";
// //         if (Math.abs(n) >= 1e6) return (n / 1e6).toFixed(1) + " jt";
// //         if (Math.abs(n) >= 1e3) return (n / 1e3).toFixed(0) + " rb";
// //         return n.toFixed(0);
// //     };

// //     const base = {
// //         paper_bgcolor: "rgba(0,0,0,0)",
// //         plot_bgcolor: "rgba(0,0,0,0)",
// //         font: {family: "Inter, Segoe UI, Arial", color: "#334155"},
// //         margin: {l: 55, r: 20, t: 20, b: 45},
// //         hoverlabel: {bgcolor: "#0f172a", font: {color: "#fff"}}
// //     };
// //     const config = {responsive: true, displayModeBar: false};

// //     if (document.getElementById("chartCabang")) {
// //         Plotly.newPlot("chartCabang", [{
// //             x: cabang.labels || [], y: cabang.values || [], type: "bar",
// //             marker: {color: "#1d4ed8", borderRadius: 4},
// //             text: (cabang.values || []).map(short), textposition: "outside",
// //             hovertemplate: "<b>%{x}</b><br>%{y:,.0f}<extra></extra>"
// //         }], {
// //             ...base, height: 360,
// //             xaxis: {showgrid: false, type: "category"},
// //             yaxis: {showgrid: true, gridcolor: "#e2e8f0", tickformat: ".2s"}
// //         }, config);
// //     }

// //     if (document.getElementById("chartDistribusi")) {
// //         const colors = {"Air": "#0ea5e9", "Listrik": "#f59e0b", "Tempat": "#22c55e"};
// //         const total = (distribusi.values || []).reduce((a,b) => a + Number(b || 0), 0);
// //         Plotly.newPlot("chartDistribusi", [{
// //             labels: distribusi.labels || [], values: distribusi.values || [],
// //             type: "pie", hole: 0.58,
// //             marker: {colors: (distribusi.labels || []).map(x => colors[x] || "#94a3b8")},
// //             textinfo: "label+percent",
// //             hovertemplate: "<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>"
// //         }], {
// //             ...base, height: 360, margin: {l: 10,r:10,t:15,b:15},
// //             legend: {orientation:"h", y:-0.02, x:0.5, xanchor:"center"},
// //             annotations: [{text:`<b>${short(total)}</b><br><span style="font-size:11px">Total</span>`, x:.5,y:.5,showarrow:false}]
// //         }, config);
// //     }

// //     if (document.getElementById("chartPasar")) {
// //         const labels = pasar.labels || [];
// //         Plotly.newPlot("chartPasar", [
// //             {name:"Listrik", x:labels, y:pasar.listrik || [], type:"bar", marker:{color:"#f59e0b"}, hovertemplate:"<b>%{x}</b><br>Listrik: %{y:,.0f}<extra></extra>"},
// //             {name:"Tempat", x:labels, y:pasar.tempat || [], type:"bar", marker:{color:"#22c55e"}, hovertemplate:"<b>%{x}</b><br>Tempat: %{y:,.0f}<extra></extra>"},
// //             {name:"Air", x:labels, y:pasar.air || [], type:"bar", marker:{color:"#0ea5e9"}, hovertemplate:"<b>%{x}</b><br>Air: %{y:,.0f}<extra></extra>"}
// //         ], {
// //             ...base, height:360, barmode:"group",
// //             margin:{l:55,r:20,t:20,b:80},
// //             xaxis:{type:"category",tickangle:-25,showgrid:false},
// //             yaxis:{showgrid:true,gridcolor:"#e2e8f0",tickformat:".2s"},
// //             legend:{orientation:"h",y:1.08,x:0}
// //         }, config);
// //     }

// //     if (document.getElementById("chartTren")) {
// //         Plotly.newPlot("chartTren", [{
// //             x:tren.labels || [], y:tren.values || [], type:"scatter",
// //             mode:"lines+markers", fill:"tozeroy",
// //             line:{color:"#1d4ed8",width:3}, marker:{size:6},
// //             hovertemplate:"<b>%{x}</b><br>%{y:,.0f}<extra></extra>"
// //         }], {
// //             ...base, height:300,
// //             xaxis:{showgrid:false},
// //             yaxis:{showgrid:true,gridcolor:"#e2e8f0",tickformat:".2s"}
// //         }, config);
// //     }

// //     window.addEventListener("resize", () => {
// //         ["chartCabang","chartDistribusi","chartPasar","chartTren"].forEach(id => {
// //             const el=document.getElementById(id);
// //             if (el && el.data) Plotly.Plots.resize(el);
// //         });
// //     });
// // })();

// /* =========================================================
//    Dashboard Data Pasar — Chart.js
//    Visualisasi disamakan dengan versi Streamlit
//    ========================================================= */

// (function () {
//   "use strict";

//   // ===== WARNA JENIS TAGIHAN (sama seperti Streamlit) =====
//   const WARNA_JENIS = {
//     "Listrik": "#3b82f6",   // biru
//     "Tempat":  "#f59e0b",   // orange
//     "Air":     "#8b5cf6",   // ungu
//   };

//   // ===== URUTAN JENIS (sama seperti Streamlit) =====
//   const URUTAN_JENIS = ["Listrik", "Tempat", "Air"];

//   // ===== HELPER: FORMAT ANGKA =====
//   function formatRupiah(value) {
//     return "Rp " + new Intl.NumberFormat("id-ID").format(Math.round(value || 0));
//   }

//   function formatShortAxis(value) {
//     const abs = Math.abs(value);
//     if (abs >= 1e9) return (value / 1e9).toFixed(1).replace(".", ",") + "B";
//     if (abs >= 1e6) return (value / 1e6).toFixed(1).replace(".", ",") + "M";
//     if (abs >= 1e3) return (value / 1e3).toFixed(0) + "rb";
//     return value.toString();
//   }

//   // ===== AMBIL DATA JSON DARI TEMPLATE =====
//   function readJSON(id) {
//     const el = document.getElementById(id);
//     if (!el) return null;
//     try {
//       return JSON.parse(el.textContent);
//     } catch (e) {
//       console.error("Gagal parse JSON:", id, e);
//       return null;
//     }
//   }

//   const dataCabang = readJSON("chartCabangData");
//   const dataPasar = readJSON("chartPasarData");
//   const dataDistribusi = readJSON("chartDistribusiData");
//   const dataTren = readJSON("chartTrenData");

//   if (typeof Chart === "undefined") {
//     console.error("Chart.js belum dimuat!");
//     return;
//   }

//   // =========================================================
//   // CHART: NILAI TAGIHAN PER CABANG (Bar Chart)
//   // =========================================================
//   function buildChartCabang() {
//     const canvas = document.getElementById("chartCabang");
//     if (!canvas || !dataCabang) return;

//     new Chart(canvas, {
//       type: "bar",
//       data: {
//         labels: dataCabang.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataCabang.values,
//           backgroundColor: "#3b82f6",
//           borderRadius: 4,
//           barPercentage: 0.5,
//           categoryPercentage: 0.6,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: { color: "#374151", font: { size: 12 } }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: DISTRIBUSI JENIS TAGIHAN (Donut Chart)
//   // =========================================================
//   function buildChartDistribusi() {
//     const canvas = document.getElementById("chartDistribusi");
//     if (!canvas || !dataDistribusi) return;

//     const colors = dataDistribusi.labels.map(
//       (label) => WARNA_JENIS[label] || "#94a3b8"
//     );

//     const total = dataDistribusi.values.reduce((a, b) => a + b, 0);

//     new Chart(canvas, {
//       type: "doughnut",
//       data: {
//         labels: dataDistribusi.labels,
//         datasets: [{
//           data: dataDistribusi.values,
//           backgroundColor: colors,
//           borderColor: "#ffffff",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         cutout: "55%",
//         plugins: {
//           legend: {
//             position: "bottom",
//             labels: {
//               font: { size: 11 },
//               padding: 12,
//               usePointStyle: true,
//             }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => {
//                 const value = ctx.parsed;
//                 const pct = total > 0 ? ((value / total) * 100).toFixed(1) : "0";
//                 return `${ctx.label}: ${formatRupiah(value)} (${pct}%)`;
//               }
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: NILAI TAGIHAN PER PASAR (Grouped Bar Chart)
//   // =========================================================
//   function buildChartPasar() {
//     const canvas = document.getElementById("chartPasar");
//     if (!canvas || !dataPasar) return;

//     // ⭐ Support format baru (series) dan format lama (listrik/tempat/air)
//     let datasets = [];

//     if (Array.isArray(dataPasar.series) && dataPasar.series.length > 0) {
//       // Format baru: series = [{name, values}, ...]
//       datasets = dataPasar.series.map((s) => ({
//         label: s.name,
//         data: s.values,
//         backgroundColor: WARNA_JENIS[s.name] || "#94a3b8",
//         borderRadius: 3,
//         barPercentage: 0.7,
//         categoryPercentage: 0.7,
//       }));
//     } else {
//       // Format lama (fallback): listrik, tempat, air
//       datasets = [
//         {
//           label: "Listrik",
//           data: dataPasar.listrik || [],
//           backgroundColor: WARNA_JENIS["Listrik"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//         {
//           label: "Tempat",
//           data: dataPasar.tempat || [],
//           backgroundColor: WARNA_JENIS["Tempat"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//         {
//           label: "Air",
//           data: dataPasar.air || [],
//           backgroundColor: WARNA_JENIS["Air"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//       ];
//     }

//     // Pastikan urutan legend sesuai Streamlit: Listrik, Tempat, Air
//     datasets.sort((a, b) => {
//       const idxA = URUTAN_JENIS.indexOf(a.label);
//       const idxB = URUTAN_JENIS.indexOf(b.label);
//       return idxA - idxB;
//     });

//     new Chart(canvas, {
//       type: "bar",
//       data: {
//         labels: dataPasar.labels,
//         datasets: datasets,
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: {
//             position: "top",
//             labels: {
//               font: { size: 11 },
//               padding: 12,
//               usePointStyle: true,
//             }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => `${ctx.dataset.label}: ${formatRupiah(ctx.parsed.y)}`
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: {
//               color: "#374151",
//               font: { size: 10 },
//               maxRotation: 45,
//               minRotation: 0,
//             }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: TREN NILAI TAGIHAN (Area Chart)
//   // =========================================================
//   function buildChartTren() {
//     const canvas = document.getElementById("chartTren");
//     if (!canvas || !dataTren) return;

//     new Chart(canvas, {
//       type: "line",
//       data: {
//         labels: dataTren.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataTren.values,
//           borderColor: "#3b82f6",
//           backgroundColor: "rgba(59, 130, 246, 0.15)",
//           fill: true,
//           tension: 0.3,
//           pointRadius: 2,
//           pointHoverRadius: 5,
//           pointBackgroundColor: "#3b82f6",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: {
//               color: "#374151",
//               font: { size: 10 },
//               maxRotation: 45,
//               minRotation: 0,
//             }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // INIT — semua chart
//   // =========================================================
//   document.addEventListener("DOMContentLoaded", function () {
//     buildChartCabang();
//     buildChartDistribusi();
//     buildChartPasar();
//     buildChartTren();
//   });

// })();

/* =========================================================
   Dashboard Data Pasar — Chart.js
   Visualisasi disamakan dengan versi Streamlit
   ========================================================= */
// (function () {
//   "use strict";

//   const WARNA_JENIS = {
//     "Listrik": "#3b82f6",
//     "Tempat":  "#f59e0b",
//     "Air":     "#8b5cf6",
//   };

//   const URUTAN_JENIS = ["Listrik", "Tempat", "Air"];

//   function formatRupiah(value) {
//     return "Rp " + new Intl.NumberFormat("id-ID").format(Math.round(value || 0));
//   }

//   function formatShortAxis(value) {
//     const abs = Math.abs(value);
//     if (abs >= 1e9) return (value / 1e9).toFixed(1).replace(".", ",") + "B";
//     if (abs >= 1e6) return (value / 1e6).toFixed(1).replace(".", ",") + "M";
//     if (abs >= 1e3) return (value / 1e3).toFixed(0) + "rb";
//     return value.toString();
//   }

//   function readJSON(id) {
//     const el = document.getElementById(id);
//     if (!el) return null;
//     try {
//       return JSON.parse(el.textContent);
//     } catch (e) {
//       console.error("Gagal parse JSON:", id, e);
//       return null;
//     }
//   }

//   const dataCabang = readJSON("chartCabangData");
//   const dataPasar = readJSON("chartPasarData");
//   const dataDistribusi = readJSON("chartDistribusiData");
//   const dataTren = readJSON("chartTrenData");

//   if (typeof Chart === "undefined") {
//     console.error("Chart.js belum dimuat!");
//     return;
//   }

//   // CHART: NILAI TAGIHAN PER CABANG
//   function buildChartCabang() {
//     const canvas = document.getElementById("chartCabang");
//     if (!canvas || !dataCabang) return;

//     new Chart(canvas, {
//       type: "bar",
//       data: {
//         labels: dataCabang.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataCabang.values,
//           backgroundColor: "#3b82f6",
//           borderRadius: 4,
//           barPercentage: 0.5,
//           categoryPercentage: 0.6,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: { color: "#374151", font: { size: 12 } }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // CHART: DISTRIBUSI JENIS TAGIHAN (Donut)
//   function buildChartDistribusi() {
//     const canvas = document.getElementById("chartDistribusi");
//     if (!canvas || !dataDistribusi) return;

//     const colors = dataDistribusi.labels.map(
//       (label) => WARNA_JENIS[label] || "#94a3b8"
//     );
//     const total = dataDistribusi.values.reduce((a, b) => a + b, 0);

//     new Chart(canvas, {
//       type: "doughnut",
//       data: {
//         labels: dataDistribusi.labels,
//         datasets: [{
//           data: dataDistribusi.values,
//           backgroundColor: colors,
//           borderColor: "#ffffff",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         cutout: "55%",
//         plugins: {
//           legend: {
//             position: "bottom",
//             labels: { font: { size: 11 }, padding: 12, usePointStyle: true }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => {
//                 const value = ctx.parsed;
//                 const pct = total > 0 ? ((value / total) * 100).toFixed(1) : "0";
//                 return `${ctx.label}: ${formatRupiah(value)} (${pct}%)`;
//               }
//             }
//           }
//         }
//       }
//     });
//   }

//   // CHART: NILAI TAGIHAN PER PASAR (Grouped Bar)
//   function buildChartPasar() {
//     const canvas = document.getElementById("chartPasar");
//     if (!canvas || !dataPasar) return;

//     let datasets = [];

//     if (Array.isArray(dataPasar.series) && dataPasar.series.length > 0) {
//       datasets = dataPasar.series.map((s) => ({
//         label: s.name,
//         data: s.values,
//         backgroundColor: WARNA_JENIS[s.name] || "#94a3b8",
//         borderRadius: 3,
//         barPercentage: 0.7,
//         categoryPercentage: 0.7,
//       }));
//     } else {
//       datasets = [
//         { label: "Listrik", data: dataPasar.listrik || [], backgroundColor: WARNA_JENIS["Listrik"], borderRadius: 3, barPercentage: 0.7, categoryPercentage: 0.7 },
//         { label: "Tempat",  data: dataPasar.tempat || [],  backgroundColor: WARNA_JENIS["Tempat"],  borderRadius: 3, barPercentage: 0.7, categoryPercentage: 0.7 },
//         { label: "Air",     data: dataPasar.air || [],     backgroundColor: WARNA_JENIS["Air"],     borderRadius: 3, barPercentage: 0.7, categoryPercentage: 0.7 },
//       ];
//     }

//     datasets.sort((a, b) => {
//       const idxA = URUTAN_JENIS.indexOf(a.label);
//       const idxB = URUTAN_JENIS.indexOf(b.label);
//       return (idxA === -1 ? 999 : idxA) - (idxB === -1 ? 999 : idxB);
//     });

//     new Chart(canvas, {
//       type: "bar",
//       data: { labels: dataPasar.labels, datasets: datasets },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: {
//             position: "top",
//             labels: { font: { size: 11 }, padding: 12, usePointStyle: true }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => `${ctx.dataset.label}: ${formatRupiah(ctx.parsed.y)}`
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: { color: "#374151", font: { size: 10 }, maxRotation: 45, minRotation: 0 }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: { color: "#6b7280", font: { size: 11 }, callback: (v) => formatShortAxis(v) }
//           }
//         }
//       }
//     });
//   }

//   // CHART: TREN NILAI (Area)
//   function buildChartTren() {
//     const canvas = document.getElementById("chartTren");
//     if (!canvas || !dataTren) return;

//     new Chart(canvas, {
//       type: "line",
//       data: {
//         labels: dataTren.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataTren.values,
//           borderColor: "#3b82f6",
//           backgroundColor: "rgba(59, 130, 246, 0.15)",
//           fill: true,
//           tension: 0.3,
//           pointRadius: 2,
//           pointHoverRadius: 5,
//           pointBackgroundColor: "#3b82f6",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: { label: (ctx) => formatRupiah(ctx.parsed.y) }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: { color: "#374151", font: { size: 10 }, maxRotation: 45, minRotation: 0 }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: { color: "#6b7280", font: { size: 11 }, callback: (v) => formatShortAxis(v) }
//           }
//         }
//       }
//     });
//   }

//   document.addEventListener("DOMContentLoaded", function () {
//     buildChartCabang();
//     buildChartDistribusi();
//     buildChartPasar();
//     buildChartTren();
//   });

// })();

// (function () {
//   "use strict";

//   // Warna jenis tagihan — SAMA seperti Streamlit
//   const WARNA_JENIS = {
//     "Listrik": "#3b82f6",
//     "Tempat":  "#f59e0b",
//     "Air":     "#8b5cf6",
//   };

//   const URUTAN_JENIS = ["Listrik", "Tempat", "Air"];

//   // ===== HELPER FORMAT =====
//   function formatRupiah(value) {
//     return "Rp " + new Intl.NumberFormat("id-ID").format(Math.round(value || 0));
//   }

//   function formatShortAxis(value) {
//     const abs = Math.abs(value);
//     if (abs >= 1e9) return (value / 1e9).toFixed(1).replace(".", ",") + "B";
//     if (abs >= 1e6) return (value / 1e6).toFixed(1).replace(".", ",") + "M";
//     if (abs >= 1e3) return (value / 1e3).toFixed(0) + "rb";
//     return value.toString();
//   }

//   function readJSON(id) {
//     const el = document.getElementById(id);
//     if (!el) return null;
//     try {
//       return JSON.parse(el.textContent);
//     } catch (e) {
//       console.error("Gagal parse JSON:", id, e);
//       return null;
//     }
//   }

//   const dataCabang = readJSON("chartCabangData");
//   const dataPasar = readJSON("chartPasarData");
//   const dataDistribusi = readJSON("chartDistribusiData");
//   const dataTren = readJSON("chartTrenData");

//   if (typeof Chart === "undefined") {
//     console.error("Chart.js belum dimuat!");
//     return;
//   }

//   // =========================================================
//   // CHART: NILAI TAGIHAN PER CABANG
//   // =========================================================
//   function buildChartCabang() {
//     const canvas = document.getElementById("chartCabang");
//     if (!canvas || !dataCabang) return;

//     new Chart(canvas, {
//       type: "bar",
//       data: {
//         labels: dataCabang.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataCabang.values,
//           backgroundColor: "#3b82f6",
//           borderRadius: 4,
//           barPercentage: 0.5,
//           categoryPercentage: 0.6,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: { color: "#374151", font: { size: 12 } }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: DISTRIBUSI JENIS TAGIHAN (Donut)
//   // =========================================================
//   function buildChartDistribusi() {
//     const canvas = document.getElementById("chartDistribusi");
//     if (!canvas || !dataDistribusi) return;

//     const colors = dataDistribusi.labels.map(
//       (label) => WARNA_JENIS[label] || "#94a3b8"
//     );

//     const total = dataDistribusi.values.reduce((a, b) => a + b, 0);

//     new Chart(canvas, {
//       type: "doughnut",
//       data: {
//         labels: dataDistribusi.labels,
//         datasets: [{
//           data: dataDistribusi.values,
//           backgroundColor: colors,
//           borderColor: "#ffffff",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         cutout: "55%",
//         plugins: {
//           legend: {
//             position: "bottom",
//             labels: {
//               font: { size: 11 },
//               padding: 12,
//               usePointStyle: true,
//             }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => {
//                 const value = ctx.parsed;
//                 const pct = total > 0 ? ((value / total) * 100).toFixed(1) : "0";
//                 return `${ctx.label}: ${formatRupiah(value)} (${pct}%)`;
//               }
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: NILAI TAGIHAN PER PASAR (Grouped Bar)
//   // =========================================================
//   function buildChartPasar() {
//     const canvas = document.getElementById("chartPasar");
//     if (!canvas || !dataPasar) return;

//     let datasets = [];

//     // Format baru: series
//     if (Array.isArray(dataPasar.series) && dataPasar.series.length > 0) {
//       datasets = dataPasar.series.map((s) => ({
//         label: s.name,
//         data: s.values,
//         backgroundColor: WARNA_JENIS[s.name] || "#94a3b8",
//         borderRadius: 3,
//         barPercentage: 0.7,
//         categoryPercentage: 0.7,
//       }));
//     } else {
//       // Fallback format lama
//       datasets = [
//         {
//           label: "Listrik",
//           data: dataPasar.listrik || [],
//           backgroundColor: WARNA_JENIS["Listrik"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//         {
//           label: "Tempat",
//           data: dataPasar.tempat || [],
//           backgroundColor: WARNA_JENIS["Tempat"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//         {
//           label: "Air",
//           data: dataPasar.air || [],
//           backgroundColor: WARNA_JENIS["Air"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//       ];
//     }

//     // Pastikan urutan legend: Listrik, Tempat, Air
//     datasets.sort((a, b) => {
//       const idxA = URUTAN_JENIS.indexOf(a.label);
//       const idxB = URUTAN_JENIS.indexOf(b.label);
//       return (idxA === -1 ? 999 : idxA) - (idxB === -1 ? 999 : idxB);
//     });

//     new Chart(canvas, {
//       type: "bar",
//       data: {
//         labels: dataPasar.labels,
//         datasets: datasets,
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: {
//             position: "top",
//             labels: {
//               font: { size: 11 },
//               padding: 12,
//               usePointStyle: true,
//             }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => `${ctx.dataset.label}: ${formatRupiah(ctx.parsed.y)}`
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: {
//               color: "#374151",
//               font: { size: 10 },
//               maxRotation: 45,
//               minRotation: 0,
//             }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: TREN NILAI (Area)
//   // =========================================================
//   function buildChartTren() {
//     const canvas = document.getElementById("chartTren");
//     if (!canvas || !dataTren) return;

//     new Chart(canvas, {
//       type: "line",
//       data: {
//         labels: dataTren.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataTren.values,
//           borderColor: "#3b82f6",
//           backgroundColor: "rgba(59, 130, 246, 0.15)",
//           fill: true,
//           tension: 0.3,
//           pointRadius: 2,
//           pointHoverRadius: 5,
//           pointBackgroundColor: "#3b82f6",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: {
//               color: "#374151",
//               font: { size: 10 },
//               maxRotation: 45,
//               minRotation: 0,
//             }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // INIT
//   // =========================================================
//   document.addEventListener("DOMContentLoaded", function () {
//     buildChartCabang();
//     buildChartDistribusi();
//     buildChartPasar();
//     buildChartTren();
//   });

// })();

// (function () {
//   "use strict";

//   // =========================================================
//   // KONSTANTA
//   // =========================================================
//   const WARNA_JENIS = {
//     "Listrik": "#3b82f6",
//     "Tempat":  "#f59e0b",
//     "Air":     "#8b5cf6",
//   };

//   const URUTAN_JENIS = ["Listrik", "Tempat", "Air"];

//   // =========================================================
//   // HELPER FORMAT
//   // =========================================================
//   function formatRupiah(value) {
//     return "Rp " + new Intl.NumberFormat("id-ID").format(Math.round(value || 0));
//   }

//   function formatShortAxis(value) {
//     const abs = Math.abs(value);
//     if (abs >= 1e9) return (value / 1e9).toFixed(1).replace(".", ",") + "B";
//     if (abs >= 1e6) return (value / 1e6).toFixed(1).replace(".", ",") + "M";
//     if (abs >= 1e3) return (value / 1e3).toFixed(0) + "rb";
//     return value.toString();
//   }

//   // =========================================================
//   // HELPER: GET CANVAS (auto-convert div → canvas)
//   // =========================================================
//   function getCanvas(id) {
//     const el = document.getElementById(id);
//     if (!el) {
//       console.error("Element #" + id + " tidak ditemukan di DOM");
//       return null;
//     }

//     // Kalau sudah <canvas>, langsung pakai
//     if (el.tagName === "CANVAS") {
//       return el;
//     }

//     // Kalau <div> atau elemen lain, buat <canvas> di dalamnya
//     const canvas = document.createElement("canvas");
//     canvas.id = id + "-canvas";
//     canvas.style.width = "100%";
//     canvas.style.height = "100%";
//     canvas.style.display = "block";

//     // Bersihkan isi element dan masukkan canvas
//     el.innerHTML = "";
//     el.appendChild(canvas);

//     return canvas;
//   }

//   // =========================================================
//   // HELPER: READ JSON dari <script type="application/json">
//   // =========================================================
//   function readJSON(id) {
//     const el = document.getElementById(id);
//     if (!el) {
//       console.warn("JSON script #" + id + " tidak ditemukan");
//       return null;
//     }
//     try {
//       const parsed = JSON.parse(el.textContent);
//       return parsed;
//     } catch (e) {
//       console.error("Gagal parse JSON #" + id + ":", e);
//       return null;
//     }
//   }

//   // =========================================================
//   // HELPER: SAFE NEW CHART
//   // — Cek ukuran element, retry kalau 0
//   // — Auto-convert div → canvas
//   // =========================================================
//   function safeNewChart(elementId, config, retryCount) {
//     retryCount = retryCount || 0;
//     const MAX_RETRY = 20;  // max 2 detik (20 × 100ms)

//     const el = document.getElementById(elementId);
//     if (!el) {
//       console.error("Element #" + elementId + " tidak ditemukan");
//       return;
//     }

//     // Cek ukuran element
//     const rect = el.getBoundingClientRect();
//     if (rect.width === 0 || rect.height === 0) {
//       if (retryCount < MAX_RETRY) {
//         console.warn(
//           "Element #" + elementId + " ukuran 0 (" + rect.width + "x" + rect.height + "). " +
//           "Retry " + (retryCount + 1) + "/" + MAX_RETRY + "..."
//         );
//         setTimeout(() => safeNewChart(elementId, config, retryCount + 1), 100);
//         return;
//       } else {
//         console.error(
//           "Element #" + elementId + " tetap ukuran 0 setelah " + MAX_RETRY + " retry. " +
//           "Cek CSS .chart-box apakah punya height."
//         );
//         return;
//       }
//     }

//     // Ambil canvas
//     const canvas = getCanvas(elementId);
//     if (!canvas) return;

//     // Buat chart
//     try {
//       new Chart(canvas, config);
//       console.log("✅ Chart #" + elementId + " berhasil dibuat");
//     } catch (e) {
//       console.error("❌ Gagal membuat chart #" + elementId + ":", e);
//     }
//   }

//   // =========================================================
//   // AMBIL DATA JSON
//   // =========================================================
//   const dataCabang = readJSON("chartCabangData");
//   const dataPasar = readJSON("chartPasarData");
//   const dataDistribusi = readJSON("chartDistribusiData");
//   const dataTren = readJSON("chartTrenData");

//   // =========================================================
//   // CEK CHART.JS
//   // =========================================================
//   if (typeof Chart === "undefined") {
//     console.error("❌ Chart.js belum dimuat! Cek tag <script> Chart.js di base.html");
//     return;
//   }

//   // =========================================================
//   // CHART: NILAI TAGIHAN PER CABANG (Bar Chart)
//   // =========================================================
//   function buildChartCabang() {
//     if (!dataCabang) {
//       console.warn("Data chart cabang kosong, skip");
//       return;
//     }

//     safeNewChart("chartCabang", {
//       type: "bar",
//       data: {
//         labels: dataCabang.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataCabang.values,
//           backgroundColor: "#3b82f6",
//           borderRadius: 4,
//           barPercentage: 0.5,
//           categoryPercentage: 0.6,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: { color: "#374151", font: { size: 12 } }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: DISTRIBUSI JENIS TAGIHAN (Donut Chart)
//   // =========================================================
//   function buildChartDistribusi() {
//     if (!dataDistribusi) {
//       console.warn("Data chart distribusi kosong, skip");
//       return;
//     }

//     const colors = dataDistribusi.labels.map(
//       (label) => WARNA_JENIS[label] || "#94a3b8"
//     );
//     const total = dataDistribusi.values.reduce((a, b) => a + b, 0);

//     safeNewChart("chartDistribusi", {
//       type: "doughnut",
//       data: {
//         labels: dataDistribusi.labels,
//         datasets: [{
//           data: dataDistribusi.values,
//           backgroundColor: colors,
//           borderColor: "#ffffff",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         cutout: "55%",
//         plugins: {
//           legend: {
//             position: "bottom",
//             labels: {
//               font: { size: 11 },
//               padding: 12,
//               usePointStyle: true
//             }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => {
//                 const value = ctx.parsed;
//                 const pct = total > 0 ? ((value / total) * 100).toFixed(1) : "0";
//                 return `${ctx.label}: ${formatRupiah(value)} (${pct}%)`;
//               }
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: NILAI TAGIHAN PER PASAR (Grouped Bar Chart)
//   // =========================================================
//   function buildChartPasar() {
//     if (!dataPasar) {
//       console.warn("Data chart pasar kosong, skip");
//       return;
//     }

//     let datasets = [];

//     // Format baru: series
//     if (Array.isArray(dataPasar.series) && dataPasar.series.length > 0) {
//       datasets = dataPasar.series.map((s) => ({
//         label: s.name,
//         data: s.values,
//         backgroundColor: WARNA_JENIS[s.name] || "#94a3b8",
//         borderRadius: 3,
//         barPercentage: 0.7,
//         categoryPercentage: 0.7,
//       }));
//     } else {
//       // Fallback format lama
//       datasets = [
//         {
//           label: "Listrik",
//           data: dataPasar.listrik || [],
//           backgroundColor: WARNA_JENIS["Listrik"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//         {
//           label: "Tempat",
//           data: dataPasar.tempat || [],
//           backgroundColor: WARNA_JENIS["Tempat"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//         {
//           label: "Air",
//           data: dataPasar.air || [],
//           backgroundColor: WARNA_JENIS["Air"],
//           borderRadius: 3,
//           barPercentage: 0.7,
//           categoryPercentage: 0.7,
//         },
//       ];
//     }

//     // Urutkan legend: Listrik, Tempat, Air
//     datasets.sort((a, b) => {
//       const idxA = URUTAN_JENIS.indexOf(a.label);
//       const idxB = URUTAN_JENIS.indexOf(b.label);
//       return (idxA === -1 ? 999 : idxA) - (idxB === -1 ? 999 : idxB);
//     });

//     safeNewChart("chartPasar", {
//       type: "bar",
//       data: {
//         labels: dataPasar.labels,
//         datasets: datasets,
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: {
//             position: "top",
//             labels: {
//               font: { size: 11 },
//               padding: 12,
//               usePointStyle: true
//             }
//           },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => `${ctx.dataset.label}: ${formatRupiah(ctx.parsed.y)}`
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: {
//               color: "#374151",
//               font: { size: 10 },
//               maxRotation: 45,
//               minRotation: 0,
//             }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // CHART: TREN NILAI (Area Chart)
//   // =========================================================
//   function buildChartTren() {
//     if (!dataTren) {
//       console.warn("Data chart tren kosong, skip");
//       return;
//     }

//     safeNewChart("chartTren", {
//       type: "line",
//       data: {
//         labels: dataTren.labels,
//         datasets: [{
//           label: "Total Nilai",
//           data: dataTren.values,
//           borderColor: "#3b82f6",
//           backgroundColor: "rgba(59, 130, 246, 0.15)",
//           fill: true,
//           tension: 0.3,
//           pointRadius: 2,
//           pointHoverRadius: 5,
//           pointBackgroundColor: "#3b82f6",
//           borderWidth: 2,
//         }]
//       },
//       options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         plugins: {
//           legend: { display: false },
//           tooltip: {
//             callbacks: {
//               label: (ctx) => formatRupiah(ctx.parsed.y)
//             }
//           }
//         },
//         scales: {
//           x: {
//             grid: { display: false },
//             ticks: {
//               color: "#374151",
//               font: { size: 10 },
//               maxRotation: 45,
//               minRotation: 0,
//             }
//           },
//           y: {
//             beginAtZero: true,
//             grid: { color: "#f1f5f9" },
//             ticks: {
//               color: "#6b7280",
//               font: { size: 11 },
//               callback: (v) => formatShortAxis(v)
//             }
//           }
//         }
//       }
//     });
//   }

//   // =========================================================
//   // INIT
//   // =========================================================
//   document.addEventListener("DOMContentLoaded", function () {
//     console.log("=== Dashboard.js starting ===");
//     console.log("typeof Chart:", typeof Chart);
//     console.log("dataCabang:", dataCabang);
//     console.log("dataPasar:", dataPasar);
//     console.log("dataDistribusi:", dataDistribusi);
//     console.log("dataTren:", dataTren);

//     // Delay sedikit biar CSS/layout stabil
//     setTimeout(function () {
//       buildChartCabang();
//       buildChartDistribusi();
//       buildChartPasar();
//       buildChartTren();
//       console.log("=== Semua chart selesai dibangun ===");
//     }, 100);
//   });

// })();

(function () {
  "use strict";

  // =========================================================
  // KONSTANTA
  // =========================================================
  const WARNA_JENIS = {
    "Listrik": "#3b82f6",
    "Tempat":  "#f59e0b",
    "Air":     "#8b5cf6",
  };

  const URUTAN_JENIS = ["Listrik", "Tempat", "Air"];

  // =========================================================
  // HELPER FORMAT
  // =========================================================
  function formatRupiah(value) {
    return "Rp " + new Intl.NumberFormat("id-ID").format(Math.round(value || 0));
  }

  // ⭐ Format singkat untuk label angka di chart
  function formatSingkat(value) {
    const abs = Math.abs(value);
    if (abs >= 1e12) return (value / 1e12).toFixed(1).replace(".", ",") + " T";
    if (abs >= 1e9)  return (value / 1e9).toFixed(1).replace(".", ",") + " M";
    if (abs >= 1e6)  return (value / 1e6).toFixed(1).replace(".", ",") + " Jt";
    if (abs >= 1e3)  return (value / 1e3).toFixed(0) + " rb";
    return value.toString();
  }

  // ⭐ Format angka dengan pemisah ribuan (label panjang)
  function formatAngka(value) {
    return new Intl.NumberFormat("id-ID").format(Math.round(value || 0));
  }

  function formatShortAxis(value) {
    const abs = Math.abs(value);
    if (abs >= 1e9) return (value / 1e9).toFixed(1).replace(".", ",") + "B";
    if (abs >= 1e6) return (value / 1e6).toFixed(1).replace(".", ",") + "M";
    if (abs >= 1e3) return (value / 1e3).toFixed(0) + "rb";
    return value.toString();
  }

  // =========================================================
  // HELPER: GET CANVAS
  // =========================================================
  function getCanvas(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    if (el.tagName === "CANVAS") return el;

    const canvas = document.createElement("canvas");
    canvas.id = id + "-canvas";
    canvas.style.width = "100%";
    canvas.style.height = "100%";
    canvas.style.display = "block";
    el.innerHTML = "";
    el.appendChild(canvas);
    return canvas;
  }

  // =========================================================
  // HELPER: READ JSON
  // =========================================================
  function readJSON(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      console.error("Gagal parse JSON #" + id + ":", e);
      return null;
    }
  }

  // =========================================================
  // HELPER: SAFE NEW CHART
  // =========================================================
  function safeNewChart(elementId, config, retryCount) {
    retryCount = retryCount || 0;
    const MAX_RETRY = 20;

    const el = document.getElementById(elementId);
    if (!el) {
      console.error("Element #" + elementId + " tidak ditemukan");
      return;
    }

    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) {
      if (retryCount < MAX_RETRY) {
        setTimeout(() => safeNewChart(elementId, config, retryCount + 1), 100);
        return;
      } else {
        console.error("Element #" + elementId + " ukuran 0 setelah retry");
        return;
      }
    }

    // Destroy chart lama kalau ada
    try {
      const existingCanvas = el.tagName === "CANVAS" ? el : el.querySelector("canvas");
      if (existingCanvas) {
        const existingChart = Chart.getChart(existingCanvas);
        if (existingChart) existingChart.destroy();
      }
    } catch (e) { /* ignore */ }

    const canvas = getCanvas(elementId);
    if (!canvas) return;

    try {
      new Chart(canvas, config);
      console.log("✅ Chart #" + elementId + " dibuat");
    } catch (e) {
      console.error("❌ Gagal chart #" + elementId + ":", e);
    }
  }

  // =========================================================
  // AMBIL DATA
  // =========================================================
  const dataCabang = readJSON("chartCabangData");
  const dataPasar = readJSON("chartPasarData");
  const dataDistribusi = readJSON("chartDistribusiData");
  const dataTren = readJSON("chartTrenData");

  if (typeof Chart === "undefined") {
    console.error("❌ Chart.js belum dimuat!");
    return;
  }

  // ⭐ Cek plugin datalabels
  const HAS_DATALABELS = typeof ChartDataLabels !== "undefined";
  console.log("Plugin DataLabels:", HAS_DATALABELS ? "✅ aktif" : "❌ tidak ada");

  // =========================================================
  // CHART: NILAI TAGIHAN PER CABANG
  // ⭐ + Label angka di atas bar
  // =========================================================
  function buildChartCabang() {
    if (!dataCabang) return;

    safeNewChart("chartCabang", {
      type: "bar",
      data: {
        labels: dataCabang.labels,
        datasets: [{
          label: "Total Nilai",
          data: dataCabang.values,
          backgroundColor: "#3b82f6",
          borderRadius: 4,
          barPercentage: 0.5,
          categoryPercentage: 0.6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 30,   // ⭐ beri ruang untuk label di atas bar
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => formatRupiah(ctx.parsed.y)
            }
          },
          // ⭐ DATALABELS
          datalabels: {
            anchor: "end",
            align: "top",
            offset: 4,
            color: "#1f2937",
            font: {
              size: 11,
              weight: "600",
            },
            formatter: (value) => {
              if (!value || value === 0) return "";
              return formatSingkat(value);
            },
            // Kalau pakai versi lengkap (Rp 1.234.567), ganti jadi:
            // formatter: (value) => formatAngka(value),
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#374151", font: { size: 12 } }
          },
          y: {
            beginAtZero: true,
            grid: { color: "#f1f5f9" },
            ticks: {
              color: "#6b7280",
              font: { size: 11 },
              callback: (v) => formatShortAxis(v)
            }
          }
        }
      }
    });
  }

  // =========================================================
  // CHART: DISTRIBUSI JENIS TAGIHAN (Donut)
  // ⭐ + Label angka + persen di dalam donut
  // =========================================================
  function buildChartDistribusi() {
    if (!dataDistribusi) return;

    const colors = dataDistribusi.labels.map(
      (label) => WARNA_JENIS[label] || "#94a3b8"
    );
    const total = dataDistribusi.values.reduce((a, b) => a + b, 0);

    safeNewChart("chartDistribusi", {
      type: "doughnut",
      data: {
        labels: dataDistribusi.labels,
        datasets: [{
          data: dataDistribusi.values,
          backgroundColor: colors,
          borderColor: "#ffffff",
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "55%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              font: { size: 11 },
              padding: 12,
              usePointStyle: true
            }
          },
          tooltip: {
            callbacks: {
              label: (ctx) => {
                const v = ctx.parsed;
                const pct = total > 0 ? ((v / total) * 100).toFixed(1) : "0";
                return `${ctx.label}: ${formatRupiah(v)} (${pct}%)`;
              }
            }
          },
          // ⭐ DATALABELS — di dalam donut
          datalabels: {
            color: "#ffffff",
            font: {
              size: 11,
              weight: "700",
            },
            textAlign: "center",
            formatter: (value, ctx) => {
              if (!value || value === 0) return "";
              const pct = total > 0 ? ((value / total) * 100).toFixed(1) : "0";
              // Baris 1: persen, baris 2: nilai singkat
              return pct + "%\n" + formatSingkat(value);
            },
            display: (ctx) => {
              // Sembunyikan label kalau slice terlalu kecil (<3%)
              const value = ctx.dataset.data[ctx.dataIndex];
              const pct = total > 0 ? (value / total) * 100 : 0;
              return pct >= 3;
            },
          }
        }
      }
    });
  }

  // =========================================================
  // CHART: NILAI TAGIHAN PER PASAR (Grouped Bar)
  // ⭐ + Label angka di atas setiap bar
  // =========================================================
  function buildChartPasar() {
    if (!dataPasar) return;

    let datasets = [];
    if (Array.isArray(dataPasar.series) && dataPasar.series.length > 0) {
      datasets = dataPasar.series.map((s) => ({
        label: s.name,
        data: s.values,
        backgroundColor: WARNA_JENIS[s.name] || "#94a3b8",
        borderRadius: 3,
        barPercentage: 0.7,
        categoryPercentage: 0.7,
      }));
    } else {
      datasets = [
        { label: "Listrik", data: dataPasar.listrik || [], backgroundColor: WARNA_JENIS["Listrik"], borderRadius: 3, barPercentage: 0.7, categoryPercentage: 0.7 },
        { label: "Tempat",  data: dataPasar.tempat || [],  backgroundColor: WARNA_JENIS["Tempat"],  borderRadius: 3, barPercentage: 0.7, categoryPercentage: 0.7 },
        { label: "Air",     data: dataPasar.air || [],     backgroundColor: WARNA_JENIS["Air"],     borderRadius: 3, barPercentage: 0.7, categoryPercentage: 0.7 },
      ];
    }

    datasets.sort((a, b) => {
      const ia = URUTAN_JENIS.indexOf(a.label);
      const ib = URUTAN_JENIS.indexOf(b.label);
      return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
    });

    safeNewChart("chartPasar", {
      type: "bar",
      data: { labels: dataPasar.labels, datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 30,   // ⭐ beri ruang untuk label di atas bar
          }
        },
        plugins: {
          legend: {
            position: "top",
            labels: { font: { size: 11 }, padding: 12, usePointStyle: true }
          },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${formatRupiah(ctx.parsed.y)}`
            }
          },
          // ⭐ DATALABELS
          datalabels: {
            anchor: "end",
            align: "top",
            offset: 4,
            color: "#1f2937",
            font: {
              size: 9,       // ⭐ lebih kecil karena grouped bar
              weight: "600",
            },
            rotation: -90,   // ⭐ miring biar tidak tumpang tindih
            formatter: (value) => {
              if (!value || value === 0) return "";
              return formatSingkat(value);
            },
            // Sembunyikan label kalau bar terlalu kecil nilainya
            display: (ctx) => {
              const value = ctx.dataset.data[ctx.dataIndex];
              return value && value > 0;
            },
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#374151", font: { size: 10 }, maxRotation: 45, minRotation: 0 }
          },
          y: {
            beginAtZero: true,
            grid: { color: "#f1f5f9" },
            ticks: { color: "#6b7280", font: { size: 11 }, callback: (v) => formatShortAxis(v) }
          }
        }
      }
    });
  }

  // =========================================================
  // CHART: TREN (TIDAK DIUBAH — tanpa datalabels biar bersih)
  // =========================================================
  function buildChartTren() {
    if (!dataTren) return;

    safeNewChart("chartTren", {
      type: "line",
      data: {
        labels: dataTren.labels,
        datasets: [{
          label: "Total Nilai",
          data: dataTren.values,
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59, 130, 246, 0.15)",
          fill: true,
          tension: 0.3,
          pointRadius: 2,
          pointHoverRadius: 5,
          pointBackgroundColor: "#3b82f6",
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: { label: (ctx) => formatRupiah(ctx.parsed.y) }
          },
          // Tren: matikan datalabels biar tidak rame
          datalabels: { display: false }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#374151", font: { size: 10 }, maxRotation: 45, minRotation: 0 }
          },
          y: {
            beginAtZero: true,
            grid: { color: "#f1f5f9" },
            ticks: { color: "#6b7280", font: { size: 11 }, callback: (v) => formatShortAxis(v) }
          }
        }
      }
    });
  }

  // =========================================================
  // INIT
  // =========================================================
  document.addEventListener("DOMContentLoaded", function () {
    console.log("=== Dashboard.js starting ===");
    console.log("typeof Chart:", typeof Chart);
    console.log("ChartDataLabels:", typeof ChartDataLabels);
    console.log("dataCabang:", dataCabang);

    setTimeout(function () {
      buildChartCabang();
      buildChartDistribusi();
      buildChartPasar();
      buildChartTren();
      console.log("=== Semua chart selesai ===");
    }, 100);
  });

})();