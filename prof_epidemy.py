"""
    Epidemic simulator
"""
import sys
import time

from random import sample
from itertools import product

EMPTY = 0
INDIVIDU = 1
VACCINE = 2
MALADE = 3
REMIS = 4
MORT = 5

largeur = int(sys.argv[1])     # largeur
hauteur = int(sys.argv[2])     # hauteur
densite = float(sys.argv[3])   # densité en %
nb_vaccines = int(sys.argv[4]) # nombre de personnes vaccinées
nb_malades = int(sys.argv[5])  # nombre de personnes malades

def create_matrix(largeur, hauteur, densite, nb_malades, nb_vaccines):
    """Create the matrix"""
    nb_personnes = round(largeur * hauteur * densite)
    personnes = sample(list(product(range(hauteur), range(largeur))), nb_personnes)
    matrix = [[INDIVIDU if (row, col) in personnes else EMPTY for col in range(largeur)] for row in range(hauteur)]
    vaccines = sample(personnes, nb_vaccines)
    for row, col in vaccines:
        matrix[row][col] = VACCINE
    malades = []
    for row, col in sample(personnes, len(personnes)):
        if (row,col) not in vaccines:
            matrix[row][col] = MALADE
            malades.append((row,col))
        if len(malades) >= nb_malades:
            break
    return matrix

def str_matrix(matrix):
    """Translate matrix to text for printing"""
    translate = {
        EMPTY: ".", 
        INDIVIDU: "I", 
        VACCINE: "V", 
        MALADE: "m", 
        REMIS: "R", 
        MORT: "_"}
    output = ""
    for row in range(len(matrix)):
        output += " ".join([translate[val] for val in matrix[row]]) + "\n"
    return output

def est_malade(matrix, row, col):
    """test if a human is ill on next step"""
    NEIGHBORS = set([(0,1),(0,-1),(1,0),(-1,0)])
    for offrow, offcol in NEIGHBORS:
        nrow = row + offrow
        ncol = col + offcol
        if 0 <= nrow < len(matrix) and 0 <= ncol < len(matrix[0]):
            if matrix[nrow][ncol] == MALADE:
                return True
    return False

def step_matrix(matrix):
    """One step of epidemic spreading"""
    new_mat = []
    for irow, row in enumerate(matrix):
        new_mat.append([])
        for icol, cell in enumerate(row):
            if cell == INDIVIDU and est_malade(matrix, irow, icol):
                new_mat[irow].append(MALADE)
            elif cell == MALADE:
                new_mat[irow].append(MORT)
            else:
                new_mat[irow].append(cell)
    return new_mat

# Simulate the spread of a fire through a forest
matrix = create_matrix(largeur, hauteur, densite, nb_malades, nb_vaccines)
while True:
    print(str_matrix(matrix))
    time.sleep(1)
    new_matrix = step_matrix(matrix)
    if new_matrix == matrix:
        break
    matrix = new_matrix
