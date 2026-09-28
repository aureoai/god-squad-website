import sys,os
sys.path.insert(0,r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad")
from pngtool import read_png
im=read_png(sys.argv[1]); y0=int(sys.argv[2]); y1=int(sys.argv[3])
cols=set()
for y in range(y0,min(y1,im.h),3):
    for x in range(0,im.w,3):
        cols.add(im.px(x,y))
print(len(cols))
