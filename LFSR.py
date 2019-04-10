# Copyright 2019, Leejae Karinja, All rights reserved.

# Note that in addition to Python v2.7 and NumPy, SageMath v8.5 was also used for Matrix operations
import numpy

key_stream = '0110110111110100'
stream_len = len(key_stream)
lfsr_size = 8
matrix_size = stream_len - lfsr_size

lfsr = [[0] * lfsr_size for x in range(stream_len)]

for x in range(stream_len):
    lfsr[x][lfsr_size - 1] = int(key_stream[x])

for x in range(stream_len - 2, -1, -1):
    for y in range(lfsr_size - 2, -1, -1):
        lfsr[x][y] = int(lfsr[x + 1][y + 1])

key_matrix = lfsr[:lfsr_size:]
inverse_key_matrix = Matrix(IntegerModRing(2), key_matrix).inverse()
b_values = [[x[0]] for x in lfsr[1:(lfsr_size + 1)]]
dot_product = numpy.dot(inverse_key_matrix, b_values)

alg_equation = list()
for x, row in enumerate(key_matrix):
    alg_equation.append(str(lfsr[x + 1][0]) + ' = ')
    eq = list()
    for x, b in enumerate(row):
        if b == 1:
            eq.append(' xor ' if eq else '')
            eq.append('c' + str(lfsr_size - x))
    alg_equation.append(''.join(eq) + '\n')

print 'Algebraic Equation:\n%s' % ''.join(alg_equation)

print 'LFSR:\n%s\n' % Matrix(lfsr)
print 'Matrix:\n%s\n' % Matrix(key_matrix)
print 'Inverse Matrix:\n%s\n' % inverse_key_matrix
print 'B Values:\n%s\n' % Matrix(b_values)
print 'Dot Product:\n%s\n' % Matrix(dot_product)

lfsr_equation = list()
for x, b in enumerate(dot_product):
    if b == 1:
        lfsr_equation.append(' xor ' if lfsr_equation else '')
        lfsr_equation.append('b' + str(lfsr_size - x))

print 'LFSR Equation:\n%s%s\n' % ('b' + str(lfsr_size) + ' = ', ''.join(lfsr_equation))
