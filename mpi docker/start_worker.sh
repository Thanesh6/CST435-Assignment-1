#!/bin/bash
service ssh start
echo "Worker $(hostname) SSH started ✅"
tail -f /dev/null
