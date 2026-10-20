# task:fixbash-train-013
#!/bin/bash
# produce hits.txt: the ERROR lines of nodes.log
grep ERR nodes.log > hits.txt
