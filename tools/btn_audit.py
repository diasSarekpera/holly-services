import re,glob,os,json,collections
root='.'
pat=re.compile(r'(^|[-_])(btn|button|cta)($|[-_])|btn|cta',re.I)
html=glob.glob('*.html')+glob.glob('pages/*.html')
H=collections.defaultdict(lambda:collections.Counter())
tagre=re.compile(r'<(a|button)\b([^>]*)>',re.I)
for f in html:
    s=open(f,encoding='utf8').read()
    # strip partial-injected? keep all
    for m in tagre.finditer(s):
        cm=re.search(r'class="([^"]*)"',m.group(2))
        if not cm: continue
        for c in cm.group(1).split():
            if pat.search(c): H[c][os.path.basename(f)]+=1
C=collections.defaultdict(set)
for f in glob.glob('styles/**/*.css',recursive=True):
    s=open(f,encoding='utf8').read()
    for c in set(re.findall(r'\.([a-zA-Z_][\w-]*)',re.sub(r'/\*.*?\*/','',s,flags=re.S))):
        if pat.search(c): C[c].add(os.path.basename(f))
allc=sorted(set(H)|set(C))
out={c:{'html':dict(H[c]),'css':sorted(C[c])} for c in allc}
json.dump(out,open('/tmp/btn_inv.json','w'),indent=1)
print(len(allc),'classes')
for c in allc:
    print(c,sum(H[c].values()),len(H[c]),len(C[c]))
