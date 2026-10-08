import re
def rules(s):
    """yield (media_prefix, selector, body, start, end) for rules, flattening one @media level"""
    s2=re.sub(r'/\*.*?\*/',lambda m:' '*len(m.group(0)),s,flags=re.S)
    out=[];i=0;n=len(s2);stack=[]
    cur=0
    while i<n:
        c=s2[i]
        if c=='{':
            sel=s2[cur:i].strip()
            if sel.startswith('@') and not sel.startswith(('@font-face','@keyframes','@page')):
                stack.append(sel);cur=i+1
            else:
                j=s2.index('}',i)
                if sel.startswith('@keyframes'):  # skip nested
                    d=1;j=i+1
                    while d:
                        d+= (s2[j]=='{')-(s2[j]=='}');j+=1
                    j-=1
                out.append((' '.join(stack),sel,s2[i+1:j],cur,j+1));i=j;cur=j+1
        elif c=='}':
            if stack: stack.pop()
            cur=i+1
        i+=1
    return out
