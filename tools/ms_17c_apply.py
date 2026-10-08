p='styles/mission-sante.css'; s=open(p,encoding='utf-8').read()
def sub(a,b):
    global s
    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
sub('.mission-detail__intro{margin-bottom:3rem}','.mission-detail__intro{margin-bottom:var(--rhythm-media)}') if '.mission-detail__intro{margin-bottom:3rem}' in s else sub('.mission-detail__intro { margin-bottom:3rem }','.mission-detail__intro { margin-bottom:var(--rhythm-media) }')
s=s.rstrip('\n')+'\n/* 17C : cibles tactiles >= 44 px pour le sélecteur de missions (mobile) */\n@media (max-width:767px){.mission-detail__selector-link{display:inline-flex;align-items:center;min-height:44px}}\n'
open(p,'w',encoding='utf-8').write(s)
