# -*- coding: utf-8 -*-
"""zdelp.co 全站建置 v3（2026-09-21：v2 Codex 文案＋v3 設計「一個窗口，聯通全球」；zh/en 雙語可切換；手機選單）。
輸出：dist/{index,services,verify,partners,about,contact}.html ＋ dist/en/…（相對 assets）；
preview/site.html（單檔、data-URI、hash 切頁，給 Artifact）；preview/gate-<lang>-<page>.md。"""
import io, os, re, base64, json, html, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets')
LOGO_ALT = 'ZDelp'
CSS = io.open(os.path.join(ROOT, 'src', 'zdelp.css'), encoding='utf-8').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">'
ZAG = 'https://zagdim.com'
PAGES = ['index', 'services', 'verify', 'partners', 'about', 'contact']
HS_FORM = 'b67da755-3d8e-40ad-9010-2639a97704a1'
HS_PARTNER_FORM = '4db3d945-014f-4a96-879c-235381578c96'
WA = 'https://wa.me/message/K7CHUBLJY4ONN1'; LINE = 'https://line.me/R/ti/p/@257ziphh'; MAIL = 'mailto:info@zagdim.com'

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
 'zh': dict(lang='zh-Hant', nav=['首頁', '服務', '核驗制度', '機構合作', '關於 ZDelp', '聯絡'], cta='聯絡 ZDelp', sw='EN', tag='LOCAL ASSISTANCE', brand='在地・可靠・同行',
   own='ZDelp 專員辦理', ver='核驗機構提供', more='查看詳情與費用', ext='詳情刊於宅點',
   foot_note='泰國簽證由 ZDelp 專員直接辦理。其他服務由經 ZDelp 核驗的可靠持牌機構提供，ZDelp 負責評估、配對與跟進；協作服務費用由客人與機構直接結算，ZDelp 不代收代付。',
   legal='本站內容僅供一般參考，不構成稅務、法律或投資建議。辦理條件與費用以各服務詳情及實際報價為準；簽證審批由相關政府部門決定，開戶結果由銀行決定，ZDelp 不保證任何申請必然通過。'),
 'en': dict(lang='en', nav=['Home', 'Services', 'Our Vetting Process', 'Partner With Us', 'About ZDelp', 'Contact'], cta='Contact ZDelp', sw='中文', tag='LOCAL ASSISTANCE', brand='Local. Reliable. With you.',
   own='Handled by ZDelp', ver='Provided by a vetted firm', more='View details and fees', ext='Details in Chinese on Zagdim',
   foot_note='Thai visa applications are handled directly by ZDelp specialists. Other services are provided by reliable, licensed firms vetted by ZDelp. ZDelp assesses your needs, matches you with a firm and follows up. For services provided by a partner firm, you pay the firm directly; ZDelp does not collect or make payments on your behalf.',
   legal='Content on this site is general information only and does not constitute tax, legal or investment advice. Requirements and fees are set out in the relevant service details and individual quotation, and are subject to confirmation by ZDelp or the firm; visa decisions are made by the relevant government authorities and account opening decisions by the bank. ZDelp does not guarantee any outcome.'),
}

def img(f, alt, cls='', preview=False, eager=False, rel=''):
    src = du(f) if preview else rel + 'assets/' + f
    lazy = '' if eager else ' loading="lazy" decoding="async"'
    return '<img src="%s" alt="%s"%s%s>' % (src, html.escape(alt), (' class="%s"' % cls) if cls else '', lazy)

def link(page, lang, preview, rel, anchor=''):
    if preview: return '#%s-%s' % (lang, page)
    return page + '.html' + anchor

def nav(active, lang, preview, rel):
    t = T[lang]
    items = ''.join('<a%s href="%s">%s</a>' % (' class="on"' if p == active else '', link(p, lang, preview, rel), n) for p, n in zip(PAGES, t['nav']))
    other = 'en' if lang == 'zh' else 'zh'
    sw = ('#%s-%s' % (other, active)) if preview else (('en/' if other == 'en' else '../') + active + '.html')
    logo = img('zdelp.png', 'ZDelp', 'nav-logo', preview, True, rel)
    menu_label = '選單' if lang == 'zh' else 'Menu'
    return ('<header class="nav"><div class="wrap"><a class="logo" href="%s">%s<span>ZDelp<small>%s</small></span></a><nav class="links" id="zd-links">%s</nav>'
            '<button class="burger" type="button" aria-label="%s" aria-expanded="false" aria-controls="zd-links" onclick="var l=this.parentNode.querySelector(\'.links\');var o=l.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)"><span></span></button>'
            '<a class="lang" href="%s" hreflang="%s">%s</a><a class="btn btn-gold nav-cta" href="%s">%s</a></div></header>') % (
            link('index', lang, preview, rel), logo, t['tag'], items, menu_label, sw, 'en' if other == 'en' else 'zh-Hant', t['sw'], link('contact', lang, preview, rel), t['cta'])

def footer(lang, preview, rel):
    t = T[lang]
    links = ''.join('<a href="%s">%s</a>' % (link(p, lang, preview, rel), n) for p, n in zip(PAGES[1:], t['nav'][1:]))
    return ('<footer><div class="wrap"><div class="foot"><div><b>ZDelp Limited</b><p>%s<br>%s</p></div><div><b>%s</b><p class="foot-links">%s</p></div>'
            '<div><b>%s</b><p><a href="%s" target="_blank" rel="noopener">WhatsApp</a> · <a href="%s" target="_blank" rel="noopener">LINE</a> · <a href="%s">info@zagdim.com</a></p></div></div>'
            '<p class="legal">%s</p><p class="legal">%s</p></div></footer>') % (
            '香港註冊' if lang == 'zh' else 'Registered in Hong Kong', t['brand'], '網站' if lang == 'zh' else 'Site', links, '聯絡' if lang == 'zh' else 'Contact', WA, LINE, MAIL, t['foot_note'], t['legal'])

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
    return '<div id="%s" class="hs"></div><noscript>%s</noscript>' % (target, 'JavaScript 未啟用，請以 WhatsApp、LINE 或電郵聯絡 ZDelp。' if lang == 'zh' else 'JavaScript is disabled; contact ZDelp through WhatsApp, LINE or email.')

HS_SCRIPT = """<script>(function(){var t=document.querySelector('.hs');if(!t)return;var fid=t.id==='zd-partner-form'?'%s':'%s';function mount(){if(window.hbspt&&!t.querySelector('iframe'))window.hbspt.forms.create({region:'na1',portalId:'5650486',formId:fid,target:'#'+t.id});}if(window.hbspt){mount();}else{var s=document.createElement('script');s.src='https://js.hsforms.net/forms/embed/v2.js';s.onload=mount;document.head.appendChild(s);}})();</script>""" % (HS_PARTNER_FORM, HS_FORM)
ANIM = """<script>(function(){if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.documentElement.classList.add('anim');var els=[].slice.call(document.querySelectorAll('section .wrap>*'));var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.06});els.forEach(function(el){io.observe(el)});setTimeout(function(){els.forEach(function(el){el.classList.add('in')})},4000)})();</script>"""

def cta_band(lang, preview, rel, headline, btn=None, sub=None):
    t = T[lang]
    return '<section class="cta-band"><div class="wrap"><div><p>%s</p>%s</div><a class="btn btn-gold" href="%s">%s</a></div></section>' % (headline, ('<small>%s</small>' % sub) if sub else '', link('contact', lang, preview, rel), btn or t['cta'])

def split_cards(lang):
    if lang == 'zh':
        return ('<div class="split"><div class="split-card own"><span class="badge own"><i>●</i>ZDelp 專員</span><h3>直接辦理泰國簽證。</h3></div>'
                '<div class="split-card ver"><span class="badge ver"><i>✓</i>核驗機構</span><h3>提供銀行開戶、房產與公司等專業服務。</h3></div></div>'
                '<p class="split-note">辦理期間，ZDelp 持續跟進。</p>')
    return ('<div class="split"><div class="split-card own"><span class="badge own"><i>●</i>ZDelp specialists</span><h3>Handle Thai visa applications directly.</h3></div>'
            '<div class="split-card ver"><span class="badge ver"><i>✓</i>Vetted firms</span><h3>Provide professional help with bank accounts, property, company matters and other services.</h3></div></div>'
            '<p class="split-note">ZDelp continues to follow up while the work is under way.</p>')

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
<h1>需要幫忙，<br>找 <em>ZDelp</em>。</h1>
<p class="lead">簽證、銀行開戶、房產與公司事務。<br>你想辦什麼，告訴 ZDelp。</p>
<div class="actions"><a class="btn btn-gold btn-xl" href="{link('contact',lang,preview,rel)}">聯絡 ZDelp</a><a class="btn btn-ghost btn-xl" href="{svc}">查看服務</a></div>
<div class="trust"><span><i>✓</i>香港註冊公司</span><span><i>✓</i>一個窗口，聯通全球</span><span><i>✓</i>辦理期間持續跟進</span></div>
</div><div class="hero-art">{img('hero-people.jpg','ZDelp 專員與客人一起核對申請文件，背景是曼谷市景。','',preview,True,rel)}<div class="hero-cap"><i>●</i><div><b>LOCAL ASSISTANCE</b>在地辦理，持續跟進</div></div></div></div></div></section>
<section class="bg-grey" id="svc"><div class="wrap"><div class="head"><div><p class="kick">服務</p><h2>你需要哪方面協助？</h2></div><p>先說你要辦什麼、在哪裡。每項服務都標示由誰辦理。</p></div><div class="cards four">{cards}</div></div></section>
<section><div class="wrap"><div class="head"><div><p class="kick">怎麼運作</p><h2>一個窗口，<br>聯通全球。</h2></div><p>你不用自己在海外找人、比人、試人。ZDelp 協助安排合適服務，辦理期間持續跟進。</p></div>
<div class="flow"><div class="fl"><i>1</i><b>你說需求</b><p>要辦什麼、在哪個地區。</p></div><div class="fl"><i>2</i><b>ZDelp 評估</b><p>判斷能不能幫、該怎麼安排。</p></div><div class="fl"><i>3</i><b>安排辦理</b><p>由 ZDelp 專員或通過核驗的持牌機構辦理，先給你資料再決定。</p></div><div class="fl"><i>4</i><b>持續跟進</b><p>辦理期間 ZDelp 不退場，協助溝通與協調。</p></div></div>
<p class="split-note">協作服務費用由你與機構直接結算，ZDelp 不代收代付。<a href="{ver}">了解核驗制度</a></p></div></section>
<section class="bg-grey"><div class="wrap"><div class="ground"><figure class="ground-photo">{img('photo-imm.jpg','曼谷移民局入口，辦理當天的排隊人潮。','',preview,False,rel)}<figcaption><b>BANGKOK · IMMIGRATION BUREAU</b>曼谷移民局，辦理當天</figcaption></figure>
<div class="ground-text"><p class="kick">在現場</p><h2>在地辦理，<br>持續跟進。</h2><p>辦事的人在當地持牌、親自到場；跟進的是 ZDelp，隨時找得到。</p><p class="split-note"><a href="{link('contact',lang,preview,rel)}">聯絡 ZDelp</a></p></div></div></div></section>
<section class="bg-navy" id="verify"><div class="wrap"><div class="head"><div><p class="kick">核驗制度</p><h2>先核驗，再合作。</h2></div><p>你有權知道是誰在替你辦事。每一家進入網絡的機構，ZDelp 都核對資料、訪談、觀察試單，合作後年度重審。</p></div>
<div class="steps"><div class="step"><i>01</i><b>執照與登記</b><p>核對機構登記、相關執照與負責人資料。</p></div><div class="step"><i>02</i><b>視訊訪談</b><p>了解服務範圍、收費方式、溝通語言與處理經驗。</p></div><div class="step"><i>03</i><b>試單評估</b><p>觀察實際服務中的回覆、溝通與辦理情況。</p></div><div class="step"><i>04</i><b>年度重審</b><p>重新核對執照狀態、客人回饋與爭議紀錄。</p></div></div>
<div class="seal-line"><div class="ring">✓</div><div><b>徽章不能付費取得。</b><p>機構通過 ZDelp 核驗後，才會取得核驗徽章。徽章表示機構通過核驗，不代表每項申請或服務必然取得預期結果。</p></div></div>
<p class="note"><a href="{ver}" style="color:var(--gold)">查看完整核驗制度</a></p></div></section>
{cta_band(lang, preview, rel, '有事要辦，隨時告訴我們。', sub='留下你想辦的事和所在地區，我們會告訴你能不能幫上忙。')}'''
    cards = (card(lang, 'dtv', 'Thai visas', 'Explore visa services for living, working or retiring in Thailand.', True, preview, rel, url=svc + ('' if preview else '#th'), btn='Explore visa services', external=False)
             + card(lang, 'bank', 'Bank accounts', 'Find help with opening an account and preparing your documents.', False, preview, rel)
             + card(lang, 'bkk', 'Property rental and management', 'Find help with letting your property and its day-to-day management.', False, preview, rel)
             + card(lang, 'uk', 'UK property and company services', 'Explore services for buying property and company matters in the UK.', False, preview, rel))
    return f'''
<section class="hero"><div class="wrap"><div class="hero-grid"><div>
<p class="kick">{t['brand']}</p>
<h1>Need help?<br>Talk to <em>ZDelp</em>.</h1>
<p class="lead">Visas, bank accounts, property and company matters.<br>Tell us what you need help with.</p>
<div class="actions"><a class="btn btn-gold btn-xl" href="{link('contact',lang,preview,rel)}">Contact ZDelp</a><a class="btn btn-ghost btn-xl" href="{svc}">Explore services</a></div>
<div class="trust"><span><i>✓</i>Registered in Hong Kong</span><span><i>✓</i>One contact point, local help worldwide</span><span><i>✓</i>Follow-up while the work is under way</span></div>
</div><div class="hero-art">{img('hero-people.jpg','A ZDelp specialist and a client checking application documents, with the Bangkok skyline behind them.','',preview,True,rel)}<div class="hero-cap"><i>●</i><div><b>LOCAL ASSISTANCE</b>Handled locally, followed up by ZDelp</div></div></div></div></div></section>
<section class="bg-grey" id="svc"><div class="wrap"><div class="head"><div><p class="kick">Services</p><h2>What can we help you with?</h2></div><p>Tell us what you need and where. Each service shows who handles the work.</p></div><div class="cards four">{cards}</div></div></section>
<section><div class="wrap"><div class="head"><div><p class="kick">How it works</p><h2>One contact point,<br>local help worldwide.</h2></div><p>You do not have to find, compare and test people overseas yourself. ZDelp arranges the right service and follows up while the work is under way.</p></div>
<div class="flow"><div class="fl"><i>1</i><b>Tell us what you need</b><p>What you want to arrange, and where.</p></div><div class="fl"><i>2</i><b>ZDelp assesses</b><p>We tell you whether we can help and how it would be arranged.</p></div><div class="fl"><i>3</i><b>The work is arranged</b><p>Handled by ZDelp specialists or a vetted, licensed firm. You see the details before you decide.</p></div><div class="fl"><i>4</i><b>Follow-up</b><p>ZDelp stays involved, helping with communication and coordination.</p></div></div>
<p class="split-note">For services provided by a partner firm, you pay the firm directly; ZDelp does not collect or make payments on your behalf.<a href="{ver}">About our vetting process</a></p></div></section>
<section class="bg-grey"><div class="wrap"><div class="ground"><figure class="ground-photo">{img('photo-imm.jpg','The entrance of the Bangkok Immigration Bureau on an application day.','',preview,False,rel)}<figcaption><b>BANGKOK · IMMIGRATION BUREAU</b>Bangkok Immigration Bureau, application day</figcaption></figure>
<div class="ground-text"><p class="kick">On the ground</p><h2>Handled locally,<br>followed up by ZDelp.</h2><p>The work is done by licensed people who are actually there. The follow-up comes from ZDelp, and you can always reach us.</p><p class="split-note"><a href="{link('contact',lang,preview,rel)}">Contact ZDelp</a></p></div></div></div></section>
<section class="bg-navy" id="verify"><div class="wrap"><div class="head"><div><p class="kick">Our vetting process</p><h2>Vetted before we work together.</h2></div><p>You should know who is providing your service. Every firm in the network is checked, interviewed and observed on trial cases, with annual reviews after a partnership begins.</p></div>
<div class="steps"><div class="step"><i>01</i><b>Licences and registration</b><p>We check the firm's registration, relevant licences and the details of the person responsible.</p></div><div class="step"><i>02</i><b>Video interview</b><p>We discuss the firm's services, fees, communication languages and experience.</p></div><div class="step"><i>03</i><b>Trial cases</b><p>We observe responses, communication and how the work is handled in practice.</p></div><div class="step"><i>04</i><b>Annual review</b><p>We review licence status, client feedback and dispute records.</p></div></div>
<div class="seal-line"><div class="ring">✓</div><div><b>Our badge cannot be bought.</b><p>A firm receives a verification badge only after passing ZDelp's vetting process. The badge indicates that the firm has passed those checks; it does not promise a particular outcome for every application or service.</p></div></div>
<p class="note"><a href="{ver}" style="color:var(--gold)">See the full vetting process</a></p></div></section>
{cta_band(lang, preview, rel, 'Need a hand? Get in touch.', sub='Tell us what you need to arrange and where. We will let you know whether we can help.')}'''

def p_services(lang, preview, rel):
    t = T[lang]; c = link('contact', lang, preview, rel)
    if lang == 'zh':
        th = ''.join([card(lang, 'dtv', 'DTV 簽證', '查看 DTV 申請條件、文件與費用。', True, preview, rel), card(lang, 'retire', '退休簽證 Non-O／O-A', '查看 Non-O、O-A 申請方式與辦理服務。', True, preview, rel), card(lang, 'ltr', 'LTR 長期居留簽證', '查看 LTR 申請資格、文件與辦理服務。', True, preview, rel), card(lang, 'elite', 'Thailand Privilege 菁英簽證', '了解會籍方案與申請服務。', True, preview, rel), card(lang, 'nonb', 'Non-B 商務簽證', '了解商務簽證與相關申請服務。', True, preview, rel)])
        return f'''
<section class="hero sm"><div class="wrap"><h1>你需要哪方面協助？</h1><p class="lead">找到需要的服務，查看辦理內容與費用。還不確定選哪一項，也可以直接聯絡 ZDelp。</p><div class="actions"><a class="btn btn-gold" href="{c}">聯絡 ZDelp</a></div></div></section>
<section id="th" class="bg-grey"><div class="wrap"><div class="head"><div><h2>泰國簽證</h2></div></div><div class="cards">{th}</div><div class="strip-note"><p>泰國簽證提供 20 分鐘免費初審。先確認是否符合申請條件，再決定如何辦理。</p><a class="btn btn-line" href="{c}">聯絡 ZDelp</a></div></div></section>
<section id="bank"><div class="wrap"><div class="head"><div><h2>銀行開戶</h2></div></div><div class="cards">{card(lang,'bank','泰國銀行開戶協助','協助安排銀行與分行，核對開戶文件。',False,preview,rel)}</div></div></section>
<section id="property" class="bg-grey"><div class="wrap"><div class="head"><div><h2>房產出租與代管</h2></div></div><div class="cards">{card(lang,'bkk','曼谷房產出租與代管','協助處理房產出租與日常管理。',False,preview,rel)}</div></div></section>
<section id="uk"><div class="wrap"><div class="head"><div><h2>英國置業與公司</h2></div></div><div class="cards">{card(lang,'uk','英國置業與公司服務','查看英國置業及公司相關服務。',False,preview,rel)}</div></div></section>
{cta_band(lang, preview, rel, '還有其他需要？', sub='告訴我們想在哪裡辦什麼，我們會回覆是否能提供協助。')}
<section class="tiny"><div class="wrap"><p class="note">辦理條件與費用以各服務詳情及實際報價為準。簽證審批由相關政府部門決定；開戶結果由銀行決定。</p></div></section>'''
    th = ''.join([card(lang, 'dtv', 'DTV visa', 'Check DTV eligibility, required documents and fees.', True, preview, rel), card(lang, 'retire', 'Retirement visas: Non-O and O-A', 'Explore Non-O and O-A application routes and assistance.', True, preview, rel), card(lang, 'ltr', 'LTR long-term resident visa', 'Check LTR eligibility, required documents and application assistance.', True, preview, rel), card(lang, 'elite', 'Thailand Privilege', 'Explore membership options and application assistance.', True, preview, rel), card(lang, 'nonb', 'Non-B business visa', 'Learn about business visa applications and related assistance.', True, preview, rel)])
    return f'''
<section class="hero sm"><div class="wrap"><h1>What can we help you with?</h1><p class="lead">Find the service you need and check what it covers and what it costs. If you are unsure where to start, contact ZDelp.</p><div class="actions"><a class="btn btn-gold" href="{c}">Contact ZDelp</a></div></div></section>
<section id="th" class="bg-grey"><div class="wrap"><div class="head"><div><h2>Thai visas</h2></div></div><div class="cards">{th}</div><div class="strip-note"><p>A free 20-minute initial assessment is available for Thai visa applications. Check whether you meet the requirements before deciding how to proceed.</p><a class="btn btn-line" href="{c}">Contact ZDelp</a></div></div></section>
<section id="bank"><div class="wrap"><div class="head"><div><h2>Bank accounts</h2></div></div><div class="cards">{card(lang,'bank','Thailand bank account opening assistance','Help with bank and branch arrangements and checks of application documents.',False,preview,rel)}</div></div></section>
<section id="property" class="bg-grey"><div class="wrap"><div class="head"><div><h2>Property rental and management</h2></div></div><div class="cards">{card(lang,'bkk','Bangkok property rental and management','Help with letting your property and its day-to-day management.',False,preview,rel)}</div></div></section>
<section id="uk"><div class="wrap"><div class="head"><div><h2>UK property and company services</h2></div></div><div class="cards">{card(lang,'uk','UK property and company services','Explore services for buying property and company matters in the UK.',False,preview,rel)}</div></div></section>
{cta_band(lang, preview, rel, 'Need help with something else?', sub='Tell us what you need to arrange and where. We will let you know whether we can help.')}
<section class="tiny"><div class="wrap"><p class="note">Requirements and fees are set out in the relevant service details and individual quotation, subject to confirmation. Visa decisions are made by the relevant government authorities; account opening decisions are made by the bank.</p></div></section>'''

def p_verify(lang, preview, rel):
    c = link('contact', lang, preview, rel); pt = link('partners', lang, preview, rel)
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>先核驗，再合作。</h1><p class="lead">服務由誰提供，應該清楚可查。ZDelp 透過資料核對、訪談與試單了解機構，合作後持續年度重審。</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>核驗內容</h2></div></div><div class="checks four"><div class="check"><i>1</i><div><b>執照與登記</b><p>核對機構登記、相關執照與負責人資料。</p></div></div><div class="check"><i>2</i><div><b>視訊訪談</b><p>了解服務範圍、收費方式、溝通語言與處理經驗。</p></div></div><div class="check"><i>3</i><div><b>試單評估</b><p>觀察實際服務中的回覆、溝通與辦理情況。</p></div></div><div class="check"><i>4</i><div><b>年度重審</b><p>重新核對執照狀態、客人回饋與爭議紀錄，評估是否持續合作。</p></div></div></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>徽章不能付費取得。</h2><p class="muted">機構通過 ZDelp 核驗後，才會取得核驗徽章。徽章表示機構通過核驗，不代表每項申請或服務必然取得預期結果。</p><h2>知道由誰辦理。</h2><p class="muted">ZDelp 會在配對前提供機構資料與相關執照資訊，供你核對。服務內容與費用確認清楚後，再決定是否委託。</p></div><div class="seal"><div class="ring">✓</div><b>核驗機構提供</b><p>執照與登記 · 視訊訪談 · 試單評估 · 年度重審</p></div></div></div></section>
{cta_band(lang, preview, rel, '想了解更多？')}
<section class="tiny"><div class="wrap"><p class="note"><a href="{pt}">服務機構合作</a></p></div></section>'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Vetted before we work together.</h1><p class="lead">You should know who is providing your service. ZDelp checks credentials, conducts interviews and assesses trial cases to understand each firm, with annual reviews after a partnership begins.</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>What we review</h2></div></div><div class="checks four"><div class="check"><i>1</i><div><b>Licences and registration</b><p>We check the firm's registration, relevant licences and the details of the person responsible.</p></div></div><div class="check"><i>2</i><div><b>Video interview</b><p>We discuss the firm's services, fees, communication languages and experience.</p></div></div><div class="check"><i>3</i><div><b>Trial cases</b><p>We observe responses, communication and how the work is handled in practice.</p></div></div><div class="check"><i>4</i><div><b>Annual review</b><p>We review licence status, client feedback and dispute records to assess whether to continue the partnership.</p></div></div></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>Our badge cannot be bought.</h2><p class="muted">A firm receives a verification badge only after passing ZDelp's vetting process. The badge indicates that the firm has passed those checks; it does not promise a particular outcome for every application or service.</p><h2>Know who will handle the work.</h2><p class="muted">Before making a match, ZDelp provides the firm's details and relevant licence information for you to check. You can then confirm the service and fees before deciding whether to engage the firm.</p></div><div class="seal"><div class="ring">✓</div><b>Provided by a vetted firm</b><p>Licences · interview · trial cases · annual review</p></div></div></div></section>
{cta_band(lang, preview, rel, 'Want to know more?')}
<section class="tiny"><div class="wrap"><p class="note"><a href="{pt}">Partner with ZDelp</a></p></div></section>'''

def p_partners(lang, preview, rel):
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>讓專業，遇見合適需求。</h1><p class="lead">你提供在地專業，ZDelp 負責需求評估、配對與持續跟進。<br>我們先了解彼此如何工作，再開始合作。</p><div class="actions"><a class="btn btn-teal" href="#apply">申請合作</a></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>合作分工</h2></div></div><div class="cards three-text"><article class="card pend"><div class="b"><h3>需求先釐清</h3><p>ZDelp 在配對前評估客人需要，讓雙方從清楚的需求開始討論。</p></div></article><article class="card pend"><div class="b"><h3>專業由你提供</h3><p>你說明服務內容、費用與辦理安排，並直接向客人提供專業服務。</p></div></article><article class="card pend"><div class="b"><h3>ZDelp 持續跟進</h3><p>配對後，ZDelp 繼續協調與跟進。協作服務費用由客人與機構直接結算。</p></div></article></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>合作條件</h2><div class="pro-list"><div><b>1</b><span>具備服務所在地的有效執照與機構登記。</span></div><div><b>2</b><span>負責人資料可核實。</span></div><div><b>3</b><span>能以中文或英文溝通。</span></div><div><b>4</b><span>能事先說明服務範圍及收費方式。</span></div><div><b>5</b><span>接受試單與年度重審。</span></div></div></div><div><h2>加入流程</h2><div class="pro-list"><div><b>1</b><span><strong>提交資料</strong>：提供機構登記、執照、服務範圍與收費方式。</span></div><div><b>2</b><span><strong>資料核驗</strong>：核對執照與登記狀態。</span></div><div><b>3</b><span><strong>視訊訪談</strong>：了解服務方式、經驗與溝通安排。</span></div><div><b>4</b><span><strong>試單評估</strong>：觀察首批個案的實際服務情況。</span></div><div><b>5</b><span><strong>確認合作</strong>：通過核驗後加入配對名單，取得徽章；合作後每年重審。</span></div></div><p class="note">核驗徽章不能付費取得。合作條款與費用於審核後說明。</p></div></div></div></section>
<section id="apply" class="bg-grey"><div class="wrap"><div class="head"><div><h2>從認識彼此開始。</h2></div><p>告訴我們你的服務地點、專業範圍與機構資料。</p></div>{hs_block(lang, preview, 'zd-partner-form')}</div></section>'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Connect your expertise with the right needs.</h1><p class="lead">You provide local expertise. ZDelp assesses client needs, makes the match and continues to follow up.<br>We start by understanding how we can work together.</p><div class="actions"><a class="btn btn-teal" href="#apply">Apply to partner</a></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>How we work together</h2></div></div><div class="cards three-text"><article class="card pend"><div class="b"><h3>Needs assessed before matching</h3><p>ZDelp assesses the client's needs before making a match, giving both sides a clear starting point.</p></div></article><article class="card pend"><div class="b"><h3>Professional services provided by you</h3><p>Your firm explains its services, fees and arrangements, and provides the professional service directly to the client.</p></div></article><article class="card pend"><div class="b"><h3>Follow-up from ZDelp</h3><p>ZDelp continues to coordinate and follow up after the match. Clients pay your firm directly for its services.</p></div></article></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>Partnership requirements</h2><div class="pro-list"><div><b>1</b><span>Valid licences and firm registration in the location where you provide services.</span></div><div><b>2</b><span>Verifiable details for the person responsible.</span></div><div><b>3</b><span>Communication in Chinese or English.</span></div><div><b>4</b><span>A clear explanation of services and fees before engagement.</span></div><div><b>5</b><span>Participation in trial cases and annual reviews.</span></div></div></div><div><h2>Joining process</h2><div class="pro-list"><div><b>1</b><span><strong>Submit your details:</strong> registration documents, licences, service scope and fee information.</span></div><div><b>2</b><span><strong>Credential checks:</strong> we verify licences and registration status.</span></div><div><b>3</b><span><strong>Video interview:</strong> we discuss your service approach, experience and communication arrangements.</span></div><div><b>4</b><span><strong>Trial cases:</strong> we observe how the first cases are handled.</span></div><div><b>5</b><span><strong>Confirm the partnership:</strong> firms that pass vetting join the matching list and receive a verification badge, with annual reviews thereafter.</span></div></div><p class="note">Verification badges cannot be purchased. Partnership terms and fees are explained after review.</p></div></div></div></section>
<section id="apply" class="bg-grey"><div class="wrap"><div class="head"><div><h2>Let's get to know each other.</h2></div><p>Tell us where you work, your areas of expertise and about your firm.</p></div>{hs_block(lang, preview, 'zd-partner-form')}</div></section>'''

def p_about(lang, preview, rel):
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>在地・可靠・同行。</h1><p class="lead">ZDelp Limited 是於香港註冊的在地服務與協助公司。<br>從泰國簽證，到銀行開戶、房產與公司事務，你可以直接向 ZDelp 查詢所需服務。</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>服務分工</h2></div></div><div class="split"><div class="split-card own"><span class="badge own"><i>●</i>ZDelp 專員直接辦理</span><h3>泰國簽證由 ZDelp 專員提供申請與辦理服務。</h3></div><div class="split-card ver"><span class="badge ver"><i>✓</i>核驗機構提供服務</span><h3>其他服務由經 ZDelp 核驗的可靠持牌機構提供。ZDelp 負責評估、配對與跟進，協作服務不代收代付。</h3></div></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>公司資料</h2><table class="tbl"><tr><td>公司名稱</td><td>ZDelp Limited</td></tr><tr><td>註冊地</td><td>香港</td></tr><tr><td>官方網站</td><td>zdelp.co</td></tr><tr><td>聯絡電郵</td><td>info@zagdim.com</td></tr></table></div><div><h2>與宅點合作</h2><p class="muted">ZDelp 與宅點是兩間獨立公司，彼此互補協作。宅點負責研究與內容；ZDelp 負責在地服務與協助。部分服務詳情刊登於宅點，服務查詢由 ZDelp 接洽。</p></div></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>常見問題</h2></div></div><div class="faq"><details><summary>所有服務都由 ZDelp 直接辦理嗎？</summary><p>泰國簽證由 ZDelp 專員直接辦理。其他服務由經 ZDelp 核驗的可靠持牌機構提供，ZDelp 負責評估、配對與跟進。各項服務會標明實際辦理方式。</p></details><details><summary>費用支付給誰？</summary><p>ZDelp 直接辦理的服務，依該項服務的報價與付款安排支付。協作服務由你與提供服務的機構直接結算，ZDelp 不代收代付。</p></details><details><summary>配對後，還可以找 ZDelp 嗎？</summary><p>可以。ZDelp 會持續跟進，並協助處理服務過程中的溝通與協調。</p></details><details><summary>還不確定需要哪項服務，可以先聯絡嗎？</summary><p>可以。告訴我們想辦什麼，我們會回覆可以提供哪些協助。</p></details></div></div></section>
{cta_band(lang, preview, rel, '需要幫忙，找 ZDelp。')}'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Local. Reliable. With you.</h1><p class="lead">ZDelp Limited is a Hong Kong-registered company providing local services and assistance.<br>From Thai visas to bank accounts, property and company matters, you can contact ZDelp directly about the help you need.</p></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>Who provides the service</h2></div></div><div class="split"><div class="split-card own"><span class="badge own"><i>●</i>Handled directly by ZDelp specialists</span><h3>ZDelp specialists provide application assistance and handling for Thai visas.</h3></div><div class="split-card ver"><span class="badge ver"><i>✓</i>Provided by vetted firms</span><h3>Other services are provided by reliable, licensed firms vetted by ZDelp. ZDelp assesses your needs, makes the match and follows up. For these services, ZDelp does not collect or make payments on your behalf.</h3></div></div></div></section>
<section><div class="wrap"><div class="two"><div><h2>Company details</h2><table class="tbl"><tr><td>Company</td><td>ZDelp Limited</td></tr><tr><td>Registered in</td><td>Hong Kong</td></tr><tr><td>Website</td><td>zdelp.co</td></tr><tr><td>Email</td><td>info@zagdim.com</td></tr></table></div><div><h2>Working with Zagdim</h2><p class="muted">ZDelp and Zagdim are two independent companies that collaborate in complementary areas. Zagdim's role is research and content; ZDelp's role is local services and assistance. Some service details are published on Zagdim, with service enquiries handled by ZDelp.</p></div></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="head"><div><h2>Frequently asked questions</h2></div></div><div class="faq"><details><summary>Does ZDelp handle every service directly?</summary><p>ZDelp specialists handle Thai visa applications directly. Other services are provided by reliable, licensed firms vetted by ZDelp, with ZDelp assessing needs, making the match and following up. Each service indicates who handles the work.</p></details><details><summary>Who do I pay?</summary><p>For services handled directly by ZDelp, follow the quotation and payment arrangements for that service. For services provided by a partner firm, you pay the firm directly. ZDelp does not collect or make payments on your behalf for partner services.</p></details><details><summary>Can I still contact ZDelp after being matched?</summary><p>Yes. ZDelp continues to follow up and assists with communication and coordination during the service.</p></details><details><summary>Can I get in touch if I am unsure which service I need?</summary><p>Yes. Tell us what you need help with, and we will explain what assistance we can offer.</p></details></div></div></section>
{cta_band(lang, preview, rel, 'Need help? Talk to ZDelp.')}'''

def p_contact(lang, preview, rel):
    if lang == 'zh':
        return f'''
<section class="hero sm"><div class="wrap"><h1>你想辦什麼，告訴我們。</h1><p class="lead">直接傳訊息，或留下聯絡方式與需要協助的事。</p><div class="channels inline"><a class="ch" href="{WA}" target="_blank" rel="noopener"><b>WhatsApp 聯絡</b></a><a class="ch" href="{LINE}" target="_blank" rel="noopener"><b>LINE 聯絡</b></a><a class="ch" href="{MAIL}"><b>傳送電郵</b><span>info@zagdim.com</span></a></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="two top"><div><h2>留下訊息</h2><p class="muted">例如：想申請泰國簽證、需要開戶，或想找人管理房產。也請告訴我們需要在哪裡辦理。</p>{hs_block(lang, preview, 'zd-contact-form')}</div><div><p class="note">泰國簽證提供 20 分鐘免費初審。</p><p class="note">如需洽談機構合作，請一併提供機構名稱、服務地點與專業範圍。</p></div></div></div></section>'''
    return f'''
<section class="hero sm"><div class="wrap"><h1>Tell us what you need help with.</h1><p class="lead">Send us a message, or leave your contact details and a brief description of what you need.</p><div class="channels inline"><a class="ch" href="{WA}" target="_blank" rel="noopener"><b>Message on WhatsApp</b></a><a class="ch" href="{LINE}" target="_blank" rel="noopener"><b>Message on LINE</b></a><a class="ch" href="{MAIL}"><b>Send an email</b><span>info@zagdim.com</span></a></div></div></section>
<section class="bg-grey"><div class="wrap"><div class="two top"><div><h2>Leave a message</h2><p class="muted">For example: a Thai visa application, opening a bank account or finding help to manage a property. Please also tell us where you need the service.</p>{hs_block(lang, preview, 'zd-contact-form')}</div><div><p class="note">A free 20-minute initial assessment is available for Thai visa applications.</p><p class="note">For partnership enquiries, please include your firm's name, service locations and areas of expertise.</p></div></div></div></section>'''

BUILDERS = dict(index=p_index, services=p_services, verify=p_verify, partners=p_partners, about=p_about, contact=p_contact)
TITLES = {'zh': dict(index=('ZDelp｜需要幫忙，找 ZDelp。簽證、銀行開戶、房產與公司事務', 'ZDelp Limited（香港註冊）：一個窗口，聯通全球在地服務。簽證、銀行開戶、房產與公司事務，由 ZDelp 專員或經核驗的持牌機構辦理，ZDelp 評估、安排與持續跟進。'), services=('ZDelp 服務｜泰國簽證、銀行開戶、房產出租與代管、英國置業與公司', '找到需要的服務，查看辦理內容與費用；不確定也可以直接聯絡 ZDelp。'), verify=('ZDelp 核驗制度｜先核驗，再合作', '執照與登記、視訊訪談、試單評估、年度重審；徽章不能付費取得。'), partners=('機構合作｜讓專業，遇見合適需求', '你提供在地專業，ZDelp 負責需求評估、配對與持續跟進。合作條件、加入流程與申請。'), about=('關於 ZDelp｜在地・可靠・同行', 'ZDelp Limited 是於香港註冊的在地服務與協助公司；與宅點是兩間獨立公司，互補協作。'), contact=('聯絡 ZDelp｜你想辦什麼，告訴我們', 'WhatsApp、LINE、電郵或留言；泰國簽證提供 20 分鐘免費初審。')),
          'en': dict(index=('ZDelp | Need help? Talk to ZDelp. Visas, bank accounts, property and company matters', 'ZDelp Limited (Hong Kong): one contact point for local help worldwide. Visas, bank accounts, property and company matters, handled by ZDelp specialists or vetted, licensed firms, with ZDelp assessing, arranging and following up.'), services=('ZDelp services | Thai visas, bank accounts, property management, UK property and company', 'Find the service you need and check what it covers and what it costs; contact ZDelp if unsure.'), verify=('Our vetting process | Vetted before we work together', 'Licences and registration, video interview, trial cases, annual review; the badge cannot be bought.'), partners=('Partner with ZDelp | Connect your expertise with the right needs', 'You provide local expertise; ZDelp assesses needs, matches and follows up. Requirements, joining process and application.'), about=('About ZDelp | Local. Reliable. With you.', 'ZDelp Limited is a Hong Kong-registered company providing local services and assistance; ZDelp and Zagdim are two independent companies.'), contact=('Contact ZDelp | Tell us what you need help with', 'WhatsApp, LINE, email or leave a message; a free 20-minute assessment for Thai visas.'))}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": "https://zdelp.co/#organization", "name": "ZDelp", "legalName": "ZDelp Limited", "url": "https://zdelp.co/", "sameAs": ["https://zagdim.com/zdelp/", "https://www.facebook.com/ZDelpThailifeservice"], "logo": "https://zdelp.co/assets/zdelp.png", "email": "info@zagdim.com", "address": {"@type": "PostalAddress", "addressRegion": "Hong Kong", "addressCountry": "HK"}, "slogan": "Local. Reliable. With you."}

def page_html(page, lang, preview, rel):
    t = T[lang]; title, desc = TITLES[lang][page]
    body = BUILDERS[page](lang, preview, rel)
    ld = [ORG] if page in ('index', 'about') else []
    faq = re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', body, re.S)
    if faq: ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": html.unescape(re.sub('<[^>]+>', '', q)), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a))}} for q, a in faq]})
    alt = '' if preview else '<link rel="alternate" hreflang="zh-Hant" href="https://zdelp.co/%s"><link rel="alternate" hreflang="en" href="https://zdelp.co/en/%s">' % (page + '.html' if page != 'index' else '', page + '.html' if page != 'index' else '')
    scripts = (HS_SCRIPT if (not preview and 'class="hs"' in body) else '') + ANIM + ''.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><meta name="description" content="%s">%s%s<style>\n%s\n</style></head><body>%s<main>%s</main>%s%s</body></html>' % (
        t['lang'], html.escape(title), html.escape(desc), alt, FONTS, CSS, nav(page, lang, preview, rel), body, footer(lang, preview, rel), scripts)

def preview_site():
    parts = []
    for lang in ('zh', 'en'):
        for page in PAGES:
            t = T[lang]; body = BUILDERS[page](lang, True, '')
            parts.append('<div class="pg" id="%s-%s" lang="%s">%s<main>%s</main>%s</div>' % (lang, page, t['lang'], nav(page, lang, True, ''), body, footer(lang, True, '')))
    router = """<script>function show(){var h=(location.hash||'#zh-index').slice(1);var ok=false;document.querySelectorAll('.pg').forEach(function(p){var on=p.id===h;p.style.display=on?'block':'none';if(on)ok=true;});if(!ok){document.getElementById('zh-index').style.display='block';}window.scrollTo(0,0);document.querySelectorAll('section .wrap>*').forEach(function(el){el.classList.add('in')});}window.addEventListener('hashchange',show);show();</script>"""
    return '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>zdelp.co 全站預覽 v3（zh／en）</title><meta name="description" content="zdelp.co 六頁雙語預覽 v2（Codex 文案）：導覽列切頁、右上 EN／中文切換。">%s<style>\n%s\n.pg{display:none}.mockbar{background:#EEBF01;color:#10374e;font-size:13px;font-weight:700;text-align:center;padding:6px}\n</style></head><body><div class="mockbar">zdelp.co 全站預覽 v3 · 導覽列切頁 · 右上 EN／中文切換 · 圖片暫用</div>%s%s</body></html>' % (FONTS, CSS, ''.join(parts), router)

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
    for lang in ('zh', 'en'):
        for p in PAGES:
            io.open(os.path.join(ROOT, 'preview', 'gate-%s-%s.md' % (lang, p)), 'w', encoding='utf-8').write(gate_text(page_html(p, lang, False, '')))
    # 部署附檔（每次建置重生）
    import datetime; today = datetime.date.today().isoformat()
    io.open(os.path.join(D, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://zdelp.co/sitemap.xml\n')
    urls = ['https://zdelp.co/'] + ['https://zdelp.co/%s.html' % p for p in PAGES[1:]] + ['https://zdelp.co/en/'] + ['https://zdelp.co/en/%s.html' % p for p in PAGES[1:]]
    io.open(os.path.join(D, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, today) for u in urls) + '</urlset>\n')
    io.open(os.path.join(D, 'CNAME'), 'w').write('zdelp.co\n'); io.open(os.path.join(D, '.nojekyll'), 'w').write('')
    nf = '<section class="hero sm"><div class="wrap"><h1>找不到這個頁面。</h1><p class="lead">網址可能已更改。請回到首頁，或直接聯絡 ZDelp。</p><div class="actions"><a class="btn btn-gold" href="/">回首頁</a><a class="btn btn-ghost" href="/contact.html">聯絡 ZDelp</a></div></div></section>'
    io.open(os.path.join(D, '404.html'), 'w', encoding='utf-8').write('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>找不到頁面｜ZDelp</title><meta name="robots" content="noindex">%s<style>\n%s\n</style></head><body>%s<main>%s</main>%s</body></html>' % (FONTS, CSS, abs_links(nav('index', 'zh', False, '/')), nf, abs_links(footer('zh', False, '/'))))
    print('built dist/ (zh+en) + preview/site.html + robots/sitemap/CNAME/404')
