import sys

from pprint import pprint
from random import shuffle, randint, sample

WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])
DENS = float(sys.argv[3])
NB_BURN = int(sys.argv[4])

print("VERSION SYS")
print("width      =", WIDTH)
print("height     =", HEIGHT)
print("density    =", DENS)
print("nb_burning =", NB_BURN)

matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# for row in range(WIDTH):
#     for col in range(HEIGHT):
#         alea = random()
#         if alea < DENS:
#             matrix[row][col] = 1

nb_tree = round(WIDTH * HEIGHT * DENS)
nb_put = 0
coord_tree = []
while nb_put < nb_tree:
    row = randint(0, HEIGHT-1)
    col = randint(0, WIDTH-1)
    if matrix[row][col] == 0:
        matrix[row][col] = 1
        coord_tree.append((row,col))
        nb_put += 1

# VERSION SAMPLE
for row, col in sample(coord_tree, NB_BURN):
    matrix[row][col] = 2

# VERSION SHUFFLE
# shuffle(coord_tree)
# for i in range(NB_BURN):
#     row, col = coord_tree[i]
#     matrix[row][col] = 2

# VERSION ALEATOIRE
# nb_put = 0
# while nb_put < NB_BURN:
#     row = randint(0, HEIGHT-1)
#     col = randint(0, WIDTH-1)
#     if matrix[row][col] == 1:
#         matrix[row][col] = 2
#         nb_put += 1


pprint(matrix)

def str_matrix(mat):
    translate = {0: ".", 1: "T", 2: "f", 3: "_"}
    result = ""
    for ligne in mat:
        result += " ".join([translate[toto] for toto in ligne]) + "\n"
    return result

affichage = str_matrix(matrix)
print(affichage)