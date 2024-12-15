import matplotlib.pyplot as plt
import matplotlib.tri as tri
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
def afficher_maillage(coord,trian):
        
        # Affichage du maillage
    plt.figure(figsize=(10, 5))
    plt.triplot(coord[:, 0], coord[:, 1], trian)

    # Ajout des numéros des noeuds
    for i in range(nbn):
        plt.text(coord[i, 0], coord[i, 1], str(i+1), color='red', fontsize=12)

    # Ajout des numéros des triangles
    for i in range(nbe):
        x = (coord[trian[i, 0]-1, 0] + coord[trian[i, 1]-1, 0] + coord[trian[i, 2]-1, 0]) / 3
        y = (coord[trian[i, 0]-1, 1] + coord[trian[i, 1]-1, 1] + coord[trian[i, 2]-1, 1]) / 3
        plt.text(x, y, str(i+1), color='blue', fontsize=12)

    # Ajout des numéros des arêtes
    for i in range(nba):
        x = (coord[ar[i, 0]-1, 0] + coord[ar[i, 1]-1, 0]) / 2
        y = (coord[ar[i, 0]-1, 1] + coord[ar[i, 1]-1, 1]) / 2
        plt.text(x, y, str(i+1), color='green', fontsize=12)

    plt.title("Maillage Éléments Finis de type P1")
    plt.xlabel("axe Ox")
    plt.ylabel("axe Oy")
    plt.axis('equal')
    plt.show()

# Exemple d'utilisation : lecture et affichage du maillage
#nbn, nbe, nba, coord, trian, ar, refn, reft, refa = lit_fichier_msh("m1.msh")
#afficher_maillage(coord, trian)

def trace_maillage_ind(nbn, nbe, nba, coord, tri, ar):
    plt.figure(figsize=(10, 5))
    plt.triplot(coord[:, 0], coord[:, 1], tri)

    # Numéros des noeuds
    for i in range(nbn):
        plt.text(coord[i, 0], coord[i, 1], str(i+1), color='red', fontsize=10, ha='right', va='bottom')

    # Numéros des triangles
    for i in range(nbe):
        x = np.mean(coord[tri[i], 0])
        y = np.mean(coord[tri[i], 1])
        plt.text(x, y, str(i+1), color='blue', fontsize=10, ha='center', va='center')

    # Numéros des arêtes
    for i in range(nba):
        x = np.mean(coord[ar[i], 0])
        y = np.mean(coord[ar[i], 1])
        plt.text(x, y, str(i+1), color='green', fontsize=10, ha='left', va='bottom')

    plt.title("Maillage avec indices")
    plt.xlabel("axe Ox")
    plt.ylabel("axe Oy")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def trace_maillage_ref(nbn, nbe, nba, coord, tri, ar, refn, reft, refa):
    plt.figure(figsize=(10, 5))
    plt.triplot(coord[:, 0], coord[:, 1], tri)

    # Références des noeuds
    for i in range(nbn):
        plt.text(coord[i, 0], coord[i, 1], str(refn[i]), color='red', fontsize=10, ha='right', va='bottom')

    # Références des triangles
    for i in range(nbe):
        x = np.mean(coord[tri[i], 0])
        y = np.mean(coord[tri[i], 1])
        plt.text(x, y, str(reft[i]), color='blue', fontsize=10, ha='center', va='center')

    # Références des arêtes
    for i in range(nba):
        x = np.mean(coord[ar[i], 0])
        y = np.mean(coord[ar[i], 1])
        plt.text(x, y, str(refa[i]), color='green', fontsize=10, ha='left', va='bottom')

    plt.title("Maillage avec références")
    plt.xlabel("axe Ox")
    plt.ylabel("axe Oy")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def charge_et_affiche_maillage(FichierMaillage):
    # Lecture du fichier
    nbn, nbe, nba, coord, tri, ar, refn, reft, refa = lit_fichier_msh(FichierMaillage)
    
    # Affichage avec indices
    trace_maillage_ind(nbn, nbe, nba, coord, tri, ar)
    
    # Affichage avec références
    trace_maillage_ref(nbn, nbe, nba, coord, tri, ar, refn, reft, refa)

# Utilisation
#FichierMaillage = "./rectangle_4x2_non_struct.msh"
#charge_et_affiche_maillage(FichierMaillage)

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

FichierMaillage = "C:\\Users\\retio\\OneDrive\\Bureau\\CHPS706\\Finite-Elements-main\\Maillages\\m1.msh"
nbn, nbe, nba, coord, trian, ar, refn, reft, refa = lit_fichier_msh(FichierMaillage)

h_max, Q_h_max = pas_et_qualite_maillage(coord, trian)
print(f"Pas du maillage h = {h_max:.6f}")
print(f"Qualité du maillage Q_h = {Q_h_max:.6f}")
charge_et_affiche_maillage(FichierMaillage)