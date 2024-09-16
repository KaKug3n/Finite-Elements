# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

def lit_fichier_msh(fichier_msh):
    
    f=open(fichier_msh)
    
    temp=f.readline()
    
    temp=temp.split()

    nbn=int(temp[0])
    nbe=int(temp[1])
    nba=int(temp[2])

    coord=np.zeros((nbn,2),dtype=float)
    refn=np.zeros((nbn),dtype=int)
    
    for i in range(0,nbn):
        temp=f.readline()
        
        #coord & refn
        temp=temp.split()
        coord[i,0]=float(temp[0])
        coord[i,1]=float(temp[1])
        refn[i]=(temp[2])
    
    tri=np.zeros((nbe,3),dtype=int)
    reft=np.zeros((nbe),dtype=int)
    for i in range(0,nbe):
        temp=f.readline()
        
        #tri & reft
        temp=temp.split()
        tri[i,0]=int(temp[0])
        tri[i,1]=int(temp[1])
        tri[i,2]=int(temp[2])
        reft[i]=int(temp[3])
    
    ar=np.zeros((nba,2),dtype=int)
    refa=np.zeros((nba),dtype=int)
    for i in range(0,nba):
        temp=f.readline()
        
        #ar & refa
        temp=temp.split()
        ar[i][0]=temp[0]
        ar[i][1]=temp[1]
        refa[i]=temp[2]

    
    f.close()
    return [nbn,nbe,nba,coord,tri,ar,refn,reft,refa]

#indices (noeuds,tri,ar)
def trace_maillage_ind(nbn,nbe,nba,coord,tri,ar): 
   
    plt.subplot()
    plt.triplot(coord[:,0],
                coord[:,1],
                (tri[:])-1,'go-',lw=1.0)
    
    for i in range(nbn):
        plt.text(coord[i][0],coord[i][1],i,color="red",fontsize=9)


    plt.xlabel('axe Ox')
    plt.ylabel('axe Oy')
    plt.title('Maillage : indices')
    
    
    
    plt.show()   

def trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa): # :références (noeuds,tri,ar)

    plt.subplot()
    plt.triplot(coord[:,0],
                coord[:,1],
                (tri[:])-1,'go-',lw=1.0)
    
    for i in range(0,nbn):
        plt.text(coord[i, 0], coord[i, 1], f'{i+1}', color='red', fontsize=9)
        
    for i in range(0,nbe):

        x_mean = (coord[tri[i][0]-1, 0] + coord[tri[i][1]-1, 0] + coord[tri[i][2]-1, 0]) / 3

        y_mean = (coord[tri[i][0]-1, 1] + coord[tri[i][1]-1, 1] + coord[tri[i][2]-1, 1]) / 3
        
        plt.text(x_mean, y_mean, f'{i+1}', color='black', fontsize=9)

    for i in range(0,nba):
        
        x_mean = (coord[ar[i][0]-1, 0] + coord[ar[i][1]-1, 0]) / 2

        y_mean = (coord[ar[i][0]-1, 1] + coord[ar[i][1]-1, 1]) / 2

        plt.text(x_mean, y_mean, f'{i+1}', color='blue', fontsize=9)
    
    plt.xlabel('axe Ox')
    plt.ylabel('axe Oy')
    plt.title('Maillage : indices')
    
    plt.show()



def longueur(n1,n2):
   return np.sqrt((n2[0]-n1[0])**2+(n2[1]-n1[1])**2)

def max_long(n1,n2,n3):
    pas=0
    if pas<longueur(n1,n2):
        pas=longueur(n1,n2)
    if pas<longueur(n2,n3):
        pas=longueur(n2,n3)
    if pas<longueur(n1,n3):
        pas=longueur(n1,n3)
    return pas

def calc_cercle_inscrit(a,b,c):
    s = (a + b + c) / 2
    A = np.sqrt(s * (s - a) * (s - b) * (s - c))
    r = A / s
    
    return r

def pas_et_qualite_tri(n1,n2,n3):
    const=np.sqrt(3)/6

    a=longueur(n1,n2)
    b=longueur(n2,n2)
    c=longueur(n1,n3)
    r=calc_cercle_inscrit(a,b,c)
 
    hT=max_long(n1,n2,n3)

    result=const*(hT/r)

    return [hT,result]

def pas_et_qualite_maillage(nbn,coord,tri):
    maxpas=0
    QT=0
    for i in range(0,nbn):
        [tmpQT,tmpmaxpass]=pas_et_qualite_tri([coord[tri[i,0],0],coord[tri[i,0],1]],[coord[tri[i,1],0],coord[tri[i,1],1]],[coord[tri[i,2],0],coord[tri[i,2],1]])

        if maxpas<tmpmaxpass:
            maxpas=tmpmaxpass
        if QT<tmpQT:
            QT=tmpQT

    return [QT,maxpas]


def charge_et_affiche_maillage(FichierMaillage):

    [nbn,nbe,nba,coord,tri,ar,refn,reft,refa]=lit_fichier_msh(FichierMaillage)

    
    print(pas_et_qualite_maillage(nbn,coord,tri))
    
    trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa)
    

FichierMaillage="C:\\Users\\Kakugen\\Desktop\\CHPS0706\\tp1\\Maillages\\m0.msh" # :nom du fichier de maillage

charge_et_affiche_maillage(FichierMaillage)

#[nbn,nbe,nba,coord,tri,ar,refn,reft,refa]=lit_fichier_msh(FichierMaillage)
#trace_maillage_ind(nbn,nbe,nba,coord,tri,ar)
#trace_maillage_ref(nbn,nbe,nba,coord,tri,ar,refn,reft,refa)