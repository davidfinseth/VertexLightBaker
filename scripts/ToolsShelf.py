import maya.cmds as mc
import shelfBase
import VertexLightBaker
reload(VertexLightBaker)


class customShelf(shelfBase._shelf):
    def build(self):
         self.addButon("BakeVertexLights","vertexlightbake.png",VertexLightBaker.BakeLightsToVertex)


customShelf()
