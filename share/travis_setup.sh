#!/bin/bash
set -evx

mkdir ~/.crowdclassiccore

# safety check
if [ ! -f ~/.crowdclassiccore/.crowdclassic.conf ]; then
  cp share/crowdclassic.conf.example ~/.crowdclassiccore/crowdclassic.conf
fi
