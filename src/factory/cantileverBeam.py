import sys

L = 2.44
n_elem = 32
elem_size = L/n_elem
n_nodes = int(L/elem_size)

file_path = 'bin\data\dynamic\cantileverBeam.txt'
sys.stdout = open(file_path, "w")

print("#MODEL\nframe\n")
print("#TYPE\ndynamic\n")
print("#DELTATIME\n0.01\n")
print("#TIME\n5\n")

print('#NODES')
for i in range(n_nodes+1):
    if (i == 0):
        aux = str(i+1)+','+str(i*elem_size)+',0,1,1,1,0,0,0,0,0,0'
    elif (i < n_nodes):
        aux = str(i+1)+','+str(i*elem_size)+',0,1,0,0,0,0,0,0,0,0'
    else:
        aux = str(i+1)+','+str(i*elem_size)+',0,1,0,0,0,0,0,0,0,0\n'
    print(aux)

print('#ELEMENTS')
A = 0.00304
I = 4.29e-5
p = 7837.1
E = 199.95e9
for i in range(n_nodes):
    aux = str(i+1)+','+str(i+1)+','+str(i+2)+','+str(E)+','+str(A)+','+str(I)+','+str(p)+',local,0,0'
    print(aux)