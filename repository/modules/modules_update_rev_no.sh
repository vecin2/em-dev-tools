#!/bin/bash


. $HOME/.em.bash

echo Max rev number in modules:$(modules_rev_number)
EM_PYTHON_HOME=$HOME/dev/python/em_dev_tools/my_project
EM_PYTHON="$EM_PYTHON_HOME"/bin/python
PY_MODULES_HOME=$EM_PYTHON_HOME/repository/modules/

$EM_PYTHON $PY_MODULES_HOME/database.py $1
