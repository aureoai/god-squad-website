import sys,os,zlib,struct
sys.path.insert(0,r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad")
from pngtool import read_png
def write_png(path,w,h,ch,buf):
    raw=bytearray()
    stride=w*ch
    for y in range(h):
        raw.append(0); raw+=buf[y*stride:(y+1)*stride]
    ct={1:0,3:2,4:6}[ch]
    def chunk(t,d):
        c=struct.pack('>I',len(d))+t+d
        return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    out=b'\x89PNG\r\n\x1a\n'
    out+=chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,ct,0,0,0))
    out+=chunk(b'IDAT',zlib.compress(bytes(raw),6))
    out+=chunk(b'IEND',b'')
    open(path,'wb').write(out)
def crop(src,dst,w,h):
    im=read_png(src)
    assert im.w>=w and im.h>=h,(im.w,im.h,w,h)
    ch=im.ch; stride=im.w*ch; out=bytearray(w*h*ch)
    for y in range(h):
        out[y*w*ch:(y+1)*w*ch]=im.buf[y*stride:y*stride+w*ch]
    write_png(dst,w,h,ch,out)
if __name__=='__main__':
    crop(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
    print('cropped',sys.argv[2],sys.argv[3],sys.argv[4])
