# task:fixbash-train-005
#!/bin/bash
# produce hits.txt: the ERROR lines of jobs.log
sort jobs.log | grep ERROR > hits.txt
