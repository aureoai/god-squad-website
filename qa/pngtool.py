import zlib, struct, sys
def read_png(path):
    data=open(path,'rb').read(); assert data[:8]==b'\x89PNG\r\n\x1a\n'
    pos=8; idat=[]
    while pos<len(data):
        ln,=struct.unpack('>I',data[pos:pos+4]); typ=data[pos+4:pos+8]; chunk=data[pos+8:pos+8+ln]; pos+=12+ln
        if typ==b'IHDR': w,h,bd,ct,cm,fm,il=struct.unpack('>IIBBBBB',chunk)
        elif typ==b'IDAT': idat.append(chunk)
        elif typ==b'IEND': break
    assert bd==8 and il==0,(bd,il); ch={0:1,2:3,4:2,6:4}[ct]
    raw=zlib.decompress(b''.join(idat)); stride=w*ch; out=bytearray(h*stride); prev=bytearray(stride); p=0
    for y in range(h):
        ft=raw[p]; p+=1; line=bytearray(raw[p:p+stride]); p+=stride
        if ft==1:
            for i in range(ch,stride): line[i]=(line[i]+line[i-ch])&255
        elif ft==2:
            for i in range(stride): line[i]=(line[i]+prev[i])&255
        elif ft==3:
            for i in range(stride): a=line[i-ch] if i>=ch else 0; line[i]=(line[i]+((a+prev[i])>>1))&255
        elif ft==4:
            for i in range(stride):
                a=line[i-ch] if i>=ch else 0; b=prev[i]; c=prev[i-ch] if i>=ch else 0
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr=a if (pa<=pb and pa<=pc) else (b if pb<=pc else c)
                line[i]=(line[i]+pr)&255
        out[y*stride:(y+1)*stride]=line; prev=line
    class Img:
        pass
    im=Img(); im.w=w; im.h=h; im.ch=ch; im.buf=out
    def px(x,y):
        o=(y*w+x)*ch
        if ch>=3: return (out[o],out[o+1],out[o+2])
        return (out[o],out[o],out[o])
    im.px=px; return im
def bbox(im,box,pred):
    x0,y0,x1,y1=box; xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(im.px(x,y)): xs.append(x); ys.append(y)
    if not xs: return None
    return dict(x0=min(xs),y0=min(ys),x1=max(xs),y1=max(ys),w=max(xs)-min(xs)+1,h=max(ys)-min(ys)+1)
bright=lambda c: c[0]>200 and c[1]>200 and c[2]>200
def runs(xs):
    r=[]
    for x in xs:
        if r and x==r[-1][1]+1: r[-1][1]=x
        else: r.append([x,x])
    return r
