(function () {
  "use strict";

  const PRIORITIES = {
    us: [
      ["SPY", "标普500"],
      ["QQQ", "纳指100"],
      ["SMH", "半导体"],
      ["VIX"],
      ["USDJPY"],
      ["BRENT", "原油"],
    ],
    asia: [
      ["日经225"],
      ["TOPIX"],
      ["丰田"],
      ["铠侠"],
      ["KOSPI"],
      ["USDJPY"],
    ],
    full: [
      ["日经225"],
      ["丰田"],
      ["SPY", "标普500"],
      ["SMH", "半导体"],
      ["USDJPY"],
      ["BRENT", "原油"],
    ],
  };

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function normalized(text) {
    return text.toUpperCase().replace(/\s+/g, "");
  }

  function firstPercent(text) {
    const match = String(text).replace(/,/g, "").match(/[+-]?\d+(?:\.\d+)?\s*%/);
    return match ? Number.parseFloat(match[0]) : null;
  }

  function parseTable(table) {
    const headers = Array.from(table.querySelectorAll("thead th")).map((th) =>
      th.textContent.trim()
    );
    return Array.from(table.querySelectorAll("tbody tr")).map((tr) => {
      const cells = Array.from(tr.querySelectorAll("td")).map((td) =>
        td.textContent.trim()
      );
      const values = {};
      headers.forEach((header, index) => {
        values[header] = cells[index] || "";
      });
      return {
        name: cells[0] || "",
        values,
        current: cells[1] || "数据缺失",
        d1: cells[2] || "数据缺失",
        w1: cells[3] || "数据缺失",
        m1: cells[4] || "数据缺失",
      };
    });
  }

  function riskFor(row) {
    const d1 = Math.abs(firstPercent(row.d1) || 0);
    const m1 = Math.abs(firstPercent(row.m1) || 0);
    if (d1 >= 3 || m1 >= 15) return { level: "shock", label: "冲击" };
    if (d1 >= 1.5 || m1 >= 8) return { level: "watch", label: "观察" };
    return { level: "stable", label: "稳定" };
  }

  function riskScore(row) {
    return Math.abs(firstPercent(row.d1) || 0) * 2 +
      Math.abs(firstPercent(row.m1) || 0);
  }

  function chooseRows(rows, scope) {
    const selected = [];
    const used = new Set();
    const groups = PRIORITIES[scope] || PRIORITIES.full;

    groups.forEach((aliases) => {
      const row = rows.find((candidate) => {
        if (used.has(candidate)) return false;
        const name = normalized(candidate.name);
        return aliases.some((alias) => name.includes(normalized(alias)));
      });
      if (row) {
        selected.push(row);
        used.add(row);
      }
    });

    rows
      .filter((row) => !used.has(row))
      .sort((a, b) => riskScore(b) - riskScore(a))
      .forEach((row) => {
        if (selected.length < 6) selected.push(row);
      });

    return selected.slice(0, 6);
  }

  function makeMetricCard(row) {
    const risk = riskFor(row);
    const card = el("article", "metric-card");
    card.dataset.status = risk.level;
    card.setAttribute(
      "aria-label",
      `${row.name}，现值${row.current}，1日${row.d1}，1月${row.m1}，${risk.label}`
    );

    const top = el("div", "metric-card-top");
    top.append(el("span", "metric-card-name", row.name));
    top.append(el("span", `metric-status metric-status-${risk.level}`, risk.label));

    const value = el("div", "metric-card-value", row.current);
    const moves = el("div", "metric-card-moves");
    const day = el("span", "metric-move");
    day.append(el("small", "", "1日"));
    day.append(el("b", (firstPercent(row.d1) || 0) >= 0 ? "move-up" : "move-down", row.d1));
    const month = el("span", "metric-move");
    month.append(el("small", "", "1月"));
    month.append(el("b", (firstPercent(row.m1) || 0) >= 0 ? "move-up" : "move-down", row.m1));
    moves.append(day, month);
    card.append(top, value, moves);
    return card;
  }

  function makeRiskRibbon(rows) {
    const counts = { shock: 0, watch: 0, stable: 0 };
    rows.forEach((row) => {
      counts[riskFor(row).level] += 1;
    });
    const ribbon = el("div", "risk-ribbon");
    [
      ["shock", "冲击", counts.shock],
      ["watch", "观察", counts.watch],
      ["stable", "稳定", counts.stable],
    ].forEach(([level, label, count]) => {
      const item = el("div", `risk-count risk-count-${level}`);
      item.append(el("strong", "", String(count)));
      item.append(el("span", "", label));
      ribbon.append(item);
    });
    return ribbon;
  }

  function wrapMetricTable(table, label) {
    const details = el("details", "metric-details");
    details.open = !window.matchMedia("(max-width: 720px)").matches;
    const rowCount = table.querySelectorAll("tbody tr").length;
    const summary = el("summary", "metric-summary");
    summary.append(el("span", "", label));
    summary.append(el("small", "", `${rowCount}项 · 点击展开`));
    const scroller = el("div", "metric-scroll");
    table.classList.add("metric-table");
    table.parentNode.insertBefore(details, table);
    scroller.append(table);
    details.append(summary, scroller);
    return details;
  }

  function enhanceNumericBoard(article, scope) {
    const heading = Array.from(article.querySelectorAll("h2")).find((h2) =>
      h2.textContent.includes("数字看板")
    );
    if (!heading) return;

    const tables = [];
    let cursor = heading.nextElementSibling;
    while (cursor && cursor.tagName !== "H2") {
      if (cursor.tagName === "TABLE") tables.push(cursor);
      cursor = cursor.nextElementSibling;
    }
    if (!tables.length) return;

    const rows = parseTable(tables[0]);
    if (!rows.length) return;

    const dashboard = el("section", "signal-dashboard");
    dashboard.setAttribute("aria-label", "关键市场指标");
    dashboard.append(makeRiskRibbon(rows));
    const grid = el("div", "metric-card-grid");
    chooseRows(rows, scope).forEach((row) => grid.append(makeMetricCard(row)));
    dashboard.append(grid);
    tables[0].parentNode.insertBefore(dashboard, tables[0]);

    wrapMetricTable(tables[0], "全部价格与周期表现");
    if (tables[1]) wrapMetricTable(tables[1], "技术位置与关键线");
  }

  function makeNarrativeTablesResponsive(article) {
    article.querySelectorAll("table:not(.metric-table)").forEach((table) => {
      const headers = Array.from(table.querySelectorAll("thead th")).map((th) =>
        th.textContent.trim()
      );
      if (!headers.length) return;
      table.classList.add("stack-table");
      table.querySelectorAll("tbody tr").forEach((tr) => {
        Array.from(tr.querySelectorAll("td")).forEach((td, index) => {
          td.dataset.label = headers[index] || "";
        });
      });
    });
  }

  function addSectionNavigation(article) {
    const candidates = [
      ["数字看板", "数字"],
      ["新闻", "新闻"],
      ["确认", "信号"],
      ["情景", "情景"],
      ["组合", "组合"],
    ];
    const links = [];
    const headings = Array.from(article.querySelectorAll("h2"));

    candidates.forEach(([needle, label]) => {
      const heading = headings.find((h2) => h2.textContent.includes(needle));
      if (!heading || links.some((item) => item.heading === heading)) return;
      heading.id = heading.id || `section-${links.length + 1}`;
      heading.style.scrollMarginTop = "76px";
      links.push({ heading, label });
    });
    if (links.length < 2) return;

    const nav = el("nav", "report-jump");
    nav.setAttribute("aria-label", "报告章节导航");
    links.forEach(({ heading, label }) => {
      const anchor = el("a", "", label);
      anchor.href = `#${heading.id}`;
      nav.append(anchor);
    });
    article.parentNode.insertBefore(nav, article);
  }

  function markActionSections(article) {
    article.querySelectorAll("h2").forEach((heading) => {
      if (/确认|信号|组合结论|情景/.test(heading.textContent)) {
        heading.classList.add("action-heading");
      }
    });
  }

  window.enhanceMarketReport = function ({ article, type }) {
    if (!article) return;
    const scope = type === "usopen" || type === "usclose"
      ? "us"
      : type === "open" || type === "midday" || type === "close"
        ? "asia"
        : "full";
    enhanceNumericBoard(article, scope);
    makeNarrativeTablesResponsive(article);
    markActionSections(article);
    addSectionNavigation(article);
    document.body.classList.add("report-enhanced");
  };
})();
