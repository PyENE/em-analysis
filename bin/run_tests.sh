#!/bin/bash

echo -n "last test run:" > ../test/test_log.txt
date >> ../test/test_log.txt
py.test -q -s ../test/test_*.py > /tmp/test_output
cat /tmp/test_output | tail -1 >> ../test/test_log.txt
cat /tmp/test_output >> ../test/test_log.txt
rm /tmp/test_output