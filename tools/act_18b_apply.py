p='styles/actualites.css'; s=open(p,encoding='utf-8').read()
a='.actualites-pagination{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:0.5rem;margin-top:4rem}'
if a not in s: a=a.replace('{','{ ',1).replace('}',' }').replace(';',';') 
import re
m=re.search(r'\.actualites-pagination\s*\{[^}]*margin-top:\s*4rem\s*\}',s); assert m
s=s.replace(m.group(0),m.group(0).replace('margin-top:4rem','margin-top:var(--rhythm-media)').replace('margin-top: 4rem','margin-top:var(--rhythm-media)'))
s=s.rstrip('\n')+'\n/* 18B : pagination — cibles tactiles >= 44 px (mobile) */\n@media (max-width:767px){.actualites-page{width:44px;height:44px}.actualites-pagination{gap:0.5rem}}\n'
open(p,'w',encoding='utf-8').write(s)
