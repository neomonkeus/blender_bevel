Usage Description:
Adds the Destructive Modifier that was featured in Blender 2.4.x

The script is located in the ./src folder, copy this to /Blender/scripts/addons

Development:
Once you have cloned this Repo to your local, copy all files in debug files to ../Blender Foundation/Blender
Run docs/refresh_python_api.bat to generate the current the current API 
pydev_debug & Run.py will hook up Eclipse's Pydev Debug to Blender's debugger.

Import local repo into Eclipse using Team->Git as an existing project.
Link the external Api to the project:
Project->Properties->Pydev - PYTHONPATH->external libraries->
../Blender/docs/python_api/pypredef/

Start the Pydev debug server and switch to debug mode.
Open the .blend file, then open the run.py in the text editor.
Replace the strings:
1: python debugger location.
2: main execution file location.

Start the Pydev debug server and switch to debug mode.
Open the .blend file, then open the run.py in the text editor.