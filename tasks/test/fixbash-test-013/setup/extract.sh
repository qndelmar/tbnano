# task:fixbash-test-013
#!/bin/bash
# produce errors.txt: the ERROR lines of app.log
sort app.log | grep ERROR > errors.txt
