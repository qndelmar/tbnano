cat > merge.sh <<'EOF'
#!/bin/bash
head -1 data/part0.csv
tail -qn +2 data/*.csv | sort -s -t, -k1,1n
EOF
bash merge.sh > merged.csv
