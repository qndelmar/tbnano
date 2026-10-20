# task:fixbash-test-018
#!/bin/bash
# produce errors.txt: the ERROR lines of sys.log
grep ERR sys.log > errors.txt
