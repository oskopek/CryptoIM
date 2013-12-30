#!/bin/bash
clear
clear
pylint --rcfile=tools/rc_pylint crypto_im/ $1
