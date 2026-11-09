
    (() => {
      const previousButton = document.getElementById('previousReportButton');
      const previousDialog = document.getElementById('previousReportDialog');
      const closePrevious = document.getElementById('closePreviousReport');
      const archiveList = document.getElementById('reportArchiveList');
      const previousReportHelp = document.getElementById('previousReportHelp');
      const reportDateValue = document.getElementById('reportDateValue');
      const backToLatestButton = document.getElementById('backToLatestReportButton');
      const originalText = new WeakMap();
      const originalAttributes = new WeakMap();
      let currentLang = 'en';
      const latestReportDate = '2026-10-28';
      const PRESENT_REPORT_URL = 'https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/';
      let currentReportDate = reportDateValue?.dataset.reportDate || latestReportDate;
      const syncLatestButton = () => {
        // This page is a dated archive, so the way back to the present
        // report is always offered.
        if (backToLatestButton) backToLatestButton.hidden = false;
      };

      const cn = {
        'Daily Game Performance Report': '每日游戏表现报告',
        'Report Date': '报告日期',
        'Night Mode': '夜间模式',
        'Previous Daily Report': '上一日报告',
        'General Operation Data': '总体运营数据',
        'Daily snapshot · BP1 / Banana Craze': '每日快照 · 已验证后台数据（BP1 / 香蕉狂欢）',
        'Report generated': '报告已生成',
        'Bet Amount': '投注金额', 'Monthly Bet Amount': '月度投注金额', 'Monthly Payout': '月度派彩', 'Monthly GGR': '月度游戏总收入', 'Monthly Total Players': '月度玩家总数', 'Payout': '派彩', 'GGR': '游戏总收入', 'Positive GGR': '正向GGR', 'Monthly Total ₱2,444,910': '月度总计 ₱2,444,910', 'Monthly Total ₱2,343,980': '月度总计 ₱2,343,980', 'Monthly Total ₱100,930': '月度总计 ₱100,930', 'Monthly Average 95.87%': '月度平均 95.87%', 'MTD Total ₱72,840': 'MTD总计 ₱72,840', 'WoW ↑ 8.6%': '周环比 ↑ 8.6%', 'WoW ↑ 7.1%': '周环比 ↑ 7.1%', 'WoW ↑ 12.8%': '周环比 ↑ 12.8%', 'WoW +0.36 pp': '周环比 +0.36 个百分点', 'WoW ↑ 5.9%': '周环比 ↑ 5.9%', 'Monthly Total ₱1.85M': '月度总计 ₱1.85M', 'Monthly Total ₱1.77M': '月度总计 ₱1.77M', 'Monthly Total ₱72.84K': '月度总计 ₱72.84K', 'Monthly Avg 96.06%': '月度平均 96.06%',
        'Daily': '每日', 'Within target': '在目标范围内', 'MTD GGR': 'MTD GGR', 'Sep 1–21': '9月1日至21日',
        'Total Rounds': '总回合数', 'Players': '玩家数', 'New Players': '新玩家', 'ABPU': '每位玩家平均投注', 'ARPP': '人均回合数',
        'Max Payout': '最高派彩', 'Max Multiplier': '最高倍数', 'Max Bet': '最高投注', 'D1 Retention': 'D1留存率',
        'Rounds': '回合数', 'Hitrate': '命中率', 'Max Win': '最高赢额', 'Max Mult': '最高倍数',
        'REAL HITRATE': '真实命中率', 'MTD RTP': '月累计RTP',
        'Wednesday, October 28, 2026': '2026年10月28日星期三',
        'BingoPlus (BP1) Loteria listed all four Game Engine titles in its ': 'BingoPlus（BP1）乐透专区在',
        'new games': '新游戏',
        ' entry — ': '入口列出了 Game Engine 的全部四款游戏——',
        ' were visible as new games': '均作为新游戏可见',
        'All four games are discoverable from the BP1 Loteria new-games list, giving the full portfolio stronger visibility': '四款游戏均可从 BP1 乐透专区的新游戏列表中找到，整体产品组合的曝光度更高',
        'REAL HITRATE counts settled rounds whose payout is above the bet amount (payout > bet), not every round that paid something. MTD RTP is month-to-date through the report day, reconciled to the month ledger.': '真实命中率按已结算回合计：派彩高于投注金额（payout > bet）的回合，而非所有有派彩的回合。月累计RTP为报告日止的当月累计值，并与月度账本核对。',
        'Platform Performance': '平台表现', 'Platform-level contribution, status, and operational notes': '平台贡献、状态与运营备注',
        'Platform': '平台', 'Loteria': '乐透', 'Slot': '老虎机', 'Metric': '指标', 'Value': '数值', 'Active Players': '活跃玩家',
        'D1 Retention': 'D1留存率', 'Winning Tickets': '中奖票数', 'Avg Bet / Player': '每位玩家平均投注', 'GGR Share': 'GGR占比',
        'Platform Share': '平台占比', 'Contribution mix': '贡献构成', 'Revenue contribution': '收入贡献', 'Monthly GGR Share': '月度GGR占比', 'Monthly Player Share': '月度玩家占比',
        'Audience contribution': '用户贡献', 'Betting volume contribution': '投注量贡献', 'Changelog': '变更记录',
        'Latest updates': '最新更新', 'Date': '日期', 'Details': '详情', 'Outcome': '结果',
        'Launch of ': '上线', 'Launch of': '上线', 'Game Engine officially entered ArenaPlus': '游戏引擎正式进入ArenaPlus', 'RTP adjusted from ': 'RTP从', 'RTP adjusted from': 'RTP从', 'RTP configuration was successfully updated to ': 'RTP配置已成功更新为', 'RTP configuration was successfully updated to': 'RTP配置已成功更新为', 'Friday, September 18, 2026': '2026年9月18日星期五', 'Monday, September 21, 2026': '2026年9月21日星期一', 'Thursday, September 17, 2026': '2026年9月17日星期四', 'Monday, September 14, 2026': '2026年9月14日星期一', 'Thursday, September 10, 2026': '2026年9月10日星期四', 'Tuesday, September 1, 2026': '2026年9月1日星期二',
        'Game Engine officially entered GameZone; lower minimum bet provided a more accessible entry point and supported increased traffic': '游戏引擎正式进入GameZone；降低最低投注门槛，提供更易进入的起点并促进流量增长',
        'Banana Craze on ArenaPlus': 'ArenaPlus上的Banana Craze', 'Banana Craze on GameZone': 'GameZone上的Banana Craze', 'minimum bet updated to ': '最低投注更新为', 'minimum bet updated to': '最低投注更新为', '₱0.50 at 2:00 PM': '₱0.50（下午2:00）', 'System maintenance for ': '系统维护，进行', 'System maintenance for': '系统维护，进行', 'upgrade': '升级',
        '9:00 AM–10:30 AM; Game Hall temporarily closed': '上午9:00–10:30；游戏大厅暂时关闭', '9:30 AM–1:15 PM; Game Hall temporarily closed': '上午9:30–下午1:15；游戏大厅暂时关闭', 'Game Hall temporarily closed': '游戏大厅暂时关闭', 'System upgrade completed': '系统升级完成',
        'Improved ': '优化', 'Improved': '优化', 'Improved Banana Craze placement in BingoPlus Loteria': '优化Banana Craze在BingoPlus乐透专区的位置', 'around 3:00 PM': '约下午3:00', '10:42 AM:': '上午10:42：', '97.0% → 98.3%': '97.0% → 98.3%', 'reflecting the new target setting.': '反映新的目标设置。',
        'Alerts & Incident Report': '警报与事件报告', 'Daily status': '每日状态', 'GGR Status': 'GGR状态', 'Compliance & PAGCOR Update': '合规与PAGCOR更新', 'Current status': '当前状态', 'GCP Accreditation': 'GCP认证', 'GCP Walkthrough': 'GCP说明会', '📅 Oct 26, 2026 — Walkthrough for GCP Accreditation': '📅 2026年10月26日 — GCP 认证说明会', 'Game Application': '游戏申请', 'Next Games for Application': '下一批申请游戏', '✅ Approved — Numerical & ECG': '✅ 已批准 — Numerical 与 ECG', '✅ Approved — Banana Craze, PikaPika': '✅ 已批准 — Banana Craze、PikaPika', '🔄 BLAZING 7S, LUCKY COLOR, GINTO MATCH': '🔄 BLAZING 7S、LUCKY COLOR、GINTO MATCH',
        'Positive daily GGR': '每日GGR为正', 'Healthy': '正常', 'RTP Status': 'RTP状态', 'vs target ≈': 'vs 目标 ≈', 'Negative daily GGR': '每日GGR为负', 'Flat daily GGR': '每日GGR持平', 'Below target': '低于目标', 'Above 100%': '高于100%', 'Alert': '警报', 'Clear': '无异常',
        'Fusebreak / Alarm': 'Fusebreak / 警报', 'No fuse or melt alert captured for this date.': '此日期未捕获熔断或警报通知。', 'Fuse-breaker GCs not scanned for this date.': '此日期未扫描熔断监控群。', 'Monitor': '监控中',
        'Notes': '备注', 'No incident report or important operational note recorded for this date.': '此日期暂无事件报告或重要运营备注。',
        'Game Performance': '游戏表现',
        'Rounds': '回合数', 'Total': '总计', 'Avg Round / Game': '平均每局回合投注', 'Hourly RTP (00:00–23:59)': '每小时RTP（00:00–23:59）', 'Hourly RTP': '每小时RTP',
        'Bars: bet amount + payout (₱000s) · Lines: RTP + players + 97.5% threshold': '柱状图：投注金额 + 派彩（₱千元）· 折线：RTP + 玩家数 + 97.5%阈值',
        'Bet amount': '投注金额', 'RTP trendline': 'RTP趋势线', 'RTP threshold 97.5%': 'RTP阈值 97.5%',
        'Dynamic RTP': '动态RTP', 'Mode contribution': '模式贡献', 'rounds': '回合数',
        'Winning Rounds vs Losing Rounds': '中奖回合与未中奖回合', 'Loss vs win rounds': '未中奖与中奖回合', 'Total rounds': '总回合数',
        'Winning rounds': '中奖回合', 'Losing rounds': '未中奖回合',
        'Total Tickets': '总票数', 'By feature behavior': '按功能行为', 'Normal Bet': '普通投注', 'Buy Feature': '购买功能',
        'Bonus Round': '奖励回合', 'Normal Bet accounts for the majority of total tickets.': '普通投注占本示例总票数的大部分。', 'Players by Loteria / Slot': '按乐透 / 老虎机玩家',
        'Avg Round': '平均回合投注', 'Popular Bet Amount': '最常用投注金额', 'Game Performance is grouped into Loteria and Slot. Slot combines GameZone and ArenaPlus. Popular bet amount is the most frequent settled bet denomination by category.': '游戏表现按乐透与老虎机分类。老虎机合并 GameZone 与 ArenaPlus。最常用投注额为各类别中已结算订单出现频率最高的投注面额。',
        'Ticket totals are separated by Loteria and Slot for each feature behavior.': '各功能行为的票数总计按乐透与老虎机区分。', 'Unique players are separated by Loteria and Slot across each rounds-played range.': '各回合区间的唯一玩家按乐透与老虎机区分。', 'Unique players by denomination, categorized by Loteria and Slot.': '唯一玩家按投注面额统计，并按乐透与老虎机分类。',
        'Unique players per bet amount, Loteria vs Slot.': '按投注金额统计的唯一玩家，乐透与老虎机对比。',
        'Player Distribution by Rounds Played': '按已玩回合数划分的玩家分布', 'Horizontal bar chart': '横向柱状图', 'Number of Unique Players': '唯一玩家数量',
        'Most unique players are concentrated in the 1–10 rounds range.': '大多数唯一玩家集中在1–10回合区间。',
        'Bet Amount Distribution': '投注金额分布', 'Bet amount + rounds + share': '投注金额 + 回合数 + 占比', 'Bet range': '投注区间',
        'Total bet': '总投注', 'Share': '占比', 'Multiplier Distribution': '倍数分布', 'Winning outcome bands': '中奖结果区间',
        'Multiplier': '倍数', 'Player Performance': '玩家表现', 'Acquisition, retention, platform mix, and player behavior': '获客、留存、平台构成与玩家行为',
        'New Player vs Returning Player': '新玩家与回访玩家', 'New Player vs Returning Player vs Active Players': '新玩家、回访玩家与活跃玩家', '2,434 active players': '2,434名活跃玩家', 'players': '玩家',
        'New players': '新玩家', 'Returning': '回访玩家', 'Player per Platform': '各平台玩家', 'New vs returning': '新玩家与回访玩家', 'New vs returning + active players': '新玩家、回访玩家与活跃玩家', 
        'Returning players': '回访玩家', 'New share': '新玩家占比', 'Player Retention': '玩家留存', 'D1–D7 sample': 'D1–D7示例',
        'Next-day returning players': '次日回访玩家', 'D3 Retention': 'D3留存率', 'Third-day returning players': '第三日回访玩家',
        'D7 Retention': 'D7留存率', 'Seventh-day returning players': '第七日回访玩家', 'Rounds Comparison': '回合数对比',
        'Unique Players by Bet Denomination': '按投注面额划分的唯一玩家', 'Unique players by their selected bet denomination.': '按所选投注面额划分的唯一玩家。', 'The 1–10 rounds range has the most unique players, shown separately for Loteria and Slot.': '1–10回合区间的唯一玩家最多，并按乐透与老虎机分别显示。',
        'Players by Game Feature Behavior': '按游戏功能行为划分的玩家', 'Players may appear in more than one category': '玩家可能出现在多个类别中',
        'Feature Behavior': '功能行为', 'Share of Active Players': '活跃玩家占比', 'Average Rounds / Player': '平均回合数 / 玩家',
        'Player Engagement Distribution': '玩家参与度分布', 'Loteria vs Slot': '乐透与老虎机', 'Rounds per Player': '每人回合数', 'Number of Players': '玩家数量',
        'Average Bet & Rounds per Player': '人均投注与回合数', 'Average Bet / Player': '人均投注', 'Median Rounds / Player': '回合数中位数', 'Metric': '指标',
        'Top 5 Winning Players': '前5名盈利玩家', 'Biggest single-bet payout': '单注最大派彩', 'Mult.': '倍数', 'Bet site': '投注站点', 'Bet amount range': '投注金额区间', 'Highest payout': '最高派彩', 'IP': 'IP',
        'Normal Rounds': '普通回合', 'Monthly Performance': '月度表现', '30-day trend and month-to-date platform summary · Oct 1–28, 2026': '30天趋势与月初至今平台汇总',
        '30 days': '30天', 'MTD': '月初至今', '30-Day Performance Trend': '30天表现趋势',
        'Bars: bet amount + payout · Lines: RTP + D1 retention': '柱状图：投注金额 + 派彩 · 折线：RTP + D1留存率', 'D1 Retention trendline': 'D1留存趋势线', 'Red dot: RTP changed during the day': '红点：当天RTP发生变化', 'Trend Change Highlight': '趋势变化重点', 'RTP Change': 'RTP变化', 'Sep 18': '9月18日', 'Configuration updated': '配置已更新', ' current total': '当前总计', '96.35% current RTP': '当前RTP为96.35%', 'DoD: ↓ 0.22 pp': '日环比：↓ 0.22 个百分点',
        'Overall Retention': '总体留存',
        'Platform Share compares revenue, audience, and betting-volume contribution.': '平台占比比较收入、用户和投注量贡献。',
        'Recent launches and the minimum-bet update expanded platform access during the reporting period.': '报告期间的近期上线和最低投注更新扩大了平台访问范围。',
        'GCP accreditation and current Game Application approvals are shown for management tracking.': '此处显示GCP认证和当前游戏申请批准状态，供管理层追踪。',
        'GameZone carries the highest rounds and BingoPlus leads monthly GGR.': 'GameZone回合数最高，BingoPlus的月初至今GGR最高。',
        'Hourly RTP is evaluated against the 97.5% threshold while bet amount and payout intensity are shown by hour.': '每小时RTP根据97.5%阈值进行评估，同时按小时显示投注金额和派彩强度。',
        'NON drives most volume; cumulative and daily modes remain more volatile because of smaller samples.': '普通模式贡献大部分交易量；累计模式和每日模式因样本较小而波动更高。',
        'Winning rounds represent 29.7% of Loteria rounds and 29.8% of Slot rounds on October 28, 2026.': '2026 年 9 月 30 日，中奖回合占乐透回合数的 29.7%，占老虎机回合数的 29.8%。',
        'Normal Bet accounts for the majority of ticket activity.': '普通投注占票数活动的大部分。',
        'Normal Bet accounts for the majority of ticket activity across both Loteria and Slot.': '普通投注在乐透与老虎机两类平台中均占票数活动的大部分。',
        'Most unique players are concentrated in the 1–10 rounds range.': '大多数唯一玩家集中在1–10回合区间。',
        'The dominant settled denomination is ₱5.00 for Loteria and ₱1.00 for Slot, based on 105,434 settled orders on October 28, 2026.': '根据 2026 年 9 月 30 日的 105,434 笔已结算订单，乐透最常见的已结算投注面额为 ₱5.00，老虎机为 ₱1.00。',
        '0x is the largest multiplier band by rounds.': '按回合数统计，0x是最大的倍数区间。',
        'GP has the largest active-player base among the three platforms.': '在三个平台中，GameZone 的活跃玩家基数最大。',
        'Unique-player counts are highest at the lower bet denominations, with Loteria and Slot shown separately.': '较低投注面额的唯一玩家数量最高，并分别显示乐透与老虎机数据。',
        'D1 retention is the main player-engagement metric to monitor.': 'D1留存率是需要重点监控的玩家参与度指标。',
        'Unique-player counts are highest at the lower bet denominations.': '较低投注面额的唯一玩家数量最高。',
        'Normal Rounds are the primary feature behavior, while Buy Feature and Bonus Round are smaller segments.': '普通回合是主要功能行为，购买功能和奖励回合占比较小。',
        'The 30-day view compares daily bet and payout bars with RTP and D1 retention trendlines.': '30天视图通过每日投注和派彩柱状图，对比RTP与D1留存率趋势线。',
        'Key Insight': '关键洞察', 'Archive': '存档', 'Choose a date below to open the verified report for that day.': '请选择下方日期，打开该日的已验证报告。', 'Back to Present Report': '返回当前报告',
        'Daily report archive': '日报存档', 'View report': '查看报告', 'Close': '关闭', '97.5% target': '97.5%目标', 'Aug ': '8月', 'Sep ': '9月'
      };
      Object.assign(cn, {
        'DoD': '日环比', 'WoW': '周环比', 'pp': '百分点', 'Monthly Total': '月度总计', 'Monthly Average': '月度平均', 'Monthly Avg': '月度平均', 'Monthly Max': '月度最高',
        'PHT': '菲律宾时间', 'NON': '普通模式', 'Cumulative': '累计', 'rounds': '回合数', 'Player Share': '玩家占比', 'Bet Share': '投注占比', 'Popular Bet Amount': '最常用投注金额',
        'Improved game visibility and accessibility within the Loteria section.': '提升Loteria专区内的游戏可见性与可访问性。', 'September 21, 2026': '2026年9月21日',
        '30-day performance trend chart': '30天表现趋势图', 'Bet Share pie chart': '投注占比饼图', 'GGR Share pie chart': 'GGR占比饼图', 'Hourly RTP combo chart': '每小时RTP组合图', 'Language': '语言', 'Main operating metrics': '主要运营指标',
        'Loteria winning rounds versus losing rounds': 'Loteria中奖回合与未中奖回合', 'Monthly GGR Share pie chart': '月度GGR占比饼图', 'Monthly Player Share pie chart': '月度玩家占比饼图', 'Player Share pie chart': '玩家占比饼图',
        'Previous daily reports': '上一日报告', 'Report controls': '报告控制', 'Slot winning rounds versus losing rounds': 'Slot中奖回合与未中奖回合', 'Total tickets by Loteria and Slot': 'Loteria和Slot总票数',
        'Horizontal bar chart showing player distribution by rounds played, separated by Loteria and Slot': '按已玩回合数划分的玩家分布横向柱状图，数据按Loteria和Slot分别显示'
      });
      // --- CN wording for the injected Key Insights (exact full-string keys) ---
      Object.assign(cn, {
        "BingoPlus settled ₱1,155,540.00 of ₱2,173,644.50 total bet on October 28, 2026; GameZone ₱229,937.50 and ArenaPlus ₱3,369.00.": "BingoPlus 在 2026 年 10 月 20 日的 ₱481,810.00 总投注额中结算了 ₱440,920.00；GameZone ₱28,020.50，ArenaPlus ₱3,846.50。",
        "NON rounds carry most volume; Cumulative and Daily adjustments apply to a small share of rounds but pay far above their stake, which drives daily RTP variance.": "普通回合贡献绝大部分交易量；奖励回合在少量回合中以远高于投注的派彩，导致当日 RTP 波动。",
        "Winning rounds are rounds with a payout greater than zero.": "中奖回合指派彩大于零的回合。",
        "Players created on October 28, 2026 accounted for most of the day’s activity.": "10 月 28 日当天创建的新玩家贡献了当日大部分活跃度。",
        "New players recorded more rounds than returning players on every platform.": "三个平台中新玩家的回合数均多于回访玩家。",
        "Normal Bet is the primary feature behavior; Buy Feature is a smaller segment.": "普通投注是主要的功能行为；购买功能占比较小。",
        "MTD platform totals are month-to-date from the per-site settled-order ledger for October 1–28. Each site row and the month total are each rounded to the centavo, with the total rounded once from the full-precision ledger, so the rows can miss the total by ₱0.01.": "月初至今平台总计取自各分站已结算订单账目，覆盖 10 月 1–28 日。各分站行与月度总计均按分取整，总计由全精度订单账目一次取整，因此各行合计可能与总计相差 ₱0.01。",
        "Winning rounds represent 29.7% of Loteria rounds and 29.8% of Slot rounds on October 28, 2026.": "2026 年 9 月 30 日，中奖回合占乐透回合数的 29.7%，占老虎机回合数的 29.8%。",
      });
      Object.assign(cn, {
        'Active-player contribution': '活跃玩家贡献',
        '(site visits)': '（站点访问数）',
        'Combined all-active return rate': '全体活跃玩家综合回流率',
        'all-active return rate': '全体活跃玩家回流率',
        'Highest settled bet on any site': '任一平台的最高已结算投注',
        'Accounts created that day': '当日创建的账户',
        'accounts created that day': '当日创建的账户',
        'first day ever seen in the archive': '首次出现在存档中',
        'bar heights are relative across the six series': '柱高为六个系列间的相对值',
        'are settled rounds with a payout greater than zero': '为派彩大于零的已结算回合',
        'settled-order export': '已结算订单导出',
        'distinct active players': '唯一活跃玩家',
        'per-site sum': '分站合计',
        'per-site archive': '分站存档',
        'by bet denomination': '按投注面额',
        'by feature behavior': '按功能行为',
        'rounds-played band': '已玩回合区间',
        'settled rounds': '已结算回合',
        'Settled rounds': '已结算回合',
        'per bet amount': '按投注金额',
        'the tail ends at': '尾端为',
        'for this day': '（当日）',
        'month-to-date': '月初至今',
        'Source multiplier bands covering': '来源倍数区间，覆盖',
        'Losing Tickets': '未中奖票数',
        'daily maximum': '当日最高',
        'vs prior day': '对比前一日',
        'Return rate': '回流率',
        'return rate': '回流率',
        ' Starting bet': ' 起始投注',
        'Interpretation': '说明',
        'verified against the': '已对照核查：',
        'carries most volume': '贡献大部分交易量',
        'have smaller volume': '交易量较小',
        'but higher realized RTP': '但实际RTP更高',
        'and negative GGR because their payout exceeds their bet amount for the reporting day': '且GGR为负，因为当日派彩超过投注金额',
        'for the reporting day': '（报告日）',
        'minus accounts created that day': '减去当日创建的账户',
        'New = ': '新玩家 = ',
        'Returning = ': '回访玩家 = ',
        'At around': '约',
        'was added to': '已添加至',
        'Better Entry': '更优入口',
        'New Game section': '新游戏专区',
        'improved game visibility and accessibility': '优化了游戏可见性与可及性',
        'placement in': '在…中的位置：',
        'featured in ': '在…中推荐：',
        'game visibility': '游戏可见性',
        'visibility': '可见性',
        'accessibility': '可及性',
        ' within ': ' 在…内 ',
        'Starting bet': '起始投注',
        ' and ': ' 和 ',
        ' of ': ' / ',
        ' by ': ' 按 ',
        ' per ': ' 每 ',
        ' vs ': ' 对比 ',
        ' with ': ' 与 ',
        ' than ': ' 比 ',
        ' are ': ' 为 ',
        ' that ': ' 该 ',
        ' the ': ' ',
        ' combined': ' 合并',
        ' Combined': ' 合并',
        ' covering': ' 覆盖',
        ' ends': ' 末端',
        ' tail': ' 尾',
        ' active ': ' 活跃 ',
        ' settled ': ' 已结算 ',
        ' unique ': ' 唯一 ',
        ' distinct ': ' 唯一 ',
        ' created ': ' 创建 ',
        ' archive': ' 存档',
        ' daily ': ' 每日 ',
        ' sum': ' 合计',
        ' maximum': ' 最高',
        ' players': ' 玩家',
        ' rounds': ' 回合数',
        ' volume': ' 交易量',
        ' payout': ' 派彩',
        ' amount': ' 金额',
        ' contribution': ' 贡献',
        ' behavior': ' 行为',
        ' section': ' 专区',
        ' Wednesday': ' 星期三',
        'September': '9月',
        ' reporting ': ' 报告 ',
        ' greater': ' 大于',
        ' exceeds': ' 超过',
        ' smaller': ' 较小',
        ' higher': ' 更高',
        ' negative': ' 负',
        ' zero': ' 零',
        ' average': ' 平均',
        ' multiplier': ' 倍数',
      });
      Object.assign(cn, {
        'bet amount bands': '投注金额区间',
        'Bet amount band': '投注金额区间',
      });
      Object.assign(cn, {
        'Avg Round / Player': '人均回合数',
        'Avg Rounds / Player': '人均回合数',
      });
      // Dynamic CN keys registered by earlier script blocks (e.g. the Player
      // Performance notes) live on window.__dynCN: `cn` is IIFE-scoped here, so
      // an earlier block cannot reach it directly.
      Object.assign(cn, window.__dynCN || {});
      /* incident-panel-i18n */ Object.assign(cn, {"Fuse-breaker Alert": "熔断警报", "Fusebreak Alarm / Melt": "熔断警报 / 熔毁", "Fusebreak Alarm": "熔断警报", "Melt": "熔毁", "None": "无", "max ": "最大 ", "High Winning Alert": "高倍中奖警报", "High Winning": "高倍中奖", "Top Winning Player Alerts": "高额中奖玩家警报", "No high-multiplier win reached the alert threshold.": "当日无高倍中奖达到警报阈值。", "day RTP": "当日RTP", "Original": "原始", "Repeat": "重复", "Retries": "重试", "Trigger Repeat": "重复触发", "Trigger": "触发"});
      const entries = Object.entries(cn).sort((a, b) => b[0].length - a[0].length);

      const translateText = (source, lang) => {
        if (lang === 'en') return source;
        const leading = source.match(/^\s*/)?.[0] || '';
        const trailing = source.match(/\s*$/)?.[0] || '';
        let value = source.trim();
        entries.forEach(([from, to]) => { value = value.split(from).join(to); });
        return leading + value + trailing;
      };
      const englishDate = iso => new Intl.DateTimeFormat('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso}T00:00:00Z`));
      const chineseDate = iso => new Intl.DateTimeFormat('zh-CN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso}T00:00:00Z`));
      // Historical reports are served from the verified dated-report archive.
      // Keep the existing archive UI; this map supplies the actual report data per date.
      const archiveReportUrls = {
        '2026-10-28': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-28.html',
        '2026-10-27': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-27.html',
        '2026-10-26': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-26.html',
        '2026-10-25': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-25.html',
        '2026-10-24': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-24.html',
        '2026-10-23': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-23.html',
        '2026-10-22': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-22.html',
        '2026-10-21': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-21.html',
        '2026-10-20': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-20.html',
        '2026-10-19': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-19.html',
        '2026-10-18': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-18.html',
        '2026-10-17': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-17.html',
        '2026-10-16': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-16.html',
        '2026-10-15': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-15.html',
        '2026-10-14': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-14.html',
        '2026-10-13': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-13.html',
        '2026-10-12': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-12.html',
        '2026-10-11': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-11.html',
        '2026-10-10': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-10.html',
        '2026-10-09': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-09.html',
        '2026-10-08': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-08.html',
        '2026-10-07': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-07.html',
        '2026-10-06': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-06.html',
        '2026-10-05': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-05.html',
        '2026-10-04': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-04.html',
        '2026-10-03': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-03.html',
        '2026-10-02': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-02.html',
        '2026-10-01': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-10-01.html',
        '2026-09-30': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-30.html',
        '2026-09-29': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-29.html',
        '2026-09-28': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-28.html',
        '2026-09-27': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-27.html',
        '2026-09-26': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-26.html',
        '2026-09-25': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-25.html',
        '2026-09-24': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-24.html',
        '2026-09-23': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-23.html',
        '2026-09-22': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-22.html',
        '2026-09-21': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-21.html',
        '2026-09-20': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-20.html',
        '2026-09-19': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-19.html',
        '2026-09-18': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-18.html',
        '2026-09-17': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-17.html',
        '2026-09-16': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-16.html',
        '2026-09-15': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-15.html',
        '2026-09-14': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-14.html',
        '2026-09-13': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-13.html',
        '2026-09-12': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-12.html',
        '2026-09-11': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-11.html',
        '2026-09-10': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-10.html',
        '2026-09-09': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-09.html',
        '2026-09-08': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-08.html',
        '2026-09-07': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-07.html',
        '2026-09-06': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-06.html',
        '2026-09-05': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-05.html',
        '2026-09-04': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-04.html',
        '2026-09-03': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-03.html',
        '2026-09-02': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-02.html',
        '2026-09-01': 'https://mellydeguzman01-ship-it.github.io/Daily-Game-Performance-Report/Daily_Game_Performance_Report_2026-09-01.html'
      };
      const archiveDates = Object.keys(archiveReportUrls);

      const renderReportDate = () => {
        if (!reportDateValue) return;
        reportDateValue.dataset.reportDate = currentReportDate;
        reportDateValue.textContent = currentLang === 'cn' ? chineseDate(currentReportDate) : englishDate(currentReportDate);
        document.title = `${currentLang === 'cn' ? '每日游戏表现报告' : 'Daily Game Performance Report'} — ${currentLang === 'cn' ? chineseDate(currentReportDate) : englishDate(currentReportDate)}`;
        syncLatestButton();
      };

      const renderArchive = () => {
        if (!archiveList) return;
        archiveList.replaceChildren();
        archiveDates.forEach(iso => {
          const item = document.createElement('button');
          item.type = 'button';
          item.className = 'report-archive-item';
          item.dataset.reportDate = iso;
          item.innerHTML = `<span>${currentLang === 'cn' ? chineseDate(iso) : englishDate(iso)}</span><small>${currentLang === 'cn' ? '日报存档' : 'Daily report archive'}</small><b>${currentLang === 'cn' ? '查看报告' : 'View report'}</b>`;
          item.addEventListener('click', () => {
            // Open the verified dated report so every historical metric comes from its source data.
            window.location.href = archiveReportUrls[iso];
          });
          archiveList.appendChild(item);
        });
      };

      const requestedDate = new URLSearchParams(location.search).get('date');
      if (requestedDate && archiveDates.includes(requestedDate)) currentReportDate = requestedDate;
      previousButton?.addEventListener('click', () => previousDialog?.showModal());
      backToLatestButton?.addEventListener('click', () => {
        window.location.href = PRESENT_REPORT_URL;
      });
      closePrevious?.addEventListener('click', () => previousDialog?.close());
      previousDialog?.addEventListener('click', event => {
        if (event.target === previousDialog) previousDialog.close();
      });

      const applyLanguage = lang => {
        currentLang = lang;
        document.documentElement.lang = lang === 'cn' ? 'zh-CN' : 'en';
        document.dispatchEvent(new CustomEvent('dashboard-language-change', { detail: lang }));
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
          if (!originalText.has(node)) originalText.set(node, node.nodeValue);
          node.nodeValue = translateText(originalText.get(node), lang);
        }
        document.querySelectorAll('[aria-label],[title],[placeholder]').forEach(item => {
          const attrs = originalAttributes.get(item) || {};
          ['aria-label', 'title', 'placeholder'].forEach(attribute => {
            if (item.hasAttribute(attribute) && attrs[attribute] === undefined) attrs[attribute] = item.getAttribute(attribute);
            if (attrs[attribute] !== undefined) item.setAttribute(attribute, translateText(attrs[attribute], lang));
          });
          originalAttributes.set(item, attrs);
        });
        document.querySelectorAll('[data-lang]').forEach(item => item.classList.toggle('active', item.dataset.lang === lang));
        renderArchive();
        renderReportDate();
      };

      renderArchive();
      applyLanguage('en');
      document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => applyLanguage(button.dataset.lang)));
    })();
  