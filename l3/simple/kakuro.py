import itertools
import sys

def parseInput(inputFile):
    file1= open(inputFile,'r')
    r =0
    c =0
    horizontalEnable =0
    verticalEnable =0
    horizontalData = []
    verticalData = []
    for line in file1:
        if(line[0:4] == 'rows'):
            rowSize = int(line[5:len(line)-1]) 
        elif(line[0:7] == 'columns'):
            columnSize = int(line[8:len(line)-1])
        elif(line[0:len(line)-1]=='Horizontal'):
            #print("Horizontal detected")
            horizontalEnable =1;
        elif(line[0:len(line)-1]=='Vertical'):
            #print("Vertical detected")
            horizontalEnable =0;
            verticalEnable = 1;
            r=0

        if(horizontalEnable == 1):
            for line in file1:
                horizontalData.append(line[0:len(line)-1].split(","))
                r +=1
                if(r==rowSize):
                    break
        if(verticalEnable == 1):
            for line in file1:
                verticalData.append(line[0:len(line)-1].split(","))
                r +=1
                if(r==rowSize):
                    break
    
    #verticalData.pop()
    # print(horizontalData)
    # print(verticalData)
        
    return rowSize,columnSize,horizontalData,verticalData

def allPossibleCombinations(total, n):
    values = [1,2,3,4,5,6,7,8,9]
    allCombinations = []
    for combination in itertools.combinations(values,n):
        if sum(combination)==total:
            for perm in itertools.permutations(combination):
                allCombinations.append(perm)
    return allCombinations

def makeConstraintMartix(rowSize,columnSize,horizontalData,verticalData):
    constraintMatrix = []
    uConstraint = [0]*rowSize*columnSize
    isCountingZeroes = False
    noOfOnes =0
    isUvariableComplete = False
    positionsOfZero = []
    noOfTimes = rowSize*columnSize
    position  = 0
    uVariable = 0;
    UDomain = {}
    XDomain = {}
    UNeighbour = {}
    XNeighbour = {}
    UPosition =0
    neighbour = []
    q= []
    Uposition = {}
    
    
    #adding variables in horizontal matrix to constarint matrix
    for list in horizontalData:
        for value in list:
            if(value == '#'):
                position +=1
                if(isCountingZeroes):
                    for pos in positionsOfZero:
                        uConstraint[pos-1]=1
                        q.append((pos,uVariable,0))
                        Uposition[(uVariable,pos)] = noOfOnes
                        noOfOnes += 1
                    noOfOnes =0;
                    UDomain[uVariable] = (allPossibleCombinations(total,len(positionsOfZero)))
                    uVariable += 1
                    positionsOfZero.clear()
                    constraintMatrix.append(uConstraint)
                    uConstraint = [0]*rowSize*columnSize
                    isCountingZeroes = False
            
            elif (int(value) == 0):
                position +=1
                XDomain[position] = set(range(1,10))
                positionsOfZero.append(position)
            
            elif(int(value) > 0):
                if(isCountingZeroes):
                    for pos in positionsOfZero:
                        uConstraint[pos-1]=1
                        q.append((pos,uVariable,0))
                        Uposition[(uVariable,pos)] = noOfOnes
                        noOfOnes += 1
                    noOfOnes =0
                    UDomain[uVariable] = allPossibleCombinations(total,len(positionsOfZero))
                    uVariable += 1
                    constraintMatrix.append(uConstraint)
                    positionsOfZero.clear()
                    uConstraint = [0]*rowSize*columnSize
                position +=1
                total = int(value)
                isCountingZeroes = True
   
        if(isCountingZeroes):
            for pos in positionsOfZero:
                uConstraint[pos-1]=1
                q.append((pos,uVariable,0))
                Uposition[(uVariable,pos)] = noOfOnes
                noOfOnes += 1
            noOfOnes =0
            UDomain[uVariable] = allPossibleCombinations(total,len(positionsOfZero))
            uVariable += 1
            constraintMatrix.append(uConstraint)
            positionsOfZero.clear()
            uConstraint = [0]*rowSize*columnSize
            isCountingZeroes = False
    

    position =0
    #adding variables in vertical matrix
    for i in range(columnSize):
        for j in range(rowSize):
            value = verticalData[j][i]
            if(value == '#'):
                if(isCountingZeroes):
                    for pos in positionsOfZero:
                        uConstraint[pos-1]=1
                        q.append((pos,uVariable,0))
                        Uposition[(uVariable,pos)] = noOfOnes
                        noOfOnes += 1
                    noOfOnes =0
                    UDomain[uVariable] = allPossibleCombinations(total,len(positionsOfZero))
                    uVariable += 1
                    positionsOfZero.clear()
                    constraintMatrix.append(uConstraint)
                    uConstraint = [0]*rowSize*columnSize
                    isCountingZeroes = False
            
            elif (int(value) == 0):
                position = j*columnSize + i+1
                XDomain[position] = set(range(1,10))
                positionsOfZero.append(position)
            
            elif(int(value) > 0):
                if(isCountingZeroes):   
                    for pos in positionsOfZero:
                        uConstraint[pos-1]=1
                        q.append((pos,uVariable,0))
                        Uposition[(uVariable,pos)] = noOfOnes
                        noOfOnes += 1
                    noOfOnes =0
                    UDomain[uVariable] = allPossibleCombinations(total,len(positionsOfZero))
                    uVariable += 1
                    constraintMatrix.append(uConstraint)
                    positionsOfZero.clear()
                    uConstraint = [0]*rowSize*columnSize                
                total = int(value)
                isCountingZeroes = True
        
        if(isCountingZeroes):
            
            for pos in positionsOfZero:
                uConstraint[pos-1]=1
                q.append((pos,uVariable,0))
                Uposition[(uVariable,pos)] = noOfOnes
                noOfOnes += 1
            noOfOnes =0
            UDomain[uVariable] = allPossibleCombinations(total,len(positionsOfZero))
            uVariable += 1
            constraintMatrix.append(uConstraint)
            positionsOfZero.clear()
            uConstraint = [0]*rowSize*columnSize
            isCountingZeroes = False   
              
    
    #printing the UDomain
    # for key,value in UDomain.items():
    #     print(key," : ",value)

    # for key1,value1 in XDomain.items():
    #     print(key1," : ",value1
    # print(q)
    # print(Uposition)
    return constraintMatrix,UDomain,XDomain,q,Uposition
    
def AC3(constraintMatrix,UDomain,XDomain,q,UPosition):
    while len(q) != 0:
        arc=q.pop(0)
        revicedStatus,UpdatedDomain=REVICE(constraintMatrix,UDomain,XDomain,arc,UPosition)
        if(revicedStatus):
            if(len(UpdatedDomain)==0):
                return False,UDomain,XDomain
            
            if(arc[2]==0):
                XDomain[arc[0]] = UpdatedDomain
                for i in range(len(constraintMatrix)):
                    if(constraintMatrix[i][arc[0]-1]==1):
                        if(i!=arc[1]):
                            q.append((i,arc[0],1))
            
            
            elif(arc[2]==1):
                UDomain[arc[0]] = UpdatedDomain
                for i in range(len(constraintMatrix[arc[0]])):
                    if(i+1!=arc[1]):
                        if constraintMatrix[arc[0]][i] == 1:
                            q.append((i+1,arc[0],0))
    
    return True,UDomain,XDomain          

def REVICE(constraintMatrix,UDomain,XDomain,arc,UPosition):
    newDomain=set()
    
    flag =0
    reviced = False
    if(arc[2]==0):
        for val in XDomain[arc[0]]:
            newDomain.add(val)

        for val in XDomain[arc[0]]:
            flag =0
            for UVal in UDomain[arc[1]]:
                if(val == UVal[UPosition[(arc[1],arc[0])]]):
                    flag =1    
                    break
            if flag ==0:
                newDomain.remove(val)
                reviced = True
    elif(arc[2]==1):
        for UVal in UDomain[arc[0]]:
            newDomain.add(UVal)
        
        for UVal in UDomain[arc[0]]:
            flag =0
            for val in XDomain[arc[1]]:
                if(UVal[UPosition[(arc[0],arc[1])]] == val):
                    flag =1 
                    break
            if(flag ==0):
                newDomain.remove(UVal)
                reviced = True

    return reviced,newDomain

def BS(assignment,XDomain,UDomain,constraintMatrix,UPosition,noOfBT):
    temp ={}
    complete = True
    for key,value in assignment.items():
        if value == -1:
            complete = False
            break

    if(complete):
        return True,assignment,noOfBT

    #print(key)
    for val in XDomain[key]:
        if(CONSISTENT(val,key,XDomain,UDomain,constraintMatrix,assignment,UPosition)):
            assignment[key] = val
            result,temp,noOfBT = BS(assignment,XDomain,UDomain,constraintMatrix,UPosition,noOfBT)
            if result:
                return result,assignment,noOfBT
            assignment[key] = -1
        noOfBT += 1
    
    return False,assignment,noOfBT     

def CONSISTENT(val,key,XDomain,UDomain,constraintMatrix,assignment,UPosition):
    Xneighbour =[]
    consitent = False
    for i in range(len(constraintMatrix)):
        if(constraintMatrix[i][key-1]==1):
            Xneighbour.append(i)
    for n in Xneighbour:
        for Ud in UDomain[n]:
            consistent = True
            for j in range(len(constraintMatrix[n])):
                if(constraintMatrix[n][j] == 1):
                    if(assignment[j+1]!=-1):
                        if(assignment[j+1]!= Ud[UPosition[(n,j+1)]]):
                            consistent = False
                            break;
            if(val != Ud[UPosition[(n,key)]]):
                consistent = False
            if(consistent):
                break;
        if not consistent:
            return False
    
    return True

def BS_MAC(assignment,XDomain,UDomain,constraintMatrix,UPosition,noOfBT):
    temp ={}
    complete = True
    for key,value in assignment.items():
        if value == -1:
            complete = False
            break

    if(complete):
        return True,assignment,noOfBT

    for val in XDomain[key]:
        if(CONSISTENT(val,key,XDomain,UDomain,constraintMatrix,assignment,UPosition)):
            assignment[key] = val
            q=[]
            XDomainTemp = dict(XDomain)
            UDomainTemp = dict(UDomain)
            XDomainTemp[key] = {val}
           
            #making the queue
            for i in range(len(constraintMatrix)):
                if constraintMatrix[i][key-1] ==1:
                    q.append((i,key,1))

            result,UDomainTemp,XDomainTemp =AC3(constraintMatrix,UDomainTemp,XDomainTemp,q,UPosition)
            if not result:
                assignment[key] = -1
            else:  
                result,temp,noOfBT = BS_MAC(assignment,XDomainTemp,UDomainTemp,constraintMatrix,UPosition,noOfBT)
            if result:
                return result,assignment,noOfBT
        assignment[key] = -1
        XDomainTemp = dict(XDomain)
        UDomainTemp = dict(UDomain)
    return False,assignment,noOfBT

def FILEWRITE(rowSize,columnSize,horizontalData,verticalData,assignment,outputLocation= "output.txt"):
    f = open(outputLocation,"w")
    f.write("rows="+str(rowSize)+"\n")
    f.write("columns="+str(columnSize)+"\n")
    for i in range(rowSize):
        for j in range(columnSize):
            if(horizontalData[i][j]=='0'):
                horizontalData[i][j] =str(assignment[i*columnSize+j+1])
    for i in range(rowSize):
        for j in range(columnSize):
            if(verticalData[i][j]=='0'):
                verticalData[i][j] =str(assignment[i*columnSize+j+1])
    
    f.write("Horizontal\n")
    for i in range(rowSize):
        for j in range(columnSize):
            if(j==columnSize -1):
                f.write(horizontalData[i][j]+"\n")
            else:
                f.write(horizontalData[i][j]+",")
    
    f.write("Vertical\n")
    for i in range(rowSize):
        for j in range(columnSize):
            if(j==columnSize -1):
                f.write(verticalData[i][j]+"\n")
            else:
                f.write(verticalData[i][j]+",")

if __name__ == '__main__':
    assignment = {}
    lenArg = len(sys.argv)

    if(lenArg == 4):
        inputLocation = str(sys.argv[1])
        outputLocation = str(sys.argv[2])
        whatToPerform = str(sys.argv[3])
        rowSize,columnSize,horizontalData,verticalData= parseInput(inputLocation)
        constraintMatrix,UDomain,XDomain,q,UPosition = makeConstraintMartix(rowSize,columnSize,horizontalData,verticalData)
        
        # print(constraintMatrix)
        
        for key,value in XDomain.items():
            assignment[key] = -1

        if(whatToPerform == "AC3"):
            isSolution,UpdatedUDomain,UpdatedXDomain= AC3(constraintMatrix,UDomain,XDomain,q,UPosition) 
            f = open(outputLocation,"w")
            for key1,value1 in UpdatedXDomain.items():
                f.write(str(key1-1)+" : "+str(value1)+"\n")
        elif(whatToPerform == "BACK"):
            isSolution,UDomain,XDomain= AC3(constraintMatrix,UDomain,XDomain,q,UPosition)
            isBackTrack,assignment,noOfBT= BS(assignment,XDomain,UDomain,constraintMatrix,UPosition,0)
            print(noOfBT)
            FILEWRITE(rowSize,columnSize,horizontalData,verticalData,assignment,outputLocation)

        elif(whatToPerform == "MAC"):
            isSolution,UDomain,XDomain= AC3(constraintMatrix,UDomain,XDomain,q,UPosition)
            isBackTrack,assignment,noOfBT= BS_MAC(assignment,XDomain,UDomain,constraintMatrix,UPosition,0)
            print(noOfBT)
            FILEWRITE(rowSize,columnSize,horizontalData,verticalData,assignment,outputLocation)

        elif(whatToPerform == "BACKnoAC3"):
            isBackTrack,assignment,noOfBT= BS(assignment,XDomain,UDomain,constraintMatrix,UPosition,0)
            print(noOfBT)
            FILEWRITE(rowSize,columnSize,horizontalData,verticalData,assignment,outputLocation)

        elif(whatToPerform == "MACnoAC3"):
            isBackTrack,assignment,noOfBT= BS_MAC(assignment,XDomain,UDomain,constraintMatrix,UPosition,0)
            print(noOfBT)
            FILEWRITE(rowSize,columnSize,horizontalData,verticalData,assignment,outputLocation)

        else:
            print("command format: kakuro.py <inputFileLocation> <outputFileLocation> whatToPerform ")
            print("check README file for valid values for whatToPerform argument")
    elif lenArg==1:
        inputLocation = input()
        rowSize,columnSize,horizontalData,verticalData= parseInput(inputLocation)
        constraintMatrix,UDomain,XDomain,q,UPosition = makeConstraintMartix(rowSize,columnSize,horizontalData,verticalData)
        # print(constraintMatrix)
        for key,value in XDomain.items():
            assignment[key] = -1
        isSolution,UpdatedUDomain,UpdatedXDomain= AC3(constraintMatrix,UDomain,XDomain,q,UPosition)
        isBackTrack,assignment,noOfBT= BS(assignment,XDomain,UDomain,constraintMatrix,UPosition,0)
        #print(noOfBT)
        FILEWRITE(rowSize,columnSize,horizontalData,verticalData,assignment)
    else:
        print("check README file for information about how to execute the code")
