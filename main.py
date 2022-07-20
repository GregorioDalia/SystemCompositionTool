'''
                        GREGORIO DALIA, MIRKO COSTANZO , ROCCO ADDABBO
                                   ALL CREDITS TO MONTAGS
                          <https://www.gnu.org/licenses/gpl-3.0.txt>
'''

import json
import sys


class Node:
    subnodes = []
    subsystems = []
    retro = False
    subConfig = ""
    name = ""
    systemPosition = ""

    def __init__(self, subnodes, subsystems, retro, subConfig, name, systemPosition):
        self.subnodes = subnodes
        self.subsystems = subsystems
        self.retro = retro
        self.subConfig = subConfig
        self.name = name
        self.systemPosition = systemPosition


class Systems:
    sistemsColletion = []
    configurations = None

    def addSistem (self,s):
        self.sistemsColletion.append(s)

    def __init__(self):
        sistemsColletion = []

    def __init__(self,configurations):
        self.configurations=configurations
        sistemsColletion = []

    def __init__(self,sistemsColletion,configurations):
        self.sistemsColletion = sistemsColletion
        self.configurations = configurations

    def printconfiguration(self):
        print(self.configurations)


class System:
    updateFunctions=[]
    states=[]
    input=[]
    output=[]
    name=""
    initialstate=[]
    extended=""
    variable=[]
    maxTIME=dict()



    def tostring(self):
        print("nome= "+self.name)
        print("stati")
        for s in self.states:
            print(s)

        print("input")

        for x in self.input:
            print(x)
        print("output")

        for x in self.output:
            print(x)

        print("funzioni")
        for f in self.updateFunctions:
            print(f.tostring())

    def __int__(self,name,states,initialstate,input,output,updateFunctions):
        self.name=name
        self.states=states
        self.initialstate = initialstate #lista di stringhe
        self.input = input
        self.output=output
        self.updateFunctions= updateFunctions #non un oggetto ma una lista

    def __int__(self, name, states, initialstate, input, output):
        self.name = name
        self.states = states
        self.initialstate = initialstate  # lista di stringhe
        self.input = input
        self.output= output

    def addUpdate(self,updatef):
        self.updateFunctions.append(updatef)


class updateF:
    input=""
    output=""
    finalState=""
    variableaction=""
    variablecheck=""
    initialState=""

    def ciao(self):
        print("sto qua")

    def __int__(self,initialState,finalState,input,output):
        self.input = input
        self.output = output
        self.initialState=initialState
        self.finalState=finalState

    def tostring(self):
        return ("initial state= "+self.initialState+"-"+"input= "+
                str(self.input)+" - "+"finalstate= "+self.finalState+" - "+"output= "+str(self.output))


def createTopology(nodo):

    x = Node(name=nodo["name"],retro=nodo["retro"],subsystems=nodo["subsystems"],
                           subConfig=nodo["subConfig"],systemPosition=nodo["systemPosition"],subnodes=[])

    if("subnodes" in nodo.keys()):
        for y in nodo['subnodes']:
            newNodo= createTopology(y)
            x.subnodes.append(newNodo)
    return x

def CreateSistems(TXT):

    dataJson = json.loads(TXT)
    OBJ = Systems(configurations=createTopology(dataJson["configurations"]),sistemsColletion=[])
    OBJ.sistemsColletion=[]

    for singleSistem in dataJson["sistemsColletion"]:

        name = singleSistem["name"]
        states = singleSistem["states"]
        initialstates = singleSistem["initialstate"]
        ip = singleSistem["input"]
        op = singleSistem["output"]


        try:
            extended = singleSistem["extended"]
            variable = singleSistem["variable"]

            # print("DEBUG: MAXTIME è "+str(singleSistem["maxTIME"]))
            maxTIME = dict()

            for stato in states:
                maxTIME[stato + "MAX"] = singleSistem["maxTIME"][stato + "MAX"]

            print("DEBUG: MAXTIME è " + str(maxTIME))

        except: print("SISTEMA NORMALE")







        Sistem = System()
        try:
            Sistem.extended = extended
            Sistem.variable = variable
            Sistem.maxTIME = maxTIME
        except:print("SEMPRE NORMALE")

        Sistem.name=name
        Sistem.input=ip
        Sistem.output=op
        Sistem.states=states
        Sistem.initialstate=initialstates
        Sistem.updateFunctions=[]
        Sistem.subsystems=[]

        for singleupdate in singleSistem["updateFunctions"]:
            update = updateF()

            update.input=singleupdate["input"]
            try:
                update.variablecheck=singleupdate["variablecheck"]
                update.variableaction=singleupdate["variablecheck"]
            except:
                print("FUNZIONE NORMALE")

            update.output=singleupdate["output"]
            update.finalState=singleupdate["finalState"]
            update.initialState=singleupdate["initialState"]

            Sistem.addUpdate(update)
        OBJ.addSistem(Sistem)
    return OBJ

def renamevariable(s1,s2,f1,f2):

    nf2=updateF()
    nf2.output=f2.output
    nf2.finalState=f2.finalState
    nf2.initialState=f2.initialState

    nf2.input=[]

    for x in enumerate(f2.input):
        nf2.input.append("")

    #print("DEBUG: F2 "+f2.tostring()+"size" + str(len(f2.input)))
    #print("DEBUG: nf2 "+nf2.tostring() + "size" + str(len(nf2.input)))

    for i , item in enumerate(f2.input):
        #print("DEBUG: old imput "+f2.input[i] +str(i))
        nf2.input[i]=str(f2.input[i])
        #print("DEBUG: new imput "+nf2.input[i]+str(i))


        nf2.input[i] = nf2.input[i].replace(s2.input[i],s1.output[i])

        if("-" in nf2.input[i]):
            nf2.input[i]=""

    print("DEBUG: nf2 finale = "+nf2.tostring())
    return nf2

def checkfunzioniserie(f1,f2):
    valid = True

    print("DEBUG: check f1 e f2 in serie "+f1.tostring()+ " / "+f2.tostring())

    for i , item in enumerate(f2.input):

        if(f2.input[i]!="true"):
            if(f1.output[i]!=f2.input[i]):
                valid=False

    return valid

def resolveSeries(sys1,sys2,name,OBJ):
    print("DEBUG: risolvo serie "+sys1.name +" and "+sys2.name)

    newSistem = System()
    newSistem.input = []
    newSistem.output=[]
    newSistem.name=name
    newSistem.states=createNewSystemStates(sys1,sys2)

    newSistem.input=sys1.input
    newSistem.output=sys2.output

    newSistem.initialstate=[1]
    newSistem.initialstate[0]=str(sys1.initialstate[0])+str(sys2.initialstate[0])
    newSistem.updateFunctions=[]
    #poi la cambiamo con un ciclo

    if(len(sys1.output)!=len(sys2.input)):
        raise Exception(sys1.name + " and "+sys2.name +" are not compatible for series")

    print("DEBUG: i sistemi "+sys1.name + " and "+sys2.name+"sono compatibili ")

    for stato1 in sys1.states:

        for stato2 in sys2.states:

            for funzionestart1 in sys1.updateFunctions:

                if(funzionestart1.initialState == stato1 ):

                    for funzionestart2 in sys2.updateFunctions:

                        if (funzionestart2.initialState == stato2):

                            #print("DEBUG INNER SERIE f1= "+funzionestart1.tostring()+"f2= "+funzionestart2.tostring())

                            nf2=renamevariable(sys1,sys2,funzionestart1,funzionestart2)

                            if (checkfunzioniserie(funzionestart1,nf2)):

                                #print("DEBUG: Le funzioni "+funzionestart1.tostring()+" e "+nf2.tostring() +"SONO COMPATIBILI")

                                newUpdate = updateF()
                                newUpdate.input=funzionestart1.input
                                newUpdate.initialState = stato1+stato2

                                newUpdate.output = funzionestart2.output

                                newUpdate.finalState=funzionestart1.finalState+funzionestart2.finalState

                                newSistem.updateFunctions.append(newUpdate)

                            else:
                                print("DEBUG: Le funzioni "+funzionestart1.tostring()+" e "+nf2.tostring() +" NON  SONO COMPATIBILI")


    OBJ.sistemsColletion.append(newSistem)

def resolveComposite(sys1,name,OBJ):
    #caso senza storia
    #tre casi

    #caso entrambi composti


    #caso primo sistema composto



    #caso secondo sistema composto

    #caso entrambi composti


    return

def resolveSidebySide(sys1, sys2, name, OBJ):
    print("RISOLVO sbs "+sys1.name +" and "+sys2.name)

    newSistem = System()
    newSistem.input=[]
    newSistem.updateFunctions=[]
    sameInput = False
    sameOutput = False
    commonoutput=[]

    for i in sys1.output:
        for y in sys2.output:

            if (i == y):
                commonoutput.append(i)
                sameOutput = True

    commoninput=[]

    for i in sys1.input:

        for y in sys2.input:

            if(i == y):
                commoninput.append(i)
                sameInput = True

    if (sameOutput):
        newSistem.output = list(set(sys1.output + sys2.output))
        print("output comune")
        print(str(newSistem.output))
    else:
        newSistem.output = sys1.output + sys2.output

    if (sameInput):
        newSistem.input=list(set(sys1.input+sys2.input))
        print("input comune")
        print(str(newSistem.input))

    else:
        newSistem.input=sys1.input+sys2.input

    newSistem.name=name
    newSistem.states=createNewSystemStates(sys1,sys2)
    newSistem.initialstate=[1]
    newSistem.initialstate[0]=str(sys1.initialstate[0])+str(sys2.initialstate[0])

    for stato1 in sys1.states:

        for stato2 in sys2.states:

            for funzionestart1 in sys1.updateFunctions:

                if(funzionestart1.initialState == stato1 ):

                    for funzionestart2 in sys2.updateFunctions:

                        if (funzionestart2.initialState == stato2):

                            newUpdate = updateF()
                            newUpdate.initialState = stato1+stato2
                            newUpdate.input = funzionestart1.input+funzionestart2.input
                            newUpdate.output = funzionestart1.output+funzionestart2.output
                            newUpdate.finalState=funzionestart1.finalState+funzionestart2.finalState
                            correct = True

                            if(sameInput):

                                for x in newUpdate.input:

                                    if(x in commoninput ):

                                        #ci troviamo con un imput in comune

                                        for y in newUpdate.input:

                                            if(x in y):
                                                if (x != y):
                                                    correct=False

                            #newUpdate.input.append(commoninput)

                            if(correct):
                                newUpdate.input=list(set(newUpdate.input))
                                newSistem.updateFunctions.append(newUpdate)

                            if(sameOutput):
                                newUpdate.output=list(set(newUpdate.output)) #togliamo i doppioni

                                for x in newUpdate.output:

                                    if(x in commonoutput ):

                                        #ci troviamo con un imput in comune

                                        for y in newUpdate.output:

                                            if(x in y):
                                                if (x != y):
                                                    newUpdate.output.remove(x)
    OBJ.sistemsColletion.append(newSistem)

    for state in newSistem.states:
        state.replace(",","")
    return

def resolveExtended(sys1,name,OBJ):
    newSistem = System()
    newSistem.input = sys1.input
    newSistem.output = sys1.output
    newSistem.name = name

    newSistem.states = list()

    newSistem.initialstate= list()

    startduration = int(sys1.maxTIME[sys1.initialstate[0] + "MAX"])

    print("DEBUG: start duration "+str(startduration))

    if(startduration == -1):
        newSistem.initialstate.append(sys1.initialstate[0])
    else:
        newSistem.initialstate.append(sys1.initialstate[0]+"_0")
    newSistem.updateFunctions = []

    for stato in sys1.states:

        statoDuration = int(sys1.maxTIME[stato+"MAX"].split("_")[0]) #rosso 60 secondi

        if(statoDuration == -1):
            #stato senza tempo
            newSistem.states.append(stato)
            newUpdate = updateF()
            newUpdate.initialState = stato
            newUpdate.input = list()
            newUpdate.output = list()

            for x in enumerate(sys1.input):
                newUpdate.input.append("")
            for x in enumerate(sys1.output):
                newUpdate.output.append("")
            newUpdate.finalState = stato
            newSistem.updateFunctions.append(newUpdate)

        if("_" in (sys1.maxTIME[stato+"MAX"])):
            newUpdate = updateF()
            newUpdate.initialState = stato + "_" + ((sys1.maxTIME[stato+"MAX"]).split("_")[0])
            newUpdate.input=list()
            newUpdate.output=list()

            for x in enumerate(sys1.input):
                newUpdate.input.append("")
            for x in enumerate(sys1.output):
                newUpdate.output.append("")
            newUpdate.finalState = stato + "_" + ((sys1.maxTIME[stato+"MAX"]).split("_")[0])





            newSistem.updateFunctions.append(newUpdate)

        for i in range(statoDuration + 1):
            newSistem.states.append(stato+"_"+str(i))

        print("DEBUG: gli stati sono "+str(newSistem.states))

        for i in range(statoDuration + 1):

            for stat in newSistem.states:

                if stat == stato+"_"+str(i+1):
                    newUpdate = updateF()
                    newUpdate.initialState = stato + "_" + str(i)

                    newUpdate.input=[]
                    newUpdate.output=[]
                    for x in enumerate(sys1.input):
                        newUpdate.input.append("")
                    for x in enumerate(sys1.output):
                        newUpdate.output.append("")

                    newUpdate.finalState = stato + "_" + str(i + 1)
                    newSistem.updateFunctions.append(newUpdate)
                    # TICCHETTIO ok
            '''
            if( in newSistem.states ):
                newUpdate = updateF()
                newUpdate.initialState = stato+"_"+str(i)
                newUpdate.input = [""]
                newUpdate.output = [""]
                newUpdate.finalState = stato+"_"+str(i+1)
                newSistem.updateFunctions.append(newUpdate)
                #TICCHETTIO
            '''


    #passiamo alle funzioni
    for stato in sys1.states:

        for function in sys1.updateFunctions:

            print("DEBUG: funzione da analizzare "+function.tostring() + "NEW "+function.variablecheck)

            
            
            if (">=" in function.variablecheck and function.initialState == stato):
                #si va al prossimo stato


                newUpdate = updateF()

                #print("DEBUG: inner "+str(sys1.maxTIME[stato+"MAX"]))

                newUpdate.initialState = stato +"_"+(sys1.maxTIME[stato+"MAX"].split("_")[0])
                newUpdate.input = function.input
                newUpdate.output = function.output
                if(function.finalState+"_0" in newSistem.states):
                    newUpdate.finalState = function.finalState+"_0"
                else:
                    newUpdate.finalState = function.finalState

                print("DEBUG: STO AGGIUNGENDO >= "+newUpdate.tostring())

                newSistem.updateFunctions.append(newUpdate)

            
            
            elif("<" in function.variablecheck and function.initialState==stato):

                    for s in newSistem.states:

                        if (function.initialState in s):
                            newUpdate = updateF()
                            newUpdate.initialState = s
                            newUpdate.input= function.input
                            newUpdate.output= function.output

                            if("_" in s):

                                finalstat = function.finalState + "_"+ str(int(s.split("_")[1])+1)
                                if(finalstat in newSistem.states):
                                    newUpdate.finalState = finalstat
                                    newSistem.updateFunctions.append(newUpdate)

                                #print("DEBUG: fammi capè "+newUpdate.finalState)


                            else:
                                newUpdate.finalState = function.finalState
                                newSistem.updateFunctions.append(newUpdate)

                            print("DEBUG: STO AGGIUNGENDO < " + newUpdate.tostring())

            elif(function.initialState == stato and function.variablecheck== "" ):
                print("DEBUG: CI SONO :::"+function.tostring())


                newUpdate = updateF()
                newUpdate.initialState = stato
                newUpdate.input = function.input
                newUpdate.output = function.output
                if(function.finalState+"_0" in newSistem.states):
                    newUpdate.finalState = function.finalState+"_0"
                else:
                    newUpdate.finalState = function.finalState
                newSistem.updateFunctions.append(newUpdate)



            #else:
                #raise  Exception("CASO STRANO COMPOSTO")






    OBJ.sistemsColletion.append(newSistem)






    return
def resolveFeedback(sys1,name,OBJ):
    print("RISOLVO FEEDBACK "+sys1.name)

    newSistem = System()
    newSistem.input = []
    newSistem.output = sys1.output
    newSistem.name = name
    newSistem.states = sys1.states
    newSistem.updateFunctions = []

    for stato in sys1.states:
        illformed = True

        for function in sys1.updateFunctions:


            if(function.initialState == stato):

                #print("DEBUG SONO DENTRO IL FEED " + function.tostring())

                if(checkinputfeedback(function,sys1)):

                    illformed=False
                    newUpdate = updateF()
                    newUpdate.initialState=stato
                    newUpdate.input=["true"]
                    newUpdate.output=function.output
                    newUpdate.finalState=function.finalState
                    newSistem.updateFunctions.append(newUpdate)

        if(illformed and sys1.name != "SemaforoTOTALE"):
            print(sys1.tostring())
            raise Exception("Il Sistema è ILL-FORMED")

    OBJ.sistemsColletion.append(newSistem)


def findSystemByName(name,obj):

    for x in obj.sistemsColletion:
        if (x.name == name):
            return x


def resolveSistem(OBJ,nodo):
    print("DEBUG: Risolvo "+nodo.name)

    #3 casi
    #nodo foglia con due sistemi
    #nodo con sistema + nodo
    #nodo piu nodo

    if(len(nodo.subnodes) == 0):
        print("DEBUG: Risolvo " + nodo.name+" foglia ")

        if(not nodo.retro and len(nodo.subsystems)==1 and (findSystemByName(nodo.subsystems[0],OBJ).name =="TrafficLights" or
                                                           findSystemByName(nodo.subsystems[0],OBJ).name =="PedLights" )):
            print("DEBUG: RISOLVO STATI ESTESA")
            resolveExtended(findSystemByName(nodo.subsystems[0],OBJ),nodo.name,OBJ)


        elif(nodo.retro and len(nodo.subsystems)==1):
            print("DEBUG: Risolvo " + nodo.name + " foglia" +"risolvo feedback interno")

            #print(findSystemByName(nodo.subsystems[0],OBJ).tostring())

            resolveFeedback(findSystemByName(nodo.subsystems[0],OBJ),nodo.name,OBJ)

        elif (not nodo.retro and len(nodo.subsystems)==2 and nodo.subConfig=="sidebyside"):

            print("DEBUG: Risolvo " + nodo.name + " foglia" +"risolvo side by interno")

            resolveSidebySide(findSystemByName(nodo.subsystems[0],OBJ),findSystemByName(nodo.subsystems[1],OBJ),nodo.name,OBJ)

        elif (not nodo.retro and len(nodo.subsystems)==2 and nodo.subConfig=="cascade"):
            print("DEBUG: Risolvo " + nodo.name + " foglia" +"risolvo cascata interno")

            resolveSeries(findSystemByName(nodo.subsystems[0],OBJ),findSystemByName(nodo.subsystems[1],OBJ),nodo.name,OBJ)


        elif(not nodo.retro and len(nodo.subsystems) == 1 and nodo.subConfig=="composite") :
            print("DEBUG: Risolvo " + nodo.name + " foglia" +"risolvo composizione interna")

            resolveComposite(findSystemByName(nodo.subsystems[0],OBJ),nodo.name,OBJ)

        else:
            raise  Exception("SOMETHING GOES WRONG")

        return

    elif (nodo.retro and len(nodo.subnodes) == 1 and len(nodo.subsystems) == 0):
        print("DEBUG: Risolvo " + nodo.name+" retroazione unica")

        resolveSistem(OBJ,nodo.subnodes[0])
        resolveFeedback(findSystemByName(nodo.subnodes[0].name, OBJ), nodo.name, OBJ)

        return

    elif (len(nodo.subnodes) == 1 and len(nodo.subsystems) == 1 and not nodo.retro) :

        print("DEBUG: risolvo il caso sottostistema  " )

        resolveSistem(OBJ,nodo.subnodes[0])

        if ( nodo.subConfig == "sidebyside"):
            resolveSidebySide(findSystemByName(nodo.subsystems[0],OBJ),findSystemByName(nodo.subnodes[0].name,OBJ),nodo.name,OBJ)

        elif (nodo.subConfig == "cascade"):

            if(nodo.systemPosition=="left"):
                resolveSeries(findSystemByName(nodo.subsystems[0],OBJ),findSystemByName(nodo.subnodes[0].name,OBJ),nodo.name,OBJ)

            elif(nodo.systemPosition=="right"):
                resolveSeries(findSystemByName(nodo.subnodes[0].name,OBJ),findSystemByName(nodo.subsystems[0],OBJ),nodo.name,OBJ)

            else:
                raise Exception("WRONG CONFIGURATION")

        return

    elif (len(nodo.subnodes) == 2 and len(nodo.subsystems) == 0 and not nodo.retro):

        print("DEBUG: Risolvo " + nodo.name+" doppio sottonodo ")

        resolveSistem(OBJ, nodo.subnodes[0])
        resolveSistem(OBJ, nodo.subnodes[1])

        if (nodo.subConfig == "sidebyside"):
            resolveSidebySide(findSystemByName(nodo.subnodes[0].name,OBJ), findSystemByName(nodo.subnodes[1].name, OBJ),nodo.name,OBJ)

        elif (nodo.subConfig == "cascade"):
            resolveSeries(findSystemByName(nodo.subnodes[0].name,OBJ), findSystemByName(nodo.subnodes[1].name, OBJ),nodo.name, OBJ)

        return

    else:
        raise Exception("SOMETHING GOES WRONG")

def renameinputfeedback(f,sys):

    nf1=updateF()
    nf1.output=f.output.copy()
    nf1.finalState=f.finalState
    nf1.initialState=f.initialState
    nf1.input=f.input.copy()

    if(len(nf1.input)==1 and nf1.input[0] == "true"):
        return nf1

    for i , item in enumerate(f.output):
        nf1.input[i]=nf1.input[i].replace(sys.input[i],sys.output[i])

    return nf1

def checkinputfeedback(f,sys):

    nf=renameinputfeedback(f,sys)

    if (nf.input == nf.output): return True

    if(len(nf.input)==1 and nf.input[0] == "true"):
        return True

    for i , item in enumerate(nf.input):

        if("-" not in nf.input[i] and nf.input[i] != nf.output[i]):
            return False

        if("-" in nf.input[i]):
            if(nf.output[i] != nf.input[i] and nf.output[i]!=""):
                return False

    return True

def createNewSystemStates(sys1,sys2):

    stateList = []

    for x in sys1.states:

        for y in sys2.states:

            stateList.append(x+""+y)

    return stateList

'''
with open('2Systems-SIDEBYSIDE') as data:
    stringTXT = data.read()
    #systemsOBJ = CreateSistems(json.load(data.read()))

systemsOBJ = CreateSistems(stringTXT)

ResolvSidebySide(systemsOBJ.sistemsColletion[0],systemsOBJ.sistemsColletion[1],systemsOBJ.configurations.name,systemsOBJ)

with open('2Systems-CASCADE') as data:
    stringTXT = data.read()
    #systemsOBJ = CreateSistems(json.load(data.read()))

systemsOBJ = CreateSistems(stringTXT)

resolveSeries(systemsOBJ.sistemsColletion[0],systemsOBJ.sistemsColletion[1],systemsOBJ.configurations.name,systemsOBJ)

with open('1System-FEEDBACK') as data:
    stringTXT = data.read()
    #systemsOBJ = CreateSistems(json.load(data.read()))

systemsOBJ = CreateSistems(stringTXT)


resolveFeedback(systemsOBJ.sistemsColletion[0],systemsOBJ.configurations.name,systemsOBJ)
with open('1System-FEEDBACK-VARIANT') as data:
    stringTXT = data.read()
    #systemsOBJ = CreateSistems(json.load(data.read()))

systemsOBJ = CreateSistems(stringTXT)


resolveFeedback(systemsOBJ.sistemsColletion[0],systemsOBJ.configurations.name,systemsOBJ)

'''


def createDefaultTransiction(sistema):
    print("DEBUG: ADD DEFAULT TRANTICTION TO "+sistema.name )

    for stato in sistema.states:

        newUpdate = updateF()
        newUpdate.initialState = stato
        newUpdate.input = "true"
        newUpdate.output = ""
        newUpdate.finalState = stato
        sistema.updateFunctions.append(newUpdate)


    '''
    for stato in sistema.states:

        i = 0
        for ipt in sistema.input:

            flagtrue=False
            flagon=False
            flagoof=False

            for uf in sistema.updateFunctions:

                if(uf.initialState == stato):

                    if(uf.input[i] == "true"): flagtrue=True
                    elif (uf.input[i] == ipt):flagon = True
                    elif(uf.input[i]== "-"+ipt):flagoof =True


            if(not flagtrue):



                if(not flagoof):
                        newUpdate = updateF()
                        newUpdate.initialState = stato
                        newUpdate.input = "-"+ipt
                        newUpdate.output =""
                        newUpdate.finalState = stato
                        systemsOBJ.updateFunctions.append(newUpdate)
                if(not flagon):
                        newUpdate = updateF()
                        newUpdate.initialState = stato
                        newUpdate.input = ipt
                        newUpdate.output = ""
                        newUpdate.finalState = stato
                        systemsOBJ.updateFunctions.append(newUpdate)

            i = i+1
    '''


with open("1Cascade-BETWEEN-2sidebyside") as data:
    stringTXT = data.read()
    #systemsOBJ = CreateSistems(json.load(data.read()))

systemsOBJ = CreateSistems(stringTXT)

'''
for sistema in systemsOBJ.sistemsColletion:
    createDefaultTransiction(sistema)
'''

resolveSistem(systemsOBJ,systemsOBJ.configurations)

for x in systemsOBJ.sistemsColletion:
    print("############################")
    print("name "+x.name)
    print("states "+str(x.states))
    print("initial states "+ str(x.initialstate))
    print("input "+str(x.input))
    print("output "+str(x.output))
    print("Number of updates "+str(len(x.updateFunctions)))
    print("----------")

    for z in x.updateFunctions:
        print("initial state "+str(z.initialState))
        print("guard" + str(z.input))
        print("action "+str(z.output))
        print("final state "+str(z.finalState))
        print("--------------------")

