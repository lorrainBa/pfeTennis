import numpy as np

# Vos tableaux numpy à une dimension
array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])

# Créer des matrices 2D à partir des tableaux 1D
grid1, grid2 = np.meshgrid(array1, array2)

# Combiner les matrices en une matrice de tuples
result = np.empty(grid1.shape, dtype=object)
for index, (x, y) in np.ndenumerate(result):
    result[index] = (grid1[index], grid2[index])

print(result)
