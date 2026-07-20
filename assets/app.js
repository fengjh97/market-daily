/* 市場日報 chart engine — renders charts.html from a charts_*.json payload.
   Data contract (produced by tools/export_charts.py):
   {
     generated, scope, title,
     dashboard: [{group,name,ticker,last,d1,w1,m1,rsi,vs50,vs200,bbz,dd}],
     charts:    [{name,ticker,dates[],o[],h[],l[],c[],v[]}],
     scenarios: [{name,ticker,histDates[],histClose[],days[],p5[],p25[],p50[],p75[],p95[],
                  events:[{date,label}], range:[lo,hi]}]
   }                                                                              */
const UP = "#e05252", DOWN = "#2fb3c7", GOLD = "#c9a961", PURPLE = "#8b7cc4",
      INK = "#e6e8ec", DIM = "#8b93a1", GRID = "rgba(230,232,236,.06)";
const FONT = {family: "'Zen Kaku Gothic New','Hiragino Sans',sans-serif", color: DIM};
const BASE = {paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
              font: FONT, hovermode: "x unified", dragmode: false,
              hoverlabel: {bgcolor: "#1a2230", bordercolor: "#2a3444", font: {color: INK}}};
const CFG = {displayModeBar: false, responsive: true,
             scrollZoom: false, doubleClick: false, showAxisDragHandles: false,
             showTips: false};
/* 触摸设备:一切缩放/拖拽禁用,区间切换只走按钮;页面滚动永不被图表劫持 */
const COARSE = matchMedia("(pointer: coarse)").matches;
const NARROW = () => window.innerWidth < 560;

const sma = (a, n) => a.map((_, i) =>
  i < n - 1 ? null : a.slice(i - n + 1, i + 1).reduce((s, x) => s + x, 0) / n);
const std = (a, n) => a.map((_, i) => {
  if (i < n - 1) return null;
  const w = a.slice(i - n + 1, i + 1), m = w.reduce((s, x) => s + x, 0) / n;
  return Math.sqrt(w.reduce((s, x) => s + (x - m) ** 2, 0) / n);
});

function fmtPct(x) {
  if (x === null || x === undefined || Number.isNaN(x)) return "<span class=flat>—</span>";
  const cls = x > 0 ? "pos" : x < 0 ? "neg" : "flat";
  return `<span class=${cls}>${x > 0 ? "+" : ""}${x.toFixed(1)}%</span>`;
}

function renderDashboard(rows) {
  let grp = null, html = `<div class=dash-wrap><table class=dash>
    <tr><th>标的</th><th>最新</th><th>1日</th><th>1周</th><th>1月</th><th>RSI</th>
    <th>vs MA50</th><th>vs MA200</th><th>布林σ</th><th>距高点</th></tr>`;
  for (const r of rows) {
    if (r.group !== grp) { grp = r.group; html += `<tr class=grp><td colspan=10>${grp}</td></tr>`; }
    const rsi = r.rsi === null ? "—" : Math.round(r.rsi);
    const bbz = r.bbz === null ? "—" : (r.bbz > 0 ? "+" : "") + r.bbz.toFixed(1);
    html += `<tr><td>${r.name} <span style="color:var(--faint);font-size:10px">${r.ticker}</span></td>
      <td style="color:${INK}">${r.last.toLocaleString(undefined,{maximumFractionDigits:1})}</td>
      <td>${fmtPct(r.d1)}</td><td>${fmtPct(r.w1)}</td><td>${fmtPct(r.m1)}</td>
      <td>${rsi}</td><td>${fmtPct(r.vs50)}</td><td>${fmtPct(r.vs200)}</td>
      <td>${bbz}σ</td><td>${fmtPct(r.dd)}</td></tr>`;
  }
  return html + "</table></div>";
}

function candleChart(el, ch) {
  const mid = sma(ch.c, 20), sd = std(ch.c, 20);
  const upBB = mid.map((m, i) => m === null ? null : m + 2 * sd[i]);
  const dnBB = mid.map((m, i) => m === null ? null : m - 2 * sd[i]);
  const volColors = ch.c.map((c, i) => c >= ch.o[i] ? UP : DOWN);
  const lastM = ch.dates[ch.dates.length - 1], firstView =
    new Date(new Date(lastM).getTime() - 31 * 864e5).toISOString().slice(0, 10);

  /* 核心修复:Y轴始终随可见X窗口重算(否则1月窗口套6月量程,K线被压扁) */
  const yWindow = (a, b) => {
    let lo = Infinity, hi = -Infinity;
    for (let i = 0; i < ch.dates.length; i++) {
      const d = ch.dates[i];
      if (d < a || d > b) continue;
      if (ch.l[i] < lo) lo = ch.l[i];
      if (ch.h[i] > hi) hi = ch.h[i];
      if (dnBB[i] !== null && dnBB[i] < lo) lo = dnBB[i];
      if (upBB[i] !== null && upBB[i] > hi) hi = upBB[i];
    }
    if (!isFinite(lo)) return null;
    const pad = (hi - lo) * 0.05 || hi * 0.02;
    return [lo - pad, hi + pad];
  };

  Plotly.newPlot(el, [
    {x: ch.dates, y: upBB, name: "布林", showlegend: false,
     line: {width: 1, color: "rgba(139,124,196,.5)"}, hoverinfo: "skip"},
    {x: ch.dates, y: dnBB, name: "布林", showlegend: false,
     line: {width: 1, color: "rgba(139,124,196,.5)"},
     fill: "tonexty", fillcolor: "rgba(139,124,196,.07)", hoverinfo: "skip"},
    {type: "candlestick", x: ch.dates, open: ch.o, high: ch.h, low: ch.l, close: ch.c,
     name: "K线", increasing: {line: {color: UP}, fillcolor: UP},
     decreasing: {line: {color: DOWN}, fillcolor: DOWN}},
    {x: ch.dates, y: sma(ch.c, 50), name: "MA50", line: {width: 2, color: GOLD}},
    {x: ch.dates, y: sma(ch.c, 200), name: "MA200", line: {width: 2, color: PURPLE}},
    {type: "bar", x: ch.dates, y: ch.v, name: "成交量", yaxis: "y2", showlegend: false,
     marker: {color: volColors}, opacity: .45, hoverinfo: "skip"},
  ], Object.assign({}, BASE, {
    title: {text: `${ch.name} <span style="font-size:12px;color:${DIM}">${ch.ticker}</span>`,
            font: {size: 15, color: INK}, x: 0.02},
    height: NARROW() ? 350 : 430, margin: {l: 8, r: 46, t: 44, b: 8},
    legend: NARROW() ? {orientation: "h", y: -0.08, font: {size: 10}}
                     : {orientation: "h", y: 1.09, font: {size: 10.5}},
    xaxis: {rangeslider: {visible: false}, range: [firstView, lastM], gridcolor: GRID,
      fixedrange: true,
      rangeselector: {bgcolor: "#1a2230", activecolor: "#2a3444",
        font: {color: INK, size: COARSE ? 14 : 11},
        borderwidth: 0, x: 1, xanchor: "right", y: 1.12,
        buttons: [{count: 7, label: "1周", step: "day", stepmode: "backward"},
                  {count: 1, label: "1月", step: "month", stepmode: "backward"},
                  {count: 3, label: "3月", step: "month", stepmode: "backward"},
                  {count: 6, label: "6月", step: "month", stepmode: "backward"}]}},
    yaxis: {domain: [0.24, 1], side: "right", gridcolor: GRID, fixedrange: true},
    yaxis2: {domain: [0, 0.18], side: "right", gridcolor: GRID, showticklabels: false,
             fixedrange: true},
  }), CFG).then(() => {
    const yr = yWindow(firstView, lastM);
    if (yr) Plotly.relayout(el, {"yaxis.range": yr});
    el.on("plotly_relayout", ev => {           // 区间按钮切换后重算Y量程
      const a = ev["xaxis.range[0]"] || (ev["xaxis.range"] && ev["xaxis.range"][0]);
      const b = ev["xaxis.range[1]"] || (ev["xaxis.range"] && ev["xaxis.range"][1]);
      if (!a) return;                           // 我们自己的yaxis relayout不会带xaxis键,无循环
      const yr2 = yWindow(String(a).slice(0, 10), String(b).slice(0, 10));
      if (yr2) Plotly.relayout(el, {"yaxis.range": yr2});
    });
  });
}

function scenarioChart(el, sc) {
  const traces = [
    {x: sc.histDates, y: sc.histClose, name: "近40日实际", line: {width: 2, color: INK}},
    {x: sc.days, y: sc.p95, name: "乐观边界95%", line: {width: 1.5, color: UP, dash: "dot"}},
    {x: sc.days, y: sc.p5, name: "悲观边界5%", line: {width: 1.5, color: DOWN, dash: "dot"}},
    {x: sc.days, y: sc.p75, line: {width: 0}, showlegend: false, hoverinfo: "skip"},
    {x: sc.days, y: sc.p25, name: "中枢25-75%", line: {width: 0}, fill: "tonexty",
     fillcolor: "rgba(139,124,196,.14)"},
    {x: sc.days, y: sc.p50, name: "中位路径", line: {width: 2, color: PURPLE, dash: "dash"}},
  ];
  const shapes = [], annos = [], inWindow = [];
  for (const ev of sc.events || []) {
    if (ev.date >= sc.days[0] && ev.date <= sc.days[sc.days.length - 1]) {
      inWindow.push(ev);
      shapes.push({type: "line", x0: ev.date, x1: ev.date, y0: 0, y1: 1, yref: "paper",
                   line: {color: GOLD, width: 1, dash: "dash"}});
      /* 窄屏不放旋转标注(相邻日期必然叠字),改为图下事件说明行 */
      if (!NARROW()) {
        annos.push({x: ev.date, y: 1.04, yref: "paper", text: ev.label, showarrow: false,
                    font: {size: 10, color: GOLD}, textangle: -28});
      }
    }
  }
  Plotly.newPlot(el, traces, Object.assign({}, BASE, {
    title: {text: `${sc.name} 未来10日情景锥 <span style="font-size:11.5px;color:${DIM}">` +
      `10日后区间 ${sc.range[0] > 0 ? "+" : ""}${sc.range[0].toFixed(1)}% ~ +${sc.range[1].toFixed(1)}%</span>`,
      font: {size: 14.5, color: INK}, x: 0.02},
    height: NARROW() ? 300 : 360, margin: {l: 8, r: 46, t: 46, b: 8},
    shapes, annotations: annos,
    legend: {orientation: "h", y: -0.16, font: {size: NARROW() ? 9.5 : 10.5},
             itemwidth: 30},
    xaxis: {gridcolor: GRID, fixedrange: true},
    yaxis: {side: "right", gridcolor: GRID, fixedrange: true},
  }), CFG);
  if (NARROW() && inWindow.length) {          // 事件说明行(替代旋转标注)
    const cap = document.createElement("div");
    cap.className = "ev-caption";
    cap.innerHTML = "┊ " + inWindow.map(e =>
      `<b>${e.date.slice(5).replace("-", "/")}</b> ${e.label}`).join(" · ");
    el.appendChild(cap);
  }
}

async function renderCharts() {
  const p = new URLSearchParams(location.search).get("p");
  if (!p) { document.getElementById("stage").textContent = "缺少 ?p= 参数"; return; }
  const res = await fetch(`data/${p}.json?t=${Date.now()}`);
  if (!res.ok) { document.getElementById("stage").textContent = "数据不存在: " + p; return; }
  const d = await res.json();
  document.getElementById("page-title").textContent = d.title || "图表终端";
  document.getElementById("gen-ts").textContent = d.generated + " JST";
  const stage = document.getElementById("stage");
  stage.innerHTML = "";
  const add = (tag, cls) => { const e = document.createElement(tag);
    if (cls) e.className = cls; stage.appendChild(e); return e; };
  add("h2", "sec").textContent = "Dashboard · 仪表盘";
  add("div").innerHTML = renderDashboard(d.dashboard);

  /* 懒渲染:图表进入视口前只占位,滚到附近才画——手机滑动不卡 */
  const io = new IntersectionObserver(entries => {
    for (const en of entries) {
      if (!en.isIntersecting) continue;
      io.unobserve(en.target);
      const {kind, idx} = en.target.dataset;
      en.target.style.minHeight = "";
      (kind === "sc" ? scenarioChart : candleChart)(
        en.target, kind === "sc" ? d.scenarios[idx] : d.charts[idx]);
    }
  }, {rootMargin: "700px 0px"});
  const defer = (kind, idx, h) => {
    const el = add("div", "chart-box");
    el.dataset.kind = kind; el.dataset.idx = idx;
    el.style.minHeight = h + "px";
    io.observe(el);
  };
  if (d.scenarios && d.scenarios.length) {
    add("h2", "sec").textContent = "Scenarios · 情景模拟";
    d.scenarios.forEach((_, i) => defer("sc", i, NARROW() ? 340 : 400));
  }
  add("h2", "sec").textContent = "Charts · K线";
  d.charts.forEach((_, i) => defer("ch", i, NARROW() ? 400 : 470));
}
