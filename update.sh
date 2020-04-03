#!/usr/bin/env bash
# will update all of the requirements files
echo "Updating requirements files..."
pip-compile test.in -o test.txt --upgrade
pip-compile local.in -o local.txt --upgrade
pip-compile production.in -o production.txt --upgrade
pip-compile pypy.in -o pypy.txt --upgrade
pip-compile ec2.in -o ec2.txt --upgrade
echo "Complete."
