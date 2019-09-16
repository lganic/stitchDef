def mk3d(width,length,height):
    out=[]
    row=[]
    import copy
    for a in range(width):
        row.append(0)
    slice=[]
    for a in range(length):
        slice.append(copy.copy(row))
    for a in range(height):
        out.append(copy.deepcopy(slice))
    return copy.deepcopy(out)

def nothing():
    import time
    time.sleep(0)

def render(matslice):
    for y in range(len(matslice)):
        out=""
        for x in range(len(matslice[0])):
            if matslice[y][x]==1:
                out+="0"
            else:
                out+=" "
        print(out)

def stitch(matrix,fname):
    import copy
    vertexMatrix=copy.deepcopy(matrix)
    nmat=copy.deepcopy(matrix)
    width=len(matrix[0][0])
    length=len(matrix[0])
    height=len(matrix)
    print("removing inner space and finding vertex points...")
    vertex=[]
    parse=0
    dx=[-1,0,1,-1,1,-1,0,1]
    dy=[-1,-1,-1,0,0,1,1,1]
    odx=[-1,0,1,-1,1,-1,0,1,0]
    ody=[-1,-1,-1,0,0,1,1,1,0]
    for z in range(height):
        for y in range(length):
            for x in range(width):
                vertexMatrix[z][y][x]=-1
                nmat[z][y][x]=0
                if matrix[z][y][x]==1:
                    if matrix[z-1][y][x]==1:
                        for d in range(8):
                            try:
                                if matrix[z][y+dy[d]][x+dx[d]]==0:
                                    nmat[z][y][x]=1
                                    break
                            except:
                                nmat[z][y][x]=1
                    else:
                        nmat[z][y][x]=1
                    if z==0 or z==height-1 and matrix[z][y][x]==1:
                        nmat[z][y][x]=1
                    if nmat[z][y][x]==1:
                        vertexMatrix[z][y][x]=parse
                        parse+=1
                        vertex.append((x,y,z))
        render(nmat[z])
        print("")
    print("begin layer by layer scan...")
    faces=[]
    for z in range(height):
        print("("+str(z+1)+"/"+str(height)+")")
        for y in range(length):
            for x in range(width):
                if z!=height-1:
                    if nmat[z][y][x]==1:
                        ua=vertexMatrix[z][y][x]
                        ub=-1
                        la=-1
                        lb=-1
                        for d in range(9):
                            try:
                                if nmat[z][y+ody[d]][x+odx[d]]==1 and ub==-1 and d!=8:
                                    ub=vertexMatrix[z][y+ody[d]][x+odx[d]]
                            except:
                                nothing()
                            try:
                                if nmat[z+1][y+ody[d]][x+odx[d]]==1:
                                    if la==-1:
                                        la=vertexMatrix[z+1][y+ody[d]][x+odx[d]]
                                    elif lb==-1:
                                        lb=vertexMatrix[z+1][y+ody[d]][x+odx[d]]
                            except:
                                nothing()
                        if ub!=-1 and la!=-1 and lb!=-1:
                            faces.append((ua,ub,lb))
                            faces.append((la,lb,ua))
                            faces.append((ua,ub,la))
        for y in range(length-1):
            for x in range(width-1):
                if nmat[z][y][x]==1 and nmat[z][y+1][x]==1 and nmat[z][y][x+1]==1 and nmat[z][y+1][x+1]==1:
                    a=vertexMatrix[z][y+1][x]
                    b=vertexMatrix[z][y][x+1]
                    c=vertexMatrix[z][y+1][x+1]
                    d=vertexMatrix[z][y][x]
                    faces.append((a,c,d))
                    faces.append((a,d,b))
    print("generating file...")
    f=open(fname+".obj","w")
    f.write("#auto generated stitch\n\ng\n")
    for v in vertex:
        f.write("v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n")
    for face in faces:
        f.write("f "+str(face[0]+1)+" "+str(face[1]+1)+" "+str(face[2]+1)+"\n")
    f.write("#"+str(len(vertex))+" vertices "+str(len(faces))+" faces")
    f.close()


#testmat=[]
#temp=[]
#t=[]
#import copy
#for a in range(100):
#    t.append(0)
#for a in range(50):
#    temp.append(copy.copy(t))
#for a in range(50):
#    for b in range(50):
#        temp[a][b+25]=1
#for a in range(50):
#    testmat.append(copy.deepcopy(temp))
#stitch(testmat,"test")

def text(screen,x,y,text,size=100,color=(255,255,255),font="arialms"):
    pygame.font.init()
    font=pygame.font.SysFont(font,size,bold=False)
    text=font.render(text,1,color)
    textpos=text.get_rect()
    textpos[0]=x
    textpos[1]=y
    screen.blit(text,textpos)
    return textpos

import copy,math
text1=input("forward text ")
text2=input("side text ")
import pygame
screen=pygame.display.set_mode((700,700))
screen.fill((0,0,0))
r1=text(screen,0,0,text1)
r2=text(screen,0,r1[3],text2)
pygame.display.flip()
m1=[]
m2=[]
for y in range(r1[3]):
    v=copy.copy([])
    for x in range(r1[2]):
        if screen.get_at((x,y))==(255,255,255):
            v.append(1)
        else:
            v.append(0)
    m1.append(v)
for y in range(r2[3]):
    v=copy.copy([])
    for x in range(r2[2]):
        if screen.get_at((x,y+r1[3]))==(255,255,255):
            v.append(1)
        else:
            v.append(0)
    m2.append(v)
render(m1)
render(m2)
pygame.quit()
depth=int((2*r2[2])/math.sqrt(2))-r1[2]+1
if depth<0:
    print("depth error",depth)
    input()
h=r1[3]
mat=mk3d(r1[2],depth,h)
for x in range(r1[2]):
    for z in range(h):
        if m1[z][x]==1:
            for y in range(depth):
                mat[z][y][x]=1
stitch(mat,"other")
fs=r2[2]-math.sin(math.radians(45))*r1[2]
sq=math.sqrt(2)
nmat=copy.deepcopy(mat)
for n in range(r2[2]):
    if n<fs:
        y=n*sq
        x=0
    else:
        y=depth-1
        x=(n-fs)*sq
    y1=int(y)
    x1=int(x)
    for z in range(h):
        y=y1
        x=x1
        while x<r1[2] and y>0:
            for d in range(2):
                try:
                    if mat[z][y][x]==1:
                        nmat[z][y][x+d]=m2[z][n]
                except:
                    nothing()
            x+=1
            y-=1
stitch(nmat,"finish")
