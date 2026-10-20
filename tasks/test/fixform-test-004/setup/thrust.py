# task:fixform-test-004
# Rocket thrust: F = mdot*ve + (pe - p0)*Ae
# mdot is fed from the flow meter in g/s.
mdot = 25.72      # g/s
ve = 3103.6           # m/s
pe = 80000.0           # Pa
p0 = 101325.0           # Pa
Ae = 0.2629           # m^2

F = mdot * ve + (pe - p0) * Ae

with open('thrust_n.txt', 'w') as f:
    f.write(str(F))
print(F)
