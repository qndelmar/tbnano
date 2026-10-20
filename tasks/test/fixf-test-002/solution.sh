sed -i 's/T \* m/T \/ m/' accel.py
python3 accel.py | awk '{print $2}' > out.txt
