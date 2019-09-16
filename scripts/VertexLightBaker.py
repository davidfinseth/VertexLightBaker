import maya.cmds as cmds
def BakeLightsToVertex():
    folderdir = str(cmds.fileDialog2(caption="Select a Folder to save Textures",fileMode=2)[0])
    # Ask user what texture size to use
    result = cmds.promptDialog(
                    title='Vertex Light Baker',
                    message='Texture Size',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        texturesize = int(cmds.promptDialog(query=True, text=True))
        selected = cmds.ls(selection=True)
        for obj in selected:
            # Delete any extra uvsets
            ClearExtraUVSets(obj)
            # Create new automatic uv set
            shapes = cmds.listRelatives(obj, shapes=True)
            cmds.select(obj)
            cmds.polyUVSet(create=True, uvSet='automatic')
            # Automatic unwrap the object
            cmds.polyAutoProjection(obj,layoutMethod=False, projectBothDirections=False, insertBeforeDeformers=True,scaleMode=True,optimize=True,planes=6,uvSetName="automatic",percentageSpace=0.2,worldSpace=False)
            uvSetName = cmds.polyUVSet( query=True, currentUVSet=True)
            # Render the lighting to a texture
            cmds.arnoldRenderToTexture(filter="gaussian",filter_width=2.0,aa_samples=3,r=texturesize,folder=folderdir,uv_set = str(uvSetName[0]))
            # create a shader
            shader = cmds.shadingNode("surfaceShader",asShader=True)
            #a file texture node
            file_node = cmds.shadingNode("file",asTexture=True,icm=True)
            Texture2D = cmds.shadingNode("place2dTexture",asUtility=True)
            # connect the texture to the shader of the object
            cmds.connectAttr("{0}.coverage".format(Texture2D),"{0}.coverage".format(file_node),force=True)
            cmds.connectAttr("{0}.translateFrame".format(Texture2D),"{0}.translateFrame".format(file_node),force=True)
            cmds.connectAttr("{0}.rotateFrame".format(Texture2D),"{0}.rotateFrame".format(file_node),force=True)
            cmds.connectAttr("{0}.mirrorU".format(Texture2D),"{0}.mirrorU".format(file_node),force=True)
            cmds.connectAttr("{0}.mirrorV".format(Texture2D),"{0}.mirrorV".format(file_node),force=True)
            cmds.connectAttr("{0}.stagger".format(Texture2D),"{0}.stagger".format(file_node),force=True)
            cmds.connectAttr("{0}.wrapU".format(Texture2D),"{0}.wrapU".format(file_node),force=True)
            cmds.connectAttr("{0}.wrapV".format(Texture2D),"{0}.wrapV".format(file_node),force=True)
            cmds.connectAttr("{0}.repeatUV".format(Texture2D),"{0}.repeatUV".format(file_node),force=True)
            cmds.connectAttr("{0}.offset".format(Texture2D),"{0}.offset".format(file_node),force=True)
            cmds.connectAttr("{0}.rotateUV".format(Texture2D),"{0}.rotateUV".format(file_node),force=True)
            cmds.connectAttr("{0}.noiseUV".format(Texture2D),"{0}.noiseUV".format(file_node),force=True)
            cmds.connectAttr("{0}.vertexUvOne".format(Texture2D),"{0}.vertexUvOne".format(file_node),force=True)
            cmds.connectAttr("{0}.vertexUvTwo".format(Texture2D),"{0}.vertexUvTwo".format(file_node),force=True)
            cmds.connectAttr("{0}.vertexUvThree".format(Texture2D),"{0}.vertexUvThree".format(file_node),force=True)
            cmds.connectAttr("{0}.vertexCameraOne".format(Texture2D),"{0}.vertexCameraOne".format(file_node),force=True)
            cmds.connectAttr("{0}.outUV".format(Texture2D),"{0}.uv".format(file_node),force=True)
            cmds.connectAttr("{0}.outUvFilterSize".format(Texture2D),"{0}.uvFilterSize".format(file_node),force=True)
            # a shading group
            shading_group = cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
            cmds.setAttr('{0}.fileTextureName'.format(file_node), folderdir +"/"+ str(shapes[0]) +".exr", type="string")
            cmds.sets(obj,edit=True,forceElement=shading_group)
            cmds.uvLink(uvSet=shapes[0]+".uvSet[1].uvSetName",texture=file_node)
            # Multiply Divide node to fix uv seems
            multiply_divide = cmds.shadingNode('multiplyDivide',asUtility=True)
            cmds.connectAttr('{0}.outColor'.format(file_node), '{0}.input1'.format(multiply_divide), force=True)
            cmds.connectAttr('{0}.outAlpha'.format(file_node), '{0}.input2X'.format(multiply_divide), force=True)
            cmds.connectAttr('{0}.outAlpha'.format(file_node), '{0}.input2Y'.format(multiply_divide), force=True)
            cmds.connectAttr('{0}.outAlpha'.format(file_node), '{0}.input2Z'.format(multiply_divide), force=True)
            #connect shader to sg surface shader
            cmds.connectAttr('{0}.outColor'.format(shader) ,'{0}.surfaceShader'.format(shading_group),force=True)
            #connect multiply_divide node to shader's color
            cmds.connectAttr('{0}.output'.format(multiply_divide), '{0}.outColor'.format(shader),force=True)
            cmds.setAttr('{0}.operation'.format(multiply_divide), 2)
            cmds.select(obj,r=True)
            # bake the texture into the object's vertex color
            cmds.polyGeoSampler(ids=True,sf=1,su=True,cdo=True,colorBlend="overwrite",alphaBlend="overwrite")
            ClearExtraUVSets(obj)


def ClearExtraUVSets(obj):
    indices = cmds.polyUVSet(obj, query=True, allUVSetsIndices=True)
    for i in indices:
        uvsetname = cmds.getAttr(obj + ".uvSet[" + str(i) + "].uvSetName")
        if uvsetname != "map1":
            cmds.polyUVSet(delete=True, uvSet=uvsetname)
