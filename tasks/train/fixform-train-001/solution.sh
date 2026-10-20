cat > thrust.py <<'EOF'
# Rocket thrust: F = mdot*ve + (pe - p0)*Ae
# mdot is fed from the flow meter in g/s.
mdot = 49.04 / 1000.0  # convert g/s -> kg/s
ve = 3312.3           # m/s
pe = 80000.0           # Pa
p0 = 101325.0           # Pa
Ae = 0.2597           # m^2

F = mdot * ve + (pe - p0) * Ae

with open('thrust_n.txt', 'w') as f:
    f.write(str(F))
print(F)
EOF
python3 thrust.py
