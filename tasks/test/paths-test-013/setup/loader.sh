# task:paths-test-013
#!/bin/bash
set -e
cat conf/svc.conf > /dev/null || { echo 'conf/svc.conf not found' >&2; exit 1; }
cp conf/svc.conf out.txt
