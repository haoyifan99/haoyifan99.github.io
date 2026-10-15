"""Build static pages from one publication list. Run: python3 build_site.py."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
PAPERS = sorted(json.loads((ROOT / 'publications.json').read_text()), key=lambda p: p['year'], reverse=True)
SCHOLAR = 'https://scholar.google.com.hk/citations?user=lzI8IicAAAAJ&hl=en'
EMAIL = 'mailto:yifanh12@illinois.edu'
BLOG = 'https://zoeyli.com/blog/Revisiting-Predictability-of-RLVR/'
HOSTS = '<a href="https://zoeyli.com/">Zoey Li</a> and <a href="https://www.linkedin.com/in/zhenyu-edwin-shi-a479a327/">Zhenyu Shi</a>'

def page(title, current, body, description):
    nav = [('index.html', 'About'), ('research.html', 'Research'), ('Bio.html', 'Experience'), ('Miscellaneous.html', 'More')]
    links = ''.join(f'<a href="{url}"'+(' aria-current="page"' if current == url else '')+f'>{label}</a>' for url,label in nav)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Yifan Hao</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#214f42"><link rel="stylesheet" href="site.css"><script src="site.js" defer></script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap"><div class="header-inner"><a class="brand" href="index.html">Yifan Hao<span aria-hidden="true">.</span></a>
<nav class="nav" aria-label="Main navigation">{links}<a class="nav-cv" href="cv.pdf">CV <span aria-hidden="true">↗</span></a></nav></div></div></header>
<main class="wrap" id="main">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><span>Yifan Hao · University of Illinois Urbana-Champaign</span><div class="footer-links"><a href="{EMAIL}">Email</a><a href="{escape(SCHOLAR, quote=True)}">Google Scholar</a><a href="https://github.com/haoyifan99">GitHub</a></div></div></footer>
</body></html>'''

def authors(names):
    return ', '.join('<strong>'+escape(name)+'</strong>' if name.rstrip('*') == 'Yifan Hao' else escape(name) for name in names)

def paper_html(p):
    title = escape(p['title'])
    if p.get('url'):
        title = f'<a href="{escape(p["url"], quote=True)}">{title}</a>'
    links = ''.join(f'<a href="{escape(url, quote=True)}">{escape(label)} <span aria-hidden="true">↗</span></a>' for label,url in p.get('links',[]))
    link_html = f'<div class="pub-links">{links}</div>' if links else ''
    return f'''<li class="publication" data-topics="{' '.join(p['topics'])}"><div class="publication-meta"><span class="venue">{escape(p['venue'])}</span><span class="pub-year">{p['year']}</span></div><div><h3>{title}</h3><p class="authors">{authors(p['authors'])}</p>{link_html}</div></li>'''

def publication_list(ids=None):
    selected = PAPERS if ids is None else [next(p for p in PAPERS if p['id']==id_) for id_ in ids]
    return '<ol class="publication-list">'+''.join(paper_html(p) for p in selected)+'</ol>'

def heading(number, title, link=''):
    return f'<div class="section-heading"><h2><span class="section-number">{number}</span>{title}</h2>{link}</div>'

JOB = f'''<aside class="job-banner" aria-label="Career opportunities"><div><div class="job-heading"><span class="status-dot" aria-hidden="true"></span>On the job market</div><p>I’m looking for <strong>full-time and internship opportunities</strong> in applied science and machine learning research, with a focus on LLM post-training and reinforcement learning.</p></div><a class="button" href="{EMAIL}">Get in touch <span aria-hidden="true">↗</span></a></aside>'''

AMAZON = f'''<article class="experience-row"><div class="experience-date">May – Aug 2026</div><div><h3>Applied Scientist Intern · Amazon Rufus</h3><p class="subline">Hosts: {HOSTS}</p><ul><li>Developed a <strong>Muon recipe for RLVR</strong> with no momentum, achieving <strong>29.17%</strong> macro-averaged Pass@1 on Qwen3-4B-Base compared with <strong>24.47% for AdamW</strong> across three math benchmarks.</li><li>Used spectral diagnostics and checkpoint interventions to study optimization stability and how learned behavior is organized across singular directions and attention projections.</li><li>Investigated RLVR trajectory predictability with random-walk controls. <a href="{BLOG}">Read the research write-up ↗</a></li></ul></div></article>'''

PHD = '''<article class="experience-row"><div class="experience-date">Sep 2024 – present</div><div><h3>Ph.D. Student · University of Illinois Urbana-Champaign</h3><p class="subline">Computer Science · Advisor: <a href="https://tongzhang-ml.org/">Prof. Tong Zhang</a></p><ul><li>Developed <strong>Adaptive Layerwise Perturbation (ALP)</strong> to stabilize off-policy LLM reinforcement learning under policy staleness and training–inference mismatch.</li><li>Proposed <strong>DIPNeT</strong> for generalization across reasoning and adversarial robustness settings.</li><li>Developed <strong>GVM-RAFT</strong>, a prompt-specific sample allocation strategy, achieving a <strong>2–4× speedup</strong> and improved accuracy over vanilla RAFT.</li><li>Studied feature decoupling in Transformers and their expressiveness for hidden Markov processes, and explained how ensemble methods reduce overadaptation in supervised fine-tuning.</li></ul></div></article>'''

MASTER = '''<article class="experience-row"><div class="experience-date">Sep 2022 – Aug 2024</div><div><h3>MPhil · Hong Kong University of Science and Technology</h3><p class="subline">Mathematics · Advisor: <a href="https://tongzhang-ml.org/">Prof. Tong Zhang</a></p><p>Studied the harmful effects of benign overfitting on adversarial robustness, and how spurious feature diversification and overparameterization affect out-of-distribution generalization. Supported by the Hong Kong PhD Fellowship.</p></div></article>'''

BACHELOR = '''<article class="experience-row"><div class="experience-date">Sep 2018 – Jun 2022</div><div><h3>B.S. in Statistics · University of Science and Technology of China</h3><p class="subline">School of the Gifted Young</p><p>Ranked 5/91 in Statistics; outstanding graduate.</p></div></article>'''

CONTACT = f'''<section class="contact-block"><div><h2>Let’s talk research.</h2><p>I welcome conversations about LLM post-training, reinforcement learning, and full-time or internship opportunities.</p></div><a href="{EMAIL}">yifanh12@illinois.edu <span aria-hidden="true">↗</span></a></section>'''

home = f'''<section class="hero" aria-labelledby="intro-title"><div class="hero-copy"><div class="hero-heading"><div class="eyebrow">Ph.D. Student · Computer Science · UIUC</div><h1 id="intro-title">Yifan Hao</h1><p class="research-line">LLM post-training,<br>grounded in theory.</p></div><p class="intro">I study how to make machine learning systems learn more efficiently and generalize more reliably. I’m a Ph.D. student at the University of Illinois Urbana-Champaign, advised by <a href="https://tongzhang-ml.org/">Prof. Tong Zhang</a>, working at the intersection of machine learning and statistics.</p><div class="hero-links"><a href="cv.pdf">Curriculum vitae <span aria-hidden="true">↗</span></a><a href="{escape(SCHOLAR, quote=True)}">Google Scholar <span aria-hidden="true">↗</span></a><a href="{EMAIL}">Email <span aria-hidden="true">↗</span></a></div></div><figure class="portrait"><img src="cv_photo2.jpg" width="275" height="320" alt="Yifan Hao by the waterfront" fetchpriority="high"><figcaption>Research · theory &amp; practice</figcaption></figure></section>
{JOB}
<section class="section" id="research">{heading('01','Research interests')}<div class="interest-grid"><article><span class="topic-number">I.</span><h3>LLM post-training &amp; RL</h3><p>Reliable reinforcement learning, reasoning, and optimization for large language models.</p></article><article><span class="topic-number">II.</span><h3>Efficient learning</h3><p>Algorithms that improve sample efficiency and reduce the computational cost of adaptation.</p></article><article><span class="topic-number">III.</span><h3>Statistical foundations</h3><p>Generalization, robustness, and the theory behind modern machine learning systems.</p></article></div></section>
<section class="section" id="recent-work">{heading('02','Recent work')}<div class="work-grid"><article class="work-item"><div class="work-meta">Amazon Rufus · 2026</div><h3>Understanding how RLVR learns</h3><p>A practical Muon training recipe, together with spectral diagnostics and checkpoint interventions to investigate optimization and learned behavior.</p><span class="quiet-status">Muon for RLVR · Preprint</span></article><article class="work-item"><div class="work-meta">LLM reinforcement learning · 2026</div><h3>More stable off-policy learning</h3><p>Adaptive Layerwise Perturbation unifies off-policy corrections for LLM RL, addressing policy staleness and training–inference mismatch.</p><a href="https://arxiv.org/abs/2603.19470">Read the ALP paper <span aria-hidden="true">↗</span></a></article></div></section>
<section class="section" id="experience">{heading('03','Research experience','<a class="section-link" href="Bio.html">Full background ↗</a>')}{AMAZON}{PHD}</section>
<section class="section" id="publications">{heading('04','Selected publications','<a class="section-link" href="research.html">All publications ↗</a>')}{publication_list(['alp','gvm','overadapt','benign'])}<p class="pub-note">* indicates alphabetical author order or equal contribution.</p></section>
{CONTACT}'''

filters = [('all','All work'),('llm','LLMs & RL'),('theory','Learning theory'),('merging','Model merging')]
filter_html = '<div class="filters" data-publication-filters hidden aria-label="Filter publications by research area">'+''.join(f'<button type="button" class="filter-button" data-filter="{value}" aria-pressed="{"true" if value=="all" else "false"}">{label}</button>' for value,label in filters)+'</div>'
research = f'''<header class="page-intro"><div class="eyebrow">Research</div><h1>Algorithms, with foundations.</h1><p>My work connects practical questions in LLM post-training and reinforcement learning with statistical learning theory, generalization, and robustness.</p></header><section class="page-section" aria-labelledby="papers-heading"><h2 id="papers-heading">Publications &amp; preprints</h2>{filter_html}<p class="filter-status" data-filter-status role="status" hidden>Showing {len(PAPERS)} of {len(PAPERS)} publications and preprints</p>{publication_list()}<p class="pub-note">* indicates alphabetical author order or equal contribution.</p></section><section class="section">{heading('','Research writing')}<article class="work-item"><div class="work-meta">Research write-up · 2026</div><h3>Revisiting the Predictability of RLVR</h3><p>Why low-rank trajectories and strong in-sample fits do not, by themselves, establish out-of-sample predictability.</p><a href="{BLOG}">Read the write-up <span aria-hidden="true">↗</span></a></article></section>{CONTACT}'''

awards = [('Hong Kong PhD Fellowship','2022'),('Outstanding Graduate of Anhui Province','2022'),('Outstanding Graduate of USTC','2022'),('China National Scholarship · top 1.8%','2021'),('Gold Prize for Outstanding Student Scholarship','2020, 2018')]
teaching = [('CS 441 · Applied Machine Learning, UIUC','Spring 2026'),('MATH 2011 · Introduction to Multivariable Calculus','Fall 2023'),('MATH 2421 · Probability','Spring 2023, Spring 2024'),('Mathematical Analysis B3','Fall 2021'),('Complex Analysis','Spring 2021')]
def simple_list(rows):
    return '<ul class="simple-list">'+''.join(f'<li><span>{escape(label)}</span><span class="when">{escape(date)}</span></li>' for label,date in rows)+'</ul>'
biography = f'''<header class="page-intro"><div class="eyebrow">Background</div><h1>Experience &amp; education.</h1><p>Training in computer science, mathematics, and statistics, with research spanning LLM reinforcement learning and the foundations of generalization.</p></header><section class="section">{heading('01','Research & education')}{AMAZON}{PHD}{MASTER}{BACHELOR}</section><section class="section">{heading('02','Teaching assistant experience')}{simple_list(teaching)}</section><section class="section">{heading('03','Selected honors & awards')}{simple_list(awards)}</section><section class="section">{heading('04','Professional service')}<div class="service-columns"><div><h3>Conference reviewer</h3><p>NeurIPS, ICLR, ICML, AISTATS, AAAI</p></div><div><h3>Journal reviewer</h3><p>Journal of Machine Learning Research; SIAM Journal on Mathematics of Data Science; IEEE Transactions on Pattern Analysis and Machine Intelligence</p></div></div></section><section class="section">{heading('05','Technical skills')}<p class="authors"><strong>Programming:</strong> Python, PyTorch, MATLAB, R, C/C++</p></section>{CONTACT}'''

misc = f'''<header class="page-intro"><div class="eyebrow">Beyond research</div><h1>A little more about me.</h1></header><section class="misc-body"><p>Outside research, I enjoy exercising, reading books across genres, and playing board games.</p><p class="plain-note">Always happy to connect over research or shared interests.</p><a href="{EMAIL}">Say hello ↗</a></section>'''

for file, title, body, description in [
    ('index.html','LLM Post-Training & Reinforcement Learning',home,'Yifan Hao is a UIUC Computer Science Ph.D. student researching LLM post-training, reinforcement learning, and statistical machine learning. Open to full-time and internship opportunities.'),
    ('research.html','Research & Publications',research,'Publications and research by Yifan Hao on LLM post-training, reinforcement learning, model merging, generalization, and robustness.'),
    ('Bio.html','Experience & Education',biography,'Research experience, education, teaching, awards, and professional service of Yifan Hao, UIUC Ph.D. student and former Amazon Rufus Applied Scientist Intern.'),
    ('Miscellaneous.html','Beyond Research',misc,'A little more about Yifan Hao outside research.'),
]:
    (ROOT/file).write_text(page(title,file,body,description),encoding='utf-8')
print(f'Built 4 pages with {len(PAPERS)} publications from one shared source.')
