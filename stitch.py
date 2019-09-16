class vectorArray:
    class vector:
        def __init__(self,value,globalTarget=-1,localTarget=-1):
            self.value=value
            self.globalTarget=globalTarget
            self.localTarget=localTarget
    def __init__(self):
        self.array=[]
    def addPoint(self,value,globalTarget,localTarget):
        self.array.append(vector(value,globalTarget,localTarget))
    def check(self,value):
        for vec in self.array:
            if vec.value==value:
                return False
        return True
    def findIndex(self,value):
        for a in range(len(self.array)):
            if self.array[a].value==value:
                return a
        return -1
    def getTrigonalVectors(self,value):
        index=findIndex(value)
        currentVector=self.array[index]
        upperValA=currentVector.value
        upperValB=currentVector.localTarget
        targetVector=self.array[currentVector.globalTarget]
        lowerValA=targetVector.value
        lowerValB=targetVector.localTarget
        return [(upperValA,upperValB,lowerValB),(upperValA,lowerValA,lowerValB),(upperValA,upperValB,lowerValB)]

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

