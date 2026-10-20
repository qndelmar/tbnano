# task:paths-train-009
#!/bin/bash
set -e
cat etc/agent.conf > /dev/null || { echo 'etc/agent.conf not found' >&2; exit 1; }
cp etc/agent.conf end.txt
