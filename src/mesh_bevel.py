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

'''  
Type declaration: useful for auto-completion 
Comment before publishing
'''
    #edge = bpy.types.MeshEdge
    #obj = bpy.types.Object
    #bevel = bpy.types.BevelModifier

#--- ###Operator
class Bevel(bpy.types.Operator):
    '''Bevels selected edges of the mesh'''
    bl_idname = "mesh.bevel"
    bl_label = "Bevel"
    bl_description = "Bevel selected edges"
    
    @classmethod
    def poll(cls, context):
        return(context.mode == "EDIT_MESH")
    
    def execute(self, context):
        bevel(context.active_object, 0.1)
        bpy.ops.object.editmode_toggle()
        return('FINISHED')
    
    def invoke(self, context, event):
        #refresh data:
        bpy.ops.object.editmode_toggle()
        
        selected = 0
        
        #TODO: compare with active obj implementation
        for edge in context.object.data.edges:
            if edge.select:
                selected += 1
                
        if selected > 0:
            return self.execute(context)
        else:
            bpy.ops.object.editmode_toggle()
            self.report(type = "ERROR", message = "No edges selected")
            return {'CANCELLED'}
    
def bevel(obj, width):
    """Bevels selected edges of the mesh
        Arguments:
            @obj (Object): An object with a mesh
            It should have some edges selected
            This function should only be called in Edit Mode.
    """
    
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

def menu_draw(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(Bevel.bl_idname, "Bevel")
            
def register():
    register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_draw)
    
def unregister():
    unregister_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_draw)
    
if __name__ == '__main__':
    register()
        
        