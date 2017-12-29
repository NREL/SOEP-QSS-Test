import os
from jinja2 import Template
import subprocess as sp
from io import open
script_path = os.path.dirname(os.path.realpath(__file__))
MOS_TEMPLATE = """translateModelFMU("{{model_name}}", false, "", "2", "me", false);
exit();
"""

def compileFMUDymola():

    print "-------------- starting Dymola"

    #class_names = [  "Annex60.Utilities.Math.SmoothMaxInline"   ]
    class_names = [  "Events.BouncingBall", "Events.OnOffController", \
                     "Events.StateEvent1", "Events.StateEvent2", \
                     "Events.StateEvent3", "Events.StateEvent4",  \
                     "Events.StateEvent5", "Events.StateEvent6", \
                     "Events.StateEventWithIf1", "Events.StateEventWithIf2", \
                     "Events.StateTimeEventWithIf", "General.Achilles", \
                     "General.CoupledSystem", "General.ExponentialDecay",\
                     "General.Identity", "General.InputFunction",\
                     "General.Quadratic", "Events.ZCBoolean1", "Events.ZCBoolean2"]

    # Set the Modelica path to point to the Simulator Library
    current_library_path = os.environ.get('MODELICAPATH')
    if (current_library_path is None):
        os.environ['MODELICAPATH'] = script_path
    else:
        os.environ['MODELICAPATH'] = script_path\
        + os.pathsep + current_library_path

    print ("Modelicapath is " + str(os.environ['MODELICAPATH']))
    
    for class_name in class_names:

        print "=================================================================="
        class_name='QSS.'+class_name
        print "=== Compiling {}".format(class_name)
        template = Template(MOS_TEMPLATE)
        output_res = template.render(model_name=class_name)

        path_mos = os.path.join(class_name + '.mos')

        with open(path_mos, mode="w", encoding="utf-8") as mos_fil:
            mos_fil.write(output_res)
        mos_fil.close()
        retStr=sp.check_output(["dymola", path_mos])
        os.remove(path_mos)
        print "========= Finished compilation of {}".format(class_name)


if __name__=="__main__":
    compileFMUDymola()
