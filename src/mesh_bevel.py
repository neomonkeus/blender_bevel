#--- ### Header
bl_info = {
           "name": "Bevel",
           "author": "Witold Jaworski, Gerard Moran",
           "version": (1, 0, 0),
           "blender": (2, 5, 9),
           "api": 39307,
           "location": "View3D -> Edit Mode -> Special (W-key)",
           "category": "Mesh",
           "description": "Bevels selected edges",
           "warning": "Beta",
           "tracking_url": "https://github.com/neomonkeus/blender_bevel"
           }

import bpy
from bpy.utils import register_module, unregister_module
from bpy.props import FloatProperty

'''  
Type declaration: useful for auto-completion 
Comment before publishing
edge = bpy.types.MeshEdge
obj = bpy.types.Object
obj.modifiers.remove(modifier)
bevel = bpy.types.BevelModifier
width = bpy.types.FloatProperty
'''

#--- ###Operator
class Bevel(bpy.types.Operator):
    '''Bevels selected edges of the mesh'''
    bl_idname = "mesh.bevel"
    bl_label = "Bevel"
    bl_description = "Bevel selected edges"
    bl_options = {'REGISTER', 'UNDO'}
    
    #---parametres
    width = FloatProperty(name="Width", description="Bevel width",
                          subtype = 'DISTANCE', default = 0.1, min = 0.0,
                          step = 1, precision = 2)
    
    LAST_WIDTH_USED = "mesh.bevel.last_width"
    BEVEL_MODIFIER = bpy.types.BevelModifier
    PREV_POS_VAL = 0
    
    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")
    
    @classmethod
    def poll(cls, context):
        return(context.mode == "EDIT_MESH")
    
    
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            newvalue = event.mouse_x
            print("Mouse x:" + str(newvalue))
            difference = (newvalue - self.PREV_POS_VAL)/100.0
            print("Diff: " + str(difference))
            self.BEVEL_MODIFIER.width = self.BEVEL_MODIFIER.width + difference
            print("Mod Width: " + str(self.BEVEL_MODIFIER.width))
            self.PREV_POS_VAL = newvalue
        elif event.type == 'LEFTMOUSE':  # Confirm
            #self.execute(context)
            return {'FINISHED'}
        elif event.type in ('RIGHTMOUSE', 'ESC'):  # Cancel
            obj = context.active_object
            if obj.modifiers[0] == self.BEVEL_MODIFIER.name:
                obj.modifiers.remove(obj.modifiers[0])
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        print("Invoke() called")
        
        #refresh data:
        bpy.ops.object.editmode_toggle()       
        selected = 0
        #check edges
        for edge in context.object.data.edges:
            if edge.select:
                selected += 1           
        bpy.ops.object.editmode_toggle()
                
        if selected > 0:
            #check stored value
            last_width = context.scene.get(self.LAST_WIDTH_USED, None)
            if last_width:
                self.width = last_width
            else:
                self.width = 1.0       
            #Add modifier here
            self.PREV_POS_VAL = event.mouse_x
            
            #add Bevel modifier
            bpy.ops.object.modifier_add(type='BEVEL')
            
            obj = context.active_object
            #set bevel weight mode
            
            self.BEVEL_MODIFIER = obj.modifiers[-1]
            self.BEVEL_MODIFIER.limit_method = 'WEIGHT'
            self.BEVEL_MODIFIER.edge_weight_method = 'LARGEST'
            
            #move modifier to top of the list
            while obj.modifiers[0] != self.BEVEL_MODIFIER:
                bpy.ops.object.modifier_move_up(modifier = self.BEVEL_MODIFIER.name)
                
            print(context.window_manager.modal_handler_add(self))
            return {'RUNNING_MODAL'}
        else:
            self.report(type = "ERROR", message = "No edges selected")
            return {'CANCELLED'}
        
    def execute(self, context):
        print("in execute(), width = %1.2f" % self.width)
        bevel(context.object, self.width)

        context.scene[self.LAST_WIDTH_USED] = self.width
        return('FINISHED')

def bevel(obj, width):
    """Bevels selected edges of the mesh
        Arguments:
            @obj (Object): An object with a mesh, with selected edges
            @width (Float): The degree of bevel.
        This function should only be called in Edit Mode.
    """
    #assign weights
    for edge in obj.data.edges:
        if edge.select:
            edge.bevel_weight = 1.0
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = bevel.name)

    ''' clears the bevel weights for the selected edges'''
    #reset weights
    for edge in obj.data.edges:
        if edge.select:
            edge.bevel_weight = 0.0

def menu_draw(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(Bevel.bl_idname, "Bevel")
            
def register():
    register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_draw)
    
def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_draw)
    unregister_module(__name__)
    
if __name__ == '__main__':
    register()
        
        