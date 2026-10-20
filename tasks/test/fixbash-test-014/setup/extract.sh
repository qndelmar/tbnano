# task:fixbash-test-014
#!/bin/bash
# produce errors.txt: the ERROR lines of sys.log
sort sys.log | grep ERROR > errors.txt
