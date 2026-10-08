import re,sys
sys.path.insert(0,'tools')
from css_rules import rules
f,pat=sys.argv[1],sys.argv[2]
s=open('styles/'+f,encoding='utf8').read(); i=s.find('/* ===== Cartes (T10)'); j=s.find('/* ===== fin Cartes (T10)')
s=s[:i]+' '*(j-i)+s[j:]
for m,sel,body,a,b in rules(s):
    if re.search(pat,sel): print(a,(m or '-')[:22],sel.strip()[:60].replace('\n',' '),'{',' '.join(body.split())[:330],'}')
