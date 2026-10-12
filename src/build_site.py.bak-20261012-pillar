# -*- coding: utf-8 -*-
"""zdelp.co 全站建置 v3（2026-09-21：v2 Codex 文案＋v3 設計「一個窗口，聯通全球」；zh/en 雙語可切換；手機選單）。
輸出：dist/{index,services,verify,partners,about,contact}.html ＋ dist/en/…（相對 assets）；
preview/site.html（單檔、data-URI、hash 切頁，給 Artifact）；preview/gate-<lang>-<page>.md。"""
import io, os, re, sys, glob, base64, json, html, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets')
PROFILE_SKILL = os.path.expanduser('~/.claude/skills/produce-zdelp-provider-profile')
sys.path.insert(0, os.path.join(PROFILE_SKILL, 'scripts'))
import build_profile as BP  # 名片頁產生器（共用，正本在 skill 裡；此處只併頁不改邏輯）

def load_providers():
    out = []
    for f in sorted(glob.glob(os.path.join(PROFILE_SKILL, 'examples', '*.json'))):
        out.append(json.load(io.open(f, encoding='utf-8')))
    out.sort(key=lambda d: (d.get('category') or '', d.get('name') or ''))
    return out
PROVIDERS = load_providers()
LOGO_ALT = 'ZDelp'
CSS = io.open(os.path.join(ROOT, 'src', 'zdelp.css'), encoding='utf-8').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">'
ZAG = 'https://zagdim.com'
PAGES = ['index', 'services', 'verify', 'partners', 'about', 'contact']
NAV_PAGES = ['index', 'services', 'verify', 'about', 'contact']  # partners 不入主導覽（Fiamma 09-21：對客人不提合作）
HS_FORM = 'b67da755-3d8e-40ad-9010-2639a97704a1'
HS_PARTNER_FORM = '4db3d945-014f-4a96-879c-235381578c96'
WA = 'https://wa.me/message/LEFWMCKCXNF3O1'; LINE = 'https://lin.ee/yVDUzDo'; WECHAT = 'ZDelp_Official'; MAIL = 'mailto:info@zdelp.co'; MAIL_TXT = 'info@zdelp.co'  # 10-12b：不公開電話（防爬蟲／我們不會打電話）

def du(f):
    m = 'image/png' if f.endswith('.png') else 'image/jpeg'
    return 'data:%s;base64,' % m + base64.b64encode(open(os.path.join(A, f), 'rb').read()).decode()

U = {'dtv': ZAG + '/%e6%b3%b0%e5%9c%8b-dtv-%e7%b0%bd%e8%ad%89%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99/',
     'retire': ZAG + '/services/thailand-retirement-visa-non-o-oa/',
     'ltr': ZAG + '/%e6%b3%b0%e5%9c%8b%e9%95%b7%e6%9c%9f%e5%b1%85%e7%95%99-ltr-visa-%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99/',
     'elite': ZAG + '/%e6%b3%b0%e5%9c%8b%e8%8f%81%e8%8b%b1%e7%b0%bd%e8%ad%89%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99%ef%bd%9cthailand-elite-privilege-visa/',
     'nonb': ZAG + '/%e6%b3%b0%e5%9c%8b%e5%95%86%e5%8b%99%e7%b0%bd%e8%ad%89%e7%94%b3%e8%ab%8b%e4%bb%a3%e8%be%a6%e6%9c%8d%e5%8b%99%ef%bd%9cnon-immigrant-business-visa%ef%bc%88non-b%ef%bc%89/',
     'bank': ZAG + '/services/thailand-bank-account-opening-assistance/',
     'bkk': ZAG + '/services/bangkok-rental-management-overseas-owner/',
     'uk': ZAG + '/services/uk/'}
IMG = {'dtv': 'banner-dtv.jpg', 'retire': 'banner-retire.jpg', 'ltr': 'banner-ltr.jpg', 'elite': 'banner-elite.jpg', 'nonb': 'banner-nonb.jpg', 'bank': 'banner-bank.jpg', 'bkk': 'banner-bkk.jpg', 'uk': 'banner-uk.jpg'}

T = {
 'zh': dict(lang='zh-Hant', nav=['首頁', '服務', '信任與保障', '關於我們', '聯絡'], partner_link='在地機構與專業人士：加入我們', cta='聯絡我們', sw='EN', tag='LOCAL ASSISTANCE', brand='在地・可靠・同行',
   own='我們的專員辦理', ver='在地機構／專業人士辦理', more='查看詳情與費用', ext='詳情刊於宅點',
   legal='本站內容僅供一般參考，不構成稅務、法律或投資建議。辦理條件與費用以各服務詳情及正式報價為準；簽證審批由相關政府部門決定，開戶結果由銀行決定，我們不保證任何申請必然通過。'),
 'en': dict(lang='en', nav=['Home', 'Services', 'Trust & Protection', 'About us', 'Contact'], partner_link='Local firms and professionals: join us', cta='Contact us', sw='中文', tag='LOCAL ASSISTANCE', brand='Local. Reliable. With you.',
   own='Handled by our specialists', ver='Handled by a local firm or professional', more='View details and fees', ext='Details in Chinese on Zagdim',
   legal='Content on this site is general information only and does not constitute tax, legal or investment advice. Requirements and fees are set out in the relevant service details and individual quotation, and are subject to confirmation by us or the firm; visa decisions are made by the relevant government authorities and account opening decisions by the bank. We do not guarantee any outcome.'),
}

def img(f, alt, cls='', preview=False, eager=False, rel=''):
    src = du(f) if preview else rel + 'assets/' + f
    lazy = '' if eager else ' loading="lazy" decoding="async"'
    return '<img src="%s" alt="%s"%s%s>' % (src, html.escape(alt), (' class="%s"' % cls) if cls else '', lazy)

def link(page, lang, preview, rel, anchor=''):
    if preview: return '#%s-%s' % (lang, page)
    return page + '.html' + anchor

# page_prefix：預設 ''（沿用既有 zh／en 六頁與 preview 行為，不受影響）。
# providers/<slug>.html 這類巢狀一層的頁面才傳 '../'，讓 nav／footer 連回站台其他頁面時補上正確相對路徑
# （rel 本身只管 img() 的 assets/ 路徑；六頁與 en/ 六頁彼此是同層檔案，本來不需要靠 rel 連頁，故沿用舊行為不動 link()）。
def nav(active, lang, preview, rel, page_prefix=''):
    t = T[lang]
    items = ''.join('<a%s href="%s">%s</a>' % (' class="on"' if p == active else '', page_prefix + link(p, lang, preview, rel), n) for p, n in zip(NAV_PAGES, t['nav']))
    other = 'en' if lang == 'zh' else 'zh'
    sw_page = active if active in PAGES else 'index'
    sw = ('#%s-%s' % (other, active)) if preview else (page_prefix + ('en/' if other == 'en' else '../') + sw_page + '.html')
    logo = img('zdelp.png', 'ZDelp', 'nav-logo', preview, True, rel)
    menu_label = '選單' if lang == 'zh' else 'Menu'
    return ('<header class="nav"><div class="wrap"><a class="logo" href="%s">%s<span>ZDelp<small>%s</small></span></a><nav class="links" id="zd-links">%s</nav>'
            '<button class="burger" type="button" aria-label="%s" aria-expanded="false" aria-controls="zd-links" onclick="var l=this.parentNode.querySelector(\'.links\');var o=l.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)"><span></span></button>'
            '<a class="lang" href="%s" hreflang="%s">%s</a><a class="btn btn-gold nav-cta" href="%s">%s</a></div></header>') % (
            page_prefix + link('index', lang, preview, rel), logo, t['tag'], items, menu_label, sw, 'en' if other == 'en' else 'zh-Hant', t['sw'], page_prefix + link('contact', lang, preview, rel), t['cta'])

def footer(lang, preview, rel, page_prefix=''):
    t = T[lang]
    links = ''.join('<a href="%s">%s</a>' % (page_prefix + link(p, lang, preview, rel), n) for p, n in zip(NAV_PAGES[1:], t['nav'][1:])) + '<br><a class="foot-partner" href="%s">%s</a>' % (page_prefix + link('partners', lang, preview, rel), t['partner_link'])
    return ('<footer><div class="wrap"><div class="foot"><div><b>ZDelp Limited</b><p>%s</p></div><div><b>%s</b><p class="foot-links">%s</p></div>'
            '<div><b>%s</b><p><a href="%s" target="_blank" rel="noopener">WhatsApp</a> · <a href="%s" target="_blank" rel="noopener">LINE</a> · %s</p></div></div>'
            '<p class="legal">%s</p></div></footer>') % (
            t['brand'], '網站' if lang == 'zh' else 'Site', links, '聯絡' if lang == 'zh' else 'Contact', WA, LINE, ('微信 ' if lang == 'zh' else 'WeChat ') + WECHAT, t['legal'])

def badge(lang, own):
    t = T[lang]
    return '<span class="badge own"><i>●</i>%s</span>' % t['own'] if own else '<span class="badge ver"><i>✓</i>%s</span>' % t['ver']

def card(lang, key, title, desc, own, preview, rel, url=None, btn=None, external=True):
    t = T[lang]; url = url or U[key]
    tgt = ' target="_blank" rel="noopener"' if external else ''
    ext = ('<small class="ext">%s</small>' % t['ext']) if external else ''
    return ('<article class="card"><a class="card-img" href="%s"%s>%s</a><div class="b">%s<h3>%s</h3><p>%s</p><a class="more" href="%s"%s>%s</a>%s</div></article>') % (
            url, tgt, img(IMG[key], title, '', preview, False, rel), badge(lang, own), title, desc, url, tgt, btn or t['more'], ext)

def hs_block(lang, preview, target):
    if preview:
        return '<div class="form-mock">%s</div>' % ('〔既有 HubSpot 表格嵌入位，正式站接入〕' if lang == 'zh' else '[Existing HubSpot form embeds here on the live site]')
    return '<div id="%s" class="hs"></div><noscript>%s</noscript>' % (target, 'JavaScript 未啟用，請以 WhatsApp、LINE 或電郵聯絡我們。' if lang == 'zh' else 'JavaScript is disabled; contact us through WhatsApp, LINE or email.')

HS_SCRIPT = """<script>(function(){var t=document.querySelector('.hs');if(!t)return;var fid=t.id==='zd-partner-form'?'%s':'%s';function mount(){if(window.hbspt&&!t.querySelector('iframe'))window.hbspt.forms.create({region:'na1',portalId:'5650486',formId:fid,target:'#'+t.id});}if(window.hbspt){mount();}else{var s=document.createElement('script');s.src='https://js.hsforms.net/forms/embed/v2.js';s.onload=mount;document.head.appendChild(s);}})();</script>""" % (HS_PARTNER_FORM, HS_FORM)
NET_JS = '<script>' + io.open(os.path.join(ROOT, 'src', 'net_anim.js'), encoding='utf-8').read() + '</script>'
ANIM = """<script>(function(){if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.documentElement.classList.add('anim');var els=[].slice.call(document.querySelectorAll('section .wrap>*'));var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.06});els.forEach(function(el){io.observe(el)});setTimeout(function(){els.forEach(function(el){el.classList.add('in')})},4000)})();</script>"""

def cta_band(lang, preview, rel, headline, btn=None, sub=None):
    t = T[lang]
    return '<section class="cta-band"><div class="wrap"><div><p>%s</p>%s</div><a class="btn btn-gold" href="%s">%s</a></div></section>' % (headline, ('<small>%s</small>' % sub) if sub else '', link('contact', lang, preview, rel), btn or t['cta'])

def split_cards(lang):
    if lang == 'zh':
        return ('<div class="split"><div class="split-card own"><span class="badge own"><i>●</i>我們的專員</span><h3>直接辦理泰國簽證。</h3></div>'
                '<div class="split-card ver"><span class="badge ver"><i>✓</i>核驗機構</span><h3>提供銀行開戶、房產與公司等專業服務。</h3></div></div>'
                '<p class="split-note">辦理期間，我們持續跟進。</p>')
    return ('<div class="split"><div class="split-card own"><span class="badge own"><i>●</i>Our specialists</span><h3>Handle Thai visa applications directly.</h3></div>'
            '<div class="split-card ver"><span class="badge ver"><i>✓</i>Vetted firms</span><h3>Provide professional help with bank accounts, property, company matters and other services.</h3></div></div>'
            '<p class="split-note">We continue to follow up while the work is under way.</p>')

# ---------------- 頁面 ----------------
def p_index(lang, preview, rel):
    t = T[lang]; svc = link('services', lang, preview, rel); ver = link('verify', lang, preview, rel)
    if lang == 'zh':
        cards = (card(lang, 'dtv', '泰國簽證', '長住、工作或退休，查看適合的簽證服務。', True, preview, rel, url=svc + ('' if preview else '#th'), btn='查看簽證服務', external=False)
                 + card(lang, 'bank', '銀行開戶', '查看開戶協助與文件準備。', False, preview, rel)
                 + card(lang, 'bkk', '房產出租與代管', '找人協助處理出租與日常管理。', False, preview, rel)
                 + card(lang, 'uk', '英國置業與公司', '查看置業及公司相關服務。', False, preview, rel))
        return f'''
<section class="hero"><div class="wrap"><div class="hero-grid"><div>
<p class="kick">{t['brand']}</p>
<h1>需要幫忙，<br>找<em>我們</em>。</h1>
<p class="lead">簽證、銀行開戶、房產與公司事務。<br>你想辦什麼，告訴我們。</p>
<div class="actions"><a class="btn btn-gold btn-xl" href="{link('contact',lang,preview,rel)}">聯絡我們</a><a class="btn btn-ghost btn-xl" href="{svc}">查看服務</a></div>
<div class="trust"><span><i>✓</i>一個窗口，聯通全球</span><span><i>✓</i>伴隨左右，安心無憂</span></div>
</div><div class="hero-art">{img('hero-people.jpg','我們的專員與客人一起核對申請文件，背景是曼谷市景。','',preview,True,rel)}<div class="hero-cap"><i>●</i><div><b>LOCAL ASSISTANCE</b>在地辦理，持續跟進</div></div></div></div></div></section>
<section class="bg-grey" id="svc"><div class="wrap"><div class="head"><div><p class="kick">服務</p><h2>你需要哪方面協助？</h2></div><p>先說你要辦什麼、在哪裡。每項服務都標示由誰辦理。</p></div><div class="cards four">{cards}</div></div></section>
<section class="net net-how" aria-label="一個窗口，聯通全球；伴隨左右，安心無憂"><div class="wrap"><div class="net-head"><p class="kick">怎麼運作</p><h2>一個窗口，聯通全球。<br>伴隨左右，安心無憂。</h2><p>你不用自己在海外找人、比人、試人。我們協助安排合適服務，伴隨左右，安心無憂。</p></div>
<div class="net-tabs"><div class="net-pill on"><b><i>01</i>一個窗口，聯通全球</b><p>你只需要找我們；各地的在地機構與專業人士，由我們安排。</p></div><div class="net-pill"><b><i>02</i>伴隨左右，安心無憂</b><p>辦理期間我們不退場，協助溝通與協調。</p></div></div>
<div class="net-stage" data-lang="zh" data-label="動畫：ZDelp 一個窗口連到香港、台北、曼谷、東京、倫敦、新加坡、吉隆坡、馬尼拉，並陪同客人走完辦理的每一步。"></div>
<div class="flow net-flow"><div class="fl"><i>1</i><b>你說需求</b><p>要辦什麼、在哪個地區。</p></div><div class="fl"><i>2</i><b>我們評估</b><p>判斷能不能幫、該怎麼安排。</p></div><div class="fl"><i>3</i><b>安排辦理</b><p>由我們的專員，或在當地的機構與專業人士辦理，先給你資料再決定。</p></div><div class="fl"><i>4</i><b>持續跟進</b><p>辦理期間我們不退場，協助溝通與協調。</p></div></div>
<p class="split-note">安排前你會先看到由誰辦理。<a href="{ver}">了解信任與保障</a></p></div></section>
<section class="bg-grey"><div class="wrap"><div class="ground"><figure class="ground-photo">{img('photo-imm.jpg','曼谷移民局入口，辦理當天的排隊人潮。','',preview,False,rel)}<figcaption><b>BANGKOK · IMMIGRATION BUREAU</b>曼谷移民局，辦理當天</figcaption></figure>
<div class="ground-text"><p class="kick">在現場</p><h2>在地辦理，<br>持續跟進。</h2><p>辦事的人就在當地、親自到場；跟進的是我們，隨時找得到。</p><p class="split-note"><a href="{link('contact',lang,preview,rel)}">聯絡我們</a></p></div></div></div></section>
<section class="bg-navy" id="verify"><div class="wrap"><div class="head"><div><p class="kick">信任與保障</p><h2>先把關，再安排。</h2></div><p>你有權知道是誰替你辦事。每一位在地機構與專業人士，我們都先核對資格、進行專業驗證，再收集客人的口碑推薦，並給出 ZDelp 評分。</p></div>
<div class="steps"><div class="step"><i>01</i><b>先看資料，再決定</b><p>安排前，我們先給你對方的資料與資格資訊，確認後才委託。</p></div><div class="step"><i>02</i><b>費用先講清楚</b><p>服務內容與費用在委託前說明清楚。</p></div><div class="step"><i>03</i><b>我們全程跟進</b><p>辦理期間我們不退場，協助溝通與協調。</p></div><div class="step"><i>04</i><b>有問題，找我們</b><p>辦理期間有疑問或爭議，直接聯絡我們，我們協助處理。</p></div></div>
<p class="note" style="color:rgba(255,255,255,.8);margin-top:36px">在地機構與專業人士怎麼來的：資格核對 · 專業驗證 · 口碑推薦 · ZDelp 評分。<a href="{ver}" style="color:var(--gold)">查看信任與保障</a></p></div></section>
{cta_band(lang, preview, rel, '有事要辦，隨時告訴我們。', sub='留下你想辦的事和所在地區，我們會告訴你能不能幫上忙。')}'''
    cards = (card(lang, 'dtv', 'Thai visas', 'Explore visa services for living, working or retiring in Thailand.', True, preview, rel, url=svc + ('' if preview else '#th'), btn='Explore visa services', external=False)
             + card(lang, 'bank', 'Bank accounts', 'Find help with opening an account and preparing your documents.', False, preview, rel)
             + card(lang, 'bkk', 'Property rental and management', 'Find help with letting your property and its day-to-day management.', False, preview, rel)
             + card(lang, 'uk', 'UK property and company services', 'Explore services for buying property and company matters in the UK.', False, preview, rel))
    return f'''
<section class="hero"><div class="wrap"><div class="hero-grid"><div>
<p class="kick">{t['brand']}</p>
<h1>Need help?<br>Talk to <em>us</em>.</h1>
<p class="lead">Visas, bank accounts, property and company matters.<br>Tell us what you need help with.</p>
<div class="actions"><a class="btn btn-gold btn-xl" href="{link('contact',lang,preview,rel)}">Contact us</a><a class="btn btn-ghost btn-xl" href="{svc}">Explore services</a></div>
<div class="trust"><span><i>✓</i>One contact point, local help worldwide</span><span><i>✓</i>Always by Your Side</span></div>
</div><div class="hero-art">{img('hero-people.jpg','One of our specialists and a client checking application documents, with the Bangkok skyline behind them.','',preview,True,rel)}<div class="hero-cap"><i>●</i><div><b>LOCAL ASSISTANCE</b>Handled locally, followed up by us</div></div></div></div></div></section>
<section class="bg-grey" id="svc"><div class="wrap"><div class="head"><div><p class="kick">Services</p><h2>What can we help you with?</h2></div><p>Tell us what you need and where. Each service shows who handles the work.</p></div><div class="cards four">{cards}</div></div></section>
<section class="net net-how" aria-label="One contact point, local help worldwide; always by your side"><div class="wrap"><div class="net-head"><p class="kick">How it works</p><h2>One contact point, local help worldwide.<br>Always by Your Side.</h2><p>You do not have to find, compare and test people overseas yourself. We arrange the right service and follow up while the work is under way.</p></div>
<div class="net-tabs"><div class="net-pill on"><b><i>01</i>One contact point, local help worldwide</b><p>You only need to contact us. We arrange the local firms and professionals wherever you need them.</p></div><div class="net-pill"><b><i>02</i>Always by Your Side</b><p>We stay involved while the work is under way, helping with communication and coordination.</p></div></div>
<div class="net-stage" data-lang="en" data-label="Animation: one ZDelp contact point connecting to Hong Kong, Taipei, Bangkok, Tokyo, London, Singapore, Kuala Lumpur and Manila, staying alongside the client through each step."></div>
<div class="flow net-flow"><div class="fl"><i>1</i><b>Tell us what you need</b><p>What you want to arrange, and where.</p></div><div class="fl"><i>2</i><b>We assess</b><p>We tell you whether we can help and how it would be arranged.</p></div><div class="fl"><i>3</i><b>The work is arranged</b><p>Handled by our specialists, or by a local firm or professional. You see their details before you decide.</p></div><div class="fl"><i>4</i><b>Follow-up</b><p>We stay involved, helping with communication and coordination.</p></div></div>
<p class="split-note">You see who will handle the work before anything is arranged.<a href="{ver}">Trust and protection</a></p></div></section>
<section class="bg-grey"><div class="wrap"><div class="ground"><figure class="ground-photo">{img('photo-imm.jpg','The entrance of the Bangkok Immigration Bureau on an application day.','',preview,False,rel)}<figcaption><b>BANGKOK · IMMIGRATION BUREAU</b>Bangkok Immigration Bureau, application day</figcaption></figure>
<div class="ground-text"><p class="kick">On the ground</p><h2>Handled locally,<br>followed up by us.</h2><p>The work is done by people who are there on the ground. We handle the follow-up, and you can always reach us.</p><p class="split-note"><a href="{link('contact',lang,preview,rel)}">Contact us</a></p></div></div></div></section>
<section class="bg-navy" id="verify"><div class="wrap"><div class="head"><div><p class="kick">Trust and protection</p><h2>Checked before it is arranged.</h2></div><p>You should know who is doing the work. We check the credentials of every local firm and professional, verify their expertise, gather client recommendations, and give each one a ZDelp score.</p></div>
<div class="steps"><div class="step"><i>01</i><b>See who, before you decide</b><p>Before anything is arranged, we give you their details and credentials to check.</p></div><div class="step"><i>02</i><b>Fees explained up front</b><p>The service and its fees are set out before you engage anyone.</p></div><div class="step"><i>03</i><b>We follow up</b><p>We stay involved while the work is under way, helping with communication and coordination.</p></div><div class="step"><i>04</i><b>If something goes wrong, contact us</b><p>If there is a question or a dispute while the work is under way, we help sort it out.</p></div></div>
<p class="note" style="color:rgba(255,255,255,.8);margin-top:36px">How local firms and professionals are assessed: credential checks · professional verification · client recommendations · ZDelp score.<a href="{ver}" style="color:var(--gold)"> See trust and protection</a></p></div></section>
{cta_band(lang, preview, rel, 'Need a hand? Get in touch.', sub='Tell us what you need to arrange and where. We will let you know whether we can help.')}'''

def p_services(lang, preview, rel):
    t = T[lang]; c = link('contact', lang, preview, rel)
    if lang == 'zh':
        th = ''.join([card(lang, 'dtv', 'DTV 簽證', '查看 DTV 申請條件、文件與費用。', True, preview, rel), card(lang, 'retire', '退休簽證 Non-O／O-A', '查看 Non-O、O-A 申請方式與辦理服務。', True, preview, rel), card(lang, 'ltr', 'LTR 長期居留簽證', '查看 LTR 申請資格、文件與辦理服務。', True, preview, rel), card(lang, 'elite', 'Thailand Privilege 菁英簽證', '了解會籍方案與申請服務。', True, preview, rel), card(lang, 'nonb', 'Non-B 商務簽證', '了解商務簽證與相關申請服務。', True, preview, rel)])
        return f'''
<section class="hero sm"><div class="wrap"><h1>你需要哪方面協助？</h1><p class="lead">找到需要的服務，查看辦理內容與費用。還不確定選哪一項，也可以直接聯絡我們。</p><div class="actions"><a class="btn btn-gold" href="{c}">聯絡我們</a></div></div></section>
<section id="th" class="bg-grey"><div class="wrap"><div class="head"><div><h2>泰國簽證</h2></div></div><div class="cards">{th}</div><div class="strip-note"><p>泰國簽證提供 20 分鐘免費初審。先確認是否符合申請條件，再決定如何辦理。</p><a class="btn btn-line" href="{c}">聯絡我們</a></div></div></section>
<section id="bank"><div class="wrap"><div class="head"><div><h2>銀行開戶</h2></div></div><div class="cards">{card(lang,'bank','泰國銀行開戶協助','協助安排銀行與分行，核對開戶文件。',False,preview,rel)}</div></div></section>
<section id="property" class="bg-grey"><div class="wrap"><div class="head"><div><h2>房產出租與代管</h2></div></div><div class="cards">{card(lang,'bkk','曼谷房產出租與代管','協助處理房產出租與日常管理。',False,preview,rel)}</div></div></section>
<section id="uk"><div class="wrap"><div class="head"><div><h2>英國置業與公司</h2></div></div><div class="cards">{card(lang,'uk','英國置業與公司服務','查看英國置業及公司相關服務。',False,preview,rel)}</div></div></section>
{cta_band(lang, preview, rel, '還有其他需要？', sub='告訴我們想在哪裡辦什麼，我們會回覆是否能提供協助。')}
<section class="tiny"><div class="wrap"><p class="note">辦理條件與費用以各服務詳情及正式報價為準。簽證審批由相關政府部門決定；開戶結果由銀行決定。</p></div></section>'''
    th = ''.join([card(lang, 'dtv', 'DTV visa', 'Check DTV eligibility, required documents and fees.', True, preview, rel), card(lang, 'retire', 'Retirement visas: Non-O and O-A', 'Explore Non-O and O-A application routes and assistance.', True, preview, rel), card(lang, 'ltr', 'LTR long-term resident visa', 'Check LTR eligibility, required documents and application assistance.', True, preview, rel), card(lang, 'elite', 'Thailand Privilege', 'Explore membership options and application assistance.', True, preview, rel), card(lang, 'nonb', 'Non-B business visa', 'Learn about business visa applications and related assistance.', True, preview, rel)])
    return f'''
<section class="hero sm"><div class="wrap"><h1>What can we help you with?</h1><p class="lead">Find the service you need and check what it covers and what it costs. If you are unsure where to start, contact us.</p><div class="actions"><a class="btn btn-gold" href="{c}">Contact us</a></div></div></section>
<section id="th" class="bg-grey"><div class="wrap"><div class="head"><div><h2>Thai visas</h2></div></div><div class="cards">{th}</div><div class="strip-note"><p>A free 20-minute initial assessment is available for Thai visa applications. Check whether you meet the requirements before deciding how to proceed.</p><a class="btn btn-line" href="{c}">Contact us</a></div></div></section>
<section id="bank"><div class="wrap"><div class="head"><div><h2>Bank accounts</h2></div></div><div class="cards">{card(lang,'bank','Thailand bank account opening assistance','Help with bank and branch arrangements and checks of application documents.',False,preview,rel)}</div></div></section>
<section id="property" class="bg-grey"><div class="wrap"><div class="head"><div><h2>Property rental and management</h2></div></div><div class="cards">{card(lang,'bkk','Bangkok property rental and management','Help with letting your property and its day-to-day management.',False,preview,rel)}</div></div></section>
<section id="uk"><div class="wrap"><div class="head"><div><h2>UK property and company services</h2></div></div><div class="cards">{card(lang,'uk','UK property and company services','Explore services for buying property and company matters in the UK.',False,preview,rel)}</div></div></section>
{cta_band(lang, preview, rel, 'Need help with something else?', sub='Tell us what you need to arrange and where. We will let you know whether we can help.')}
<section class="tiny"><div class="wrap"><p class="note">Requirements and fees are set out in the relevant service details and individual quotation, subject to confirmation. Visa decisions are made by the relevant government authorities; account opening decisions are made by the bank.</p></div></section>'''

def p_verify(lang, preview, rel):
    c = link('contact', lang, preview, rel)
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>先把關，再安排。</h1><p class="lead">你有權知道是誰替你辦事。我們先評估在地機構與專業人士，再安排辦理，辦理期間持續跟進。</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>對你的保障</h2></div></div><div class="checks four"><div class="check"><i>1</i><div><b>先看資料，再決定</b><p>安排前，我們先提供對方的資料與資格資訊，供你核對；確認服務內容與費用後，再決定是否委託。</p></div></div><div class="check"><i>2</i><div><b>費用先講清楚</b><p>服務範圍與收費方式在委託前說明清楚。</p></div></div><div class="check"><i>3</i><div><b>我們全程跟進</b><p>辦理期間我們不退場，協助溝通與協調。</p></div></div><div class="check"><i>4</i><div><b>有問題，找我們</b><p>辦理期間如有疑問或爭議，直接聯絡我們，我們協助溝通與處理。</p></div></div></div></div></section>
<section><div class="wrap"><div class="head"><div><h2>在地機構與專業人士怎麼來的</h2></div><p>每一位進入我們安排名單的機構與專業人士，都經過以下四步。</p></div><div class="checks four"><div class="check"><i>1</i><div><b>資格核對</b><p>核對登記資料、專業資格或執業登記（依該行業規定）與負責人身分。</p></div></div><div class="check"><i>2</i><div><b>專業驗證</b><p>了解服務範圍、收費方式、溝通語言與處理經驗。</p></div></div><div class="check"><i>3</i><div><b>口碑推薦</b><p>邀請服務過的客人提供回饋，經我們審核後計入。</p></div></div><div class="check"><i>4</i><div><b>ZDelp 評分</b><p>我們依評估與辦理經驗給每家機構評分，並隨後續案件持續更新，作為是否繼續安排的依據。</p></div></div></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="two"><div><h2>知道由誰辦理。</h2><p class="muted">每項服務都標明由我們的專員，或由在地機構與專業人士辦理。安排前你會先看到對方是誰。</p><h2>隨時找得到我們。</h2><p class="muted">從第一次聯絡到辦理完成，你面對的窗口都是我們。</p></div><div class="seal"><div class="ring">✓</div><b>評估 · 安排 · 跟進</b><p>資格核對 · 專業驗證 · 口碑推薦 · ZDelp 評分</p></div></div></div></section>
{cta_band(lang, preview, rel, '想了解更多？')}'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Checked before it is arranged.</h1><p class="lead">You should know who is doing the work. We assess local firms and professionals first, then arrange the service and follow up while the work is under way.</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>How you are protected</h2></div></div><div class="checks four"><div class="check"><i>1</i><div><b>See who, before you decide</b><p>Before anything is arranged, we give you their details and credentials to check. You confirm the service and fees before deciding whether to engage them.</p></div></div><div class="check"><i>2</i><div><b>Fees explained up front</b><p>The scope of the service and its fees are set out before you engage anyone.</p></div></div><div class="check"><i>3</i><div><b>We follow up</b><p>We stay involved while the work is under way, helping with communication and coordination.</p></div></div><div class="check"><i>4</i><div><b>If something goes wrong, contact us</b><p>If there is a question or a dispute while the work is under way, contact us and we will help sort it out.</p></div></div></div></div></section>
<section><div class="wrap"><div class="head"><div><h2>How local firms and professionals are assessed</h2></div><p>Everyone on our list goes through these four steps.</p></div><div class="checks four"><div class="check"><i>1</i><div><b>Credential checks</b><p>We check registration details, professional qualifications or registration where the industry requires them, and the identity of the person responsible.</p></div></div><div class="check"><i>2</i><div><b>Professional verification</b><p>We discuss their services, fees, communication languages and experience.</p></div></div><div class="check"><i>3</i><div><b>Client recommendations</b><p>We invite clients they have served to share feedback, counted after our review.</p></div></div><div class="check"><i>4</i><div><b>ZDelp score</b><p>We score each firm and professional based on our assessment and how cases are handled, updates the score as work continues, and uses it to decide whether to keep arranging work with them.</p></div></div></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="two"><div><h2>Know who will handle the work.</h2><p class="muted">Each service says whether it is handled by our specialists or by a local firm or professional. You see who they are before anything is arranged.</p><h2>You can always reach us.</h2><p class="muted">From first contact to completion, we are your one point of contact.</p></div><div class="seal"><div class="ring">✓</div><b>Assess · arrange · follow up</b><p>Credential checks · professional verification · client recommendations · ZDelp score</p></div></div></div></section>
{cta_band(lang, preview, rel, 'Want to know more?')}'''

def p_partners(lang, preview, rel):
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>讓專業，遇見合適需求。</h1><p class="lead">你是在地機構或專業人士，提供在地專業；我們負責需求評估、安排與持續跟進。<br>我們先了解彼此如何工作，再開始合作。</p><div class="actions"><a class="btn btn-teal" href="#apply">申請合作</a></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>合作分工</h2></div></div><div class="cards three-text"><article class="card pend"><div class="b"><h3>需求先釐清</h3><p>我們在安排前評估客人需要，讓雙方從清楚的需求開始討論。</p></div></article><article class="card pend"><div class="b"><h3>專業由你提供</h3><p>你說明服務內容、費用與辦理安排，並直接向客人提供專業服務。</p></div></article><article class="card pend"><div class="b"><h3>我們持續跟進</h3><p>安排後，我們繼續協調與跟進。</p></div></article></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>合作條件</h2><div class="pro-list"><div><b>1</b><span>具備服務所在地所需的專業資格或登記（依該行業規定）。</span></div><div><b>2</b><span>負責人資料可核實。</span></div><div><b>3</b><span>能以中文或英文溝通。</span></div><div><b>4</b><span>能事先說明服務範圍及收費方式。</span></div><div><b>5</b><span>接受口碑推薦與 ZDelp 評分。</span></div></div></div><div><h2>加入流程</h2><div class="pro-list"><div><b>1</b><span><strong>提交資料</strong>：提供機構或個人登記資料、專業資格、服務範圍與收費方式。</span></div><div><b>2</b><span><strong>資料核對</strong>：核對資格與登記狀態。</span></div><div><b>3</b><span><strong>專業驗證</strong>：了解服務方式、經驗與溝通安排。</span></div><div><b>4</b><span><strong>口碑推薦</strong>：邀請服務過的客人提供回饋，經審核後計入。</span></div><div><b>5</b><span><strong>確認合作</strong>：通過評估後加入安排名單；之後以口碑推薦與 ZDelp 評分持續檢視。</span></div></div><p class="note">合作條款與費用於審核後說明。</p></div></div></div></section>
<section id="apply" class="bg-grey"><div class="wrap"><div class="head"><div><h2>從認識彼此開始。</h2></div><p>告訴我們你的服務地點、專業範圍，以及機構或個人資料。</p></div>{hs_block(lang, preview, 'zd-partner-form')}</div></section>'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Connect your expertise with the right needs.</h1><p class="lead">You are a local firm or professional and provide the local expertise. We assess client needs, arrange the service and continue to follow up.<br>We start by understanding how we can work together.</p><div class="actions"><a class="btn btn-teal" href="#apply">Apply to partner</a></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>How we work together</h2></div></div><div class="cards three-text"><article class="card pend"><div class="b"><h3>Needs assessed before matching</h3><p>We assess the client's needs before making a match, giving both sides a clear starting point.</p></div></article><article class="card pend"><div class="b"><h3>Professional services provided by you</h3><p>Your firm explains its services, fees and arrangements, and provides the professional service directly to the client.</p></div></article><article class="card pend"><div class="b"><h3>Follow-up from us</h3><p>We continue to coordinate and follow up after the service is arranged.</p></div></article></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>Partnership requirements</h2><div class="pro-list"><div><b>1</b><span>The professional qualifications or registration required where you provide services, as applicable to your industry.</span></div><div><b>2</b><span>Verifiable details for the person responsible.</span></div><div><b>3</b><span>Communication in Chinese or English.</span></div><div><b>4</b><span>A clear explanation of services and fees before engagement.</span></div><div><b>5</b><span>Participation in client recommendations and ZDelp scoring.</span></div></div></div><div><h2>Joining process</h2><div class="pro-list"><div><b>1</b><span><strong>Submit your details:</strong> registration details, professional qualifications, service scope and fee information.</span></div><div><b>2</b><span><strong>Credential checks:</strong> we verify qualifications and registration status.</span></div><div><b>3</b><span><strong>Professional verification:</strong> we discuss your service approach, experience and communication arrangements.</span></div><div><b>4</b><span><strong>Live client recommendations:</strong> we follow how the first cases are handled.</span></div><div><b>5</b><span><strong>Confirm the partnership:</strong> firms and professionals that pass assessment join the list, and are then reviewed on an ongoing basis through client recommendations and the ZDelp score.</span></div></div><p class="note">Partnership terms and fees are explained after review.</p></div></div></div></section>
<section id="apply" class="bg-grey"><div class="wrap"><div class="head"><div><h2>Let's get to know each other.</h2></div><p>Tell us where you work, your areas of expertise and about your firm or practice.</p></div>{hs_block(lang, preview, 'zd-partner-form')}</div></section>'''

def p_about(lang, preview, rel):
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>在地・可靠・同行。</h1><p class="lead">我們是一間在地服務與協助公司。<br>簽證、銀行開戶、房產與公司事務，你可以直接向我們查詢所需服務。</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>服務方式</h2></div></div><p class="muted">各項服務由我們的專員，或由我們評估過的在地機構與專業人士辦理；我們負責評估、安排與跟進，各項服務會標明辦理方式。</p></div></section>
<section><div class="wrap"><div class="head"><div><h2>與宅點的關係</h2></div></div><p class="muted">宅點是海外房產與全球生活的資訊與研究平台，幫讀者看懂政策、比較選項，做好決定前的功課。我們接手的是下一步：讀者決定要辦了，由我們安排合適的專員，或在當地的機構與專業人士，並全程跟進。</p><p class="muted" style="margin-top:12px">你在宅點讀到的研究與查證，就是我們安排服務時的起點，所以不必從頭再解釋一次；讀者在宅點提出的服務需求，也會轉由我們接手。</p><p class="muted" style="margin-top:12px"><b>宅點幫你理解與判斷，我們幫你執行與完成。</b></p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>常見問題</h2></div></div><div class="faq"><details><summary>你們和宅點有什麼不同？</summary><p>宅點提供研究與資訊，幫你看懂、做決定；我們負責接下來的辦理：安排合適的專員或在地機構與專業人士，並跟進到完成。</p></details><details><summary>在宅點看到的服務，是由你們辦理嗎？</summary><p>是。宅點服務頁上的服務查詢，由我們接手安排；每項服務會標明由我們的專員，或由在地機構與專業人士辦理。</p></details><details><summary>你們提供哪些國家的服務？</summary><p>目前涵蓋香港、台灣、泰國、日本、英國、新加坡、馬來西亞、菲律賓，以及更多國家與地區。告訴我們你要辦的事和地點，我們會回覆能否協助。</p></details><details><summary>費用怎麼計算？</summary><p>費用依服務內容與個人情況而定，會在開始前說明清楚，你確認後才開始辦理。</p></details><details><summary>我的資料會怎麼使用？</summary><p>只用於安排你要的服務；需要交給辦理的機構或專業人士時，會先徵得你的同意。</p></details><details><summary>可以用什麼語言溝通？</summary><p>中文與英文都可以；其他語言可以先告訴我們，我們會盡量安排。</p></details><details><summary>辦理過程不順利怎麼辦？</summary><p>直接告訴我們。我們會協助你與辦理的一方溝通與協調；有任何不滿意，也請讓我們知道。</p></details><details><summary>安排之後，還可以找你們嗎？</summary><p>可以。我們會持續跟進，並協助處理服務過程中的溝通與協調。</p></details><details><summary>還不確定需要哪項服務，可以先聯絡嗎？</summary><p>可以。告訴我們想辦什麼，我們會回覆可以提供哪些協助。</p></details></div></div></section>
{cta_band(lang, preview, rel, '需要幫忙，找我們。')}'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Local. Reliable. With you.</h1><p class="lead">We are a company providing local services and assistance.<br>Visas, bank accounts, property and company matters: you can contact us directly about the help you need.</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>How services are provided</h2></div></div><p class="muted">Each service is handled by our specialists or by local firms and professionals we have assessed. We assess your needs, arrange the service and follow up, and each service indicates who handles the work.</p></div></section>
<section><div class="wrap"><div class="head"><div><h2>ZDelp and Zagdim</h2></div></div><p class="muted">Zagdim is a research and information platform on international property and global living. It helps readers understand policies, compare options and prepare before they decide. We take over the next step: once a reader decides to go ahead, we arrange the right specialist, or a local firm or professional, and follow up throughout.</p><p class="muted" style="margin-top:12px">The research you read on Zagdim is where we start when we arrange your service, so you do not need to explain everything again. Service requests that readers leave on Zagdim are passed to us to handle.</p><p class="muted" style="margin-top:12px"><b>Zagdim helps you understand and decide. We help you get it done.</b></p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>Frequently asked questions</h2></div></div><div class="faq"><details><summary>How are you different from Zagdim?</summary><p>Zagdim provides research and information to help you understand and decide. We handle what comes next: arranging the right specialist or local professional, and following up until it is done.</p></details><details><summary>Are the services I see on Zagdim handled by you?</summary><p>Yes. Service enquiries from Zagdim service pages are arranged by us, and each service indicates whether it is handled by our specialists or by local firms and professionals.</p></details><details><summary>Which countries do you cover?</summary><p>We currently cover Hong Kong, Taiwan, Thailand, Japan, the UK, Singapore, Malaysia, the Philippines and beyond. Tell us what you need and where, and we will let you know whether we can help.</p></details><details><summary>How are fees worked out?</summary><p>Fees depend on the service and your situation. We explain them clearly before we start, and work begins only after you confirm.</p></details><details><summary>How is my information used?</summary><p>Only to arrange the service you ask for. If it needs to be shared with the firm or professional handling the work, we ask for your consent first.</p></details><details><summary>Which languages can I use?</summary><p>Chinese and English. If you prefer another language, let us know and we will try to arrange it.</p></details><details><summary>What if something does not go smoothly?</summary><p>Tell us directly. We help you communicate and coordinate with whoever is handling the work, and if you are unhappy with anything, please let us know.</p></details><details><summary>Can I still contact you after the service is arranged?</summary><p>Yes. We continue to follow up and assist with communication and coordination during the service.</p></details><details><summary>Can I get in touch if I am unsure which service I need?</summary><p>Yes. Tell us what you need help with, and we will explain what assistance we can offer.</p></details></div></div></section>
{cta_band(lang, preview, rel, 'Need help? Talk to us.')}'''

ICO_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3z"/></svg>'
ICO_LINE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11.1c0 4 3.6 7.4 8.4 8 .3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.8-3.4 7.9-5.9A7.3 7.3 0 0 0 22 11.1C22 6.6 17.5 3 12 3zM8.2 13.5H6.3a.5.5 0 0 1-.5-.5V9.1a.5.5 0 0 1 1 0v3.4h1.4a.5.5 0 0 1 0 1zm2-.5a.5.5 0 0 1-1 0V9.1a.5.5 0 0 1 1 0zm4.6 0a.5.5 0 0 1-.9.3l-2-2.6V13a.5.5 0 0 1-1 0V9.1a.5.5 0 0 1 .9-.3l2 2.6V9.1a.5.5 0 0 1 1 0zm3.1-2.4a.5.5 0 0 1 0 1h-1.4v.9h1.4a.5.5 0 0 1 0 1h-1.9a.5.5 0 0 1-.5-.5V9.1a.5.5 0 0 1 .5-.5h1.9a.5.5 0 0 1 0 1h-1.4v.9z"/></svg>'
ICO_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3 5.5h18v13H3zM3.5 6l8.5 7 8.5-7"/></svg>'

def contact_buttons(lang):
    zh = lang == 'zh'
    return ('<div class="cbtns"><a class="cbtn wa" href="%s" target="_blank" rel="noopener">%s<span><b>WhatsApp</b><small>%s</small></span></a>'
            '<a class="cbtn line" href="%s" target="_blank" rel="noopener">%s<span><b>LINE</b><small>%s</small></span></a>'
            '<a class="cbtn mail" href="%s">%s<span><b>%s</b><small>%s</small></span></a></div>') % (
            WA, ICO_WA, '傳訊息給我們' if zh else 'Send us a message', LINE, ICO_LINE, '加入官方帳號' if zh else 'Add our official account',
            MAIL, ICO_MAIL, '電郵' if zh else 'Email', MAIL_TXT)

def p_contact(lang, preview, rel):
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>你想辦什麼，告訴我們。</h1><p class="lead">直接傳訊息，或留下聯絡方式與需要協助的事。</p></div></section>
<section class="bg-grey"><div class="wrap"><h2>留下訊息</h2><p class="muted">例如：想申請簽證、需要開戶，或想找人管理房產。也請告訴我們需要在哪裡辦理。</p><div class="contact-grid"><div class="contact-form">{hs_block(lang, preview, 'zd-contact-form')}</div><aside class="contact-side" aria-label="直接聯絡">{contact_buttons(lang)}</aside></div></div></section>'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Tell us what you need help with.</h1><p class="lead">Send us a message, or leave your contact details and a brief description of what you need.</p></div></section>
<section class="bg-grey"><div class="wrap"><h2>Leave a message</h2><p class="muted">For example: a visa application, opening a bank account or finding help to manage a property. Please also tell us where you need the service.</p><div class="contact-grid"><div class="contact-form">{hs_block(lang, preview, 'zd-contact-form')}</div><aside class="contact-side" aria-label="Contact us directly">{contact_buttons(lang)}</aside></div></div></section>'''

BUILDERS = dict(index=p_index, services=p_services, verify=p_verify, partners=p_partners, about=p_about, contact=p_contact)
TITLES = {'zh': dict(index=('ZDelp｜需要幫忙，告訴我們。簽證、銀行開戶、房產與公司事務', '一個窗口，聯通全球在地服務。簽證、銀行開戶、房產與公司事務，由我們的專員或在地機構與專業人士辦理，我們評估、安排與持續跟進。'), services=('ZDelp 服務｜泰國簽證、銀行開戶、房產出租與代管、英國置業與公司', '找到需要的服務，查看辦理內容與費用；不確定也可以直接聯絡我們。'), verify=('ZDelp 信任與保障｜先把關，再安排', '先看資料再決定、費用先講清楚、我們全程跟進、有問題找我們；在地機構與專業人士經資格核對、專業驗證、口碑推薦與 ZDelp 評分。'), partners=('在地機構與專業人士加入我們｜讓專業，遇見合適需求', '你提供在地專業，我們負責需求評估、安排與持續跟進。加入條件、流程與申請。'), about=('關於我們｜在地・可靠・同行', '我們是一間在地服務與協助公司，與宅點互補協作。'), contact=('聯絡我們｜你想辦什麼，告訴我們', 'WhatsApp、LINE、電郵或留言，告訴我們你需要的協助。')),
          'en': dict(index=('ZDelp | Need help? Talk to us. Visas, bank accounts, property and company matters', 'One contact point for local help worldwide. Visas, bank accounts, property and company matters, handled by our specialists or by local firms and professionals we have assessed. We assess, arrange and follow up.'), services=('ZDelp services | Thai visas, bank accounts, property management, UK property and company', 'Find the service you need and check what it covers and what it costs; contact us if unsure.'), verify=('Trust and protection | Checked before it is arranged', 'See who handles the work before you decide, fees explained up front, we follow up, one point of contact if something goes wrong; local firms and professionals go through credential checks, a professional verification, client recommendations and a ZDelp score.'), partners=('Join us as a local firm or professional | Connect your expertise with the right needs', 'You provide local expertise; we assess needs, arrange the service and follow up. Requirements, joining process and application.'), about=('About us | Local. Reliable. With you.', 'ZDelp Limited is a company providing local services and assistance; ZDelp and Zagdim are two independent companies.'), contact=('Contact us | Tell us what you need help with', 'WhatsApp, LINE, email or leave a message about the help you need.'))}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": "https://zdelp.co/#organization", "name": "ZDelp", "legalName": "ZDelp Limited", "url": "https://zdelp.co/", "sameAs": ["https://zagdim.com/zdelp/", "https://www.facebook.com/ZDelpThailifeservice"], "logo": "https://zdelp.co/assets/zdelp.png", "address": {"@type": "PostalAddress", "addressRegion": "Hong Kong", "addressCountry": "HK"}, "slogan": "Local. Reliable. With you."}

def page_html(page, lang, preview, rel):
    t = T[lang]; title, desc = TITLES[lang][page]
    body = BUILDERS[page](lang, preview, rel)
    ld = [ORG] if page in ('index', 'about') else []
    faq = re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', body, re.S)
    if faq: ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": html.unescape(re.sub('<[^>]+>', '', q)), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a))}} for q, a in faq]})
    alt = '' if preview else '<link rel="alternate" hreflang="zh-Hant" href="https://zdelp.co/%s"><link rel="alternate" hreflang="en" href="https://zdelp.co/en/%s">' % (page + '.html' if page != 'index' else '', page + '.html' if page != 'index' else '')
    scripts = (HS_SCRIPT if (not preview and 'class="hs"' in body) else '') + (NET_JS if 'net-stage' in body else '') + ANIM + ''.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><meta name="description" content="%s">%s%s<style>\n%s\n</style></head><body>%s<main>%s</main>%s%s</body></html>' % (
        t['lang'], html.escape(title), html.escape(desc), alt, FONTS, CSS, nav(page, lang, preview, rel), body, footer(lang, preview, rel), scripts)

# ---------------- 名片頁併入（內部預覽，2026-09-22）----------------
# 資料正本在 skill produce-zdelp-provider-profile/examples/；本檔只負責併頁（nav／foot／CSS 共用、logo 改檔案）。
# 2026-10-11 兩層上線條件（skill v1.7）：BP.blockers() 為空＝基本／完整名片頁，以公開版渲染；否則內部預覽（MOCK 條＋虛線）。
# provider-publish-override.json：Fiamma 點名覆寫 blocker 的名單 {slug: {by, date, note}}（Claude 不自行加入）。
# 所有名片頁仍 noindex、不進 sitemap，直到 Fiamma 決定開放索引。
OVERRIDE_F = os.path.join(ROOT, 'provider-publish-override.json')
OVERRIDE = json.load(io.open(OVERRIDE_F, encoding='utf-8')) if os.path.exists(OVERRIDE_F) else {}
def provider_mode(d):
    if not BP.blockers(d): return 'public'
    if d['slug'] in OVERRIDE: return 'override'
    return 'preview'
def p_providers_list():
    groups = {}
    for d in PROVIDERS:
        groups.setdefault(d.get('category') or '其他', []).append(d)
    body = ''
    for cat, items in groups.items():
        cards = ''
        for d in items:
            zs = d.get('zdelp_score') or {}
            score = ('<div class="pv-score"><b>%s</b>%s</div>' % (html.escape(str(zs['score'])), BP.stars(zs['score']))) if zs.get('score') else ''
            cards += ('<a class="pv-card" href="providers/%s.html"><div class="pv-logo"><img src="assets/providers/%s.png" alt="%s 標誌"></div>'
                      '<div class="pv-b"><b>%s</b><span>%s</span>%s</div></a>') % (
                      d['slug'], d['slug'], html.escape(d['name']), html.escape(d['name']),
                      html.escape('・'.join(x for x in [d.get('country'), d.get('city')] if x)), score)
        body += '<div class="pv-group"><h2>%s</h2><div class="pv-grid">%s</div></div>' % (html.escape(cat), cards)
    note = '內部預覽：以下為已建檔的在地機構與專業人士。名片頁上線條件＝身分與資格核對通過＋同意加入協議與具名上頁；同一服務類別滿 3 家才會開放該類別名單。'
    return ('<section class="hero sm"><div class="wrap"><h1>在地機構與專業人士</h1>'
            '<p class="lead">我們評估過的在地機構與專業人士，安排前你會先看到是誰。</p></div></section>'
            '<section class="bg-grey"><div class="wrap"><div class="pv-note">%s</div>%s</div></section>') % (note, body)

def _provider_wrap(body, title, desc):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><meta name="robots" content="noindex">%s<style>\n%s%s\n</style></head><body>%s<main>%s</main>%s%s</body></html>') % (
            html.escape(title), html.escape(desc), FONTS, CSS, BP.EXTRA, nav('providers', 'zh', False, ''), body, footer('zh', False, ''), ANIM)

def providers_list_html():
    return _provider_wrap(p_providers_list(), 'ZDelp 在地機構與專業人士名單（內部預覽）', '已建檔在地機構與專業人士，尚未公開，等待 Fiamma 核可上線條件。')

def provider_page_html(d):
    mode = provider_mode(d); clean = mode in ('public', 'override')
    body = BP.build(d, embed=True, rel='../', public=(mode == 'public'), sample=(mode == 'override'))
    title = '%s｜ZDelp 在地機構與專業人士' % d['name'] if clean else '%s 名片頁｜ZDelp（內部預覽）' % d['name']
    desc = ('%s・%s・%s' if clean else '%s・%s・%s（尚未公開，內部預覽）') % (d['name'], d.get('category') or '', d.get('country') or '')
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><meta name="robots" content="noindex">%s<style>\n%s%s\n</style></head><body>%s<main>%s</main>%s%s</body></html>') % (
            html.escape(title), html.escape(desc),
            FONTS, CSS, BP.EXTRA, nav('providers', 'zh', False, '../', page_prefix='../'), body, footer('zh', False, '../', page_prefix='../'), ANIM)

def preview_site():
    parts = []
    for lang in ('zh', 'en'):
        for page in PAGES:
            t = T[lang]; body = BUILDERS[page](lang, True, '')
            parts.append('<div class="pg" id="%s-%s" lang="%s">%s<main>%s</main>%s</div>' % (lang, page, t['lang'], nav(page, lang, True, ''), body, footer(lang, True, '')))
    router = """<script>function show(){var h=(location.hash||'#zh-index').slice(1);var ok=false;document.querySelectorAll('.pg').forEach(function(p){var on=p.id===h;p.style.display=on?'block':'none';if(on)ok=true;});if(!ok){document.getElementById('zh-index').style.display='block';}window.scrollTo(0,0);document.querySelectorAll('section .wrap>*').forEach(function(el){el.classList.add('in')});}window.addEventListener('hashchange',show);show();</script>"""
    return '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>zdelp.co 全站預覽 v3（zh／en）</title><meta name="description" content="zdelp.co 六頁雙語預覽 v2（Codex 文案）：導覽列切頁、右上 EN／中文切換。">%s<style>\n%s\n.pg{display:none}.mockbar{background:#EEBF01;color:#10374e;font-size:13px;font-weight:700;text-align:center;padding:6px}\n</style></head><body><div class="mockbar">zdelp.co 全站預覽 v3 · 導覽列切頁 · 右上 EN／中文切換 · 圖片暫用</div>%s%s</body></html>' % (FONTS, CSS, ''.join(parts), NET_JS + router)

def abs_links(h):
    h = h.replace('href="index.html"', 'href="/"').replace('href="en/index.html"', 'href="/en/"')
    return re.sub(r'href="(%s)\.html"' % '|'.join(PAGES[1:]), r'href="/\1.html"', h)

def gate_text(h):
    t = re.sub(r'<style>.*?</style>', '', h, flags=re.S); t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'</(p|h1|h2|h3|li|tr|td|summary|div|section|header|article|a|span|footer|b|em|small|strong)>', '\n', t); t = re.sub(r'<[^>]+>', '', t); t = html.unescape(t)
    return re.sub(r'\n\s*\n+', '\n', t).strip()

if __name__ == '__main__':
    D = os.path.join(ROOT, 'dist'); shutil.rmtree(D, ignore_errors=True); os.makedirs(os.path.join(D, 'en')); shutil.copytree(A, os.path.join(D, 'assets'))
    os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
    for page in PAGES:
        io.open(os.path.join(D, page + '.html'), 'w', encoding='utf-8').write(page_html(page, 'zh', False, ''))
        io.open(os.path.join(D, 'en', page + '.html'), 'w', encoding='utf-8').write(page_html(page, 'en', False, '../'))
    io.open(os.path.join(ROOT, 'preview', 'site.html'), 'w', encoding='utf-8').write(preview_site())
    # 名片頁（內部預覽，未過 --public 前 noindex；不進 sitemap）
    os.makedirs(os.path.join(D, 'providers'), exist_ok=True)
    os.makedirs(os.path.join(D, 'assets', 'providers'), exist_ok=True)
    for d in PROVIDERS:
        shutil.copy(os.path.expanduser(d['logo']), os.path.join(D, 'assets', 'providers', d['slug'] + '.png'))
        for p in (d.get('people') or []):  # 人員照片：只複製有照片且已同意的（與公開版渲染條件一致）
            if p.get('photo') and (p.get('consent') or provider_mode(d) == 'preview'):
                os.makedirs(os.path.join(D, 'assets', 'providers', 'people'), exist_ok=True)
                shutil.copy(os.path.expanduser(p['photo']), os.path.join(D, 'assets', 'providers', 'people', os.path.basename(p['photo'])))
        io.open(os.path.join(D, 'providers', d['slug'] + '.html'), 'w', encoding='utf-8').write(provider_page_html(d))
        print('  provider %-16s %s' % (d['slug'], provider_mode(d)))
    io.open(os.path.join(D, 'providers.html'), 'w', encoding='utf-8').write(providers_list_html())
    for lang in ('zh', 'en'):
        for p in PAGES:
            io.open(os.path.join(ROOT, 'preview', 'gate-%s-%s.md' % (lang, p)), 'w', encoding='utf-8').write(gate_text(page_html(p, lang, False, '')))
    # 部署附檔（每次建置重生）
    import datetime; today = datetime.date.today().isoformat()
    io.open(os.path.join(D, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://zdelp.co/sitemap.xml\n')
    urls = ['https://zdelp.co/'] + ['https://zdelp.co/%s.html' % p for p in PAGES[1:]] + ['https://zdelp.co/en/'] + ['https://zdelp.co/en/%s.html' % p for p in PAGES[1:]]
    io.open(os.path.join(D, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, today) for u in urls) + '</urlset>\n')
    io.open(os.path.join(D, 'CNAME'), 'w').write('zdelp.co\n'); io.open(os.path.join(D, '.nojekyll'), 'w').write('')
    nf = '<section class="hero sm"><div class="wrap"><h1>找不到這個頁面。</h1><p class="lead">網址可能已更改。請回到首頁，或直接聯絡我們。</p><div class="actions"><a class="btn btn-gold" href="/">回首頁</a><a class="btn btn-ghost" href="/contact.html">聯絡我們</a></div></div></section>'
    io.open(os.path.join(D, '404.html'), 'w', encoding='utf-8').write('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>找不到頁面｜ZDelp</title><meta name="robots" content="noindex">%s<style>\n%s\n</style></head><body>%s<main>%s</main>%s</body></html>' % (FONTS, CSS, abs_links(nav('index', 'zh', False, '/')), nf, abs_links(footer('zh', False, '/'))))
    print('built dist/ (zh+en) + preview/site.html + robots/sitemap/CNAME/404')
