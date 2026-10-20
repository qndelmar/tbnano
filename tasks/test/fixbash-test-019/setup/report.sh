# task:fixbash-test-019
#!/bin/bash
# produce errs.txt: the ERROR lines of sys.log
grep ERR sys.log > errs.txt
