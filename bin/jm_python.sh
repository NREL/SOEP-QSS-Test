#!/bin/sh

if test "${JAVA_HOME}" = ""; then
  export JAVA_HOME=/usr/lib/jvm/java-openjdk/
fi
JMODELICA_HOME=/opt/JModelica \
IPOPT_HOME=/opt/ipopt \
SUNDIALS_HOME=/opt/JModelica/ThirdParty/Sundials \
PYTHONPATH=:/opt/JModelica/Python/::$PYTHONPATH \
LD_LIBRARY_PATH=:/opt/ipopt/lib/:/opt/JModelica/ThirdParty/Sundials/lib:/opt/JModelica/ThirdParty/CasADi/lib:$LD_LIBRARY_PATH \
SEPARATE_PROCESS_JVM=/usr/lib/jvm/java-openjdk/ \
python $@
