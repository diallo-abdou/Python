"""Calcul des distances entre une liste de genes et une liste de régions"""
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




print("Read Genes")
df_gene = pd.read_csv(gene_filename , header=None, delimiter='\t')
df_gene = df_gene[range(4)]
df_gene.columns = ["Chromosome","GeneStart","GeneStop","GeneName"]
nb_gene, _ = df_gene.shape
# print(df_gene)

print("Read Regions")
df_region = pd.read_csv(region_filename , header=None, delimiter='\t')
df_region = df_region[range(4)]
df_region.columns = ["Chromosome","RegionStart","RegionStop","RegionName"]
nb_region, _ = df_region.shape
# print(df_region)

################################################################################
# Fonction qui calcule une distance avec 4 paramètres
################################################################################
def calc_dist(gene_start, gene_end, region_start, region_end):
    """Calcul de la distance entre le gène et la région"""
    if region_end < gene_start :
        return gene_start - region_end
    if gene_end < region_start:
        return region_start - gene_end
    return 0

################################################################################
# Fonction qui calcule une distance avec 1 paramètre
################################################################################
def calc_dist_row(df_row):
    """Calcul de la distance entre le gène et la région"""
    region_start = df_row["RegionStart"]
    region_stop = df_row["RegionStop"]
    gene_start = df_row["GeneStart"]
    gene_stop = df_row["GeneStop"]
    if region_stop < gene_start :
        return gene_start - region_stop
    if gene_stop < region_start:
        return region_start - gene_stop
    return 0


################################################################################
# Énumération avec double boucle
################################################################################
brut_res = set()
if nb_gene * nb_region > 150000:
    print("Too much pairs for basic enumerate :", nb_gene * nb_region)
else:
    start = default_timer()
    nb_paire = 0
    # Pour chaque region
    for r_row in range(len(df_region['Chromosome'])) :
        region_name = df_region.iloc[r_row]['RegionName']
        region_chrom = df_region.iloc[r_row]['Chromosome']
        # pour chaque gene
        for g_row in range(len(df_gene['Chromosome'])) :
            gene_name = df_gene.iloc[g_row]['GeneName']
            gene_chrom = df_gene.iloc[g_row]['Chromosome']
            if gene_chrom == region_chrom:
                region_start = df_region.iloc[r_row]["RegionStart"]
                region_stop = df_region.iloc[r_row]["RegionStop"]
                gene_start = df_gene.iloc[g_row]["GeneStart"]
                gene_stop = df_gene.iloc[g_row]["GeneStop"]
                dist = calc_dist(gene_start, gene_stop, region_start, region_stop)
                brut_res.add(dist)
    end = default_timer()
    print("nb paire :", nb_paire)
    print("temps double boucle                      :", end - start)
time_brut = end - start
################################################################################
# Énumération avec group_by
################################################################################
# start = default_timer()
# gene_groups = df_gene.groupby('Chromosome')
# region_groups = df_region.groupby('Chromosome')
# nb_paire = 0
# for chrom, sub_region in region_groups:
#     if chrom in gene_groups.indices:
#         sub_gene = gene_groups.get_group(chrom)
#         for i in range(len(sub_region)):
#             for j in range(len(sub_gene)):
#                 nb_paire += 1
# end = default_timer()
# print("nb paire :", nb_paire)
# print("temps group_by :", end - start)

###############################################################################
# Énumération avec group_by + distance
###############################################################################
gr_res = set()
start = default_timer()
gene_groups = df_gene.groupby('Chromosome')
region_groups = df_region.groupby('Chromosome')
common_chrom = set(gene_groups.indices.keys()) & set(region_groups.indices.keys())
for chrom in common_chrom:
    sub_region = region_groups.get_group(chrom)
    sub_gene = gene_groups.get_group(chrom)
    for i in range(len(sub_region)):
        region_start = sub_region.iloc[i]["RegionStart"]
        region_stop = sub_region.iloc[i]["RegionStop"]
        for j in range(len(sub_gene)):
            gene_start = sub_gene.iloc[j]["GeneStart"]
            gene_stop = sub_gene.iloc[j]["GeneStop"]
            dist = calc_dist(gene_start, gene_stop, region_start, region_stop)
            gr_res.add(dist)
end = default_timer()
print("temps group_by + dist                    :", end - start, "\tratio :", time_brut / (end - start))
print(gr_res==brut_res)
###############################################################################
# Énumération avec group_by + iterrows + dist
###############################################################################
gr_iter_res = set()
start = default_timer()
gene_groups = df_gene.groupby('Chromosome')
region_groups = df_region.groupby('Chromosome')
common_chrom = set(gene_groups.indices.keys()) & set(region_groups.indices.keys())
for chrom in common_chrom:
    sub_region = region_groups.get_group(chrom)
    sub_gene = gene_groups.get_group(chrom)
    for _, region_row in sub_region.iterrows():
        region_start = region_row["RegionStart"]
        region_stop = region_row["RegionStop"]
        for _, gene_row in sub_gene.iterrows():
            gene_start = gene_row["GeneStart"]
            gene_stop = gene_row["GeneStop"]
            dist = calc_dist(gene_start, gene_stop, region_start, region_stop)
            gr_iter_res.add(dist)
end = default_timer()
print("temps group_by + iterrows + dist         :", end - start, "\tratio :", time_brut / (end - start))
print(gr_iter_res==brut_res)
###############################################################################
# Énumération avec group_by + merge + iterrows + dist
###############################################################################
merge_iter_res = set()
start = default_timer()
gene_groups = df_gene.groupby('Chromosome')
region_groups = df_region.groupby('Chromosome')
common_chrom = set(gene_groups.indices.keys()) & set(region_groups.indices.keys())
for chrom in common_chrom:
    sub_region = region_groups.get_group(chrom)
    sub_gene = gene_groups.get_group(chrom)
    sub_df = pd.merge(sub_region, sub_gene, how='left', on='Chromosome')
    for _, df_row in sub_df.iterrows():
        region_start = df_row["RegionStart"]
        region_stop = df_row["RegionStop"]
        gene_start = df_row["GeneStart"]
        gene_stop = df_row["GeneStop"]
        dist = calc_dist(gene_start, gene_stop, region_start, region_stop)
        merge_iter_res.add(dist)
end = default_timer()
print("temps group_by + merge + iterrows + dist :", end - start, "\tratio :", time_brut / (end - start))
print(merge_iter_res==brut_res)
###############################################################################
# Énumération avec group_by + merge + apply + dist
###############################################################################
merge_apply_res = set()
start = default_timer()
gene_groups = df_gene.groupby('Chromosome')
region_groups = df_region.groupby('Chromosome')
common_chrom = set(gene_groups.indices.keys()) & set(region_groups.indices.keys())
for chrom in common_chrom:
    sub_region = region_groups.get_group(chrom)
    sub_gene = gene_groups.get_group(chrom)
    sub_df = pd.merge(sub_region, sub_gene, how='left', on='Chromosome')
    sub_df['Distance'] = sub_df.apply(calc_dist_row , axis=1)
    merge_apply_res |= set(sub_df['Distance'])
end = default_timer()
print("temps group_by + merge + apply + dist    :", end - start, "\tratio :", time_brut / (end - start))
print(merge_apply_res==brut_res)
###############################################################################
# Énumération avec group_by + merge + column
###############################################################################
merge_col_res = set()
start = default_timer()
gene_groups = df_gene.groupby('Chromosome')
region_groups = df_region.groupby('Chromosome')
common_chrom = set(gene_groups.indices.keys()) & set(region_groups.indices.keys())
for chrom in common_chrom:
    sub_region = region_groups.get_group(chrom)
    sub_gene = gene_groups.get_group(chrom)
    sub_df = pd.merge(sub_region, sub_gene, how='left', on='Chromosome')
    sub_df['Distance'] = 0
    sub_df.loc[sub_df["RegionStop"] < sub_df["GeneStart"], "Distance"] = sub_df["GeneStart"] - sub_df["RegionStop"]
    sub_df.loc[sub_df["GeneStop"] < sub_df["RegionStart"], "Distance"] = sub_df["RegionStart"] - sub_df["GeneStop"]
    merge_col_res |= set(sub_df['Distance'])
    # print(sub_df['Distance'])
end = default_timer()
print("temps group_by + merge + column          :", end - start, "\tratio :", time_brut / (end - start))
print(merge_col_res==brut_res)