# task:fixbash-test-000
#!/bin/bash
# produce errors.txt: the ERROR lines of app.log
grep error app.log > errors.txt
