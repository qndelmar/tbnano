# task:fixbash-test-005
#!/bin/bash
# produce errs.txt: the ERROR lines of app.log
grep ERR app.log > errs.txt
