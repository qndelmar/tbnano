# task:fixbash-train-001
#!/bin/bash
# produce found.txt: the ERROR lines of jobs.log
grep ERR jobs.log > found.txt
