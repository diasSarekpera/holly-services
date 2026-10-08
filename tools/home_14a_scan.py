#!/usr/bin/env python3
"""14A : liste, dans styles/home.css, les regles des sections hero/about/missions contenant blur, transform au survol, fond rose, ou tailles/marges en dur sur titres/en-tetes."""
import re,sys
css=open('styles/home.css',encoding='utf8').read()
pat=re.compile(r'([^{}@]+)\{([^{}]*)\}')
sec=re.compile(r'\.(hero|about|mission)')
bad=[('blur',r'backdrop-filter:\s*blur|filter:\s*blur'),('transform-hover',r':hover[^{]*\{[^}]*transform:\s*translate'),('rose',r'rgba\(\s*(2[0-9]{2}\s*,\s*(1[0-9]{2}|2[0-9]{2}))')]
for m in pat.finditer(css):
    s,b=m.group(1).strip(),m.group(2)
    if not sec.search(s): continue
    if re.search(r'backdrop-filter:\s*blur|(?<!-)filter:\s*blur',b): print('BLUR',s[:70],'|',b[:110])
    if ':hover' in s and re.search(r'translate|scale',b): print('HOVERMOVE',s[:70],'|',b[:110])
    if re.search(r'__(card|item)',s) and re.search(r'box-shadow|border',b): print('CARD',s[:60],'|',re.findall(r'(?:border|box-shadow|background)[a-z-]*:[^;]+',b)[:3])
