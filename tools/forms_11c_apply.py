"""T11C : mise en page formulaires Benevole / Rejoindre (feuilles locales uniquement). Usage: forms_11c_apply.py"""
import re
def rd(f): return open(f,encoding='utf8').read()
def rule(s,sel,new=None,body_re=r'[^{}]*'):
    p=re.compile(r'(?<=[}\n])'+re.escape(sel)+r'\{'+body_re+r'\}')
    m=p.findall(s); assert len(m)==1,(sel,len(m)); return p.sub(lambda _:new if new is not None else '',s,1)
f='styles/devenir-benevole.css'; s=rd(f)
s=rule(s,'.benevolat-form-grid','.benevolat-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--rhythm-block);margin-bottom:var(--rhythm-block)}')
s=rule(s,'.benevolat-field','.benevolat-field{display:flex;flex-direction:column}')
s=rule(s,'.benevolat-label')
s=rule(s,'.benevolat-consent','.benevolat-consent{margin-bottom:var(--rhythm-block)}')
s=rule(s,'.benevolat-consent label','.benevolat-consent label{font-size:var(--fs-base-sm)}')
s=rule(s,'.benevolat-consent input')
s=s.rstrip('\n')+'\n@media (max-width:767px){.benevolat-form-grid{grid-template-columns:1fr}.benevolat-form button[type="submit"]{width:100%}}\n'
# le bloc partage est en fin de fichier : on place le media avant lui
i=s.find('/* ===== Cartes (T10)')
if i>0:
    tail=s[s.rfind('\n@media (max-width:767px){.benevolat-form-grid'):]; s=s[:s.rfind('\n@media (max-width:767px){.benevolat-form-grid')]
    s=s[:i].rstrip('\n')+tail.rstrip('\n')+'\n\n'+s[i:]
open(f,'w',encoding='utf8').write(s)
f='styles/rejoindre-equipe.css'; s=rd(f)
s=rule(s,'.form-group','.form-group{margin-bottom:var(--rhythm-block)}')
s=rule(s,'.form-row','.form-row{display:grid;grid-template-columns:1fr 1fr;column-gap:var(--rhythm-block)}')
s=rule(s,'.candidature-layout label')
s=re.sub(r'(?<=[}\n])\.candidature-layout input\[type="text"\],\.candidature-layout input\[type="email"\]\{[^}]*\}','',s,count=1)
s=rule(s,'.candidature-layout input[type="file"]')
s=rule(s,'.candidature-layout input:focus-visible')
s=rule(s,'.form-consent','.form-consent{margin-bottom:var(--rhythm-block)}')
s=rule(s,'.candidature-layout .form-consent label','.candidature-layout .form-consent label{margin-bottom:0}')
s=rule(s,'.form-consent input')
j=s.find('/* ===== Cartes (T10)')
add='@media (max-width:767px){.form-row{grid-template-columns:1fr}.candidature-form button[type="submit"]{width:100%}}\n\n'
s=s[:j]+add+s[j:]
open(f,'w',encoding='utf8').write(s)
