import re,hashlib
P=['mentions-legales','conditions-utilisation','politique-confidentialite']
CSS='''
/* Pages legales (22A) : sommaire >= 44 px, listes visibles, marqueurs [A COMPLETER] discrets. Bloc identique dans les 3 feuilles legales. */
.legal-toc__list{gap:0}
.legal-toc__list a{display:flex;align-items:center;min-height:44px;overflow-wrap:anywhere}
.legal-section ul,.legal-box__list{list-style:disc}
.legal-section ol{list-style:decimal}
.legal-section ul,.legal-section ol,.legal-box__list{padding-left:0.25rem}
.legal-section li{line-height:var(--lh-compact);overflow-wrap:break-word}
.legal-section li + li,.legal-box__list li + li{margin-top:0.5rem}
.legal-section li::marker,.legal-box__list li::marker{color:var(--clr-accent-dark)}
.legal-todo{color:var(--clr-text-soft);font-style:italic;border-bottom:1px dashed var(--clr-border-btn)}
'''
h=set()
for p in P:
    f=f'styles/{p}.css';s=open(f,encoding='utf-8').read()
    if '(22A)' not in s: s=s.rstrip('\n')+'\n'+CSS
    open(f,'w',encoding='utf-8').write(s); h.add(hashlib.md5(CSS.encode()).hexdigest())
    f=f'pages/{p}.html';t=open(f,encoding='utf-8').read()
    t2=re.sub(r'(?<!>)(\[À COMPLÉTER[^\]]*\])',r'<span class="legal-todo">\1</span>',t) if 'legal-todo' not in t else t
    open(f,'w',encoding='utf-8').write(t2); print(p,t2.count('legal-todo'))
print('hash bloc CSS unique:',len(h)==1,h)
