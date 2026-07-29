# Mobile Numeric Report Design

Date: 2026-07-29  
Status: Approved

## Problem

Scheduled reports now contain explicit values for every discussed market
indicator. The current Markdown rendering preserves the data, but on a phone
the two wide metric tables dominate the page and make the report tiring to
scan.

## Considered approaches

1. **Anomaly-first progressive disclosure — selected.** Derive six key cards
   from the report's numeric table, show risk counts, and collapse the complete
   price and technical tables on narrow screens. This keeps every number
   available while making the first screen useful.
2. **Accordion-only.** Collapse every report section. This is simpler, but
   hides news and conclusions that should remain visible.
3. **Separate dashboard and narrative pages.** This gives maximum layout
   freedom, but splits one report across multiple URLs and increases navigation
   cost on mobile.

## Approved experience

- The report header is followed by a sticky section navigator.
- `核心数字看板` is enhanced into:
  - a compact risk summary showing shock, watch, and stable counts;
  - six key metric cards selected by report scope, with current value, 1-day
    change, and 1-month change;
  - two accessible detail panels containing all price and technical rows.
- On screens up to 720 px, metric detail panels default closed. On desktop
  they default open.
- News, confirmation signals, scenarios, and portfolio conclusions remain
  visible without extra taps.
- Narrative/evidence tables become vertical labelled cards on mobile. Numeric
  tables retain horizontal comparison, a sticky first column, and an explicit
  scroll affordance.

## Selection and risk semantics

- US reports prioritize SPY, QQQ, SMH, VIX, USDJPY, and Brent.
- Asia reports prioritize Nikkei 225, TOPIX, Toyota, Kioxia, KOSPI, and
  USDJPY.
- Full reports prioritize Nikkei 225, Toyota, SPY, SMH, USDJPY, and Brent.
- Missing priorities are filled by the largest absolute 1-day move.
- A row is `shock` when absolute 1-day change is at least 3% or absolute
  1-month change is at least 15%; `watch` at 1.5%/8%; otherwise `stable`.
- VIX and Brent use risk semantics rather than equity up/down semantics.
  Status is always conveyed with text as well as color.

## Architecture and data flow

The Markdown contract is unchanged. `report.html` parses the generated HTML,
finds the `核心数字看板` heading and its next two tables, then enhances the DOM.
The feature is progressive: if headings or tables are absent, the original
report remains readable.

No framework or build step is introduced. New behavior lives in
`assets/report.js`; presentation remains in `assets/style.css`.

## Accessibility and error handling

- Touch targets are at least 44 px.
- `details/summary` provides native keyboard and screen-reader behavior.
- Cards include text status labels; color is not the sole signal.
- Reduced-motion preferences disable transitions.
- If table parsing fails, no data is removed and the original table remains.

## Verification

- Test at 390 x 844 and 430 x 932 mobile viewports plus a 1440 px desktop.
- Confirm no document-level horizontal overflow.
- Confirm six cards, risk counts, sticky navigation, and expandable metric
  details.
- Confirm news tables render as labelled cards on mobile.
- Confirm desktop tables are open and remain comparable.
- Confirm links, report loading, and chart navigation still work.

