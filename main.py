import cantera as ct
import numpy as np
import matplotlib.pyplot as plt


# -------------------------------
# Parametry początkowe
# -------------------------------

T_initial = 288.15      # temperatura [K]
P_initial = ct.one_atm   # ciśnienie [Pa]

fuels = {
    "Methane CH4": "CH4",
    "Hydrogen H2": "H2",
    "Propane C3H8": "C3H8"
}


# wyniki
temperature = []
CO2 = []
H2O = []
O2 = []


# -------------------------------
# Obliczenia spalania
# -------------------------------

for name, fuel in fuels.items():

    gas = ct.Solution("gri30.yaml")

    # mieszanka stechiometryczna paliwo + powietrze
    gas.TP = T_initial, P_initial

    gas.set_equivalence_ratio(
        phi=1.0,
        fuel=fuel,
        oxidizer="O2:1, N2:3.76"
    )


    # spalanie adiabatyczne przy stałym ciśnieniu
    gas.equilibrate("HP")


    temperature.append(gas.T)

    CO2.append(
        gas["CO2"].X[0]
    )

    H2O.append(
        gas["H2O"].X[0]
    )

    O2.append(
        gas["O2"].X[0]
    )


    print("---------------------------")
    print(name)
    print(f"Flame Temperature: {gas.T:.1f} K")
    print(f"CO2: {gas['CO2'].X[0]*100:.2f} %")
    print(f"H2O: {gas['H2O'].X[0]*100:.2f} %")
    print(f"O2: {gas['O2'].X[0]*100:.2f} %")


# -------------------------------
# Wykres temperatury
# -------------------------------

plt.figure(figsize=(8,5))

plt.bar(
    fuels.keys(),
    temperature
)

plt.ylabel("Flame Temperature [K]")
plt.title(
    "Comparison of Fuel Combustion Temperatures"
)

plt.grid(axis="y")

plt.show()



# -------------------------------
# Wykres CO2
# -------------------------------

plt.figure(figsize=(8,5))

plt.bar(
    fuels.keys(),
    np.array(CO2)*100
)

plt.ylabel("CO2 content [%]")
plt.title(
    "CO2 Emissions for Different Fuels"
)

plt.grid(axis="y")

plt.show()



# -------------------------------
# Skład produktów spalania
# -------------------------------

x = np.arange(len(fuels))

width = 0.25


plt.figure(figsize=(8,5))

plt.bar(
    x-width,
    np.array(CO2)*100,
    width,
    label="CO2"
)

plt.bar(
    x,
    np.array(H2O)*100,
    width,
    label="H2O"
)

plt.bar(
    x+width,
    np.array(O2)*100,
    width,
    label="O2"
)


plt.xticks(
    x,
    fuels.keys()
)

plt.ylabel("Mole Fraction [%]")
plt.title(
    "Combustion Products Composition"
)

plt.legend()

plt.grid(axis="y")

plt.show()
