#!/bin/sh

if test "${JAVA_HOME}" = ""; then
  export JAVA_HOME=/usr/lib/jvm/java-openjdk/
fi
JMODELICA_HOME=/opt/OCT \
IPOPT_HOME=/opt/ipopt \
SUNDIALS_HOME=/opt/OCT/ThirdParty/Sundials \
PYTHONPATH=:/opt/OCT/Python/::$PYTHONPATH \
LD_LIBRARY_PATH=:/opt/ipopt/lib/:/opt/OCT/ThirdParty/Sundials/lib:/opt/OCT/ThirdParty/CasADi/lib:$LD_LIBRARY_PATH \
SEPARATE_PROCESS_JVM=/usr/lib/jvm/java-openjdk/ \
python $@
