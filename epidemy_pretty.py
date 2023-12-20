"""
    Epidemic simulator
"""
import time
import click

from random import random, sample
from rich.live import Live
from rich.text import Text
from itertools import product

EMPTY = 0
INDIVIDU = 1
VACCINE = 2
MALADE = 3
REMIS = 4
MORT = 5

def create_matrix(largeur, hauteur, densite, nb_malades, nb_vaccines):
    """Create the matrix"""
    nb_personnes = round(largeur * hauteur * densite)
    personnes = sample(list(product(range(hauteur), range(largeur))), nb_personnes)
    matrix = [[INDIVIDU if (row, col) in personnes else EMPTY for row in range(largeur)] for col in range(hauteur)]
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

def print_matrix(matrix) -> Text:
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
    return Text(output)

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

@click.command()
@click.option('--width', default=5, help='Width of the matrix.')
@click.option('--height', default=5, help='Height of the matrix.')
@click.option('--density', default=1.0, help='Density of trees in the matrix.')
@click.option('--vaccine', default=1, help='Percent of vaccine.')
@click.option('--nbill', default=1, help='Number of ill people.')
def forest_fire(width, height, density, vaccine, nbill):
    """Simulate the spread of a fire through a forest"""
    matrix = create_matrix(width, height, density, nbill, vaccine)
    with Live(print_matrix(matrix), refresh_per_second=2) as live:  # update 4 times a second to feel fluid
        while True:
            time.sleep(1)
            new_matrix = step_matrix(matrix)
            if new_matrix == matrix:
                break
            matrix = new_matrix
            live.update(print_matrix(matrix))
            
        
if __name__ == '__main__':
    forest_fire()

