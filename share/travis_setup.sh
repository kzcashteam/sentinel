#!/bin/bash
set -evx

mkdir ~/.ucom

# safety check
if [ ! -f ~/.ucom/.ucom.conf ]; then
  cp share/ucom.conf.example ~/.ucom/ucom.conf
fi
