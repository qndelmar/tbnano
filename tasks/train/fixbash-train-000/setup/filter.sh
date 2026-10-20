# task:fixbash-train-000
#!/bin/bash
# produce hits.txt: the ERROR lines of nodes.log
grep error nodes.log > hits.txt
