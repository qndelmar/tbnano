# task:fixbash-test-002
#!/bin/bash
# produce errors.txt: the ERROR lines of app.log
grep ERR app.log > errors.txt
