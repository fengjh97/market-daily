# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: market-mobile-check.spec.js >> us close report fits a 390px mobile viewport
- Location: ../../../../private/tmp/market-mobile-check.spec.js:9:1

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  -  1
+ Received  + 32

- Array []
+ Array [
+   Object {
+     "node": "TH.",
+     "parent": "TR.",
+     "rect": Object {
+       "bottom": 2881.34375,
+       "height": 35.765625,
+       "left": 337.703125,
+       "right": 407.390625,
+       "top": 2845.578125,
+       "width": 69.6875,
+       "x": 337.703125,
+       "y": 2845.578125,
+     },
+     "text": "六月回撤",
+   },
+   Object {
+     "node": "TH.",
+     "parent": "TR.",
+     "rect": Object {
+       "bottom": 2881.34375,
+       "height": 35.765625,
+       "left": 407.390625,
+       "right": 489.5,
+       "top": 2845.578125,
+       "width": 82.109375,
+       "x": 407.390625,
+       "y": 2845.578125,
+     },
+     "text": "下一确认线",
+   },
+ ]
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - banner [ref=e3]:
    - heading "市場日報 🌃 美股收盘 US CLOSE" [level=1] [ref=e4]:
      - link "市場日報" [ref=e5] [cursor=pointer]:
        - /url: ./
      - generic [ref=e6]: 🌃 美股收盘 US CLOSE
    - generic [ref=e8]:
      - text: 2026-08-06 05:13 JST
      - generic [ref=e9]:
        - text: ·
        - link "❖ 打开图表端末" [ref=e10] [cursor=pointer]:
          - /url: charts.html?p=2026-08-06/charts_us
  - navigation "报告章节导航" [ref=e11]:
    - link "数字" [ref=e12] [cursor=pointer]:
      - /url: "#section-1"
    - link "新闻" [ref=e13] [cursor=pointer]:
      - /url: "#section-2"
    - link "组合" [ref=e14] [cursor=pointer]:
      - /url: "#section-3"
  - article [ref=e15]:
    - heading "美股收盘快照 · 2026-08-06 JST早" [level=1] [ref=e16]
    - paragraph [ref=e17]:
      - strong [ref=e18]: 一句话定性：事件驱动的高位轮动，不是全面risk-off。
      - text: SPY收769.77美元（-0.20%）、QQQ 717.30美元（-0.90%）、SMH 569.70美元（-1.04%），但NVDA独涨3.43%，VIX恐慌指数反而降5.88%至15.53。
    - heading "核心数字看板" [level=2] [ref=e19]
    - region "关键市场指标" [ref=e20]:
      - generic [ref=e21]:
        - generic [ref=e22]:
          - strong [ref=e23]: "3"
          - generic [ref=e24]: 冲击
        - generic [ref=e25]:
          - strong [ref=e26]: "0"
          - generic [ref=e27]: 观察
        - generic [ref=e28]:
          - strong [ref=e29]: "12"
          - generic [ref=e30]: 稳定
      - generic [ref=e31]:
        - article "SPY，现值769.77美元，1日-0.20%，1月+2.95%，稳定" [ref=e32]:
          - generic [ref=e33]:
            - generic [ref=e34]: SPY
            - generic [ref=e35]: 稳定
          - generic [ref=e36]: 769.77美元
          - generic [ref=e37]:
            - generic [ref=e38]:
              - generic [ref=e39]: 1日
              - generic [ref=e40]: "-0.20%"
            - generic [ref=e41]:
              - generic [ref=e42]: 1月
              - generic [ref=e43]: +2.95%
        - article "QQQ，现值717.30美元，1日-0.90%，1月+1.11%，稳定" [ref=e44]:
          - generic [ref=e45]:
            - generic [ref=e46]: QQQ
            - generic [ref=e47]: 稳定
          - generic [ref=e48]: 717.30美元
          - generic [ref=e49]:
            - generic [ref=e50]:
              - generic [ref=e51]: 1日
              - generic [ref=e52]: "-0.90%"
            - generic [ref=e53]:
              - generic [ref=e54]: 1月
              - generic [ref=e55]: +1.11%
        - article "SMH，现值569.70美元，1日-1.04%，1月-2.02%，稳定" [ref=e56]:
          - generic [ref=e57]:
            - generic [ref=e58]: SMH
            - generic [ref=e59]: 稳定
          - generic [ref=e60]: 569.70美元
          - generic [ref=e61]:
            - generic [ref=e62]:
              - generic [ref=e63]: 1日
              - generic [ref=e64]: "-1.04%"
            - generic [ref=e65]:
              - generic [ref=e66]: 1月
              - generic [ref=e67]: "-2.02%"
        - article "VIX，现值15.53点，1日-5.88%，1月-3.72%，冲击" [ref=e68]:
          - generic [ref=e69]:
            - generic [ref=e70]: VIX
            - generic [ref=e71]: 冲击
          - generic [ref=e72]: 15.53点
          - generic [ref=e73]:
            - generic [ref=e74]:
              - generic [ref=e75]: 1日
              - generic [ref=e76]: "-5.88%"
            - generic [ref=e77]:
              - generic [ref=e78]: 1月
              - generic [ref=e79]: "-3.72%"
        - article "USDJPY，现值157.719，1日+0.190/+0.12%，1月-2.70%，稳定" [ref=e80]:
          - generic [ref=e81]:
            - generic [ref=e82]: USDJPY
            - generic [ref=e83]: 稳定
          - generic [ref=e84]: "157.719"
          - generic [ref=e85]:
            - generic [ref=e86]:
              - generic [ref=e87]: 1日
              - generic [ref=e88]: +0.190/+0.12%
            - generic [ref=e89]:
              - generic [ref=e90]: 1月
              - generic [ref=e91]: "-2.70%"
        - article "Brent，现值79.39美元/桶，1日+0.04%，1月+7.05%，稳定" [ref=e92]:
          - generic [ref=e93]:
            - generic [ref=e94]: Brent
            - generic [ref=e95]: 稳定
          - generic [ref=e96]: 79.39美元/桶
          - generic [ref=e97]:
            - generic [ref=e98]:
              - generic [ref=e99]: 1日
              - generic [ref=e100]: +0.04%
            - generic [ref=e101]:
              - generic [ref=e102]: 1月
              - generic [ref=e103]: +7.05%
    - group [ref=e104]:
      - generic "＋ 全部价格与周期表现 15项 · 点击展开" [ref=e105] [cursor=pointer]:
        - text: ＋
        - generic [ref=e106]: 全部价格与周期表现
        - generic [ref=e107]: 15项 · 点击展开
      - text: 横向滑动查看全部 →
    - paragraph [ref=e108]: RSI14是14日相对强弱指数，MA50/MA200是50/200日移动平均线，VIX是标普500期权隐含波动率指数，bp为基点（0.01个百分点）。
    - group [ref=e109]:
      - generic "＋ 技术位置与关键线 15项 · 点击展开" [ref=e110] [cursor=pointer]:
        - text: ＋
        - generic [ref=e111]: 技术位置与关键线
        - generic [ref=e112]: 15项 · 点击展开
      - text: 横向滑动查看全部 →
    - paragraph [ref=e113]: 美国数据源：Yahoo Finance via yfinance，生成于2026-08-06 05:08 JST；最后一根日线为8月5日美国交易日。
    - heading "亚洲前置仓位（8月5日收盘）" [level=3] [ref=e114]
    - table [ref=e115]:
      - rowgroup [ref=e116]:
        - row [ref=e117]:
          - columnheader "标的" [ref=e118]
          - columnheader "现值" [ref=e119]
          - columnheader "1日" [ref=e120]
          - columnheader "1周" [ref=e121]
          - columnheader "1月" [ref=e122]
          - columnheader "当日高低" [ref=e123]
      - rowgroup [ref=e124]:
        - row [ref=e125]:
          - cell "标的 日经225" [ref=e126]
          - cell "现值 66,300.44点" [ref=e127]
          - cell "1日 +3.66%" [ref=e128]
          - cell "1周 +7.92%" [ref=e129]
          - cell "1月 -4.93%" [ref=e130]
          - cell "当日高低 64,555.52–66,302.52" [ref=e131]
        - row [ref=e132]:
          - cell "标的 丰田" [ref=e133]
          - cell "现值 2,914.5日元" [ref=e134]
          - cell "1日 -0.14%" [ref=e135]
          - cell "1周 -9.60%" [ref=e136]
          - cell "1月 -0.29%" [ref=e137]
          - cell "当日高低 2,869.5–2,924.5" [ref=e138]
        - row [ref=e139]:
          - cell "标的 铠侠" [ref=e140]
          - cell "现值 54,300日元" [ref=e141]
          - cell "1日 +4.24%" [ref=e142]
          - cell "1周 +41.48%" [ref=e143]
          - cell "1月 -33.45%" [ref=e144]
          - cell "当日高低 53,400–56,800" [ref=e145]
        - row [ref=e146]:
          - cell "标的 软银集团" [ref=e147]
          - cell "现值 5,958日元" [ref=e148]
          - cell "1日 +13.96%" [ref=e149]
          - cell "1周 +25.67%" [ref=e150]
          - cell "1月 -0.35%" [ref=e151]
          - cell "当日高低 5,605–5,958" [ref=e152]
        - row [ref=e153]:
          - cell "标的 东京电子" [ref=e154]
          - cell "现值 58,550日元" [ref=e155]
          - cell "1日 +3.26%" [ref=e156]
          - cell "1周 +17.10%" [ref=e157]
          - cell "1月 -19.04%" [ref=e158]
          - cell "当日高低 58,300–59,700" [ref=e159]
        - row [ref=e160]:
          - cell "标的 Advantest" [ref=e161]
          - cell "现值 33,720日元" [ref=e162]
          - cell "1日 +8.77%" [ref=e163]
          - cell "1周 +33.81%" [ref=e164]
          - cell "1月 +14.05%" [ref=e165]
          - cell "当日高低 32,390–33,840" [ref=e166]
    - table [ref=e167]:
      - rowgroup [ref=e168]:
        - row [ref=e169]:
          - columnheader "标的" [ref=e170]
          - columnheader "RSI14" [ref=e171]
          - columnheader "MA50（差距）" [ref=e172]
          - columnheader "MA200（差距）" [ref=e173]
          - columnheader "六月回撤" [ref=e174]
          - columnheader "下一确认线" [ref=e175]
      - rowgroup [ref=e176]:
        - row [ref=e177]:
          - cell "标的 日经225" [ref=e178]
          - cell "RSI14 52.0" [ref=e179]
          - cell "MA50（差距） 67,132.96（-1.24%）" [ref=e180]
          - cell "MA200（差距） 57,226.25（+15.86%）" [ref=e181]
          - cell "六月回撤 -8.38%" [ref=e182]
          - cell "下一确认线 66,800/65,535" [ref=e183]
        - row [ref=e184]:
          - cell "标的 丰田" [ref=e185]
          - cell "RSI14 48.5" [ref=e186]
          - cell "MA50（差距） 2,872.29（+1.47%）" [ref=e187]
          - cell "MA200（差距） 3,162.36（-7.84%）" [ref=e188]
          - cell "六月回撤 -25.00%" [ref=e189]
          - cell "下一确认线 2,924.5/2,869.5" [ref=e190]
        - row [ref=e191]:
          - cell "标的 铠侠" [ref=e192]
          - cell "RSI14 44.7" [ref=e193]
          - cell "MA50（差距） 73,505.8（-26.13%）" [ref=e194]
          - cell "MA200（差距） 33,555.8（+61.82%）" [ref=e195]
          - cell "六月回撤 -50.05%" [ref=e196]
          - cell "下一确认线 56,800/53,400" [ref=e197]
        - row [ref=e198]:
          - cell "标的 软银集团" [ref=e199]
          - cell "RSI14 52.9" [ref=e200]
          - cell "MA50（差距） 6,393.46（-6.81%）" [ref=e201]
          - cell "MA200（差距） 5,119.78（+16.37%）" [ref=e202]
          - cell "六月回撤 -30.98%" [ref=e203]
          - cell "下一确认线 6,000/5,605" [ref=e204]
        - row [ref=e205]:
          - cell "标的 东京电子" [ref=e206]
          - cell "RSI14 43.6" [ref=e207]
          - cell "MA50（差距） 65,664.8（-10.84%）" [ref=e208]
          - cell "MA200（差距） 45,374.3（+29.04%）" [ref=e209]
          - cell "六月回撤 -25.70%" [ref=e210]
          - cell "下一确认线 59,700/58,300" [ref=e211]
        - row [ref=e212]:
          - cell "标的 Advantest" [ref=e213]
          - cell "RSI14 59.8" [ref=e214]
          - cell "MA50（差距） 29,197.3（+15.49%）" [ref=e215]
          - cell "MA200（差距） 24,599.4（+37.08%）" [ref=e216]
          - cell "六月回撤 -6.07%" [ref=e217]
          - cell "下一确认线 33,840/32,390" [ref=e218]
    - paragraph [ref=e219]: 亚洲数据源：Yahoo Finance via yfinance，8月5日亚洲收盘快照。
    - heading "收盘主线" [level=2] [ref=e220]
    - paragraph [ref=e221]:
      - strong [ref=e222]: 已确认事实
      - text: ：开盘09:39 ET时SMH仍为576.47美元（+0.13%），最终收569.70美元（-1.04%），跌破早间失效线573.83；QQQ从开盘726.23回落至717.30，几乎收在日低716.92。NVDA收219.22（+3.43%），MU从日高928.95回落至893.19（+0.06%），TSM收413.79（-0.81%）。
    - paragraph [ref=e223]:
      - text: AP报道，SpaceX宣布AI计算将专用Nvidia芯片，一度推动NVDA涨约3.6%，同时SpaceX跌8.7%、AMD跌6.5%；市场正从“奖励AI支出”转向审核这些支出能否带来收入和利润。
      - link "AP美股跟踪" [ref=e224] [cursor=pointer]:
        - /url: https://apnews.com/article/stocks-markets-rates-oil-prices-53179dc1c0148c5afeb47379b8f5b5c5
    - paragraph [ref=e225]:
      - strong [ref=e226]: 分析推断
      - text: ：今日的核心不是利率冲击，因为美债10年收益率下降1.0bp至4.617%，VIX也降至15.53；而是资金集中到NVDA、同时压缩其他芯片估值的内部轮动。SMH低于MA50 4.38%、MU低8.12%、TSM低2.77%，半导体整体修复仍未完成。
    - paragraph [ref=e227]:
      - text: 黄金收4,307.7美元（+5.18%），Brent仅79.39美元（+0.04%）。价格分叉已确认，但未找到足以解释黄金全部涨幅的单一Tier A/B消息，因此不把它硬归因为某一事件。霍尔木兹海峡谈判接近协议、Brent约80美元的事实，支持“油价供给风险溢价回落”，但黄金仍在计入其他避险或货币风险。
      - link "AP霍尔木兹谈判报道" [ref=e228] [cursor=pointer]:
        - /url: https://apnews.com/article/ecdbd96f2b46c70beb5926d8508f9c55
    - heading "对今日日股开盘的传导" [level=2] [ref=e229]
    - list [ref=e230]:
      - listitem [ref=e231]: 日经：现货66,300.44，美元日经期货65,820。若现货开在65,535下方且首小时无法收回66,300，前一日AI反弹将被定性为一日修复；站上66,800、再站MA50的67,133才是延续确认。
      - listitem [ref=e232]:
        - text: 铠侠：MU收平、SMH跌1.04%，外部信号偏弱；Sandisk FY2026四季度业绩会于05:30 JST召开，当前报告时点尚未发布。今日观53,400/56,800日元。
        - link "Sandisk IR" [ref=e233] [cursor=pointer]:
          - /url: https://investor.sandisk.com/
      - listitem [ref=e234]:
        - text: 软银：NVDA +3.43%支持AI资产净值，但NQ -0.66%与QQQ -0.90%限制估值扩张。今日15:30 JST披露Q1财报、16:30说明会，比早盘波动更重要。
        - link "软银集团官方日程" [ref=e235] [cursor=pointer]:
          - /url: https://group.softbank/en/news/info/20260702
      - listitem [ref=e236]: 东京电子/Advantest：TSM -0.81%、SMH -1.04%对东京电子更不利，NVDA +3.43%对Advantest有结构性支撑。分别观58,300/59,700与32,390/33,840日元。
      - listitem [ref=e237]: 丰田：Brent 79.39未触发80.93美元压力线，USDJPY 157.719也未跌破157.298；基本传导中性，观2,869.5/2,924.5日元。
    - heading "组合与下一交易日" [level=2] [ref=e238]
    - paragraph [ref=e239]: 按NISA权重作静态代理估算：标普52%×-0.20%与纳指10%×-0.90%合计拖累约0.19个百分点；黄金10%×+5.18%贡献约+0.52个百分点，未计欧洲、印度和基金跟踪误差时，净缓冲约+0.32个百分点。USDJPY +0.12%还对未对冲海外资产有小幅日元计价顺风。
    - paragraph [ref=e240]:
      - strong [ref=e241]: 结论：今天无需动作。
      - text: 维持52/20/10/8/10与TOPIX 0，继续监视丰田金融资产加人力资本的重复暴露。黄金当日缓冲有效，不因NVDA单日上涨追加纳指或个股。
    - paragraph [ref=e242]:
      - strong [ref=e243]: 情景假设
      - text: ：
    - list [ref=e244]:
      - listitem [ref=e245]: 风险重启：QQQ重回728.54、SMH站上585，同时VIX守在17.33下方。
      - listitem [ref=e246]: 轮动延续：QQQ在716.92–728.54、SMH在568.38–585之间，NVDA守住216.40；指数定投不变。
      - listitem [ref=e247]: 触发再评估：QQQ跌破MA50 714.72、SMH跌破568.38且VIX站上18.43；这是提高警戒，仍不等于立即卖出。
    - heading "新闻证据与来源" [level=2] [ref=e248]
    - table [ref=e249]:
      - rowgroup [ref=e250]:
        - row [ref=e251]:
          - columnheader "时间" [ref=e252]
          - columnheader "已确认事实" [ref=e253]
          - columnheader "来源" [ref=e254]
          - columnheader "传导" [ref=e255]
      - rowgroup [ref=e256]:
        - row [ref=e257]:
          - cell "时间 8月5日" [ref=e258]
          - cell "已确认事实 SpaceX宣布AI计算专用Nvidia芯片；NVDA强、AMD弱" [ref=e259]
          - cell [ref=e260]:
            - text: 来源
            - link "AP（Tier B）" [ref=e261] [cursor=pointer]:
              - /url: https://apnews.com/article/stocks-markets-rates-oil-prices-53179dc1c0148c5afeb47379b8f5b5c5
          - cell "传导 解释NVDA个别强势，不代表费半整体强" [ref=e262]
        - row [ref=e263]:
          - cell "时间 7月29日" [ref=e264]
          - cell "已确认事实 SK海力士Q2营收79.3187万亿韩元、营业利润60.5426万亿，HBM4开始量产" [ref=e265]
          - cell [ref=e266]:
            - text: 来源
            - link "公司官方（Tier A）" [ref=e267] [cursor=pointer]:
              - /url: https://news.skhynix.com/en/q2-2026-business-results/
          - cell "传导 AI内存基本面强，但MU收平显示价格未追随" [ref=e268]
        - row [ref=e269]:
          - cell "时间 8月5日16:30 ET" [ref=e270]
          - cell "已确认事实 Sandisk FY2026四季度电话会，截止本报告尚未开始" [ref=e271]
          - cell [ref=e272]:
            - text: 来源
            - link "Sandisk IR（Tier A）" [ref=e273] [cursor=pointer]:
              - /url: https://investor.sandisk.com/news-events/events
          - cell "传导 铠侠/NAND最直接的盘前催化剂" [ref=e274]
        - row [ref=e275]:
          - cell "时间 8月6日15:30 JST" [ref=e276]
          - cell "已确认事实 软银集团Q1财报，16:30说明会" [ref=e277]
          - cell [ref=e278]:
            - text: 来源
            - link "软银官方（Tier A）" [ref=e279] [cursor=pointer]:
              - /url: https://group.softbank/en/news/info/20260702
          - cell "传导 决定软银反弹能否脱离美股外部定价" [ref=e280]
        - row [ref=e281]:
          - cell "时间 8月6日08:30 ET" [ref=e282]
          - cell "已确认事实 美国Q2生产率/单位劳动成本；8月7日公布7月就业" [ref=e283]
          - cell [ref=e284]:
            - text: 来源
            - link "BLS（Tier A）" [ref=e285] [cursor=pointer]:
              - /url: https://www.bls.gov/opub/update.htm
          - cell "传导 影响美债4.617%与AI估值折现率" [ref=e286]
        - row [ref=e287]:
          - cell "时间 8月5日" [ref=e288]
          - cell "已确认事实 美伊称霍尔木兹协议接近，Brent约80美元" [ref=e289]
          - cell [ref=e290]:
            - text: 来源
            - link "AP（Tier B）" [ref=e291] [cursor=pointer]:
              - /url: https://apnews.com/article/ecdbd96f2b46c70beb5926d8508f9c55
          - cell "传导 油价供给风险下降，丰田成本端暂未恶化" [ref=e292]
    - heading "数据局限" [level=2] [ref=e293]
    - paragraph [ref=e294]: 黄金数字为期货连续合约，可受换月与结算时点影响；日经美元期货与大阪现货不能直接等同。Sandisk业绩、美国生产率和软银财报均是未来事件，没有预先填入结果。技术位仅作风险确认，不是单独买卖理由。
    - paragraph [ref=e295]: 仅供研究与风险管理，不构成投资建议。
  - link "← 返回目录" [ref=e297] [cursor=pointer]:
    - /url: ./
  - contentinfo [ref=e298]: automated research bulletin — not investment advice
```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | test.use({
  4  |   viewport: { width: 390, height: 844 },
  5  |   userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1',
  6  |   launchOptions: { channel: 'chrome' },
  7  | });
  8  | 
  9  | test('us close report fits a 390px mobile viewport', async ({ page }) => {
  10 |   await page.goto('https://fengjh97.github.io/market-daily/report.html?p=2026-08-06/usclose&verify=88098fe0', { waitUntil: 'networkidle' });
  11 |   await expect(page.locator('.signal-dashboard')).toBeVisible();
  12 |   await expect(page.locator('h1').filter({ hasText: '美股收盘快照' })).toBeVisible();
  13 | 
  14 |   const overflow = await page.evaluate(() => {
  15 |     const viewport = document.documentElement.clientWidth;
  16 |     const offenders = [...document.querySelectorAll('body *')]
  17 |       .filter((el) => {
  18 |         if (el.closest('.metric-scroll, .report-jump')) return false;
  19 |         const style = getComputedStyle(el);
  20 |         if (style.position === 'fixed') return false;
  21 |         const rect = el.getBoundingClientRect();
  22 |         return rect.right > viewport + 1 || rect.left < -1;
  23 |       })
  24 |       .map((el) => ({
  25 |         node: `${el.tagName}.${el.className}`,
  26 |         text: el.textContent.trim().slice(0, 80),
  27 |         rect: el.getBoundingClientRect().toJSON(),
  28 |         parent: `${el.parentElement?.tagName}.${el.parentElement?.className}`,
  29 |       }))
  30 |       .slice(0, 20);
  31 |     return { viewport, documentWidth: document.documentElement.scrollWidth, offenders };
  32 |   });
  33 | 
  34 |   console.log(JSON.stringify(overflow));
  35 |   expect(overflow.documentWidth).toBeLessThanOrEqual(overflow.viewport + 1);
> 36 |   expect(overflow.offenders).toEqual([]);
     |                              ^ Error: expect(received).toEqual(expected) // deep equality
  37 | });
  38 | 
```