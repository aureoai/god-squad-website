def lin(c):
    c=c/255
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(r,g,b): return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def ratio(a,b):
    la,lb=L(*a),L(*b)
    hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)
def comp(fg,a,bg): return tuple(a*f+(1-a)*b for f,b in zip(fg,bg))
ink=(13,12,10); cream=(243,239,230); tile=(235,230,220); gold=(216,192,138)
print("border .12 on ink      ", round(ratio(comp(cream,0.12,ink),ink),3))
print("border-inv .14 on cream", round(ratio(comp(ink,0.14,cream),cream),3))
print("border-sub .08 on ink  ", round(ratio(comp(cream,0.08,ink),ink),3))
print("swatch ring .25 on cream", round(ratio(comp((0,0,0),0.25,cream),cream),3))
print("swatch ring .25 on tile ", round(ratio(comp((0,0,0),0.25,tile),tile),3))
print("ring vs cream swatch fill", round(ratio(comp((0,0,0),0.25,cream),cream),3))
print("5F5A50 on cream        ", round(ratio((0x5F,0x5A,0x50),cream),3))
print("gold on cream          ", round(ratio(gold,cream),3))
print("footer vdiv .2 on ink  ", round(ratio(comp(cream,0.2,ink),ink),3))
