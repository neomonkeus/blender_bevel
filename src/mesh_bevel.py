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
'''
    #edge = bpy.types.MeshEdge
    #obj = bpy.types.Object
    #bevel = bpy.types.BevelModifier
    #width = bpy.types.FloatProperty

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
    
    @classmethod
    def poll(cls, context):
        return(context.mode == "EDIT_MESH")
    
    def invoke(self, context, event):
        print("in invoke()")
        #refresh data:
        bpy.ops.object.editmode_toggle()       
        selected = 0
        
        #@TODO: compare with an active_obj implementation
        for edge in context.object.data.edges:
            if edge.select:
                selected += 1
                
        bpy.ops.object.editmode_toggle()
                
        if selected > 0:
            last_width = context.scene.get(self.LAST_WIDTH_USED, None)
            if last_width:
                self.width = last_width
            return self.execute(context)
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
    
    bpy.ops.object.editmode_toggle()
    
    #add Bevel modifier
    bpy.ops.object.modifier_add(type='BEVEL')
    
    #set bevel weight mode
    bevel = obj.modifiers[-1]
    bevel.limit_method = 'WEIGHT'
    bevel.edge_weight_method = 'LARGEST'
    bevel.width = width
    
    #move modifier to top of the list
    while obj.modifiers[0] != bevel:
        bpy.ops.object.modifier_move_up(modifier = bevel.name)
    
    #assign weights
    for edge in obj.data.edges:
        if edge.select:
            edge.bevel_weight = 1.0
    
    bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = bevel.name)
    
    #reset weights
    for edge in obj.data.edges:
        if edge.select:
            edge.bevel_weight = 0.0
    
    bpy.ops.object.editmode_toggle()

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
        
        