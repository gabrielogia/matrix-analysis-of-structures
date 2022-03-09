import sys

file_path = 'bin\data\\test.csv'
sys.stdout = open(file_path, "w")

print("id,x,y,z,supx,supy,supz,kx,ky,kz,fx,fy,fz")

x = []
y = []
m = 8.4
for i in range(1, 6):
    if (i - 1 == 0):
        x.append(0)
        y.append(0)
        
    x.append((0.6+(i-1)*0.9)/m)
    y.append(0.6+(i-1)*0.9)
    
for i in range(5, 0, -1):
    x.append(2 - (0.6+(i-1)*0.9)/m)
    y.append(0.6+(i-1)*0.9)
    
    if (i - 1 == 0):
        x.append(2)
        y.append(0)
        
for i in range(1, 5):
    x.append(1)
    y.append(0.6+(i-1)*0.9)

for i in range(len(x)):
    if (i == 0 or i == (len(x) - 1)):
        aux = str(i+1) + ',' + str(x[i]) + ',' + str(y[i]) + ',1,1,1,0,0,0,0,0,0'
    else:
        aux = str(i+1) + ',' + str(x[i]) + ',' + str(y[i]) + ',0,0,0,0,0,0,0,0,0'
    print(aux)
    
file_path = 'bin\data\\elements.csv'
sys.stdout = open(file_path, "w")
    
print("id,ni,nf,E,A,I,p,local,a,b")
E = 2.1e11
A = 6.16e-4
I = 7.4e-7
p = 700
i = 0
j = 0
while (i <= 18):
    if (i < 11):
        aux = str(i+1) + ',' + str(i+1) + ',' + str(i+2) + ',' + str(E) + ',' + str(A) + ',' + str(I) + ',' + str(p) + ',local,0,0'
        i += 1
    elif (i <= 18):
        a = i - 9
        b = i + 2
        
        if (i == 12):
            i+=1
            j+=1
        aux = str(i+1) + ',' + str(a) + ',' + str(b) + ',' + str(E) + ',' + str(A) + ',' + str(I) + ',' + str(p) + ',local,0,0'
        
        c = i - j
        i += 1
        aux = str(i+1) + ',' + str(b) + ',' + str(c) + ',' + str(E) + ',' + str(A) + ',' + str(I) + ',' + str(p) + ',local,0,0'
        j += 1
    
    print(aux)
    
    