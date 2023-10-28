import matplotlib.pyplot as plt

types=["oblatos", "prolatos"]

roots=["BPI", "BPII", "CHOL"]
names=["BPI", "BPII", "CHOL"]
folders=["00eps", "20eps", "40eps", "60eps", "130eps"]
difference = [-0.0001779999999999976, -0.0001830000000000026]
counter = 0
for tipos in types:

    all_ldg = []
    all_elastic = []
    all_chiral = []
    seeds_energies = []
    all_ldg2 = []
    all_elastic2 = []
    all_chiral2 = []
    seeds_energies2 = []

    for root in roots:

        allenergies = []
        allenergies2 = []
        energy_result = []
        
        for folder in folders:
            file = open(tipos + "/" + root + "/" + folder + "/separated_energy.out", "r")
            File = file.readlines()
            file2 = open(tipos + "_puros" + "/" + root + "/" + folder + "/energy.out", "r")
            File2 = file2.readlines()
            #Tomaremos la antepenúltima línea del archivo, la cual es la única que nos interesa.
            last = File[-1]
            last2 = File2[-3]

            #Este código fue escrito con el propósito de leer y separar por tabulaciones, 
            #los datos contenidos en la antepenúltima línea del documento.
            #for lines in last.split("\t"):
            #    print("{}".format(lines))

            #removeremos el espacio al final de las líneas.
            last = last.rstrip("\n")
            last2 = last2.rstrip("\n")

            #removeremos la tabulación y haremos lista.
            last = last.split("\t")
            last2 = last2.split("\t")

            #Asignaremos los valores convertidos a float a las variables necesarias.
            LandauDG = float(last[3])
            Lastic1 = float(last[6])
            Chiral = float(last[9])
            SurfEnergy = float(last[11])
            TotalEnergy = float(last[12])

            LandauDG2 = float(last2[2])
            Lastic12 = float(last2[3])
            Chiral2 = float(last2[7])
            SurfEnergy2 = float(last2[8])
            TotalEnergy2 = float(last2[10])

            file.close()
            file2.close()

            with open(tipos + "/" + root + "/" + folder + "/nohup.out", 'r') as nohup:
                lines = nohup.readlines()
                for line in lines:
                    if line.find("Bulk nodes") != -1:
                        bulk_index = lines.index(line)
                        droplet_index = bulk_index - 1
                        surface_index = bulk_index + 1
                        internal_index = bulk_index + 2
                        break
            
            with open(tipos + "_puros" + "/" + root + "/" + folder + "/nohup.out", 'r') as nohup:
                lines2 = nohup.readlines()
                for line in lines2:
                    if line.find("Bulk nodes") != -1:
                        bulk_index2 = lines2.index(line)
                        droplet_index2 = bulk_index2 - 1
                        surface_index2 = bulk_index2 + 1
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

            droplet_lines2 = lines2[droplet_index2]
            bulk_lines2 = lines2[bulk_index2]
            surface_lines2 = lines2[surface_index2]
          
            droplet_lines2 = droplet_lines2.split()
            bulk_lines2 = bulk_lines2.split()
            surface_lines2 = surface_lines2.split()

            droplet_nodes2 = float(droplet_lines2[-1])
            bulk_nodes2 = float(bulk_lines2[-1])
            surface_nodes2 = float(surface_lines2[-1])

            #Valores de las energías divididos entre el número de nodos para
            #obtener la densidad de energía.

            LDG_density = LandauDG / internal_nodes
            L1_density = Lastic1 / internal_nodes
            Chiral_density = Chiral / internal_nodes
            SurfEnergy_density = SurfEnergy / surface_nodes
            TotalEnergy_density = (LandauDG + Lastic1 + Chiral) / internal_nodes

            LDG_density2 = LandauDG2 / bulk_nodes2
            L1_density2 = Lastic12 / bulk_nodes2
            Chiral_density2 = Chiral2 / bulk_nodes2
            SurfEnergy_density2 = SurfEnergy2 / surface_nodes2
            TotalEnergy_density2 = TotalEnergy2 / droplet_nodes2

            TypesOfEnergy = ['LdG', 'Elastic', 'Chiral', 'Surf', 'Total']
            Energy = [round(LandauDG, 2), round(Lastic1, 2), round(Chiral, 2), round(SurfEnergy, 2), round(TotalEnergy, 2)]
            Energy_density = [round(LDG_density, 6), round(L1_density, 6), round(Chiral_density, 6), round(SurfEnergy_density, 6), round(TotalEnergy_density, 6)]

            Energy2 = [round(LandauDG, 2), round(Lastic1, 2), round(Chiral, 2), round(SurfEnergy, 2), round(TotalEnergy, 2)]
            Energy_density2 = [round(LDG_density2, 6), round(L1_density2, 6), round(Chiral_density2, 6), round(SurfEnergy_density2, 6), round(TotalEnergy_density2, 6)]

            all_ldg.append(Energy_density[0])
            all_elastic.append(Energy_density[1])
            all_chiral.append(Energy_density[2])
            allenergies.append(Energy_density[4])

            all_ldg2.append(Energy_density2[0])
            all_elastic2.append(Energy_density2[1])
            all_chiral2.append(Energy_density2[2])
            allenergies2.append(Energy_density2[4])

            energy_result.append(Energy_density[4] - Energy_density2[4] - difference[counter])
            print(tipos + "/" + root + "/" + folder)
            print(Energy_density[4])
            print(Energy_density2[4])
            print(Energy_density[4] - Energy_density2[4] - difference[counter])
            
            # plt.plot(TypesOfEnergy, Energy_density, marker = 'o')
            # plt.ylabel("Energy Density")
            # plt.xlabel("Type of Energy")
            # plt.title("Energy contributions")
            # plt.savefig(folder + '/Energy_Contribution.png', dpi = 1200, bbox_inches='tight')
            # plt.clf()

        configurations=["0.00", "0.20", "0.40", "0.60", "1.30"]
        plt.plot(configurations, energy_result, marker = 'o')
        plt.legend(names)

    counter += 1

    plt.ylabel('\u0394F*')
    #plt.title("Total Energy Density for Different Distortions")
    plt.xlabel('\u03B5')
    #plt.yscale('log')

    plt.savefig('Total_Inner_comparison_' + tipos + '.png', dpi = 1200 , bbox_inches='tight')
    plt.clf()
    #plt.show()
