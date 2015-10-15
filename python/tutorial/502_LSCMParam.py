# Add the igl library to the modules search path
import sys, os
sys.path.insert(0, os.getcwd() + "/../")

import igl

V = igl.eigen.MatrixXd()
F = igl.eigen.MatrixXi()
V_uv = igl.eigen.MatrixXd()

def key_down(viewer, key, modifier):
    if key == ord('1'):
        # Plot the 3D mesh
        viewer.data.set_mesh(V,F)
        viewer.core.align_camera_center(V,F)
    elif key == ord('2'):
        # Plot the mesh in 2D using the UV coordinates as vertex coordinates
        viewer.data.set_mesh(V_uv,F)
        viewer.core.align_camera_center(V_uv,F)
    viewer.data.compute_normals()
    return False

# Load a mesh in OFF format
igl.readOFF("../../tutorial/shared/camelhead.off", V, F);

# Fix two points on the boundary
bnd = igl.eigen.MatrixXi()
b   = igl.eigen.MatrixXi(2,1)

igl.boundary_loop(F,bnd)
b[0] = bnd[0]
b[1] = bnd[int(bnd.size()/2)]
bc = igl.eigen.MatrixXd([[0,0],[1,0]])

# LSCM parametrization
igl.lscm(V,F,b,bc,V_uv)

# Scale the uv
V_uv *= 5

# Plot the mesh
viewer = igl.viewer.Viewer()
viewer.data.set_mesh(V, F)
viewer.data.set_uv(V_uv)
viewer.callback_key_down = key_down

# Disable wireframe
viewer.core.show_lines = False

# Draw checkerboard texture
viewer.core.show_texture = True

# Launch the viewer
viewer.launch()
