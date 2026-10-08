import re
p='styles/article-prevention-cancer-peau.css'; s=open(p,encoding='utf-8').read()
def rep(pat,new):
    global s
    m=re.search(pat,s); assert m,pat; s=s.replace(m.group(0),new,1)
rep(r'\.article-nav__link:hover\s*\{\s*color:var\(--clr-primary\)\s*\}','.article-nav__link:hover{color:var(--clr-secondary)}')
rep(r'\.article-campaign \.btn--ghost:hover\s*\{\s*background:transparent\s*\}','.article-campaign .btn--ghost:hover{background:rgba(255,255,255,0.08)}')
s=s.rstrip('\n')+'\n/* 18C : liens precedent/suivant >= 44 px ; bouton du bloc don sur 1 ligne (mobile) */\n@media (max-width:767px){.article-nav__link{min-height:44px}.article-donation{align-items:stretch}.article-donation .btn{width:100%}}\n'
open(p,'w',encoding='utf-8').write(s)
