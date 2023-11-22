
# TD UE Python 2
import argparse
import random




def affichage(matrice): # prend en argument la matrice de base
    # modifion l'affiche de la matrice: vide = ., tree = T, feu = f et cendre = _
    # On doit afficher la forêt initiale sans modifier la matrice de base
    print("\n")
    for row in matrice:
        symbols = {'0': '.', '1': 'T', '2': 'f','3':'_'}
        print(' '.join(symbols[str(cell)] for cell in row))
# fin


def simulation(matrice):
    # symboles
    empty = 0
    tree = 1
    burning_tree = 2
    ashes = 3

    # nouvelle matrice pour l'étappe suivant
    nouvelle_matrice = [[0 for _ in range(len(matrice[0]))] for _ in range(len(matrice))]

    # On parcour la matrice existante pour appliquer les règles
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            cellule_actuelle = matrice[i][j]
            cellule_suivante = empty  # Par défaut, la cellule reste vide

            if cellule_actuelle == tree:
                # Si un arbre est à côté d'un arbre en feu, il brûlera à l'étape suivante
                if any(
                    matrice[x][y] == burning_tree
                    for x in range(max(0, i - 1), min(len(matrice), i + 2))
                    for y in range(max(0, j - 1), min(len(matrice[0]), j + 2))
                ):
                    cellule_suivante = burning_tree
                else:
                    cellule_suivante = tree  # Sinon, l'arbre reste tel quel
            elif cellule_actuelle == burning_tree:
                # Si un arbre est en train de brûler, il sera réduit en cendres à l'étape suivante
                cellule_suivante = ashes
            elif cellule_actuelle == ashes:
                # Si une cellule est dèja en cendre, elle reste en cendres a l'étappe suivant 
                cellule_suivante = ashes

            # Mettre à jour la nouvelle matrice
            nouvelle_matrice[i][j] = cellule_suivante

    return nouvelle_matrice



def simulation_feux(width, height, density, nb_burning):
    # On cree d'abord une matrice avec que des 0
    matrice = [[0 for _ in range(width)] for _ in range(height)]

    # On ajote les arbres
    num_trees = int(width * height * density)
    tree_positions = random.sample(range(width * height), num_trees)
    for position in tree_positions:
        row, col = divmod(position, width)
        matrice[row][col] = 1  # les positions des arbres sont marquées comme 1

    # Choisir aléatoirement des arbres en feu au début
    b_positions = random.sample(tree_positions, nb_burning)
    for position in b_positions:
        row, col = divmod(position, width)
        matrice[row][col] = 2  # Les positions des arbres en feux comme 2

    print("\n")
    print("\n **************** Matrice de base est: *****************")
    for row in matrice:
        print(row) # on affiche la matrice de base / forêt initale
    
    matrice_affiche =matrice
    print("\n **************** Matrice transformée est: *****************")
    matrice_affiche = affichage(matrice_affiche)


    #  simulation 
    matrice_simul= simulation(matrice)

    print("\n **************** Après une 1ere simultiona, la matrice est: *****************")
    matrice_simul= affichage(matrice_simul)
   
    return  matrice_simul
# fin


    # Création d'un objet ArgumentParser
parser = argparse.ArgumentParser(description='Simulation de feux de forêt.')

    # On ajote les arguments
parser.add_argument('-w' ,'--width', type=int, default=10)
parser.add_argument('-h' ,'--height', type=int, default=10)
parser.add_argument('-d' ,'--density', type=float, default=0.5)
parser.add_argument('-b' ,'--nb_burning', type=int, default=1)

 
    # On analyse les arguments de la ligne de commande
args = parser.parse_args()
if __name__ == '__main__':
    #simulation_feux(args.w, args.h, args.d, args.b)
    simulation_feux(args.width, args.height, args.density, args.nb_burning) 