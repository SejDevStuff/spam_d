#!/bin/bash 

TYPE=$1
MSG=$2

RED='\033[1;31m'
BLUE='\033[1;34m'
ORANGE='\033[1;33m'
NC='\033[0m' # No Color

if [[ $TYPE == "-w" ]]; then
    echo -e "${ORANGE}WARNING!${NC} $MSG"
elif [[ $TYPE == "-c" ]]; then
    echo -e "${RED}CRITICAL!${NC} $MSG"
elif [[ $TYPE == "-i" ]]; then
    echo -e "${BLUE}$MSG${NC}"
else
    echo "$0: Unknown option '$TYPE'"
fi

exit