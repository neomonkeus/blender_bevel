Usage Description:
Adds the Destructive Modifier that was featured in Blender 2.4.x

The script is located in the ./src folder, copy this to /Blender/scripts/addons

Development:
Once you have cloned this Repo to your local import it as a git project into Eclipse

Copy the debug files into the ../Blender Folder
These will hook up Eclipse's Pydev Debug to Blender's debugger.
Run refresh_python_api.bat to generate the bpy api for the current Blender rev.

Open the Run.py and replace the strings:
1: module main file to be executed.
2: python debugger location.

Start the Pydev debug server and switch to debug mode.
Open the .blend file, then open the run.py in the text editor.