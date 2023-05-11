import matplotlib.pyplot as plt
#Abrir el archivo donde tenemos guardadas las energías.

#folders=["seed4/", "seed5/", "seed6/", "seed9/"]
<<<<<<< HEAD
folders=["07epsilon", "14epsilon", "21epsilon", "28epsilon"]
=======
<<<<<<< HEAD
folders=["rds070", "rds072", "rds074", "rds076", "rds078", "rds080", "rds082", "rds084", "rds086", "rds088", "rds090"]
=======
folders=["07epsilon", "14epsilon", "21epsilon", "28epsilon", ]
>>>>>>> 082f4e5a2b8b3f79ac1fe64d836e98147b5064ee
#folders=["rds080", "rds082", "rds084", "rds086", "rds088", "rds090"]
>>>>>>> d351ab9b73833c848210215bdb0215f96628296f
allenergies = []
all_ldg = []
all_elastic = []
all_chiral = []

for folder in folders:
    file = open(folder + "/energy.out", "r")
    File = file.readlines()
    #Tomaremos la antepenúltima línea del archivo, la cual es la única que nos interesa.
    last = File[-3]

#Este código fue escrito con el propósito de leer y separar por tabulaciones, 
#los datos contenidos en la antepenúltima línea del documento.
#for lines in last.split("\t"):
#    print("{}".format(lines))

#removeremos el espacio al final de las líneas.
    last = last.rstrip("\n")

#removeremos la tabulación y haremos lista.
    last = last.split("\t")

#Asignaremos los valores convertidos a float a las variables necesarias.
    LDG = float(last[2])
    L1 = float(last[3])
    Chiral = float(last[7])
    SurfEnergy = float(last[8])
    TotalEnergy = float(last[10])

    file.close()

    with open(folder + "/nohup.out", 'r') as nohup:
        lines = nohup.readlines()
        for line in lines:
            if line.find("Bulk nodes") != -1:
                bulk_index = lines.index(line)
                droplet_index = bulk_index - 1
                surface_index = bulk_index + 1
                break
                
    droplet_lines = lines[droplet_index]
    bulk_lines = lines[bulk_index]
    surface_lines = lines[surface_index]

    droplet_lines = droplet_lines.split()
    bulk_lines = bulk_lines.split()
    surface_lines = surface_lines.split()

    droplet_nodes = float(droplet_lines[-1])
    bulk_nodes = float(bulk_lines[-1])
    surface_nodes = float(surface_lines[-1])

    #Valores de las energías divididos entre el número de nodos para
    #obtener la densidad de energía.

    LDG_density = LDG / bulk_nodes
    L1_density = L1 / bulk_nodes
    Chiral_density = Chiral / bulk_nodes
    SurfEnergy_density = SurfEnergy / surface_nodes
    TotalEnergy_density = TotalEnergy / droplet_nodes

    TypesOfEnergy = ['LdG', 'Elastic', 'Chiral', 'Surf', 'Total']
    Energy = [round(LDG, 2), round(L1, 2), round(Chiral, 2), round(SurfEnergy, 2), round(TotalEnergy, 2)]
    Energy_density = [round(LDG_density, 6), round(L1_density, 6), round(Chiral_density, 6), round(SurfEnergy_density, 6), round(TotalEnergy_density, 6)]
    all_ldg.append(Energy_density[0])
    all_elastic.append(Energy_density[1])
    all_chiral.append(Energy_density[2])
    allenergies.append(Energy_density[4])

    plt.plot(TypesOfEnergy, Energy_density, marker = 'o')
    plt.ylabel("Energy Density")
    plt.xlabel("Type of Energy")
    plt.title("Energy contributions")
    plt.savefig(folder + '/Energy_Contribution.png', dpi = 1200, bbox_inches='tight')
    plt.clf()


#configurations=["BP1[200]", "BP1[110]", "BP2[100]", "BP2[111]"]
<<<<<<< HEAD
configurations=["0.70", "0.72", "0.74", "0.76", "0.78", "0.80", "0.82", "0.84", "0.86", "0.88", "0.90"]
=======
#configurations=["0.80", "0.82", "0.84", "0.86", "0.88", "0.90"]
configurations=["07epsilon", "14epsilon", "21epsilon", "28epsilon", ]

>>>>>>> d351ab9b73833c848210215bdb0215f96628296f
TypesOfEnergy_no_surf = ['LdG', 'Elastic', 'Chiral', 'Total']

for i in range(len(configurations)):
    plotter = []
    plotter.append(all_ldg[i])
    plotter.append(all_elastic[i])
    plotter.append(all_chiral[i])
    plotter.append(allenergies[i])

    plt.plot(TypesOfEnergy_no_surf, plotter, marker = 'o')

plt.legend(configurations)
plt.ylabel("Energy Density")
plt.xlabel("Type of Energy")
plt.title("Energy contributions for all systems")
plt.savefig('All_Energy_Contribution.png', dpi = 1200, bbox_inches='tight')

plt.clf()

plt.plot(configurations, allenergies, marker = 'o')
plt.ylabel('Energy Density')
plt.title("Total Energy Density for Different Redshift")
plt.xlabel('Redshift')
#plt.yscale('log')
plt.savefig('Total_Energy.png', dpi = 1200 , bbox_inches='tight')
#plt.show()