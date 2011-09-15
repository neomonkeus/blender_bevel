#script to run:
SCRIPT = "C:/Users/User/workspace/Bevel/src/mesh_bevel.py"  
    
#path to your org.python.pydev.debug* folder (it may have different version number, in your configuration):
PYDEVD_PATH='C:/Eclipse/plugins/org.python.pydev.debug_2.2.0.2011062419/pysrc'

import pydev_debug as pydev

pydev.debug(SCRIPT, PYDEVD_PATH, trace = True)
