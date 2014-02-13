--[[

ngPlant-plugin : model-export
menu-name : Render with Povray

--]]

--[[

Pov-ray file exporter & renderer for ngplant
by Yorik van Havre - http://yorik.orgfree.com


                    ========== USAGE ==============

This file must be placed in the ngPlant plugins directory.
Then, an entry will appear in ngPlant File -> Export menu.
For the plugin to work, povray must be installed on your system, and
be available from the command line: typing: 

povray 

in terminal must work (it shows a list of povray options).
On Debian/Ubuntu systems, installing the povray package is enough,
on windows, you must maybe add the povray path to your search path.

Another important thing, by default, povray is not allowed to
access all your directory structure. If you want to use textures,
you'll probably need to grant povray normal access to your files.
For that, you must edit your povray.conf file and change 
File I/O Security to none or read-only.


                   ====== BEGIN GPL LICENSE BLOCK =====

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

                   ===== END GPL LICENSE BLOCK =====
--]]

function VisibleGroupsIter(Model)
	local IntGroupIndex = 0
	local VisGroupIndex = 0
	local GroupCount    = Model:GetGroupCount()
	return function ()
	local LODLevel = GetCurrentLOD()
	IntGroupIndex = IntGroupIndex + 1

	while IntGroupIndex <= GroupCount do
		local Group = Model:GetGroup(IntGroupIndex)
		local MinLOD,MaxLOD
		MinLOD,MaxLOD = Group:GetLODVisRange()

		if (ExportHiddenGroups or (not Group:IsHidden())) and
		(ExportOutVisRangeGroups or ((LODLevel >= MinLOD) and (LODLevel <= MaxLOD))) then
			VisGroupIndex = VisGroupIndex + 1
			return VisGroupIndex,Group
		else
			IntGroupIndex = IntGroupIndex + 1
		end
	end

	return nil
end
end

function ExportPovFile(PovFileName,lightDir,lightInt)
	PovFile = io.open(PovFileName,"w")
	PovFile:write("//povray file exported from ngplant\n")

	VertexIndexOffset   = 1
	NormalIndexOffset   = 1
	TexCoordIndexOffset = 1

	for GroupIndex,Group in VisibleGroupsIter(PlantModel) do
		Material = Group:GetMaterial()

		PovFile:write("mesh2 {\n\tvertex_vectors {\n")
		Buffer = Group:GetVAttrBuffer(NGP_ATTR_VERTEX)
		VertexIndexStep = table.getn(Buffer)
		PovFile:write(string.format("\t\t%s,\n",table.getn(Buffer)))
		for i,v in ipairs(Buffer) do
			PovFile:write(string.format("\t\t< %f, %f, %f>,\n",v[1],v[2],v[3]))
		end
		PovFile:write("\t\t}\n")

		PovFile:write("\tnormal_vectors {\n")
		Buffer = Group:GetVAttrBuffer(NGP_ATTR_NORMAL)
		NormalIndexStep = table.getn(Buffer)
		PovFile:write(string.format("\t\t%s,\n",table.getn(Buffer)))
		for i,v in ipairs(Buffer) do
			PovFile:write(string.format("\t\t< %f, %f, %f>,\n",v[1],v[2],v[3]))
		end
		PovFile:write("\t\t}\n")

		PovFile:write("\tuv_vectors {\n")
		Buffer = Group:GetVAttrBuffer(NGP_ATTR_TEXCOORD0)
		TexCoordIndexStep = table.getn(Buffer)
		PovFile:write(string.format("\t\t%s,\n",table.getn(Buffer)))
		for i,v in ipairs(Buffer) do
			PovFile:write(string.format("\t\t<%f,%f>,\n",v[1],v[2]))
		end
		PovFile:write("\t\t}\n")

		Buffer = nil
		VertexIndexBuffer   = Group:GetVAttrIndexBuffer(NGP_ATTR_VERTEX,true,VertexIndexOffset)
		NormalIndexBuffer   = Group:GetVAttrIndexBuffer(NGP_ATTR_NORMAL,true,NormalIndexOffset)
		TexCoordIndexBuffer = Group:GetVAttrIndexBuffer(NGP_ATTR_TEXCOORD0,true,TexCoordIndexOffset)
		PrimitiveCount = table.getn(VertexIndexBuffer)

		facesCount = 0
		for PrimitiveIndex = 1,PrimitiveCount do
			facesCount = facesCount + 1
			if Group:GetPrimitiveType(PrimitiveIndex) == NGP_QUAD then
				facesCount = facesCount + 1
			end
		end

		PovFile:write("\tface_indices {\n")
		PovFile:write(string.format("\t\t%s,\n",facesCount)) 
		for PrimitiveIndex = 1,PrimitiveCount do
			vi = VertexIndexBuffer[PrimitiveIndex]
			if Group:GetPrimitiveType(PrimitiveIndex) == NGP_QUAD then
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",vi[1]-1,vi[2]-1,vi[3]-1))
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",vi[1]-1,vi[3]-1,vi[4]-1))
			else
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",vi[1]-1,vi[2]-1,vi[3]-1))
			end
		end
		PovFile:write("\t\t}\n")

		PovFile:write("\tnormal_indices {\n")
		PovFile:write(string.format("\t\t%s,\n",facesCount))
		for PrimitiveIndex = 1,PrimitiveCount do
			ni = NormalIndexBuffer[PrimitiveIndex]
			if Group:GetPrimitiveType(PrimitiveIndex) == NGP_QUAD then
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",ni[1]-1,ni[2]-1,ni[3]-1))
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",ni[1]-1,ni[3]-1,ni[4]-1))
			else
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",ni[1]-1,ni[2]-1,ni[3]-1))
			end
		end
		PovFile:write("\t\t}\n")

		PovFile:write("\tuv_indices {\n")
		PovFile:write(string.format("\t\t%s,\n",facesCount))
		for PrimitiveIndex = 1,PrimitiveCount do
			ti = TexCoordIndexBuffer[PrimitiveIndex]
			if Group:GetPrimitiveType(PrimitiveIndex) == NGP_QUAD then
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",ti[1]-1,ti[2]-1,ti[3]-1))
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",ti[1]-1,ti[3]-1,ti[4]-1))
			else
				PovFile:write(string.format("\t\t<%u,%u,%u>,\n",ti[1]-1,ti[2]-1,ti[3]-1))
			end
		end
		PovFile:write("\t\t}\n")
		if Material.TexNames[NGP_TEX_DIFFUSE] then
			PovFile:write("\tuv_mapping\n")
		end

		PovFile:write("\ttexture {\n")
		PovFile:write(string.format("\t\tpigment { rgb <%f,%f,%f> }\n",Material.Color.R,Material.Color.G,Material.Color.B))
		if Material.TexNames[NGP_TEX_DIFFUSE] then
			PovFile:write(string.format("\t\tpigment { image_map {tga \"%s\"} }\n",GetTextureFileName(Material.TexNames[NGP_TEX_DIFFUSE])))
			PovFile:write(string.format("\t\tnormal { bump_map {tga \"%s\"} }\n",GetTextureFileName(Material.TexNames[NGP_TEX_DIFFUSE])))
		end
		PovFile:write("\t\t}\n")


		PovFile:write("\t}\n")
	end

-- 	camera setup

	MinX,MinY,MinZ,MaxX,MaxY,MaxZ = PlantModel:GetBoundingBox()
	PlantLength = (MaxX-MinX)
	PlantHeight = (MaxY-MinY)
	if PlantHeight >= PlantLength then
		PovFile:write("//high plant\n")
		camAxis = PlantHeight/2+2.5
		camY = PlantHeight/2
	else
		camAxis = PlantLength/2+2.5
		camY = MinY+PlantLength/2
	end
	camX = MaxX-PlantLength/2
	PovFile:write(string.format("camera { orthographic right %f up %f location <%f , %f ,-10> look_at  <%f , %f , 0.0> }\n",camAxis,camAxis,camX,camY,camX,camY))

--	light setup

	lightX = 150
	if lightDir == "Right" then
		lightX = -150
	end
		PovFile:write(string.format("light_source { <%f,250,-250> color rgb <%f,%f,%f> }\n",lightX,lightInt*0.97,lightInt*0.95,lightInt*0.70))
		PovFile:write(string.format("global_settings { ambient_light rgb <%f,%f,%f> }\n",lightInt*0.86,lightInt*1,lightInt*1.1))

	PovFile:close()

end

PngFileName = ShowFileSaveDialog("Choose a .PNG file name")

resol = "256"
Params = ShowParameterDialog(
	{
		{
			label   = "Image resolution",
			name    = "imageres",
			type    = "choice",
			choices = { "256x256","512x512", "1024x1024", "2048x2048" },
		},
		{
			label   = "Light coming from",
			name    = "light",
			type    = "choice",
			choices = { "Left", "Right"}
		},
		{
			label   = "Light intensity",
			name    = "intensity",
			type    = "number",
			default = 1
		},
		{
			label   = "Keep .POV file after render?",
			name    = "pov",
			type    = "choice",
			choices = { "No", "Yes" }
		}
	})

if Params == nil then
	return nil
else
	if Params.imageres == "2048x2048" then
		resol = "2048"
	elseif Params.imageres == "1024x1024" then
		resol = "1024"
	elseif Params.imageres == "512x512" then
		resol = "512"
	end

	if PngFileName then
		if ExportPreferences.HiddenGroupsExportMode == NGP_ALWAYS then
			ExportHiddenGroups = true
		elseif ExportPreferences.HiddenGroupsExportMode == NGP_NEVER then
			ExportHiddenGroups = false
		else
			ExportHiddenGroups = ShowYesNoMessageBox('Render hidden branch groups?','Export mode')
		end

		if ExportPreferences.OutVisRangeExportMode == NGP_ALWAYS then
			ExportOutVisRangeGroups = true
		elseif ExportPreferences.OutVisRangeExportMode == NGP_NEVER then
			ExportOutVisRangeGroups = false
		else
			ExportOutVisRangeGroups = ShowYesNoMessageBox('Render branch groups which are outside LOD visibility range?','Export mode')
		end

		PovFileName = string.sub(PngFileName,0,-4)..("pov")
		ExportPovFile(PovFileName,Params.light,Params.intensity)

		execString="povray +UA +P +H"..resol.." +W"..resol.." +A +O"..PngFileName.." "..PovFileName
		os.execute (execString)

		if Params.pov == "No" then
			os.remove(PovFileName)
		end

	end

end


