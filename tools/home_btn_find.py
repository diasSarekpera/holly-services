import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
cls=['btn--donate-primary','btn--donate-inline','btn--donate-inline--edu','btn--donate-inline--social','soutenir__way-btn','soutenir__way-btn--primary','soutenir__way-btn--secondary','soutenir__way-btn--tertiary','hero__cta-primary','hero__cta-secondary']
h=open('index.html',encoding='utf8').read()
for m in re.finditer(r'<(a|button)\b[^>]*class="[^"]*(?:%s)[^"]*"[^>]*>'%'|'.join(re.escape(c) for c in ['donate','way-btn','hero__cta']),h):
    print(m.start(),m.group(0)[:230])
s=open('styles/home.css',encoding='utf8').read()
print('---CSS')
for mp,sel,body,a,b in rules(s):
    if any(k in sel for k in ['donate','way-btn','hero__cta','__cta','btn']) and 'T9' not in sel and not sel.startswith('.btn'):
        print(mp,'|',sel[:100],'|',body[:260])
