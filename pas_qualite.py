import numpy as np 

def calcul_longueur_arrete(p1, p2):
    return np.linalg.norm(p1 - p2)

def calcul_rayon_cercle_circonscrit(a, b, c):
    # Utilise la formule de Héron pour l'aire
    s = (a + b + c) / 2
    aire = np.sqrt(s * (s - a) * (s - b) * (s - c))
    # Rayon du cercle circonscrit
    return (a * b * c) / (4 * aire)

def pas_et_qualite_maillage(coord, tri):
    h_max = 0
    Q_h_max = 0
    
    for t in tri:
        # Récupération des coordonnées des sommets du triangle
        p1, p2, p3 = coord[t[0]], coord[t[1]], coord[t[2]]
        
        # Calcul des longueurs des arêtes
        l1 = calcul_longueur_arrete(p1, p2)
        l2 = calcul_longueur_arrete(p2, p3)
        l3 = calcul_longueur_arrete(p3, p1)
        
        # Calcul du pas local (la plus grande longueur d'arête)
        h_T = max(l1, l2, l3)
        h_max = max(h_max, h_T)
        
        # Calcul de la qualité locale
        R = calcul_rayon_cercle_circonscrit(l1, l2, l3)
        lmin = min(l1, l2, l3)
        Q_T = R / lmin
        Q_h_max = max(Q_h_max, Q_T)

    return h_max, Q_h_max

# Exemple d'utilisation
coord = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0.5, 0]])
tri = np.array([[0, 1, 2], [0, 1, 3]])

h_max, Q_h_max = pas_et_qualite_maillage(coord, tri)
print("Pas du maillage h:", h_max)
print("Qualité du maillage Qh:", Q_h_max)





def calcul_longueur_arrete(p1, p2):
    return np.linalg.norm(p1 - p2)

def calcul_rayon_cercle_circonscrit(a, b, c):
    # Utilise la formule de Héron pour l'aire
    s = (a + b + c) / 2
    aire = np.sqrt(s * (s - a) * (s - b) * (s - c))
    # Rayon du cercle circonscrit
    return (a * b * c) / (4 * aire)

def pas_et_qualite_maillage(coord, tri):
    h_max = 0
    Q_h_max = 0
    
    for t in tri:
        # Récupération des coordonnées des sommets du triangle
        p1, p2, p3 = coord[t[0]], coord[t[1]], coord[t[2]]
        
        # Calcul des longueurs des arêtes
        l1 = calcul_longueur_arrete(p1, p2)
        l2 = calcul_longueur_arrete(p2, p3)
        l3 = calcul_longueur_arrete(p3, p1)
        
        # Calcul du pas local (la plus grande longueur d'arête)
        h_T = max(l1, l2, l3)
        h_max = max(h_max, h_T)
        
        # Calcul de la qualité locale
        R = calcul_rayon_cercle_circonscrit(l1, l2, l3)
        lmin = min(l1, l2, l3)
        Q_T = R / lmin
        Q_h_max = max(Q_h_max, Q_T)

    return h_max, Q_h_max

# Exemple d'utilisation
coord = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0.5, 0]])
tri = np.array([[0, 1, 2], [0, 1, 3]])

h_max, Q_h_max = pas_et_qualite_maillage(coord, tri)
print("Pas du maillage h:", h_max)
print("Qualité du maillage Qh:", Q_h_max)