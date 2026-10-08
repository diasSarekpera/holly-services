p='styles/actualites.css'; s=open(p,encoding='utf-8').read()
a='.actualites-link:hover { color:var(--clr-primary) }'
if a not in s: a='.actualites-link:hover{color:var(--clr-primary)}'
assert s.count(a)==1
s=s.replace(a,a.replace('var(--clr-primary)','var(--clr-secondary)'))
s=s.rstrip('\n')+'\n/* 18A : cible tactile >= 44 px pour le lien « Lire » (mobile) */\n@media (max-width:767px){.actualites-link{display:inline-flex;align-items:center;min-height:44px}}\n'
open(p,'w',encoding='utf-8').write(s)
