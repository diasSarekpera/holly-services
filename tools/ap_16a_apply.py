#!/usr/bin/env python3
"""16A : section Mission (styles/a-propos.css) : rythme sur tokens --rhythm-* ; flou retire du badge de la photo (fond --clr-secondary opaque)."""
import re
f="styles/a-propos.css";c=open(f,encoding="utf8").read()
def sub(old,new,n=1):
    global c
    assert c.count(old)==n,(old,c.count(old));c=c.replace(old,new)
sub("gap:3rem 4rem;margin-top:1.75rem","gap:var(--rhythm-media) 4rem;margin-top:var(--rhythm-title)")
sub("margin-top:1.5rem;gap:2.5rem 2rem","margin-top:var(--rhythm-title);gap:var(--rhythm-media) 2rem")
# .mission__quote{margin-top:Xrem} (2 occurrences, hors regle principale)
c,k=re.subn(r"(\.mission__quote\{)margin-top:(?:1|0\.75)rem\}",r"\1margin-top:calc(var(--rhythm-block) - var(--rhythm-p))}",c);assert k==2,k
sub("background:rgba(16,35,63,0.88);border-radius:var(--radius-badge);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)","background:var(--clr-secondary);border-radius:var(--radius-badge)")
open(f,"w",encoding="utf8").write(c);print("ok")
