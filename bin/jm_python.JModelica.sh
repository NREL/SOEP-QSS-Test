#!/bin/sh

if test "${JAVA_HOME}" = ""; then
  export JAVA_HOME=/usr/lib/jvm/java-openjdk/
fi
JMODELICA_HOME=/opt/JModelica \
IPOPT_HOME=/opt/ipopt \
SUNDIALS_HOME=${JMODELICA_HOME}/ThirdParty/Sundials \
PYTHONPATH=:${JMODELICA_HOME}/Python/::$PYTHONPATH \
LD_LIBRARY_PATH=:/lib/:${IPOPT_HOME}/lib/:${JMODELICA_HOME}/ThirdParty/Sundials/lib:${JMODELICA_HOME}/ThirdParty/CasADi/lib:$LD_LIBRARY_PATH \
SEPARATE_PROCESS_JVM=${JAVA_HOME} \
python2 $@
