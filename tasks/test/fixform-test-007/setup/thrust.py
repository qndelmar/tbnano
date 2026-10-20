# task:fixform-test-007
# Rocket thrust: F = mdot*ve + (pe - p0)*Ae
# mdot is fed from the flow meter in g/s.
mdot = 38.43      # g/s
ve = 2672.5           # m/s
pe = 80000.0           # Pa
p0 = 101325.0           # Pa
Ae = 0.3559           # m^2

F = mdot * ve + (pe - p0) * Ae

with open('thrust_n.txt', 'w') as f:
    f.write(str(F))
print(F)
