 Sudoku colores

# Instrucciones de instalación: 
from gurobipy import * 
import numpy as np

# Creacion del modelo: Sudoku colores
Matriz = np.zeros((6,6))
m = Model('Sudoku colores')
secciones = np.genfromtxt("aij_colores.csv", delimiter = ",")
n = int(np.amax(secciones[:,2])+1) # Numero de regiones + 1
suma = 9

I = np.arange(1,7)       #I = {1,..,6}
J = np.arange(1,7)       #J = {1,..,6}
K = np.arange(1,7)       #K = {1,..,6}

# Creacion de las variables
y = m.addVars(I,J,K, vtype = GRB.BINARY, name = "y")

# Restricciones de fila y columna no repetidas
m.addConstrs(quicksum(y[i,j,k] for j in J) == 1 for i in I for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in I) == 1 for j in J for k in K)

# Restricciones de suma por regiones
for i in range(1, n):
  tmp = np.where(secciones[:,2] == i)
  m.addConstr(quicksum(k*y[secciones[int(l),0], secciones[int(l),1], k] for k in K for l in tmp[0]) == suma)

# Restriccion cada celda debe de tener un valor entre 1 y 6
m.addConstrs(quicksum(y[i,j,k] for k in K ) == 1 for j in J for i in I)

m.setObjective(0 , GRB.MAXIMIZE)
m.optimize()
for i in I:
  for j in J:
    for k in K: 
      if y[i,j,k].X != 0:
        Matriz[i-1,j-1] = k   

print(Matriz)
