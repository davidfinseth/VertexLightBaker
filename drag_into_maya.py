import maya.cmds as cmds
import os as os
directoryPath = "/Users/Shared/Autodesk/modules/maya/" + cmds.about(version=True) +"/"
if not os.path.exists(directoryPath):
    os.makedirs(directoryPath)
folderdir = cmds.fileDialog2(caption="Select the root Vertex Light Baker folder that you downloaded.",fileMode=2)[0]
f = open(directoryPath+"VertexLightBaker.mod","w")
f.write("+ VertexLightBaker 1.0 " + folderdir)
f.close()