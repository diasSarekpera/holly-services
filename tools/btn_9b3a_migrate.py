import re,glob,hashlib,sys
# HTML
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf8').read();o=s
    s=s.replace('class="navbar__cta"','class="navbar__cta btn btn--primary btn--sm"').replace('class="mobile-menu__cta"','class="mobile-menu__cta btn btn--primary btn--block"')
    if s!=o: open(f,'w',encoding='utf8').write(s)
# CSS
pat=re.compile(r'(?<![\w-])\.(?:navbar__cta|mobile-menu__cta)(?::hover|:focus-visible)?(?:\s+svg)?\s*\{[^{}]*\}')
for f in glob.glob('styles/*.css'):
    s=open(f,encoding='utf8').read();o=s
    if 'navbar__cta' not in s: continue
    s=pat.sub(lambda m:'.mobile-menu__cta{flex:1.4}' if m.group(0).startswith('.mobile-menu__cta{flex:1.4') else '',s)
    s=re.sub(r'@media[^{}]*\{\s*\}','',s)
    s=s.rstrip('\n')+'\n/* Header CTA (T9B3a) */\n.navbar__cta{flex-shrink:0;white-space:nowrap}\n.mobile-menu__cta{margin:0}\n'
    open(f,'w',encoding='utf8').write(s)
