# 交接：把 zdelp.co＋名片頁推上線（給新 session，2026-09-22）

## 現況（一句話）
zdelp.co 六頁雙語 v3 已在 staging（https://firebee09.github.io/zdelp-site/），DNS 未切；七家 A 級名片頁資料檔與產生器已完成（`~/.claude/skills/produce-zdelp-provider-profile/`），尚未併入網站。

## 正本在哪
- 網站原始碼：`~/Desktop/Claude/zdelp-site/`（`src/build_site.py`＋`src/zdelp.css`；`./deploy.sh "訊息"` 一鍵建置＋推 main＋推 gh-pages）。README 有部署與 DNS 步驟。
- 名片頁：skill `produce-zdelp-provider-profile`（SKILL.md v1.5 是唯一現行規格；`examples/<slug>.json` 七家資料；`scripts/build_profile.py`、`check_profile.py`、`build_batch_preview.py`、`build_fill_list.py`）。
- 待 Fiamma 填清單：`~/Desktop/Claude/provider-services/PROFILE-FILL-LIST-2026-09-21.md`（必要 26 項／可後補 59 項）。
- 記憶：`memory/project-zdelp-provider-profile-pages.md`、`project-zdelp-entity-disclosure.md`、`reference-zdelp-site-deploy.md`。
- Codex 往來：`CODEX-READBACK-2026-09-21-provider-profiles.md`（含五段補充）。

## 推上線要做的事（順序）
1. **名片頁併入網站**：在 `build_site.py` 加 `providers/<slug>.html`（zh）＋一頁名單頁（按類別分組，沿用 v3 樣式），把 `build_profile.py` 的 `build()` 改成回傳 body、共用 nav／footer／CSS；`dist/assets/providers/` 放 logo（現在是 data URI，上線改檔案）。
2. **公開條件**：`build_profile.py --public` 目前七家全部 BLOCKED（缺：機構同意具名、身分與資格核對、訪談、實際評估紀錄、facts 全欄）。**上線前要 Fiamma 決定**：補齊後再上，或她點名先上哪幾家（用她的判斷覆寫 blocker）。同一類別 ≥3 家才公開名單頁的規則也由她拍板。
3. **ZDelp 評分**：七家現為她 09-22 口頭區間分（4.8／4.9／4.7／4.7／4.8／4.7／4.9），上線前請她逐家確認。
4. **DNS**（GoDaddy → GitHub Pages）：A @ 185.199.108.153／109／110／111，CNAME www → firebee09.github.io；然後 repo 根建 `LIVE` 檔讓 deploy.sh 帶回 CNAME；GitHub Pages 設定 Enforce HTTPS；取消 GoDaddy Website Builder。
5. 仍待她提供：hero 真實照片（現用 Codex AI 圖左半）、人員圓形頭像＋全名＋書面同意、ZDelp 自家 WhatsApp／LINE／email、logo 顏色。
6. 外部寫入鐵律：每一步「推 gh-pages／切 DNS／上線名片頁」都要她對該動作點名。

## 用語與裁定（別踩）
客人頁不寫：合作／協作／配對／核驗／持牌／執照／徽章／不代收代付／保證／必然／cross-border／任何價格／作業語言（訪談日期、書面問答、核對紀錄）。四步＝身分與資格核對・視訊訪談・實際評估・ZDelp 評分。名片頁結構＝名稱＋一句 → 三勾＋ZDelp 評分（金星、半星半灰）→ 能辦什麼＋不包含一行 → 三段評估 → 在地專員（圓形頭像＋全名）→ 側欄（聯絡＋基本資料，「告訴我們你的需要。」）→ 頁尾。gate：`check_profile.py`。對 Fiamma 一律台灣書面國語。
