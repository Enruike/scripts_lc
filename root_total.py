import matplotlib.pyplot as plt
#Abrir el archivo donde tenemos guardadas las energías.

roots=["seed5_80rds", "seed6_72rds", "seed135_80rds", "seed875_80rds"]
names=["BPII", "BPI", "RSS", "HelZ"]
#folders=["seed4/", "seed5/", "seed6/", "seed9/"]
folders=["00epsilon", "07epsilon", "14epsilon", "21epsilon", "28epsilon"]
#folders=["rds080", "rds082", "rds084", "rds086", "rds088", "rds090"]
all_ldg = []
all_elastic = []
all_chiral = []
seeds_energies = []

for root in roots:

    allenergies = []

    for folder in folders:
        file = open(root + "/" + folder + "/energy.out", "r")
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

        with open(root + "/" + folder + "/nohup.out", 'r') as nohup:
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

        # plt.plot(TypesOfEnergy, Energy_density, marker = 'o')
        # plt.ylabel("Energy Density")
        # plt.xlabel("Type of Energy")
        # plt.title("Energy contributions")
        # plt.savefig(folder + '/Energy_Contribution.png', dpi = 1200, bbox_inches='tight')
        # plt.clf()

    configurations=["0.00", "0.07", "0.14", "0.21", "0.28"]
    plt.plot(configurations, allenergies, marker = 'o')
    plt.legend(names)

plt.ylabel('F')
#plt.title("Total Energy Density for Different Distortions")
plt.xlabel('\u03B5')
#plt.yscale('log')

plt.savefig('Energy_comparo.png', dpi = 1200 , bbox_inches='tight')
#plt.show()