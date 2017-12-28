# Compile a stand-alone Modelica ME file with JModelica
# Run from an environment set up for JModelica such as jm_python.sh

import sys
from pymodelica import compile_fmu

try:
    model = sys.argv[ 1 ]
    if model.endswith( '.mo' ): model = model[ :-3 ]
    fmu_file = compile_fmu( model, model + '.mo' )
except:
    print( 'Usage: ' + sys.argv[ 0 ] + ' <model_name>' )
