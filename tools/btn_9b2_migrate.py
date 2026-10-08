"""9B2 : migration des boutons locaux des pages interieures vers le socle .btn"""
import re,sys,glob
sys.path.insert(0,'tools')
from css_rules import rules
def rw(f,fn):
    s=open(f,encoding='utf8').read();n=fn(s)
    assert n!=s,f
    open(f,'w',encoding='utf8').write(n)
def drop_decls(s,sel,props,media=None):
    """retire des declarations d'une regle (selecteur exact)"""
    for mp,sl,body,a,b in reversed(rules(s)):
        if sl==sel and (media is None or media in mp):
            nb=body
            for p in props: nb=re.sub(r'(^|;)\s*'+re.escape(p)+r'\s*:[^;]*',r'\1',nb)
            nb=nb.strip(';').strip()
            seg=s[a:b]
            new=(sel+'{'+nb+'}') if nb else ''
            s=s[:a]+new+s[b:]
    return re.sub(r'@media[^{]*\{\s*\}','',s)
H=lambda f,a,b:rw(f,lambda s:s.replace(a,b))
# HTML
H('pages/campagne-proteger-500-enfants.html','class="btn btn--primary campagne-don__cta"','class="btn btn--primary btn--lg campagne-don__cta"')
H('pages/devenir-benevole.html','class="btn benevolat-mission-card__btn"','class="btn btn--primary benevolat-mission-card__btn"')
H('pages/partager-temoignage.html','class="btn btn--ghost temoignage-signal__btn"','class="btn btn--primary temoignage-signal__btn"')
# CSS
rw('styles/campagne-proteger-500-enfants.css',lambda s:drop_decls(s,'.campagne-don__cta',['justify-content','font-size']))
def benev(s):
    s=drop_decls(s,'.benevolat-mission-card__btn',['background-color','color','border-color'])
    for mp,sl,body,a,b in reversed(rules(s)):
        if sl=='.benevolat-mission-card__btn:hover': s=s[:a]+s[b:]
    return s
rw('styles/devenir-benevole.css',benev)
rw('styles/maintenance.css',lambda s:drop_decls(s,'.maintenance__btn',['justify-content','min-height'],media='700px'))
rw('styles/partager-temoignage.css',lambda s:drop_decls(s,'.temoignage-signal__btn',['border-color']))
