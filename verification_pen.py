from math import sin, cos, pi, sqrt
import numpy as np

def lit_fichier_msh(fichier_msh):
    with open(fichier_msh, 'r') as f:
        # Lecture de la première ligne
        nbn, nbe, nba = map(int, f.readline().split())
        
        # Lecture des coordonnées et références des noeuds
        coord = np.zeros((nbn, 2))
        refn = np.zeros(nbn, dtype=int)
        for i in range(nbn):
            line = f.readline().split()
            coord[i] = [float(line[0]), float(line[1])]
            refn[i] = int(line[2])
        
        # Lecture des triangles et leurs références
        trian = np.zeros((nbe, 3), dtype=int)
        reft = np.zeros(nbe, dtype=int)
        for i in range(nbe):
            line = f.readline().split()
            trian[i] = [int(line[0])-1, int(line[1])-1, int(line[2])-1]
            reft[i] = int(line[3])
        
        # Lecture des arêtes et leurs références
        ar = np.zeros((nba, 2), dtype=int)
        refa = np.zeros(nba, dtype=int)
        for i in range(nba):
            line = f.readline().split()
            ar[i] = [int(line[0])-1, int(line[1])-1]
            refa[i] = int(line[2])
    
    return nbn, nbe, nba, coord, trian, ar, refn, reft, refa



def pas_et_qualite_maillage(coord, trian):
    h_max = 0  # Pas du maillage
    Q_h_max = 0  # Qualité du maillage
    
    for triangle in trian:
        # Récupération des coordonnées des sommets du triangle
        S1, S2, S3 = coord[triangle[0]], coord[triangle[1]], coord[triangle[2]]
        
        # Calcul des longueurs des arêtes
        L1 = np.linalg.norm(S2 - S1)
        L2 = np.linalg.norm(S3 - S2)
        L3 = np.linalg.norm(S1 - S3)
        
        # Calcul du pas du triangle
        h_T = max(L1, L2, L3)
        
        # Mise à jour du pas du maillage
        h_max = max(h_max, h_T)
        
        # Calcul du demi-périmètre
        s = (L1 + L2 + L3) / 2
        
        # Calcul de l'aire du triangle (formule de Héron)
        aire = np.sqrt(s * (s - L1) * (s - L2) * (s - L3))
        
        # Calcul du rayon du cercle inscrit
        r_T = aire / s
        
        # Calcul de la qualité du triangle
        Q_T = (np.sqrt(3) / 6) * (h_T / r_T)
        
        # Mise à jour de la qualité du maillage
        Q_h_max = max(Q_h_max, Q_T)

    return h_max, Q_h_max

#fonction solution du problème
def fct_u(x,y):
    return 1 + sin((pi/2)*x) + x*(x-4)*cos((pi/2)*y)

#fonction de bord
def fct_uE(x,y): 
    return 1

#fonction source de chaleur
def fct_f(x,y):
    return ((pi**2)/4)*sin((pi/2)*x) + (((pi**2)/4)*x**2 - (pi**2)*x -2)*cos((pi/2)*y)

#fonction de conductivite                                                                     
def fct_kappa(x,y):
    return 1

#facteur de transfert
def fct_alpha(x,y):
    return 10**8

#coordonnees 3 arg 
def coeffelem_P1_rigid(x1, x2, x3, y1, y2, y3):

    #calcul aire triangle
    mesT = (1/2)*((x3-x1)*(y3-y2) - ((x3-x2)*(y3-y1)))

    """initialisation et remplissage matrice de rigidité"""
    K = np.zeros((3,3)) 

    K[0][0] = (x2-x3)**2 + (y2-y3)**2
    K[1][1] = (x3-x1)**2 + (y3-y1)**2
    K[2][2] = (x1-x2)**2 + (y1-y2)**2
    K[0][1] = -((x1-x3)*(x2-x3)+(y1-y3)*(y2-y3))
    K[1][0] = -((x1-x3)*(x2-x3)+(y1-y3)*(y2-y3))
    K[0][2] = -((x3-x2)*(x1-x2)+(y3-y2)*(y1-y2))
    K[1][2] = -((x2-x1)*(x3-x1)+(y2-y1)*(y3-y1))
    K[2][1] = -((x2-x1)*(x3-x1)+(y2-y1)*(y3-y1))
    K[2][0] = -((x3-x2)*(x1-x2)+(y3-y2)*(y1-y2))

    K = (fct_kappa((1/3)*(x1+x2+x3), (1/3)*(y1+y2+y3))/(4*mesT))*K

    return K

#coordonnees de 3 points 
def coeffelem_P1_source(x1, x2, x3, y1, y2, y3):
    """initialisation vecteur coef de la fonction source"""
    #Calcul aire triangle
    mesT = (1/2)*((x3-x1)*(y3-y2) - ((x3-x2)*(y3-y1)))

    #variable contenant le barycentre
    milieu_bary = np.zeros((2,1))
    milieu_bary[0] = (1/3)*(x1+x2+x3)
    milieu_bary[1] = (1/3)*(y1+y2+y3)

    f = (mesT/3)*fct_f(milieu_bary[0], milieu_bary[1])*np.ones((3,1))

    return f

#coordonnées 2 points 
def coeffelem_P1_transf(x1, x2, y1, y2):
    """vecteur du flux extérieur de transfert thermique"""
    #calcul longueur arrete
    mesA = sqrt((x1-x2)**2 + (y1-y2)**2)

    #calcul milieu de l'arrete
    milieu = np.array([0,0])
    milieu[0] = (1/2)*(x1+x2)
    milieu[1] = (1/2)*(y1+y2)

    b = np.ones((2,1))
    e = (mesA/2)*fct_alpha(x1, y1)*fct_uE(milieu[0], milieu[1])*b

    return e


#coordonnées 2 points
def coeffelem_P1_poids(x1, x2, y1, y2):
    """vecteur poids transfert thermique"""

    #calcul longueur de l'arrete
    mesA = sqrt((x1-x2)**2 + (y1-y2)**2)

    #déclaration matrice pour formule poids
    A = np.array([[2,1],[1,2]])
    p = (mesA/6)*fct_alpha(x1, y1)*A 

    return p


#coordonnées de 3 points
def coeffelem_P1_masse(x1, x2, x3, y1, y2, y3):
    """matrice coefficients de masse"""

    #Calcul aire triangle
    mesT = (1/2)*((x3-x1)*(y3-y2) - ((x3-x2)*(y3-y1)))

    #initialisation de la matrice I3
    I = np.eye(3,3)
    m = mesT/3 * I


    return m

def assemblage_EF_P1(nbn, nbe, nba, tri, ar, coord, refa):
    """construction du système linéaire"""

    N = nbn
    A = np.zeros((N,N))
    F = np.zeros((N,1))

    for l in range (0,nbe):
        k = coeffelem_P1_rigid(coord[int(tri[l,0]),0],coord[int(tri[l,1]),0],coord[int(tri[l,2]),0],coord[int(tri[l,0]),1],coord[int(tri[l,1]),1],coord[int(tri[l,2]),1])
        f = coeffelem_P1_source(coord[int(tri[l,0]),0],coord[int(tri[l,1]),0],coord[int(tri[l,2]),0],coord[int(tri[l,0]),1],coord[int(tri[l,1]),1],coord[int(tri[l,2]),1])
        
        I1 = int(tri[l,0])
        I2 = int(tri[l,1])
        I3 = int(tri[l,2])

        A[I1][I1] += k[0][0]
        A[I1][I2] += k[0][1]
        A[I1][I3] += k[0][2]
        A[I2][I1] += k[1][0]
        A[I2][I2] += k[1][1]
        A[I2][I3] += k[1][2]
        A[I3][I1] += k[2][0]
        A[I3][I2] += k[2][1]
        A[I3][I3] += k[2][2]
        F[I1] += f[0]
        F[I2] += f[1]
        F[I3] += f[2]

    K = A.copy()
    
    for i in range(nba): 
        #arretes Fourier-Robin
        if refa[i] == 1:
            p = coeffelem_P1_poids(coord[int(ar[i,0]),0], coord[int(ar[i,1]),0], coord[int(ar[i,0]),1], coord[int(ar[i,1]),1])
            e = coeffelem_P1_transf(coord[int(ar[i,0]),0], coord[int(ar[i,1]),0], coord[int(ar[i,0]),1], coord[int(ar[i,1]),1])
            
            I1 = int(ar[i,0])
            I2 = int(ar[i,1])
            
            A[I1][I1] += p[0][0]
            A[I1][I2] += p[0][1]
            A[I2][I1] += p[1][0]
            A[I2][I2] += p[1][1]
            F[I1] += e[0] 
            F[I2] += e[1]

    return [K,A,F]

def main():

    """fichier du maillage, A MODIFIER"""
    fichier_msh = "C:\\Users\\retio\\OneDrive\\Bureau\\CHPS706\\Finite-Elements-main\\Maillages\\m4.msh"
    
    """différents paramètres du maillage"""
    [nbn, nbe, nba, coord, tri, ar, refn, reft, refa]= lit_fichier_msh(fichier_msh)
    
    """Récupère matrices construites pour le système et résolution de ce dernier"""
    [K,A,F] = assemblage_EF_P1(nbn, nbe, nba, tri, ar, coord, refa)
    b = np.linalg.inv(A)@F
    


    """Calcul de la solution exacte"""
    U = np.zeros((nbn,1))
    for i in range(nbn):
        U[i] = fct_u(coord[i,0], coord[i,1]) 

    """Calcul de l'erreur en norme H1"""
    erreur = (U-b).T @ K @(U-b)
    
    """Calcul de l'erreur en norme infini"""
    err_inf = 0
    for i in range(nbn):
        err_i = abs(U[i] - b[i])
        if err_i > b[i]:
            err_inf = err_i[0]
    

    """Calcul du pas h et de la qualtité Q"""
    h_max, Q_h_max = pas_et_qualite_maillage(coord, tri)

    """Affichage des différentes valeurs obtenues"""
    print("================= validation_pas_a_pas ===================")
    print("nbn = ", nbn)
    print("nbe = ", nbe)
    print("nba = ", nba)
    print("A = \n", A)
    print("F = \n", F)
    print("Uh = \n", b)
    print("\n___---===*** RESULTATS: ***===---___")
    print("----------------------------------------")
    print("min(Uh) : {:.2f}".format(float(min(b))))
    print("max(Uh) : {:.2f}".format(float(max(b))))
    print("mean(Uh) : {:.2f}".format(np.mean(b)))

    print("h : ",h_max)
    print("Q : ",Q_h_max)

    print("Erreur en norme H1 entre U et Uh : \n", erreur)
    print("Erreur en norme infinie entre U et Uh  : \n", err_inf)
    
    return [A,F,b]

if __name__ =='__main__':
    [A,F,b] = main()