# task:fixbash-train-012
#!/bin/bash
# produce hits.txt: the ERROR lines of jobs.log
grep error jobs.log > hits.txt
