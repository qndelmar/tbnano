# task:paths-train-005
#!/bin/bash
set -e
cat etc/node.conf > /dev/null || { echo 'etc/node.conf not found' >&2; exit 1; }
cp etc/node.conf end.txt
