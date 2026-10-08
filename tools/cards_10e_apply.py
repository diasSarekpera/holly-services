"""T10E : retire les regles locales de cartes (actualites / article / campagne) et ajuste fonds + gaps + padding. Usage: cards_10e_apply.py"""
import re,sys
sys.path.insert(0,'tools')
def rd(f): return open(f,encoding='utf8').read()
def wr(f,s): open(f,'w',encoding='utf8').write(s)
def sub(s,old,new,n=1):
    assert s.count(old)==n,(old[:60],s.count(old)); return s.replace(old,new)
# ---- actualites
f='styles/actualites.css'; s=rd(f)
s=sub(s,'.actualites-grid-sec{padding:4rem 0;background-color:var(--clr-surface)}','.actualites-grid-sec{padding:4rem 0;background-color:var(--clr-section-alt)}')
s=sub(s,'.actualites-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}','.actualites-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}')
s=sub(s,'.actualites-card{position:relative;display:flex;flex-direction:column;border-radius:var(--radius-card);background:var(--clr-white);box-shadow:var(--shadow-md);overflow:hidden;transition:transform var(--transition-cta)}','.actualites-card{position:relative;display:flex;flex-direction:column;overflow:hidden}')
s=sub(s,'.actualites-card:hover{transform:translateY(-4px)}','')
s=sub(s,'.actualites-card:hover{transform:none}','')
s=re.sub(r'(@media \(max-width:767px\)\{)',r'\1',s)
wr(f,s)
# ---- article
f='styles/article-prevention-cancer-peau.css'; s=rd(f)
s=sub(s,'.article-related{padding:5rem 0;background-color:var(--clr-white)}','.article-related{padding:5rem 0;background-color:var(--clr-section-alt)}')
s=sub(s,'.article-related__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}','.article-related__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}')
s=sub(s,'.article-card{background:var(--clr-white);border-radius:var(--radius-card);overflow:hidden;box-shadow:var(--shadow-md);transition:transform var(--transition-cta),box-shadow var(--transition-cta),border-color var(--transition-cta);display:flex;flex-direction:column;border:1px solid transparent}','.article-card{overflow:hidden;display:flex;flex-direction:column}')
s=sub(s,'.article-card:hover{transform:translateY(-4px);border-color:var(--clr-primary)}','')
s=sub(s,'.article-card__title a:hover{color:var(--clr-primary)}','')
s=sub(s,'.article-cta{background-color:var(--clr-off-white);','.article-cta{background-color:var(--clr-section-alt);')
s=sub(s,'gap:1.5rem;max-width:900px;margin:0 auto}','gap:1.25rem;max-width:900px;margin:0 auto}')
s=sub(s,'.article-cta__card{display:flex;align-items:center;justify-content:space-between;padding:1.5rem;background:var(--clr-white);border:1px solid var(--clr-border-card);border-radius:var(--radius-card);font-weight:600;transition:border-color var(--transition-cta),color var(--transition-cta),box-shadow var(--transition-cta)}','.article-cta__card{display:flex;align-items:center;justify-content:space-between;padding:1.5rem;font-weight:600}')
s=sub(s,'.article-cta__card:hover{border-color:var(--clr-border-hover);color:var(--clr-primary);box-shadow:var(--shadow-md)}','')
wr(f,s)
# ---- campagne
f='styles/campagne-proteger-500-enfants.css'; s=rd(f)
s=sub(s,'.campagne-actions{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}','.campagne-actions{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}')
s=sub(s,'.campagne-card{padding:1.5rem;background:var(--clr-white);border:1px solid var(--clr-border-strong);border-radius:var(--radius-md);box-shadow:var(--shadow-md)}','.campagne-card{padding:1.5rem}')
s=sub(s,'padding:2rem;background:var(--clr-white);border:1px solid var(--clr-border-strong);border-radius:var(--radius-md);box-shadow:var(--shadow-md)}','padding:1.5rem}')
s=sub(s,'.campagne-layout{','.campagne-body{background-color:var(--clr-section-alt)}\n.campagne-layout{')
wr(f,s)
# html wrapper campagne
f='pages/campagne-proteger-500-enfants.html'; h=rd(f)
h=sub(h,'<div class="container campagne-layout">','<div class="campagne-body">\n    <div class="container campagne-layout">')
i=h.index('<section class="campagne-banner"'); j=h.rindex('</div>',0,i)
h=h[:j]+'</div>\n    </div>'+h[j+6:]
wr(f,h)
