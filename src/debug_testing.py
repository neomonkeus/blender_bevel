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
    
class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        context.object.location.x = self.value / 100.0

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.value = event.mouse_x
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in ('RIGHTMOUSE', 'ESC'):  # Cancel
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.value = event.mouse_x
        self.execute(context)

        print(context.window_manager.modal_handler_add(self))
        return {'RUNNING_MODAL'}


bpy.utils.register_class(ModalOperator)

# test call
bpy.ops.object.modal_operator('INVOKE_DEFAULT')