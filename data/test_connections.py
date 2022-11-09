import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})
plt.rcParams["font.family"] = "Palatino"

nodes = pd.read_csv('D:\Documentos\TCC\\bin\data\\test_nodes.csv')
#print(nodes)

elem = pd.read_csv('D:\Documentos\TCC\\bin\data\\test_elements.csv')

nodes_dict = {'id': nodes['id'].values, 'x': nodes['x'].values, 'y': nodes['y'].values}
elem_dict = {'id': elem['id'].values, 'ni': elem['ni'].values, 'nf': elem['nf'].values, 
             'xi': [0]*len(elem['nf'].values), 'yi': [0]*len(elem['nf'].values), 
              'xf': [0]*len(elem['nf'].values), 'yf': [0]*len(elem['nf'].values)}

for i in range(len(elem_dict['ni'])):
    for j in range(len(nodes_dict['x'])):
        if (elem_dict['ni'][i] == nodes['id'][j]):
            elem_dict['xi'][i] = nodes['x'][j] 
            elem_dict['yi'][i] = nodes['y'][j]
            break
        
for i in range(len(elem_dict['nf'])):
    for j in range(len(nodes_dict['x'])):
        if (elem_dict['nf'][i] == nodes['id'][j]):
            elem_dict['xf'][i] = nodes['x'][j] 
            elem_dict['yf'][i] = nodes['y'][j]
            break

for i in range(len(elem_dict['xi'])):
    X = [elem_dict['xi'][i], elem_dict['xf'][i]]
    Y = [elem_dict['yi'][i], elem_dict['yf'][i]]
    plt.plot(X,Y, 'k.-', markersize=9, linewidth=1)

for i in range(len(nodes_dict['x'])):
    if round(nodes_dict['y'][i], 2) == 0.03:
        plt.plot(nodes_dict['x'][i],nodes_dict['y'][i], 'r.')
#plt.xlabel("X [m]")
#plt.ylabel("Y [m]")
plt.axis('off')
plt.show()