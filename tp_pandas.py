"""Calcul des distances entre une liste de regions et une liste de régions"""
import pandas as pd
from timeit import default_timer

# gene_filename = "data/gene1.bed"
# region_filename = "data/region1.bed"
gene_filename = "data/gene_300.bed"
region_filename = "data/region_400.bed"
# gene_filename = "data/gene_chr20_300.bed"
# region_filename = "data/region_chr20_300.bed"
# gene_filename = "data/gene_localisation.bed"
# region_filename = "data/region_localisation.bed"

def calc_dist(gstart, gstop, rstart, rstop):
    if gstart > rstop:
        return gstart - rstop
    if rstart > gstop:
        return rstart - gstop
    return 0

def calc_dist_row(df_row):
    gstart = df_row["GeneStart"]
    gstop = df_row["GeneStop"]
    rstart = df_row["RegionStart"]
    rstop = df_row["RegionStop"]
    if gstart > rstop:
        return gstart - rstop
    if rstart > gstop:
        return rstart - gstop
    return 0

print("Read Genes")
df_gene = pd.read_csv(gene_filename , header=None, delimiter='\t')
df_gene = df_gene[range(4)]
df_gene.columns = ["Chromosome","GeneStart","GeneStop","GeneName"]
nb_gene_row, nb_gene_col = df_gene.shape
# print(df_gene)

print("Read Regions")
df_region = pd.read_csv(region_filename , header=None, delimiter='\t')
df_region = df_region[range(4)]
df_region.columns = ["Chromosome","RegionStart","RegionStop","RegionName"]
nb_region_row, nb_region_col = df_region.shape
# print(df_region)

############################################################
# Version brute avec double boucle
############################################################
start_time = default_timer()
paires_brute = set()
nb_paire = 0
nb_total = 0
# Pour chaque region
for r_row in range(nb_region_row) :
    region_name = df_region.iloc[r_row]['RegionName']
    region_chrom = df_region.iloc[r_row]['Chromosome']
    region_start = df_region.iloc[r_row]['RegionStart']
    region_stop = df_region.iloc[r_row]['RegionStop']
    # pour chaque gene
    for g_row in range(nb_gene_row) :
        gene_name = df_gene.iloc[g_row]['GeneName']
        gene_chrom = df_gene.iloc[g_row]['Chromosome']
        gene_start = df_gene.iloc[g_row]['GeneStart']
        gene_stop = df_gene.iloc[g_row]['GeneStop']
        nb_total += 1
        if gene_chrom == region_chrom:
            distance = calc_dist(gene_start, gene_stop, region_start, region_stop)
            paires_brute.add(distance)
            nb_paire += 1

print(nb_paire, "/", nb_total, "=", nb_paire/nb_total)
end_time = default_timer()
print("brute-force loops =", end_time-start_time)

############################################################
# Version avec groupby
############################################################
group_gene = df_gene.groupby(by="Chromosome")
group_region = df_region.groupby(by="Chromosome")

## enumère les chromosomes dans les sous-groupes
start_time = default_timer()
paires_groupby = set()
for chrom in group_gene.indices:
    if chrom in group_region.indices:
        sub_gene = group_gene.get_group(chrom)
        sub_region = group_region.get_group(chrom)
        nb_sub_gene_row, nb_sub_gene_col = sub_gene.shape
        nb_sub_region_row, nb_sub_region_col = sub_region.shape
        # énumère les lignes des sous-groupes
        for r_row in range(nb_sub_region_row) :
            region_name = sub_region.iloc[r_row]['RegionName']
            region_start = sub_region.iloc[r_row]['RegionStart']
            region_stop = sub_region.iloc[r_row]['RegionStop']
            for g_row in range(nb_sub_gene_row) :
                gene_name = sub_gene.iloc[g_row]['GeneName']
                gene_start = sub_gene.iloc[g_row]['GeneStart']
                gene_stop = sub_gene.iloc[g_row]['GeneStop']
                distance = calc_dist(gene_start, gene_stop, region_start, region_stop)
                paires_groupby.add(distance)
end_time = default_timer()
print("groupby loops =", end_time-start_time)
print(paires_brute == paires_groupby)

############################################################
# Version avec iterrows
############################################################
start_time = default_timer()
paires_iter = set()
for chrom in group_gene.indices:
    if chrom in group_region.indices:
        sub_gene = group_gene.get_group(chrom)
        sub_region = group_region.get_group(chrom)
        # énumère les lignes des sous-groupes
        for r_row, region_line in sub_region.iterrows() :
            region_name = region_line['RegionName']
            region_start = region_line['RegionStart']
            region_stop = region_line['RegionStop']
            for g_row, gene_line in sub_gene.iterrows() :
                gene_name = gene_line['GeneName']
                gene_start = gene_line['GeneStart']
                gene_stop = gene_line['GeneStop']
                distance = calc_dist(gene_start, gene_stop, region_start, region_stop)
                paires_iter.add(distance)
end_time = default_timer()
print("iterrows loops =", end_time-start_time)
print(paires_brute == paires_iter)

############################################################
# Version avec merge
############################################################
start_time = default_timer()
paires_merge = set()
for chrom in group_gene.indices:
    if chrom in group_region.indices:
        sub_gene = group_gene.get_group(chrom)
        sub_region = group_region.get_group(chrom)
        sub_df = pd.merge(sub_region, sub_gene, how='left', on='Chromosome')
        for _, df_line in sub_df.iterrows():
            region_name  = df_line['RegionName']
            gene_name    = df_line['GeneName']
            distance = calc_dist_row(df_line)
            paires_merge.add(distance)
end_time = default_timer()
print("merge loops =", end_time-start_time)
print(paires_brute == paires_merge)



############################################################
# Version avec apply
############################################################
start_time = default_timer()
paires_apply = set()
for chrom in group_gene.indices:
    if chrom in group_region.indices:
        sub_gene = group_gene.get_group(chrom)
        sub_region = group_region.get_group(chrom)
        sub_df = pd.merge(sub_region, sub_gene, how='left', on='Chromosome')
        sub_df['Distance'] = sub_df.apply(calc_dist_row , axis=1)
        paires_apply |= set(sub_df['Distance'])
end_time = default_timer()
print("apply loops =", end_time-start_time)
print(paires_brute == paires_apply)
