# -*- coding: utf-8 -*-
"""zdelp.co 靜態站建置：dist/（正式，相對路徑 assets/）＋ preview/（Artifact 用，data-URI）。
沿用 canonical v2 設計系統（ltr-base.css＋DTV extra）＋站層 site.css。"""
import io, os, re, base64, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets')
T = '/Users/zagdim01/.claude/skills/service-page-builder/templates/canonical-v2-dtv/'
UPDATED = '2026 年 9 月 20 日'
ZAG = 'https://zagdim.com'

def du(f):
    m = 'image/png' if f.endswith('.png') else 'image/jpeg'
    return 'data:%s;base64,' % m + base64.b64encode(open(os.path.join(A, f), 'rb').read()).decode()

base_css = io.open(T + 'ltr-base.css', encoding='utf-8').read().replace(
    '/* ZDelp LTR Optimized V2 | 2026-09-15 | isolated service blocks */', '/* zdelp.co — canonical v2 design system | 2026-09-20 */')
extra_css = io.open(T + 'th-dtv-b-extra.css', encoding='utf-8').read()
site_css = io.open(os.path.join(ROOT, 'src', 'site.css'), encoding='utf-8').read()
CSS = base_css + '\n' + extra_css + '\n' + site_css
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap">'

# ---------------- 服務資料（唯一來源）----------------
SERVICES = [
  dict(k='dtv', group='own', img='banner-dtv.jpg', name='泰國 DTV 數位遊民／遠端工作簽證', en='Destination Thailand Visa',
       who='遠端工作者、自由工作者，或來泰國參加課程與活動的人', fact='5 年多次入境，每次停留 180 天',
       url=ZAG + '/%e6%b3%b0%e5%9c%8b-dtv-%e7%b0%bd%e8%ad%89%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99/'),
  dict(k='retire', group='own', img='banner-retire.jpg', name='泰國退休簽證 Non-O／O-A', en='Thailand Retirement Visa',
       who='年滿 50 歲、計劃在泰國長住的人', fact='一年一延，不設總年限',
       url=ZAG + '/services/thailand-retirement-visa-non-o-oa/'),
  dict(k='ltr', group='own', img='banner-ltr.jpg', name='泰國 LTR 長期居留簽證', en='Long-Term Resident Visa',
       who='收入或資產達門檻的專業人士、退休人士與其家屬', fact='10 年效期，海外收入免稅',
       url=ZAG + '/%e6%b3%b0%e5%9c%8b%e9%95%b7%e6%9c%9f%e5%b1%85%e7%95%99-ltr-visa-%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99/'),
  dict(k='elite', group='own', img='banner-elite.jpg', name='泰國菁英簽證', en='Thailand Privilege Visa',
       who='不想每 180 天出境、想一次解決長住身份的人', fact='5／10／15／20 年會籍',
       url=ZAG + '/%e6%b3%b0%e5%9c%8b%e8%8f%81%e8%8b%b1%e7%b0%bd%e8%ad%89%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99%ef%bd%9cthailand-elite-privilege-visa/'),
  dict(k='nonb', group='own', img='banner-nonb.jpg', name='泰國 Non-B 商務簽證', en='Non-Immigrant B Visa',
       who='在泰國受僱、開公司或以投資身份居留的人', fact='1 年，可配合工作許可',
       url=ZAG + '/%e6%b3%b0%e5%9c%8b%e5%95%86%e5%8b%99%e7%b0%bd%e8%ad%89%e7%94%b3%e8%ab%8b%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99%ef%bd%9cnon-immigrant-business-visa%ef%bc%88non-b%ef%bc%89/'),
  dict(k='bank', group='partner', img='banner-bank.jpg', name='泰國銀行開戶協助', en='Thailand Bank Account',
       who='持長期簽證、需要泰銖帳戶收租或存放簽證財力的人', fact='銀行與分行安排、文件核對',
       url=ZAG + '/services/thailand-bank-account-opening-assistance/'),
  dict(k='bkk', group='partner', img='banner-bkk.jpg', name='曼谷房產出租與代管', en='Bangkok Rental Management',
       who='人不在泰國的海外業主', fact='放租、代管、報告，由持牌管理公司執行',
       url=ZAG + '/services/bangkok-rental-management-overseas-owner/'),
  dict(k='uk', group='partner', img='banner-uk.jpg', name='英國置業與公司服務', en='UK Property & Company',
       who='以個人或公司名義在英國置業、需要稅務與架構安排的人', fact='買賣、按揭、公司架構、租金申報',
       url=ZAG + '/services/uk/'),
]
PENDING = [('日本虛擬辦公室與公司註冊', '已有個案經驗，服務頁籌備中'), ('其他國家簽證', '越南、馬來西亞、杜拜等，按個案評估'), ('稅務與法律', '由協作的會計師與律師提供，先評估再配對')]

def img(f, alt, cls='', w=None, h=None, preview=False, eager=False):
    src = du(f) if preview else 'assets/' + f
    dims = (' width="%d" height="%d"' % (w, h)) if w else ''
    lazy = '' if eager else ' loading="lazy" decoding="async"'
    return '<img src="%s" alt="%s"%s%s%s>' % (src, html.escape(alt), (' class="%s"' % cls) if cls else '', dims, lazy)

def nav(active, preview, rel=''):
    items = [('index.html', '首頁'), ('services.html', '服務'), ('about.html', '關於 ZDelp'), ('partners.html', '合作夥伴'), ('contact.html', '聯絡')]
    if preview:
        links = ''.join('<a%s href="#%s">%s</a>' % (' class="is-active"' if a == active else '', a.replace('.html', ''), t) for a, t in items)
    else:
        links = ''.join('<a%s href="%s%s">%s</a>' % (' class="is-active"' if a == active else '', rel, a, t) for a, t in items)
    logo = img('zdelp.png', 'ZDelp', preview=preview, eager=True)
    return ('<header class="zs-nav"><div class="zs-nav-in"><a class="zs-logo" href="%sindex.html">%s<span>ZDelp<small>在地協助</small></span></a>'
            '<nav class="zs-links">%s</nav><a class="zs-cta" href="%scontact.html">20 分鐘免費初審</a></div></header>') % (rel, logo, links, rel)

def footer(preview, rel=''):
    return ('<footer class="zs-foot"><div class="zs-foot-in"><div><b>ZDelp Limited</b><p>香港註冊 · 海外在地協助平台<br>與宅點（Zagdim）互補協作：宅點指引方向，ZDelp 在地協助。</p></div>'
            '<div><b>聯絡</b><p>info@zagdim.com<br>WhatsApp · LINE · WeChat（Zagdim）</p></div>'
            '<div><b>研究與內容</b><p><a href="https://zagdim.com/" target="_blank" rel="noopener">zagdim.com 宅點海外</a><br><a href="https://zagdim.com/zdelp/" target="_blank" rel="noopener">ZDelp 在宅點的公司頁</a></p></div></div>'
            '<p class="zs-legal">ZDelp Limited 提供泰國簽證代辦服務，並為其他海外服務提供評估、配對與跟進；法律、稅務與房地產代理服務由具當地合法執照的協作機構提供，ZDelp 不對其操作結果承擔法律責任，亦不代收代付。本站內容僅供一般參考，不構成稅務、法律或投資建議；簽證審批結果由相關政府部門決定，ZDelp 不保證任何申請必然通過。資訊更新於 %s。</p></footer>') % UPDATED

def card(s, preview):
    tag = '自營 · ZDelp 專員辦理' if s['group'] == 'own' else '協作 · 持牌機構提供'
    return ('<article class="zs-card"><a class="zs-card-img" href="%s" target="_blank" rel="noopener">%s</a><div class="zs-card-body"><p class="zlv-kicker">%s</p><h3>%s<small>%s</small></h3>'
            '<p><strong>適合：</strong>%s</p><p class="zs-fact">%s</p><a class="zs-more" href="%s" target="_blank" rel="noopener">查看詳情與費用</a></div></article>') % (
            s['url'], img(s['img'], s['name'] + ' 服務橫幅', w=1200, h=400, preview=preview), tag, s['name'], s['en'], s['who'], s['fact'], s['url'])

def page(title, desc, body, preview, active, rel='', ld=None):
    ldtags = ''.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in (ld or []))
    anim = """<script>(function(){if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.documentElement.classList.add('zlv-anim');var els=[].slice.call(document.querySelectorAll('.zlv-shell>*'));var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});els.forEach(function(el){io.observe(el)});setTimeout(function(){els.forEach(function(el){el.classList.add('is-in')})},4000)})();</script>"""
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><meta name="description" content="%s">%s<style>\n%s\n</style></head><body class="zs-body">%s%s%s%s%s</body></html>') % (
        html.escape(title), html.escape(desc), FONTS, CSS, nav(active, preview, rel), body, footer(preview, rel), anim, ldtags)

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": "https://zdelp.co/#organization", "name": "ZDelp", "legalName": "ZDelp Limited", "url": "https://zdelp.co/", "sameAs": ["https://zagdim.com/zdelp/", "https://www.facebook.com/ZDelpThailifeservice"], "logo": "https://zdelp.co/assets/zdelp.png", "email": "info@zagdim.com", "foundingDate": "2018", "address": {"@type": "PostalAddress", "addressRegion": "Hong Kong", "addressCountry": "HK"}, "areaServed": ["Thailand", "Japan", "United Kingdom", "Vietnam", "Malaysia", "Germany"], "description": "ZDelp Limited 是於香港註冊的海外在地協助公司，與宅點（Zagdim）互補協作：泰國簽證由 ZDelp 專員代辦，其他海外服務由協作的持牌機構提供，ZDelp 負責評估、配對與跟進。"}

def home(preview):
    own = ''.join(card(s, preview) for s in SERVICES if s['group'] == 'own')
    part = ''.join(card(s, preview) for s in SERVICES if s['group'] == 'partner')
    body = f'''
<section id="index" class="zlv-section zlv-hero zlv-hero-a zs-hero"><div class="zlv-shell"><div class="zlv-hero-stack"><div class="zlv-hero-copy"><div class="zlv-brandline" aria-label="宅點與 ZDelp"><span class="zlv-bl-zag">宅點｜指引方向</span><span class="zlv-bl-x" aria-hidden="true">×</span><span class="zlv-bl-zd">{img('zdelp.png','',preview=preview,eager=True)}ZDelp｜在地協助</span></div><p class="zlv-kicker">ZDelp Limited · 香港註冊 · 2018 年起</p><h1>海外在地協助平台<span>泰國簽證代辦 · 海外服務配對</span></h1><p class="zlv-lead">ZDelp Limited 是於香港註冊的海外在地協助公司。泰國簽證由 ZDelp 專員直接代辦；銀行開戶、房產代管、英國置業與公司、稅務與法律等服務，由 ZDelp 協作的持牌機構提供，ZDelp 負責評估、配對與全程跟進。研究與判斷交給宅點，把事情辦成交給 ZDelp。</p><div class="zlv-actions"><a class="zlv-btn zlv-primary" href="{'#services' if preview else 'services.html'}">查看全部服務</a><a href="{'#contact' if preview else 'contact.html'}">20 分鐘免費初審</a></div></div><figure class="zlv-hero-art">{img('hero-home.jpg','ZDelp 海外在地協助：一對退休夫婦在泰國海景客廳手持護照',w=1774,h=887,preview=preview,eager=True)}</figure></div><div class="zlv-strip"><span>2018 年至今協助超過 3,000 位會員</span><span>泰國簽證自營代辦</span><span>持牌機構協作配對</span><span>本頁資訊更新於 {UPDATED}</span></div></div></section>
<section class="zlv-section zlv-paper"><div class="zlv-shell"><header class="zlv-head"><p class="zlv-kicker">01 · 兩類服務</p><h2>ZDelp 做什麼，誰來做</h2></header><div class="zlv-grid"><article class="zlv-card"><p class="zlv-kicker">自營服務</p><h3>泰國簽證代辦<small>By ZDelp Specialists</small></h3><p><strong>由 ZDelp 專員直接辦理</strong>，收取代辦服務費，未成功退還 70%。20 分鐘初審資格、制定方案、資料籌備、遞件、跟進至獲批，全程遠端完成。服務費以各詳情頁公布及專員實際報價為準。</p></article><article class="zlv-card"><p class="zlv-kicker">協作服務</p><h3>海外在地協助配對<small>With Licensed Partners</small></h3><p><strong>由 ZDelp 協作的持牌機構提供</strong>（律師、會計師、房產代理、物業管理、移民顧問）。ZDelp 評估需求、配對、協調與跟進，費用由你與該機構直接結算，ZDelp 不代收代付。</p></article></div></div></section>
<section class="zlv-section"><div class="zlv-shell"><header class="zlv-head zlv-head-mascot"><div><p class="zlv-kicker">02 · 泰國簽證</p><h2>五種泰國長期簽證，由 ZDelp 專員代辦</h2></div>{img('mascot-thai-flag.png','宅點松鼠舉著泰國國旗','zlv-mascot',w=349,h=360,preview=preview)}</header><div class="zs-cards">{own}</div></div></section>
<section class="zlv-section zlv-paper"><div class="zlv-shell"><header class="zlv-head"><p class="zlv-kicker">03 · 海外在地協助</p><h2>由協作持牌機構提供，ZDelp 配對與跟進</h2></header><div class="zs-cards">{part}</div><p class="zlv-note">籌備中：{'；'.join(n for n,_ in PENDING)}。歡迎先聯絡評估。</p></div></section>
<section class="zlv-section zlv-paper" id="dtv-service" style="background:#0b3442"><div class="zlv-shell"><div class="zlv-service-top"><div><div class="zlv-brand">{img('zdelp.png','ZDelp 標誌',w=300,h=300,preview=preview)}<p><b>ZDelp</b>海外在地協助平台</p></div><header class="zlv-head"><p class="zlv-kicker">04 · 怎麼開始</p><h2>先評估，再開始</h2></header></div><div class="zlv-count"><b>20</b><div><span>分鐘免費初審，不符合就直接說</span></div></div></div><ol class="zlv-flow"><li><span class="zlv-step">01</span><h3>留下所在地與需要</h3></li><li><span class="zlv-step">02</span><h3>專員初審與評估</h3></li><li><span class="zlv-step">03</span><h3>確認方案與費用</h3></li><li><span class="zlv-step">04</span><h3>開始辦理，跟進到完成</h3></li></ol></div></section>
<section class="zlv-section"><div class="zlv-shell"><div class="zlv-grid zlv-intro"><div><header class="zlv-head"><p class="zlv-kicker">05 · 與宅點的關係</p><h2>宅點幫你理解與判斷，ZDelp 幫你執行與完成</h2></header><p>宅點（Zagdim）是內容與研究品牌，追蹤政策變動、查證與分析，讓你在行動前看清楚現在適用什麼、接下來可能變什麼。ZDelp 是執行端：把研究結論變成可以辦成的事。兩者互補協作，共用一組聯絡方式。</p><p>各項服務的詳細說明、費用與政策變動時間線刊登於 zagdim.com；本站是 ZDelp Limited 的公司頁與服務目錄。</p></div><div class="zlv-benefits"><div class="zlv-benefit"><b>研究在前</b><p>每項服務都先有宅點的政策追蹤與分析。</p></div><div class="zlv-benefit"><b>評估先於銷售</b><p>20 分鐘免費初審，不符合就直接說。</p></div><div class="zlv-benefit"><b>誰來做寫清楚</b><p>自營或協作機構，每頁都註明。</p></div><div class="zlv-benefit"><b>費用公開</b><p>官方費與服務費分開列，按申請地公布。</p></div><div class="zlv-benefit"><b>不代收代付</b><p>協作服務的費用由你與該機構直接結算。</p></div><div class="zlv-benefit"><b>持續跟進</b><p>協作服務出現溝通問題，ZDelp 協助協調。</p></div></div></div></div></section>
<section class="zlv-section zlv-paper" id="contact"><div class="zlv-shell"><div class="zlv-end"><p>告訴我們所在地與需要的服務，專員會以 WhatsApp、LINE 或電郵回覆。</p><a class="zlv-btn zlv-primary" href="{'#contact' if preview else 'contact.html'}">聯絡 ZDelp</a></div></div></section>'''
    return page('ZDelp Limited｜海外在地協助平台：泰國簽證代辦與海外服務配對', 'ZDelp Limited 是香港註冊的海外在地協助公司，與宅點互補協作：泰國簽證自營代辦，其他海外服務由協作持牌機構提供，ZDelp 負責評估、配對與跟進。', body, preview, 'index.html', ld=[ORG])

def services(preview):
    own = ''.join(card(s, preview) for s in SERVICES if s['group'] == 'own')
    part = ''.join(card(s, preview) for s in SERVICES if s['group'] == 'partner')
    pend = ''.join('<article class="zlv-card zs-card-pending"><p class="zlv-kicker">籌備中</p><h3>%s</h3><p>%s。</p><a class="zs-more" href="%s">聯絡評估</a></article>' % (n, d, '#contact' if preview else 'contact.html') for n, d in PENDING)
    body = f'''
<section id="services" class="zlv-section zlv-hero zlv-hero-a zs-hero-sm"><div class="zlv-shell"><div class="zlv-hero-copy"><p class="zlv-kicker">服務總覽 · {UPDATED} 更新</p><h1>ZDelp 服務總覽<span>泰國簽證代辦與海外在地協助</span></h1><p class="zlv-lead">自營服務由 ZDelp 專員直接辦理並收取服務費；協作服務由 ZDelp 協作的持牌機構提供，ZDelp 負責評估、配對與跟進。每項服務的申請條件、費用與政策變動時間線，見宅點（zagdim.com）的詳情頁。</p></div></div></section>
<section class="zlv-section zlv-paper"><div class="zlv-shell"><header class="zlv-head zlv-head-mascot"><div><p class="zlv-kicker">01 · 自營服務</p><h2>泰國簽證代辦</h2></div>{img('mascot-thai-flag.png','宅點松鼠舉著泰國國旗','zlv-mascot',w=349,h=360,preview=preview)}</header><p>年滿條件、財力門檻、申請地與官方費用各不相同，先做 20 分鐘免費初審再決定走哪一種。未成功退還 70% 服務費；服務費以各詳情頁公布及專員實際報價為準。</p><div class="zs-cards">{own}</div></div></section>
<section class="zlv-section"><div class="zlv-shell"><header class="zlv-head"><p class="zlv-kicker">02 · 協作服務</p><h2>海外在地協助</h2></header><p>由當地持牌機構提供（律師、會計師、房產代理、物業管理、移民顧問），配對前提供該機構的資料與執照資訊供你核對；費用由你與該機構直接結算。</p><div class="zs-cards">{part}</div><div class="zlv-grid zs-pending">{pend}</div></div></section>
<section class="zlv-section zlv-paper" id="contact"><div class="zlv-shell"><div class="zlv-end"><p>不確定自己適合哪一種？先做 <mark class="zlv-ul">20 分鐘免費初審</mark>。</p><a class="zlv-btn zlv-primary" href="{'#contact' if preview else 'contact.html'}">聯絡 ZDelp</a></div></div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": "ZDelp 服務總覽", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": s['name'], "url": s['url'], "provider": {"@id": "https://zdelp.co/#organization"}}} for i, s in enumerate(SERVICES)]}]
    return page('ZDelp 服務總覽｜泰國簽證代辦與海外在地協助', '泰國 DTV／退休簽／LTR／菁英／Non-B 由 ZDelp 專員代辦；銀行開戶、曼谷代管、英國置業與公司服務由協作持牌機構提供。', body, preview, 'services.html', ld=ld)

if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
    for name, fn in [('index.html', home), ('services.html', services)]:
        io.open(os.path.join(ROOT, 'dist', name), 'w', encoding='utf-8').write(fn(False))
        io.open(os.path.join(ROOT, 'preview', name.replace('index', 'home')), 'w', encoding='utf-8').write(fn(True))
    # gate text
    for name, fn in [('home', home), ('services', services)]:
        t = fn(False)
        t = re.sub(r'<style>.*?</style>', '', t, flags=re.S); t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
        t = re.sub(r'</(p|h1|h2|h3|li|tr|summary|figcaption|div|section|header|article|a|span|footer)>', '\n', t); t = re.sub(r'<[^>]+>', '', t); t = html.unescape(t); t = re.sub(r'\n\s*\n+', '\n', t).strip()
        io.open(os.path.join(ROOT, 'preview', 'gate-%s.md' % name), 'w', encoding='utf-8').write(t)
    import shutil; shutil.copytree(A, os.path.join(ROOT,'dist','assets'), dirs_exist_ok=True)
    print('built dist/ + preview/')
