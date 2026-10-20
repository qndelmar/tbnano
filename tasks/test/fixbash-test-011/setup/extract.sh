# task:fixbash-test-011
#!/bin/bash
# produce errs.txt: the ERROR lines of sys.log
grep error sys.log > errs.txt
