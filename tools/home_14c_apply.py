#!/usr/bin/env python3
"""14C : (1) retire le flou de .team-card__index (fond plus opaque) ; (2) survol neutre sans teinte rose : .team-card__social-btn et .soutenir__amount. Uniquement ces regles de styles/home.css."""
f="styles/home.css";c=open(f,encoding="utf8").read()
def sub(old,new):
    global c
    assert c.count(old)==1,(old,c.count(old));c=c.replace(old,new)
i=c.index(".team-card__index{");j=c.index("}",i);r=c[i:j]
n=r.replace("background:rgba(16,35,63,0.35);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);","background:rgba(16,35,63,0.55);");assert n!=r and "blur" not in n;c=c[:i]+n+c[j:]
sub(".team-card__social-btn:hover{background:var(--clr-primary-soft);border-color:var(--clr-primary-overlay)}",".team-card__social-btn:hover{background:var(--clr-secondary-soft)}")
sub(".team-card__social-btn:hover svg{stroke:var(--clr-primary)}",".team-card__social-btn:hover svg{stroke:var(--clr-secondary)}")
sub(".soutenir__amount:hover{border-color:var(--clr-primary);color:var(--clr-primary)}",".soutenir__amount:hover{background:var(--clr-surface)}")
open(f,"w",encoding="utf8").write(c);print("ok")
