!python -m pip install -i https://pypi.gurobi.com gurobipy
# Sudoku diagonal
# Instrucciones de instalación: 
from gurobipy import * 
import numpy as np

# Creacion del modelo: Sudoku Diagonal 
Matriz = np.zeros((9,9))
m = Model('Sudoku con Diagonal')
I = np.arange(1,10)       #I = {1,..,9}
J = np.arange(1,10)       #J = {1,..,9}
K = np.arange(1,10)

#Creacion de las variables
y = m.addVars(I,J,K, vtype = GRB.BINARY, name = "y")

# Restricciones
entradas = open("aij_diagonal_4.csv", "r")

for lineas in entradas:
    fil = int(lineas[0])
    col = int(lineas[2])
    var = int(lineas[4])
    m.addConstr(y[fil,col,var] == 1)


# Restricciones de fila y columna no repetidas
m.addConstrs(quicksum(y[i,j,k] for j in J) == 1 for i in I for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in I) == 1 for j in J for k in K)

# Restricciones de diagonales 
m.addConstrs(quicksum(y[i,i,k] for i in I) == 1 for k in K)
m.addConstrs(quicksum(y[i,10 - i,k] for i in I ) == 1  for k in K)

# Restricciones de secciones cuadradas
m.addConstrs(quicksum(y[i,j,k] for i in range(1,4) for j in range(1,4)) == 1 for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in range(1,4) for j in range(4,7)) == 1 for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in range(1,4) for j in range(7,10)) == 1 for k in K)

m.addConstrs(quicksum(y[i,j,k] for i in range(4,7) for j in range(1,4)) == 1 for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in range(4,7) for j in range(4,7)) == 1 for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in range(4,7) for j in range(7,10)) == 1 for k in K)

m.addConstrs(quicksum(y[i,j,k] for i in range(7,10) for j in range(1,4)) == 1 for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in range(7,10) for j in range(4,7)) == 1 for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in range(7,10) for j in range(7,10)) == 1 for k in K)

# Restriccion cada celda debe de tener un valor entre 1 y 9
m.addConstrs(quicksum(y[i,j,k] for k in K ) == 1 for j in J for i in I)
m.setObjective(0 , GRB.MINIMIZE)
m.optimize()

for i in I:
  for j in J:
    for k in K: 
      if y[i,j,k].X != 0:
        Matriz[i-1,j-1] = k   

print(Matriz)