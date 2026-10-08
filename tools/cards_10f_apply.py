"""T10F : retire les regles locales de cartes (benevole/equipe/partenaire/temoignage), fonds de section, gaps, padding. Usage: cards_10f_apply.py"""
def rd(f): return open(f,encoding='utf8').read()
def wr(f,s): open(f,'w',encoding='utf8').write(s)
def sub(s,old,new):
    assert s.count(old)==1,(old[:70],s.count(old)); return s.replace(old,new)
def edit(f,pairs):
    s=rd('styles/'+f)
    for o,n in pairs: s=sub(s,o,n)
    wr('styles/'+f,s)
A='var(--clr-section-alt)'
edit('devenir-benevole.css',[
('.benevolat-formats{padding:5rem 0;background-color:var(--clr-white)}','.benevolat-formats{padding:5rem 0;background-color:%s}'%A),
('.benevolat-missions{padding:5rem 0;background-color:var(--clr-surface)}','.benevolat-missions{padding:5rem 0;background-color:%s}'%A),
('grid-template-columns:repeat(4,1fr);gap:1.5rem','grid-template-columns:repeat(4,1fr);gap:1.25rem'),
('grid-template-columns:repeat(3,1fr);gap:1.5rem}','grid-template-columns:repeat(3,1fr);gap:1.25rem}'),
('.benevolat-format-card{background-color:var(--clr-off-white);border-radius:var(--radius-card);padding:2rem 1.5rem;box-shadow:var(--shadow-md);border:1px solid var(--clr-secondary-soft);','.benevolat-format-card{padding:1.5rem;'),
('.benevolat-mission-card{background-color:var(--clr-white);border-radius:var(--radius-card);padding:1.5rem;box-shadow:var(--shadow-md);border:1px solid var(--clr-secondary-soft)','.benevolat-mission-card{padding:1.5rem'),
])
edit('rejoindre-equipe.css',[
('gap:2rem;margin-bottom:3rem','gap:1.25rem;margin-bottom:3rem'),
('.why-card{background:var(--clr-white);padding:2rem;border-radius:var(--radius-card);box-shadow:var(--shadow-md);border:1px solid var(--clr-surface)','.why-card{padding:1.5rem'),
('.job-sidebar{background:var(--clr-white);padding:1.5rem;border-radius:var(--radius-card);border:1px solid var(--clr-surface)','.job-sidebar{padding:1.5rem'),
('grid-template-columns:repeat(3,1fr);gap:1.5rem}','grid-template-columns:repeat(3,1fr);gap:1.25rem}'),
('.metier-card{background:var(--clr-off-white);padding:2rem;border-radius:var(--radius-card);border-left:4px solid var(--clr-accent)','.metier-card{padding:1.5rem'),
('.banner-links{display:flex;flex-wrap:wrap;justify-content:center;gap:2rem','.banner-links{display:flex;flex-wrap:wrap;justify-content:center;gap:1.25rem'),
('.banner-card{background:var(--clr-white);padding:2rem;border-radius:var(--radius-card);width:250px','.banner-card{padding:1.5rem;width:250px'),
('box-shadow:var(--shadow-md);font-weight:600','font-weight:600'),
('.banner-card:hover{box-shadow:var(--shadow-lg,var(--shadow-md))}',''),
('.final-banner{background:var(--clr-accent-soft)','.final-banner{background:%s'%A),
])
edit('devenir-partenaire.css',[
('.partenariats-why{padding:var(--section-pad-y) 0;background-color:var(--clr-off-white)}','.partenariats-why{padding:var(--section-pad-y) 0;background-color:%s}'%A),
('grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:var(--section-header-gap)','grid-template-columns:repeat(3,1fr);gap:1.25rem;margin-top:var(--section-header-gap)'),
('.partenariats-why__card{padding:2.5rem;background:var(--clr-white);border-radius:var(--radius-card);box-shadow:var(--shadow-md)}','.partenariats-why__card{padding:1.5rem;background:var(--clr-white);border:1px solid var(--clr-border-card);border-radius:var(--radius-card);box-shadow:var(--shadow-card);transition:border-color 0.2s ease,box-shadow 0.2s ease}\n.partenariats-why__card:hover{border-color:var(--clr-border-hover);box-shadow:var(--shadow-hover);transform:none}'),
('.partenariats-why__card{padding:2rem}',''),
])
edit('partager-temoignage.css',[
('.temoignage-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}','.temoignage-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}'),
('.reason-card{padding:2rem;background:var(--clr-off-white);border-radius:var(--radius-card);box-shadow:var(--shadow-md)}','.reason-card{padding:1.5rem}'),
('.temoignage-form-section{background-color:var(--clr-off-white)}','.temoignage-form-section{background-color:%s}\n.temoignage-section:not(.temoignage-control):not(.temoignage-form-section){background-color:%s}'%(A,A)),
('.form-card{background:var(--clr-white);padding:3rem;border-radius:var(--radius-card);box-shadow:var(--shadow-md)}','.form-card{padding:3rem}'),
])
# sections de rejoindre sans id (why, metiers)
s=rd('styles/rejoindre-equipe.css'); s=s.replace('.final-banner{','.rejoindre-section:not([id]){background-color:%s}\n.final-banner{'%A,1); wr('styles/rejoindre-equipe.css',s)
