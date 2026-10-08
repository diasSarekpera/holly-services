import re,sys
p='styles/nos-missions.css'; s=open(p,encoding='utf-8').read(); o=s
def sub(a,b):
    global s
    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
sub('.missions-intro{margin-bottom:3rem;padding-bottom:3rem;','.missions-intro{margin-bottom:var(--rhythm-media);padding-bottom:var(--rhythm-media);')
sub('.missions-anchors__link{display:flex;align-items:center;gap:0.5rem;padding:1rem 1.5rem;','.missions-anchors__link{display:flex;align-items:center;gap:0.5rem;min-height:44px;padding:0.75rem 1.5rem;')
sub('.missions-anchors__link:hover{border-color:var(--clr-primary)}','.missions-anchors__link:hover{border-color:var(--clr-border-hover)}')
sub('.resultats{background-color:var(--clr-secondary);color:var(--clr-white);padding:5rem 0','.resultats{background-color:var(--clr-secondary);color:var(--clr-white);padding:var(--section-pad-y) 0')
s=s.replace('gap:2rem;margin-top:3rem','gap:2rem;margin-top:var(--rhythm-media)')
open(p,'w',encoding='utf-8').write(s)
print(len(o),len(s))
