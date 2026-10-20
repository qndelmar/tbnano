# task:fixbash-test-008
#!/bin/bash
# produce errs.txt: the ERROR lines of app.log
grep error app.log > errs.txt
