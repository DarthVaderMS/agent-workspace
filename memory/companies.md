# Companies & Tickers — Working Cache

Local cache of company-to-ticker mappings I've used or am likely to use in articles. Append to this file every time I write about a company that isn't already listed. The memory consolidation cron will pick up new entries from daily logs.

This file is a CACHE, not the authority. The authoritative source is **SEC EDGAR's company tickers JSON** at <https://www.sec.gov/files/company_tickers.json> (US-listed). For non-US listings, Yahoo Finance search at <https://finance.yahoo.com/lookup?s=> is the lookup tool. If a cached entry seems wrong (renamed, delisted, ticker changed), re-verify against EDGAR or Yahoo and update here.

## Traded (verified)

Sorted by mention count in `My Website/Articles/Published/` as of 2026-04-21 — top entries are most likely to recur.

| Company | Ticker | Exchange | Yahoo URL | Mentions | Notes |
|---|---|---|---|---|---|
| Nvidia | NVDA | NASDAQ | https://finance.yahoo.com/quote/NVDA | 128 | Counts both "Nvidia" and "NVIDIA" spellings |
| Meta Platforms | META | NASDAQ | https://finance.yahoo.com/quote/META | 45 | Facebook parent |
| Alphabet | GOOGL | NASDAQ | https://finance.yahoo.com/quote/GOOGL | 17 | Class A; use GOOG for Class C only when context demands |
| Microsoft | MSFT | NASDAQ | https://finance.yahoo.com/quote/MSFT | 12 | Owns GitHub, LinkedIn |
| Amazon | AMZN | NASDAQ | https://finance.yahoo.com/quote/AMZN | 8 | |
| Cisco Systems | CSCO | NASDAQ | https://finance.yahoo.com/quote/CSCO | 7 | |
| CrowdStrike | CRWD | NASDAQ | https://finance.yahoo.com/quote/CRWD | 6 | |
| Uber | UBER | NYSE | https://finance.yahoo.com/quote/UBER | 6 | |
| Apple | AAPL | NASDAQ | https://finance.yahoo.com/quote/AAPL | 5 | |
| Hewlett Packard Enterprise | HPE | NYSE | https://finance.yahoo.com/quote/HPE | 5 | Distinct from HP Inc (`HPQ`) |
| Oracle | ORCL | NYSE | https://finance.yahoo.com/quote/ORCL | 4 | |
| Reddit | RDDT | NYSE | https://finance.yahoo.com/quote/RDDT | 3 | IPO'd 2024 |
| Adobe | ADBE | NASDAQ | https://finance.yahoo.com/quote/ADBE | 3 | |
| Dell Technologies | DELL | NYSE | https://finance.yahoo.com/quote/DELL | 3 | |
| Bank of America | BAC | NYSE | https://finance.yahoo.com/quote/BAC | 3 | |
| Walt Disney | DIS | NYSE | https://finance.yahoo.com/quote/DIS | 2 | |
| Morgan Stanley | MS | NYSE | https://finance.yahoo.com/quote/MS | 2 | |
| IBM | IBM | NYSE | https://finance.yahoo.com/quote/IBM | 2 | |
| Samsung Electronics | 005930.KS | KRX | https://finance.yahoo.com/quote/005930.KS | 2 | Korea Stock Exchange |
| T-Mobile US | TMUS | NASDAQ | https://finance.yahoo.com/quote/TMUS | 2 | |
| Lenovo | 0992.HK | HKEX | https://finance.yahoo.com/quote/0992.HK | 2 | Hong Kong listing; ADR is `LNVGY` (OTC) |
| AMD | AMD | NASDAQ | https://finance.yahoo.com/quote/AMD | 2 | Advanced Micro Devices |
| Alibaba Group | BABA | NYSE | https://finance.yahoo.com/quote/BABA | 2 | NYSE ADR; Hong Kong listing is `9988.HK` |
| Wells Fargo | WFC | NYSE | https://finance.yahoo.com/quote/WFC | 1 | |
| Salesforce | CRM | NYSE | https://finance.yahoo.com/quote/CRM | 1 | Owns Slack |
| Texas Instruments | TXN | NASDAQ | https://finance.yahoo.com/quote/TXN | 1 | |
| Eli Lilly | LLY | NYSE | https://finance.yahoo.com/quote/LLY | 1 | |
| Roche Holding | RHHBY | OTC (US ADR) | https://finance.yahoo.com/quote/RHHBY | 1 | Primary listing `ROG.SW` (SIX Swiss) |
| Intel | INTC | NASDAQ | https://finance.yahoo.com/quote/INTC | 1 | |
| Tesla | TSLA | NASDAQ | https://finance.yahoo.com/quote/TSLA | 1 | |
| Shopify | SHOP | NYSE | https://finance.yahoo.com/quote/SHOP | 1 | Also TSX `SHOP.TO` |
| Cloudflare | NET | NYSE | https://finance.yahoo.com/quote/NET | 1 | |
| Broadcom | AVGO | NASDAQ | https://finance.yahoo.com/quote/AVGO | 1 | |
| Goldman Sachs | GS | NYSE | https://finance.yahoo.com/quote/GS | 1 | |
| Citigroup | C | NYSE | https://finance.yahoo.com/quote/C | 1 | |

## Private / not traded (no ticker)

Named in articles but not publicly traded — name them plainly, no ticker.

| Company | Mentions | Notes |
|---|---|---|
| Anthropic | 105 | Private; reported considering IPO mid-2026 — re-check before publishing |
| OpenAI | 34 | Private; capped-profit hybrid structure |
| GitHub | 20 | Owned by Microsoft (`MSFT`); no separate ticker |
| Slack | 7 | Owned by Salesforce (`CRM`); no separate ticker |
| Discord | 3 | Private |
| Mistral | 3 | Private (France) — Mistral AI |
| Cursor | 3 | Private — Anysphere |
| Vercel | 2 | Private |
| Substack | 2 | Private |
| KPMG | 2 | Private partnership (Big Four) |
| DeepSeek | — | Private (China) |
| Moonshot AI | — | Private (China) |
| MiniMax | — | Private (China) |
| xAI | — | Private (Musk) |
| Stripe | — | Private |
| Bloomberg LP | — | Private partnership (the news/terminal company) |
| SpaceX | — | Private (Musk) |
| Cohere | — | Private |
| Hugging Face | — | Private |

## Append rule

When I write about a company not in this file, I:
1. Look up the ticker — Yahoo Finance search at <https://finance.yahoo.com/lookup?s=> for any market, or pull from SEC EDGAR JSON for US-listed precision
2. Add a row under the right table (Traded or Private)
3. Apply the linked-ticker format in the article on first mention

If the company is private, add it to the second table so the next article doesn't waste time re-checking.

# Companies

Seed: Working cache of company → ticker → Yahoo URL mappings used in articles, plus private-company list. Append on every new company mentioned.
