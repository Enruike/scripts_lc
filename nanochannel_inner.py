import matplotlib.pyplot as plt
#Abrir el archivo donde tenemos guardadas las energías.

#folders=["seed4/", "seed5/", "seed6/", "seed9/"]


#folders=["00", "05", "10", "15", "20", "25"]
#names=["0°", "5°", "10°", "15°", "20°", "25°"]
folders=["00", "05", "10", "15", "16", "17", "18", "19", "20", "25", "30"]
names=["0°", "5°", "10°", "15°", "16°", "17°", "18°", "19°", "20°", "25°", "30°"]
#folders=["rds080", "rds082", "rds084", "rds086", "rds088", "rds090"]

allenergies = []
all_ldg = []
all_elastic = []
all_surf = []
all_chiral = []

for folder in folders:
    file = open(folder + "/separated_energy.out", "r")
    File = file.readlines()
    #Tomaremos la antepenúltima línea del archivo, la cual es la única que nos interesa.
    last = File[-1]

#Este código fue escrito con el propósito de leer y separar por tabulaciones, 
#los datos contenidos en la antepenúltima línea del documento.
#for lines in last.split("\t"):
#    print("{}".format(lines))

#removeremos el espacio al final de las líneas.
    last = last.rstrip("\n")

#removeremos la tabulación y haremos lista.
    last = last.split("\t")

#Asignaremos los valores convertidos a float a las variables necesarias.
    LandauDG = float(last[3])
    Lastic1 = float(last[6])
    Chiral = float(last[9])
    SurfEnergy = float(last[11])
    TotalEnergy = float(last[12])

    file.close()

    with open(folder + "/nohup.out", 'r') as nohup:
        lines = nohup.readlines()
        for line in lines:
            if line.find("Bulk nodes") != -1:
                bulk_index = lines.index(line)
                droplet_index = bulk_index - 1
                surface_index = bulk_index + 1
                internal_index = bulk_index + 3
                
                break
                
    droplet_lines = lines[droplet_index]
    bulk_lines = lines[bulk_index]
    surface_lines = lines[surface_index]
    internal_lines = lines[internal_index]
   

    droplet_lines = droplet_lines.split()
    bulk_lines = bulk_lines.split()
    surface_lines = surface_lines.split()
    internal_lines = internal_lines.split()
   
    
    droplet_nodes = float(droplet_lines[-1])
    bulk_nodes = float(bulk_lines[-1])
    surface_nodes = float(surface_lines[-1])
    internal_nodes = float(internal_lines[-1])
    

    bulk_nodes -= internal_nodes

    #Valores de las energías divididos entre el número de nodos para
    #obtener la densidad de energía.

    LDG_density = LandauDG / bulk_nodes 
    L1_density = Lastic1 / bulk_nodes
    Chiral_density = Chiral / bulk_nodes
    SurfEnergy_density = SurfEnergy / surface_nodes
    TotalEnergy_density = (LandauDG + Lastic1 + Chiral) / bulk_nodes + SurfEnergy_density

    TypesOfEnergy = ['LdG', 'Elastic', 'Chiral', 'Surf', 'Total']
    Energy = [round(LandauDG, 2), round(Lastic1, 2), round(Chiral, 2), round(SurfEnergy, 2), round(TotalEnergy, 2)]
    Energy_density = [round(LDG_density, 6), round(L1_density, 6), round(Chiral_density, 6), round(SurfEnergy_density, 6), round(TotalEnergy_density, 6)]
    all_ldg.append(Energy_density[0])
    all_elastic.append(Energy_density[1])
    all_chiral.append(Energy_density[2])
    all_surf.append(Energy_density[3])
    allenergies.append(Energy_density[4])

    # plt.plot(TypesOfEnergy, Energy_density, marker = 'o')
    # plt.ylabel("Energy Density")
    # plt.xlabel("Type of Energy")
    # plt.title("Energy contributions")
    # plt.savefig(folder + '/Energy_Contribution.png', dpi = 1200, bbox_inches='tight')
    # plt.clf()

plt.plot(names, allenergies, marker = '^')
#plt.legend(names)

plt.ylabel('F')
plt.title("Densidad de Energía Total")
plt.xlabel('Inclinación')
#plt.ylim([-0.0060, -0.0030])
#plt.ylim([-0.00585, -0.0056]) #estabilizado
#plt.ylim([-0.00585, -0.0056])
plt.grid(linestyle = '--')
#plt.yscale('log')

plt.savefig('Total_Inner_comparison.png', dpi = 1200 , bbox_inches='tight')
#plt.show()