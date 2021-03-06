#import numpy
import numpy as np
import matplotlib.pyplot as plt



## Number of elements and nodes.
e = int(input("Enter number of Elements : "))
n = (e*3)-(e-1)
print("Total Number of nodes are : ", n)
K = np.zeros(shape=(n, n), dtype=float)
D = np.array([[7, 1, -8], [1, 7, -8], [-8, -8, 16]])
L1 = []
A1 = []
E1 = []
F = []
ST = []
S1 = []
S2 = []


# given Data and stiffness matrices and global stiffness matrix
m = e*2
for i in range(0, m, 2):
    EN = int(input("Enter Element number :"))
    L = float(input("Enter length of element %d  in mm : " % EN))
    A = float(input("Enter area of element %d  in mm^2 : " % EN))
    E = float(input("Enter Young's modulus for element %d  in Gpa : " % EN))
    L1.append(L)
    A1.append(A)
    E1.append(E)
    C = (A*E*10**3)/(3*L)
    ke = np.multiply(C, D)
    print("\n k%d = \n" % EN, ke, "\n")
    ke[:, [1, 2]] = ke[:, [2, 1]]
    ke[[1, 2], :] = ke[[2, 1], :]
    K[i:i+3, i:i+3] += ke
print("\n K= \n", K)
print("\n")
kr = K[1:, 1:]


# forces acting on nodes and gives nodal displacements
# forces are taken from 2nd nodes because first node is at fixed support of bar
p = 1
for j in range(n-1):
    p += 1
    f = float(input("Enter load in kN action on node %d : " % p))
    f = f*10**3
    F.append(f)
X = np.linalg.solve(kr, F)
X = np.insert(X, 0, 0)
X = np.array(X).T
X = np.around(X, 8, out=None)
F.insert(0, 0)
S = np.size(X)
Q = np.empty((1, S))


# calculation Nodal Displacement
for l in range(n):
   o = l+1
   print("\n q%d = " % o, X[l], "mm\n")


#Calculations for Elemental Stress
for s in range(S-1):
    if s % 2 != 0:
        continue
    else:
        Z = X[s:s+3]
        Y = np.array(Z)
        st = Y.tolist()
    ST.append(st)
STR = np.array(ST)
for t in range(e):
    S = (E1[t]*10**3)*(2/L1[t])
    STR1 = STR[t].T
    M = np.multiply(S, STR1)
    for w in range(-1, 2, 1):
        B = [(2*w-1)/2, (2*w+1)/2, -2*w]
        N = np.matmul(M, B)
        S1.append(N)
        print("\n Stress Value is ", N, "\n")


# reaction at fixed support
R1 = (np.matmul(K[0], X)-F[0])/10**3
R1 = np.around(R1, 8, out=None)
print("\n Reaction at Fixed node(R1)=  ", R1, "kN")

# Calculation Of Strain
for h in range(e):
    for r in range(e):
        Strain = S1[r]/(E1[h]*10**3)
        print("\n  Strain  =", Strain, "\n")
        S2.append(Strain)


#Plotting Stress-Strain Variation Curve
plt.title("STRESS vs STRAIN Variation Curve ")
plt.xlabel("STRAIN")
plt.ylabel("STRESS")
plt.grid(True)
plt.plot(S2, S1, 'r-', S2, S1, 'bo')
plt.show()
