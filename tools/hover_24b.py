import re,sys,glob,hashlib,collections
HOVER=re.compile(r':hover')
def skip_str(t,i):
    q=t[i];i+=1
    while i<len(t) and t[i]!=q: i+= 2 if t[i]=='\\' else 1
    return i+1
def read_prelude(t,i):
    j=i;par=0
    while j<len(t):
        c=t[j]
        if c=='/' and t[j:j+2]=='/*': j=t.index('*/',j)+2;continue
        if c in '"\'': j=skip_str(t,j);continue
        if c=='(' or c=='[': par+=1
        elif c==')' or c==']': par-=1
        elif par<=0 and c in '{;}': return j
        j+=1
    return j
def match_brace(t,i):
    d=0;j=i
    while j<len(t):
        c=t[j]
        if c=='/' and t[j:j+2]=='/*': j=t.index('*/',j)+2;continue
        if c in '"\'': j=skip_str(t,j);continue
        if c=='{': d+=1
        elif c=='}':
            d-=1
            if d==0: return j
        j+=1
    raise ValueError('brace')
def split_sel(p):
    out=[];d=0;cur='';i=0
    while i<len(p):
        c=p[i]
        if c in '([': d+=1
        elif c in ')]': d-=1
        if c==',' and d==0: out.append(cur);cur=''
        else: cur+=c
        i+=1
    out.append(cur);return out
ST=collections.Counter();WRAPPED=[]
def process(t,hov,f):
    out=[];i=0;n=len(t)
    while i<n:
        m=re.compile(r'\s+|/\*.*?\*/',re.S).match(t,i)
        if m: out.append(m.group(0));i=m.end();continue
        j=read_prelude(t,i)
        if j>=n: out.append(t[i:]);break
        if t[j]==';': out.append(t[i:j+1]);i=j+1;continue
        if t[j]=='}': out.append(t[i:j]);i=j;break
        pre=t[i:j];e=match_brace(t,j);body=t[j+1:e];low=pre.strip().lower()
        if low.startswith('@'):
            if re.match(r'@(-\w+-)?(keyframes|font-face|page|property|counter-style)',low): out.append(pre+'{'+body+'}')
            else:
                h=hov or bool(re.search(r'hover\s*:\s*hover',low))
                out.append(pre+'{'+process(body,h,f)+'}')
        else:
            sels=split_sel(pre)
            hs=[s for s in sels if HOVER.search(s)];ns=[s for s in sels if not HOVER.search(s)]
            if not hs or hov: out.append(pre+'{'+body+'}')
            else:
                bad=[s for s in hs if ':not(:hover)' in s.replace(' ','')]
                ST['not_hover']+=len(bad)
                if ns: out.append(','.join(ns)+'{'+body+'}')
                lead=re.match(r'\s*',pre).group(0)
                w=','.join(s.strip() for s in hs)+'{'+body+'}'
                WRAPPED.append((f,w))
                out.append(lead+'@media (hover:hover){'+w+'}');ST['wrapped']+=1
        i=e+1
    return ''.join(out)
def audit(t,hov=False):
    """compte les regles :hover hors @media(hover:hover)"""
    bad=0;tot=0;i=0;n=len(t)
    while i<n:
        m=re.compile(r'\s+|/\*.*?\*/',re.S).match(t,i)
        if m: i=m.end();continue
        j=read_prelude(t,i)
        if j>=n or t[j]==';': i=j+1;continue
        if t[j]=='}': break
        pre=t[i:j];e=match_brace(t,j);body=t[j+1:e];low=pre.strip().lower()
        if low.startswith('@'):
            if not re.match(r'@(-\w+-)?(keyframes|font-face)',low):
                b,a=audit(body,hov or bool(re.search(r'hover\s*:\s*hover',low)));bad+=b;tot+=a
        elif HOVER.search(pre):
            tot+=1
            if not hov: bad+=1
        i=e+1
    return bad,tot
if __name__=='__main__':
    mode=sys.argv[1];B=T=0
    for f in sorted(glob.glob('styles/*.css')):
        s=open(f,encoding='utf-8').read()
        if mode=='scan': b,a=audit(s);B+=b;T+=a;print(f.split('/')[-1].ljust(34),'hover hors media:',b,'/',a)
        elif mode=='apply':
            o=s;t=process(s,False,f)
            assert t.count('{')==t.count('}'),f
            if t!=o: open(f,'w',encoding='utf-8').write(t)
        elif mode=='verify':
            b,a=audit(s);B+=b;T+=a;assert s.count('{')==s.count('}'),f
    if mode=='apply': print(dict(ST))
    else: print('TOTAL hors media:',B,'sur',T)
