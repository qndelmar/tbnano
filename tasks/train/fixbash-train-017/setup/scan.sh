# task:fixbash-train-017
#!/bin/bash
# produce hits.txt: the ERROR lines of jobs.log
grep ERR jobs.log > hits.txt
