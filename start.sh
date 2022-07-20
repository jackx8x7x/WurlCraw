#!/bin/bash

VENV="./virtual-environment"

if [ ! -d $VENV ]
then
  make setup
fi

source virtual-environment/bin/activate
python3 wurlcraw.py $@
