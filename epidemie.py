import argparse
from random import shuffle, randint, sample
import matplotlib.pyplot as plt


def graphique (x,y):
    plt.figure()
    plt.plot(x,y)
    plt.xlabel("temps")
    plt.ylabel("Pourcentage du nombre de mort")
    plt.title("Evolution de la population")
    
    plt.show()


def evolution (matrice,ind):
    nbr=[]
    for row in range(len(matrice)):
        for col in range(len(matrice[0])):
            if matrice[row][col] == int(ind):
                   nbr.append(1)
    pourc= (sum(nbr)*100)/len(matrice)**2
    return pourc

def propagation (matrice):
        # symboles
    empty = 0; sain_nv = 1 ; sain_v = 2 ; atteint = 3; retabli = 4; mort = 5
    
    # nouvelle matrice pour l'étappe suivante
    nouvelle_matrice = [[0 for _ in range(len(matrice[0]))] for _ in range(len(matrice))]
    
    # On parcour la matrice existante pour appliquer les règles
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            cellule_actuelle = matrice[i][j]
            cellule_suivante = cellule_actuelle  # Par défaut, la cellule reste vide

            # 1. un ”individu sain vacciné” ne peut pas être malade ;
            if cellule_actuelle == sain_v:
                cellule_suivante== sain_v
                
            # 2. un ”individu sain non vacciné” dont un des voisins est un ”individu atteint” à
            #l’état actuel devient un ”individu atteint” à l’étape suivante, sinon il ne change pas d’état ;
            elif cellule_actuelle == sain_nv:
                # Si un arbre est à côté d'un arbre en feu, il brûlera à l'étape suivante
                if any(
                    matrice[x][y] == atteint
                    for x in range(max(0, i - 1), min(len(matrice), i + 2))
                    for y in range(max(0, j - 1), min(len(matrice[0]), j + 2))
                ):
                    cellule_suivante = atteint
                else:
                    cellule_suivante = sain_nv  # Sinon, l'arbre reste tel quel
            
            #3. un ”individu atteint” à l’état actuel devient un ”individu mort” à l’étape suivante ;
            elif cellule_actuelle == atteint:
                cellule_suivante = mort
                
            #4. un ”individu rétabli” ne peut plus être malade ;
            elif cellule_actuelle == retabli:
                cellule_suivante = retabli
            
            #5. les cellules vides restent vides.
            elif cellule_actuelle == empty:
                cellule_suivante = empty
            
            elif cellule_actuelle==mort:
                cellule_suivante=mort
                
            # on met  à jour la nouvelle matrice
            nouvelle_matrice[i][j] = cellule_suivante

    return nouvelle_matrice




def simul_epidemie (larg, long, sain_nv, sain_v,  atteint):
    
    # On cree d'abord une matrice avec que des 0: pas d'individu
    matrice = [[0 for _ in range(larg)] for _ in range(long)]
    
    
    nb_case_all = round(larg * long * sain_nv)
    nb_put = 0
    #coord_tree = []
    while nb_put < nb_case_all:
        row = randint(0, long-1)
        col = randint(0, larg-1)
        if matrice[row][col] == 0:
            matrice[row][col] = 1
            #coord_tree.append((row,col))
            nb_put += 1
    
    
    
    # Definition d'une fonction pour le remplissage aleatoir
    def rempli_alea (dens, valeur):
        nb_case_all= round(larg * long * sain_nv)
        nb_case = round(int(nb_case_all* dens))
        nb_put = 0
        #coord_tree = []
        while nb_put < nb_case:
            row = randint(0, long-1)
            col = randint(0, larg-1)
            if matrice[row][col] == 1:
                matrice[row][col] = int(valeur)
                #coord_tree.append((row,col))
                nb_put += 1
        return matrice
    
    
    # pour les individu sain non vacine :1 position aleatoi
    #rempli_alea(dens=sain_nv,valeur=1)
    
    # pour les individu sain  vacine :2 position aleatoi
    rempli_alea(dens=sain_v,valeur=2)
    
    # pour les individu atteint :3 position aleatoi
    rempli_alea(dens=atteint,valeur=3)
    
    
    # def fonction pour affiché les matrice
    def print_matric (mat):
        print( "\n ******************************************** \n")
        for row in mat:
            print(row)
    
    # affiche de la matrice de base
    #print_matric(matrice.copy())
    
    # Suivi des evolution dans le temps
    mat=matrice.copy()
    #tau_mort=[0]
    #dens_tot=[long*larg*sain_nv]
    #for _ in range(10):
        #matrice_propa = propagation(mat) # propagaton
        #nbr_mort = evolution(matrice_propa.copy(),5)# suivi des mort
        #tau_mort.append(nbr_mort)
        #print_matric(matrice_propa.copy())
        #dens_tot.append ( (long*larg*sain_nv) - nbr_mort- evolution(matrice_propa.copy(),0))
        #mat=matrice_propa.copy()
    
    matrice_suiv = propagation(mat)
    while matrice_suiv != mat:
        matrice_suiv = propagation(mat) # propagaton
        mat= matrice_suiv
    
    nbr_mort = evolution(matrice_suiv.copy(),5)# suivi des mort
    #tau_mort.append(nbr_mort)
    #print_matric(matrice_propa.copy())
    
    
    print(nbr_mort)
    #print(dens_tot)
    #graphique (list(range(11)),tau_mort)
    
    
    
    # Propagation
    #matrice_propa = propagation(matrice.copy())
    #print_matric(matrice_propa.copy())
    
    
    # Suivi de l'evolution
    #nbr_mort = evolution(matrice_propa.copy(),5)
    #print(sum(nbr_mort))
    
    return [ nbr_mort,  sain_nv ]



    # On cree d'un objet ArgumentParser



print("Recuperation du nombre de mort et de la densité")
print(simul_epidemie(10,10,0.1,0.1,0.1) )