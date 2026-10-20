# task:paths-test-012
#!/bin/bash
set -e
cat conf/app.conf > /dev/null || { echo 'conf/app.conf not found' >&2; exit 1; }
cp conf/app.conf result.txt
