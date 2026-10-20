# task:fixbash-test-004
#!/bin/bash
# produce errors.txt: the ERROR lines of app.log
grep ERR app.log > errors.txt
