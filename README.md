# zdelp.co 靜態站

- `src/build.py`＋`src/site.css`：建置腳本（沿用 canonical v2 設計系統：ltr-base.css＋DTV extra）。`SERVICES` 是服務目錄唯一來源。
- `assets/`：圖片（橫幅 3:1 1200×400、首頁頭圖 2:1、logo、松鼠）。
- `dist/`：正式輸出（相對路徑），直接部署到 Cloudflare Pages／Netlify。
- `preview/`：Artifact 預覽（data-URI）＋雙 gate 用純文字。
- 原則：zdelp.co 只放摘要卡＋外連 zagdim.com 詳情頁，不複製全文。

## 部署（待 Fiamma 開 GitHub 帳號）
1. repo `zdelp-site`，push 整個資料夾。
2. Cloudflare Pages 連 repo，build command 無、output `dist`。
3. GoDaddy DNS：`@` CNAME → `<project>.pages.dev`（或 A/AAAA 依 Cloudflare 指示）、`www` CNAME 同上；取消 Website Builder。

## 進度
- 2026-09-20 v1：首頁＋服務總覽（雙 gate PASS）。待做：關於 ZDelp／合作夥伴／聯絡（HubSpot b67da755）、EN。
