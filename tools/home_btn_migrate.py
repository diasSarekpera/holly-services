import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
H='index.html';C='styles/home.css'
h=open(H,encoding='utf8').read();s=open(C,encoding='utf8').read()
# ---------- HTML ----------
rep=[('class="hero__cta-primary"','class="btn btn--primary hero__cta-primary"'),
('class="hero__cta-secondary"','class="btn btn--ghost-light hero__cta-secondary"'),
('class="btn--donate-primary"','class="btn btn--primary camp-card__cta-main"'),
('class="btn--donate-inline btn--donate-inline--social"','class="btn btn--primary btn--sm camp-card__cta-inline"'),
('class="btn--donate-inline btn--donate-inline--edu"','class="btn btn--primary btn--sm camp-card__cta-inline"'),
('class="soutenir__way-btn soutenir__way-btn--primary"','class="btn btn--primary soutenir__way-btn"'),
('class="soutenir__way-btn soutenir__way-btn--secondary"','class="btn btn--ghost soutenir__way-btn"'),
('class="soutenir__way-btn soutenir__way-btn--tertiary"','class="btn btn--ghost soutenir__way-btn"')]
for a,b in rep:
    assert h.count(a)>=1,a
    h=h.replace(a,b)
open(H,'w',encoding='utf8').write(h)
# ---------- CSS : remove obsolete rules ----------
def drop(sel_exact=None,pred=None):
    global s
    for mp,sel,body,a,b in reversed(rules(s)):
        if (sel_exact and sel in sel_exact) or (pred and pred(mp,sel)):
            # remove rule text; if inside @media leave media (cleaned after)
            s=s[:a]+s[b:]
gone=['.hero__cta-primary','.hero__cta-primary:hover','.hero__cta-primary svg','.hero__cta-secondary','.hero__cta-secondary:hover','.hero__cta-arrow','.hero__cta-secondary:hover .hero__cta-arrow',
'.btn--donate-primary','.btn--donate-primary svg','.btn--donate-primary:hover','.btn--donate-inline','.btn--donate-inline svg','.btn--donate-inline--social','.btn--donate-inline--edu','.btn--donate-inline--social:hover','.btn--donate-inline--edu:hover',
'.soutenir__way-btn','.soutenir__way-btn--primary','.soutenir__way-btn--primary:hover','.soutenir__way-btn--secondary','.soutenir__way-btn--secondary:hover','.soutenir__way-btn--tertiary','.soutenir__way-btn--tertiary:hover','.soutenir__way-btn svg','.soutenir__way-btn svg:first-child','.soutenir__way-btn svg:last-child','.soutenir__way-btn:hover svg:last-child','.soutenir__way-btn--primary svg:first-child']
def p(mp,sel):
    if sel in gone and 'reduced-motion' not in mp: return True
    if sel in ('.hero__cta-primary','.hero__cta-secondary') : return True
    if sel in ('.btn--donate-primary','.btn--donate-inline') and ('640px' in mp or '480px' in mp): return True
    if sel=='.soutenir__way-btn' : return True
    return False
drop(pred=p)
s=re.sub(r'@media[^{]*\{\s*\}','',s)
# reduced-motion lists
s=s.replace('.camp-card,.camp-card__img-real,.btn--donate-primary,.btn--donate-inline,.camp-card__learn-more','.camp-card,.camp-card__img-real,.camp-card__learn-more')
s=s.replace('.soutenir__way,.soutenir__way-line,.soutenir__way-icon,.soutenir__way-btn,.soutenir__amount','.soutenir__way,.soutenir__way-line,.soutenir__way-icon,.soutenir__amount')
# 899px rules
s=s.replace('.soutenir__amount,.soutenir__way-btn{min-height:44px}','.soutenir__amount{min-height:44px}')
s=s.replace('.soutenir__amount:focus-visible,.soutenir__way-btn:focus-visible{','.soutenir__amount:focus-visible{')
# ---------- CSS : minimal local layout ----------
s=s.rstrip('\n')+'''

/* ===== Accueil : boutons migrés vers le socle .btn (V68 / 9B1) — uniquement le layout local ===== */
.hero__cta-primary,.hero__cta-secondary{flex-shrink:0}
.hero__cta-primary svg{width:16px;height:16px;fill:currentColor;stroke:none}
.hero__cta-secondary svg{width:16px;height:16px}
.camp-card__cta-main{flex:1}
.camp-card__cta-main svg,.camp-card__cta-inline svg{fill:currentColor;stroke:none}
.camp-card__cta-inline{width:100%;margin-top:auto}
.soutenir__way-btn{width:fit-content}
.soutenir__way-btn.btn--primary svg:first-child{fill:currentColor;stroke:none}
.partners__footer-actions{flex-wrap:wrap}
@media (max-width:767px){.hero__cta-primary,.hero__cta-secondary{width:100%}}
@media (max-width:640px){.camp-card__cta-main{flex:unset;width:100%}}
@media (max-width:639px){.soutenir__way-btn{width:100%}.partners__footer-actions{flex-direction:column;align-items:stretch;width:100%}.partners__footer-actions .btn{width:100%}}
'''
open(C,'w',encoding='utf8').write(s)
