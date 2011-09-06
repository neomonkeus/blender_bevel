#--- ### Header
bl_info = {
           "name": "Bevel",
           "author": "Witold Jaworski, Gerard Moran",
           "version": (0, 0, 5),
           "blender": (2, 5, 9),
           "api": 39307,
           "location": "View3D -> Edit Mode -> Special (W-key)",
           "category": "Mesh",
           "description": "Bevels selected edges",
           "warning": "",
           "wiki_url": "",
           "tracking_url": "https://github.com/neomonkeus/blender_bevel"
           }

import bpy
from bpy.utils import register_module, unregister_module

#=== ###Operator
class Bevel(bpy.types.Operator):
    '''Bevels selected edges of the mesh'''
    bl_idname = "mesh.bevel"
    bl_label = "Bevel"
    bl_description = "Bevel selected edges"
    
    def execute(self, context):
        bevel(context.active_object, 0.1)
        return('FINISHED')
    
def bevel(obj, width):
    """Bevels selected edges of the mesh
        Arguments:
            @obj (Object): An object with a mesh
            It should have some edges selected
            This function should only be called in Edit Mode.
    """

    #edge = bpy.types.MeshEdge
    #obj = bpy.types.Object
    #bevel = bpy.types.BevelModifier

    bpy.ops.object.mode_set(mode='OBJECT',toggle=False)
    #add Bevel modifier
    bpy.ops.object.modifier_add(type='BEVEL')
    
    bevel = obj.modifiers[-1]
    bevel.limit_method = 'WEIGHT'
    bevel.edge_weight_method = 'LARGEST'
    bevel.width = width
    
    #move modifier to top of the list
    while obj.modifiers[0] != bevel:
        bpy.ops.object.modifier_move_up(modifier = bevel.name)
    
    for edge in obj.data.edges:
        if edge.select:
            edge.bevel_weight = 1.0
    
    bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = bevel.name)
    
    for edge in obj.data.edges:
        if edge.select:
            edge.bevel_weight = 0.0
    
    bpy.ops.object.editmode_toggle()
    #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    print(obj)
            
def register():
    register_module(__name__)
    
def unregister():
    unregister_module(__name__)
    
if __name__ == '__main__':
    register()
        
        