# task:fixbash-train-007
#!/bin/bash
# produce found.txt: the ERROR lines of nodes.log
sort nodes.log | grep ERROR > found.txt
