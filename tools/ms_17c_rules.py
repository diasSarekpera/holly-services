import re,sys
s=open('styles/'+__import__('sys').argv[2]+'.css',encoding='utf-8').read()
pat=re.compile(sys.argv[1])
for m in re.finditer(r'([^{}]+)\{([^{}]*)\}',s):
    sel=m.group(1).strip().split('*/')[-1].strip()
    if pat.search(sel) and not sel.startswith(('@',)):
        print(sel[:110],'{',m.group(2)[:230],'}')
