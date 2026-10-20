# task:fixbash-test-006
#!/bin/bash
# produce errors.txt: the ERROR lines of sys.log
grep error sys.log > errors.txt
