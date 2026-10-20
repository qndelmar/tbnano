# task:fixform-train-010
# Rocket thrust: F = mdot*ve + (pe - p0)*Ae
# mdot is fed from the flow meter in g/s.
mdot = 34.32      # g/s
ve = 3395.3           # m/s
pe = 80000.0           # Pa
p0 = 101325.0           # Pa
Ae = 0.456           # m^2

F = mdot * ve + (pe - p0) * Ae

with open('thrust_n.txt', 'w') as f:
    f.write(str(F))
print(F)
