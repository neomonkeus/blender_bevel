'''
Created on 06 Sept 2011

@author: User
'''

import bpy

def procedure():
    '''
    Used to debug sections of code, trouble-shooting etc,
    '''
    #obj = bpy.types.object
    print("Current Mode: " + bpy.context.mode)
    bpy.ops.object.mode_set(mode='SCULPT', toggle=False)
    print("Toggle = False, Mode: " + bpy.context.mode)
    bpy.ops.object.mode_set(mode='SCULPT', toggle=False)
    print("Toggle = False, Mode: " + bpy.context.mode)
    bpy.ops.object.mode_set(mode='SCULPT', toggle=True)
    print("Toggle = True, Mode: " + bpy.context.mode)
    bpy.ops.object.mode_set(mode='SCULPT', toggle=True)
    print("Toggle = True, Mode: " + bpy.context.mode)

procedure()