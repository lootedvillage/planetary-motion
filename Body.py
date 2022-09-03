# Program to create a class to model a celestial body
import numpy as np
from numpy.linalg import norm

class Body (object):
    #Initial method to set the variables that will be needed during the simulation
    def __init__(self, name, m, r, colour, rx, ry, vx, vy):
        self.name = name
        self.r = r
        self.m = m
        self.colour = colour
        self.pLast = np.array([rx, ry])
        self.p = np.array([rx, ry])
        self.pNext = np.array([rx, ry])
        self.vLast = np.array([vx, vy])
        self.v = np.array([vx, vy])
        self.vLast = np.array([vx, vy])
        self.aLast = np.array([0.0, 0.0])
        self.a = np.array([0.0, 0.0])
        self.aNext = np.array([0.0, 0.0])
        self.flag = True
        
    #Method to set the acceleration of a body using Newton's Laws
    def setAcc(self, bodyList):
        G = float(6.674e-11)
        netForce = np.array([0.0, 0.0])
        #Cycling through each body and working out the contribution to the total force it experiences
        for i in range(len(bodyList)):
            if bodyList[i].name != self.name:
                r = bodyList[i].pNext - self.pNext
                F = (G * bodyList[i].m * self.m * r)/(norm(r) ** 3)
                netForce = netForce + F
        #Actual calculation of the acceleration the body experiences
        self.aNext = netForce/self.m

        temp = 0.0
        for j in range(len(bodyList)):
            if (bodyList[j].name == "Earth1"):
                temp = temp + bodyList[j].aNext[0]
                #print("rigid rod")
            elif (bodyList[j].name == "Earth2"):
                temp = temp + bodyList[j].aNext[0]
                #print("rigid rod")
            else:
                #print("Not using the rigid rod approximation")
                pHold = 1.0

        temp_new = temp / 2.0

        for k in range(len(bodyList)):
            if (bodyList[k].name == "Earth1") or (bodyList[k].name == "Earth2"):
                bodyList[j].aNext[0] = temp_new
                
    #Method to calculate the position of a body using the Beeman scheme
    def setPos(self, dt, T, CoM_Position):
        self.pNext = self.p + (self.v)*dt + (1/6)*(4*self.a - self.aLast)*(dt ** 2)
        #CoM_Position = CoM_Position
        #self.pNext = self.pNext - CoM_Position
        #This small loop calculates the orbital period of a body, the flag ensures it only does the once
        if (self.flag == True):
            if (self.pNext[1] > 0.0 and self.p[1] < 0.0): #Checks to see whether a body has crossed the x-axis
                print(str(self.name) + " has orbited with a period of: " + str(T/86400) + " Earth days")
                self.flag = False
    #Method to calculate the velocity of a body using the Beean scheme
    def setVel(self, dt):
        self.vNext = self.v + (1/6)*(2*self.aNext + 5*self.a - self.aLast)*dt
    #Stepping forward through the simulation, updates the relevant variables
    def stepForward(self):
        self.pLast = self.p
        self.vLast = self.v
        self.aLast = self.a
        self.p = self.pNext
        self.v = self.vNext
        self.a = self.aNext
    #Method to calculate the KE of a body
    def getKE(self):
        KE = 0.5 * self.m * norm(self.v) * norm(self.v)
        return(KE)
    #Method to calculate the GPE of a body
    def getGPE(self, bodyList):
        G = float(6.674e-11)
        PE = 0.0
        for i in range(len(bodyList)):# Works out contirbution from each interaction
            if bodyList[i].name != self.name:
                r = bodyList[i].pNext - self.pNext
                PE = PE + G * bodyList[i].m * self.m / norm(r)
        PE = -1.0 * PE #GPE has to be -ve
        return(PE)

    #Method for calculating the centre of mass coordinate such that the simulation can be kept in the centre of mass frame
    def getCoM(self, bodyList):
        total_mass = 0.0
        for i in range(len(bodyList)):
            dm = self.bodyList[i].m
            total_mass = total_mass + dm

        CoM_r = np.array([0.0, 0.0])
        for i in range(len(bodyList)):
            dr = (bodyList[i].m) * (bodyList[i].p)
            CoM_r = CoM_r + dr

        CoM_r = CoM_r / total_mass
        return(CoM_r)
        

    
