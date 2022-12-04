# Sudoku Secciones con suma

# Instrucciones de instalación: 
from gurobipy import * 
import numpy as np

# Creacion del modelo: Sudoku seccion suma
Matriz = np.zeros((9,9))
m = Model('Sudoku Secciones suma')
I = np.arange(1,10)       #I = {1,..,9}
J = np.arange(1,10)       #J = {1,..,9}
K = np.arange(1,10)       #K = {1,..,9}

#Creacion de las variables
y = m.addVars(I,J,K, vtype = GRB.BINARY, name = "y")

# Restricciones
entradas = open("aij_seccioness4_posiciones.csv", "r")
for lineas in entradas:
  fil = int(lineas[0])
  col = int(lineas[2])
  var = int(lineas[4])
  m.addConstr(y[fil,col,var] == 1 )

# Restricciones de fila y columna no repetidas
m.addConstrs(quicksum(y[i,j,k] for j in J) == 1 for i in I for k in K)
m.addConstrs(quicksum(y[i,j,k] for i in I) == 1 for j in J for k in K)

# Restricciones de suma por regiones
secciones = np.genfromtxt("aij_seccionessuma_4.csv", delimiter = ",")
for i in range(1, int(np.amax(secciones[:,3]))):
  tmp = np.where(secciones[:,3] == i)
  suma = secciones[tmp[0][0],2]
  m.addConstr(quicksum(k*y[secciones[int(l),0], secciones[int(l),1], k] for k in K for l in tmp[0]) == suma)

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

#Restriccion cada celda debe de tener un valor entre 1 y 9
m.addConstrs(quicksum(y[i,j,k] for k in K ) == 1 for j in J for i in I)

m.setObjective(0 , GRB.MAXIMIZE)
m.optimize()
for i in I:
  for j in J:
    for k in K: 
      if y[i,j,k].X != 0:
        Matriz[i-1,j-1] = k   

print(Matriz)

m.write("file.lp")