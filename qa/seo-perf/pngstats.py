import struct, zlib, sys, os
def read_png(path):
    d=open(path,'rb').read()
    assert d[:8]==b'\x89PNG\r\n\x1a\n'
    pos=8; idat=b''; w=h=bd=ct=il=None
    while pos<len(d):
        ln=struct.unpack('>I',d[pos:pos+4])[0]; typ=d[pos+4:pos+8]; body=d[pos+8:pos+8+ln]; pos+=12+ln
        if typ==b'IHDR': w,h,bd,ct,_,_,il=struct.unpack('>IIBBBBB',body)
        elif typ==b'IDAT': idat+=body
        elif typ==b'IEND': break
    return w,h,bd,ct,il,idat
def decode(path):
    w,h,bd,ct,il,idat=read_png(path)
    ch={2:3,6:4,0:1,4:2}[ct]
    raw=zlib.decompress(idat); stride=w*ch; out=[]; prev=bytearray(stride); p=0
    for y in range(h):
        f=raw[p]; p+=1; line=bytearray(raw[p:p+stride]); p+=stride
        for i in range(stride):
            a=line[i-ch] if i>=ch else 0; b=prev[i]; c=prev[i-ch] if i>=ch else 0
            if f==1: line[i]=(line[i]+a)&255
            elif f==2: line[i]=(line[i]+b)&255
            elif f==3: line[i]=(line[i]+((a+b)>>1))&255
            elif f==4:
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
                line[i]=(line[i]+pr)&255
        out.append(bytes(line)); prev=line
    return w,h,ct,ch,out
root="C:/Users/TEST/OneDrive/Documents/GodSquad Website/images/"
for n in ['hero-group.png','icons-sprite.png','social-sprite.png','logo.png']:
    w,h,bd,ct,il,_=read_png(root+n); print(f'{n}: {w}x{h} bitdepth={bd} colortype={ct} ({ {0:"gray",2:"RGB",4:"gray+alpha",6:"RGBA"}[ct] }) interlace={il} bytes={os.path.getsize(root+n)}')
for n in ['WHITE FONT LOGO.png','icon-globe.png','icon-search.png','icon-account.png','icon-cart.png','icon-crown.png','icon-community.png','icon-diamond.png','icon-facebook.png','icon-instagram.png']:
    w,h,ct,ch,rows=decode(root+n)
    if ch!=4: print(n,'not RGBA'); continue
    opaque=semi=0; minx,miny,maxx,maxy=w,h,-1,-1; cols={}; fringe=0
    for y,row in enumerate(rows):
        for x in range(w):
            r,g,b,a=row[4*x:4*x+4]
            if a==0: continue
            if a==255: opaque+=1
            else: semi+=1
            minx=min(minx,x);miny=min(miny,y);maxx=max(maxx,x);maxy=max(maxy,y)
            if a>=200:
                k=(r//16*16,g//16*16,b//16*16); cols[k]=cols.get(k,0)+1
            # fringe: semi-transparent pixel whose colour is far from the dominant later
    top=sorted(cols.items(),key=lambda kv:-kv[1])[:2]
    bw,bh=maxx-minx+1,maxy-miny+1
    print(f'{n}: {w}x{h} opaque={opaque} semi={semi} ({semi*100//max(1,opaque+semi)}% of visible px semi-transparent) visible_bbox={bw}x{bh} at ({minx},{miny}) = {bw*100//w}% x {bh*100//h}% of canvas; dominant opaque colours={top}')
