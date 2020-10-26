from z3 import *
import time

n = 100

Q = [ Int('Q_%i' % (i + 1)) for i in range(n) ]

# Each queen is in a column {1, ... 8 }
val_c = [ And(1 <= Q[i], Q[i] <= n) for i in range(n) ]

# At most one queen per column
col_c = [ Distinct(Q) ]

# Diagonal constraint
diag_c = [ If(i == j,
              True,
              And(Q[i] - Q[j] != i - j, Q[i] - Q[j] != j - i))
           for i in range(n) for j in range(i) ]

s = time.time()
solve(val_c + col_c + diag_c)
print(time.time() - s)