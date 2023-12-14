
larg=10
long=10
DENS=0.1
dens=0.1

all_dens=larg*long*DENS
print(all_dens)

print(all_dens*dens)


    if (sain_nv +sain_v+atteint+retabli)>1:
        message=["La densité des casses des individus depasse 1"]
        return message
    





parser = argparse.ArgumentParser(description='Simulation d\'une propagation bi-dimensionnelle : épidémie.')

    # On ajote les arguments
parser.add_argument('-la' ,'--larg', type=int, default=10)
parser.add_argument('-lo' ,'--long', type=int, default=10) # j'ai mis -he car -h creer un conflit avec l'argument help (-h)
#parser.add_argument('-d' ,'--dens_pop', type=float, default=0.1)
parser.add_argument('-snv' ,'--sain_nv', type=float, default=0.5)
parser.add_argument('-sv' ,'--sain_v', type=float, default=0.1)
parser.add_argument('-a' ,'--atteint', type=float, default=0.1)
# On analyse les arguments de la ligne de commande
args = parser.parse_args()
if __name__ == '__main__':
    simul_epidemie(args.larg, args.long,args.sain_nv, args.sain_v, args.atteint,)
    

#simul_epidemie(10,10,0.3,0.1,0.4,0.1)
