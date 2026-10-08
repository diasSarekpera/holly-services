#!/usr/bin/env python3
"""14B : cibles tactiles >=44px (mobile) pour .stats__note-link, .action-card__link, .camp-card__learn-more. Ajout en fin de styles/home.css (idempotent)."""
f="styles/home.css";c=open(f,encoding="utf8").read();tag="/* 14B : cibles tactiles accueil sections 4-6 */"
if tag not in c:
    c=c.rstrip("\n")+"\n"+tag+"\n@media (max-width:767px){.stats__note-link{display:block;margin-left:0;margin-top:0.35rem;min-height:44px;padding:0.5rem 0;line-height:1.4}.action-card__link,.camp-card__learn-more{min-height:44px}}\n"
    open(f,"w",encoding="utf8").write(c)
print("ok")
