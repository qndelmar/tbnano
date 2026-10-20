# task:fixbash-train-011
#!/bin/bash
# produce found.txt: the ERROR lines of jobs.log
grep error jobs.log > found.txt
