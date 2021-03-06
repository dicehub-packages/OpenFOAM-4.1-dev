#!/bin/bash

export PY=$1

SCRIPT_PATH=$0
cd `dirname "$SCRIPT_PATH"`

$PY -m pip wheel --wheel-dir dist \
https://github.com/dicehub/dice_tools/archive/18.01.0.zip \
https://github.com/dicehub/dice_vtk/archive/18.01.0.zip \
numpy-stl==2.3.2 \
http://backup1.foxcloud.net/mcubcsro/public/dice/wheels/pythonocc_core-0.18.0-cp36-cp36m-linux_x86_64.whl \
http://backup1.foxcloud.net/mcubcsro/public/dice/wheels/vtk-8.0.0-cp36-cp36m-linux_x86_64.whl \
matplotlib==2.0.0 \
https://github.com/dicehub/dice_plot/archive/18.01.0.zip

