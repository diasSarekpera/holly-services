#!/usr/bin/env python3
"""14A : retire le flou (backdrop-filter) de .about__stat-card et .mission__img-kpi, fonds opaques. Uniquement ces 2 regles de styles/home.css."""
import re
f='styles/home.css';c=open(f,encoding='utf8').read()
n=0
def fix(sel,old_bg,new_bg,blur):
    global c,n
    a=f'{sel}{{';i=c.index(a);j=c.index('}',i)
    rule=c[i:j]
    new=rule.replace(old_bg,new_bg).replace(f'backdrop-filter:blur({blur}px);','').replace(f'-webkit-backdrop-filter:blur({blur}px);','')
    assert new!=rule and 'blur' not in new;c=c[:i]+new+c[j:];n+=1
fix('.about__stat-card','background:rgba(16,35,63,0.88)','background:var(--clr-secondary)',12)
fix('.mission__img-kpi','background:rgba(255,255,255,0.95)','background:var(--clr-white)',8)
open(f,'w',encoding='utf8').write(c);print('rules patched',n)
