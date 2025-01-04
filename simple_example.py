import sys

# importa o solver Gurobi
import gurobipy as gp
from gurobipy import GRB

text = """
Minimize
 z: 2 x11 + 5 x12 + 1 x13 + 2 x14 + 5 x15 - 50 y1 + 4 x21 + 4 x22 + 9 x23 + 1 x24 + 4 x25 - 32 y2 + 1 x31 + 8 x32 + 5 x33 + 6 x34 + 2 x35 - 28 y3 + 7 x41 + 1 x42 + 2 x43 + 1 x44 + 8 x45 - 36 y4
Subject To
 l1: y1 + y2 + y3 + y4 <= 4
 c1: x11 + x12 + x13 + x14 + x15 <= 35
 c2: x21 + x22 + x23 + x24 + x25 <= 28
 c3: x31 + x32 + x33 + x34 + x35 <= 22
 c4: x41 + x42 + x43 + x44 + x45 <= 28
 p1: x11 + x21 + x31 + x41 = 14
 p2: x12 + x22 + x32 + x42 = 12
 p3: x13 + x23 + x33 + x43 = 10
 p4: x14 + x24 + x34 + x44 = 12
 p5: x15 + x25 + x35 + x45 = 8
Bounds
 x11 >= 0
 x12 >= 0
 x13 >= 0
 x14 >= 0
 x15 >= 0
 x21 >= 0
 x22 >= 0
 x23 >= 0
 x24 >= 0
 x25 >= 0
 x31 >= 0
 x32 >= 0
 x33 >= 0
 x34 >= 0
 x35 >= 0
 x41 >= 0
 x42 >= 0
 x43 >= 0
 x44 >= 0
 x45 >= 0
 y1 >= 0
 y2 >= 0
 y3 >= 0
 y4 >= 0
 y1 <= 1
 y2 <= 1
 y3 <= 1
 y4 <= 1
End
"""

# cria um arquivo "file_entry.lp"
with open("file_entry.lp", "w") as file:
    file.write(text)

# Lê e resolve o modelo
model = gp.read("file_entry.lp")
model.optimize()

if model.Status == GRB.INF_OR_UNBD:
    # Desativa a pré-resolução para determinar se o modelo é inviável
    # ou ilimitado
    model.setParam(GRB.Param.Presolve, 0)
    model.optimize()

# O seguinte bloco condicional é modificado para gravar a solução apenas se for ótima.
# e para sempre continuar com o cálculo do IIS.
if model.Status == GRB.OPTIMAL:
    print(f"Optimal objective: {model.ObjVal:g}")
    model.write("model.sol")

    print("\n********** Begin model.sol *************")
    with open("model.sol", "r") as f:
        for line in f:
            print(line.strip())

    print("\n********** End model.sol *************")

elif model.Status != GRB.INFEASIBLE:
    print(f"Optimization was stopped with status {model.Status}")

else:
    # O modelo é inviável - calcula um Sistema Inconsistente Irredutível (IIS)
    print("")
    print("Model is infeasible")
    model.computeIIS()
    model.write("model.ilp")
    print("IIS written to file 'model.ilp'")
