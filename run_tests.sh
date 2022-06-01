#!/bin/bash

shopt -s nullglob

# color codes
red='\033[0;31m'
green='\033[0;32m'
reset='\033[0m'

# ensure correct directory
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

tests=(tests/test_*_in.txt)
num_tests="${#tests[@]}"

if [ "$num_tests" -eq 0 ]; then
  echo 'No tests found.'
  exit 1
fi

echo "Running $num_tests test(s) ..."

count_failed=0
trap 'rm tests/temp.txt' EXIT

for test_in in "${tests[@]}"; do

    # run the test
    ./quartet.py a b c < "$test_in" > tests/temp.txt 2>&1

    # print test results
    teststr="${test_in:6:6}: $(tail -1 "$test_in")"
    if [ "$(tail -1 tests/temp.txt)" = "$(tail -1 ${test_in::12}_out.txt)" ]; then
        echo -e "- $teststr ${green}passed${reset}"
    else
        echo -e "- $teststr ${red}failed"
        echo -e " Intended output is \"$(tail -1 ${test_in::12}_out.txt)\" but actual output is \"$(tail -1 tests/temp.txt)\"${reset}"
        (( count_failed++ ))
    fi
done

# print test summary
echo -e "${green}Passed${reset}: $(($num_tests - $count_failed))/$num_tests tests"
if [ "$count_failed" -gt 0 ]; then
  echo -e "${red}Failed${reset}: $count_failed/$num_tests tests"
  exit 1
fi

exit 0
