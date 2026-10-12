#!/bin/zsh
# 建置並部署 zdelp.co：main（原始碼）＋ gh-pages（dist）。用法：./deploy.sh "commit message"
set -e
export PATH=$HOME/bin:$PATH
cd "$(dirname "$0")"
PYTHONIOENCODING=utf-8 python3 src/build_site.py
git add -A && git commit -qm "${1:-update}" || true
git push -q origin main
rm -rf /tmp/ghp && mkdir /tmp/ghp && cp -R dist/. /tmp/ghp/
[ -f LIVE ] || rm -f /tmp/ghp/CNAME   # 建立 LIVE 檔後才帶 CNAME（正式上線）
cd /tmp/ghp && git init -q && git checkout -q -b gh-pages && git add -A && git -c user.name="Fiamma (Zagdim)" -c user.email="zagdimoverseas@gmail.com" commit -qm "deploy: ${1:-update}" && git remote add origin https://github.com/firebee09/zdelp-site.git && git push -qf origin gh-pages
echo "deployed → https://firebee09.github.io/zdelp-site/"
