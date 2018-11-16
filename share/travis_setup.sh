#!/bin/bash
set -evx

mkdir ~/.kzcash

# safety check
if [ ! -f ~/.kzcash/.kzcash.conf ]; then
  cp share/kzcash.conf.example ~/.kzcash/kzcash.conf
fi
