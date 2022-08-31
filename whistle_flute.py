import bpy
import bmesh
import math
import os
import sys

def make_path_work(pathstr):
	new_path = ""
	for char in pathstr:
		if (char == '\\'):
			new_path += r"\\"
		else:
			new_path += char
	return new_path

def parse_line_into_array(line):
	arr = line.split(",")
	for i in range(len(arr)):
		old_string = arr[i]
		new_string = ""
		for char in old_string:
			if char.isdigit() == 1 or char == '.':
				new_string += char
		arr[i] = new_string
	for i in range(len(arr)):
		string = arr[i]
		fl = float(string)
		arr[i] = fl
	return arr 

def get_inputs(filename):
	resFile = open(og_directory + filename, "r")	
	hole_diameters_line = resFile.readline()
	hole_distances_line = resFile.readline()
	bore = float(resFile.readline())
	total_length = float(resFile.readline())
	od = float(resFile.readline())
	hole_diameters = parse_line_into_array(hole_diameters_line)
	hole_distances = parse_line_into_array(hole_distances_line)
	return hole_diameters, hole_distances, bore, total_length, od

def create_body(od, bore, total_length):
	bpy.ops.object.select_all(action='SELECT')
	for obj in bpy.context.selected_objects:
		bpy.ops.object.delete()
	bpy.ops.mesh.primitive_cylinder_add(vertices = 200, radius=od*0.5, depth = total_length, enter_editmode=False, align='WORLD', location=(total_length/2, 0, 0), scale=(1, 1, 1))
	scj = bpy.context.scene
	ob = bpy.context.object
	ob.rotation_euler = (0,math.radians(90),0)
	for obj in bpy.context.selected_objects:
		obj.name = "outer"
		obj.data.name = "outer"
	bpy.ops.mesh.primitive_cylinder_add(vertices = 200,radius=bore*0.5, depth = total_length+1, enter_editmode=False, align='WORLD', location=(total_length/2, 0, 0), scale=(1, 1, 1))
	scj = bpy.context.scene
	ob = bpy.context.object
	ob.rotation_euler = (0,math.radians(90),0)
	context = bpy.context
	scene = context.scene
	outer = scene.objects.get("outer")
	inner = scene.objects.get("Cylinder")
	if outer and inner:
		bool = outer.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = inner
		bool.operation = 'DIFFERENCE'
		bpy.ops.object.modifier_apply({"object": outer}, modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cylinder'].select_set(True)
		bpy.ops.object.delete()

def make_holes(hole_diameters, hole_distances, bore, total_length):
	for i in range(len(hole_diameters)):
		from_end = total_length - hole_distances[i]
		bpy.ops.mesh.primitive_cylinder_add(radius = hole_diameters[i]/2, depth=2*bore, enter_editmode=False, align='WORLD', location=(from_end, 0, bore), scale=(1, 1, 1))
		context = bpy.context
		scene = context.scene
		flute = scene.objects.get("outer")
		cyl = scene.objects.get("Cylinder")
		if flute and cyl:
			bool = flute.modifiers.new(name='booly', type='BOOLEAN')
			bool.object = cyl
			bool.operation = 'DIFFERENCE'
			bpy.ops.object.modifier_apply(
			{"object": flute},
			modifier=bool.name)
			bpy.ops.object.select_all(action='DESELECT')
			bpy.data.objects['Cylinder'].select_set(True)
			bpy.ops.object.delete()


def make_fipple(hole_diameters, hole_distances, bore, total_length):
	bpy.ops.mesh.primitive_cylinder_add(vertices = 200, radius=od*0.5, depth = total_length*0.15, enter_editmode=False, align='WORLD', location=(-total_length*0.075, 0, 0), scale=(1, 1, 1))
	scj = bpy.context.scene
	ob = bpy.context.object
	ob.rotation_euler = (0,math.radians(90),0)
	bpy.ops.mesh.primitive_cylinder_add(vertices = 200,radius=bore*0.5, depth = total_length*0.15+1, enter_editmode=False, align='WORLD', location=(-total_length*0.075, 0, 0), scale=(1, 1, 1))
	scj = bpy.context.scene
	ob = bpy.context.object
	ob.rotation_euler = (0,math.radians(90),0)
	bpy.ops.mesh.primitive_cylinder_add(radius = hole_diameters[0]/2, depth=2*bore, enter_editmode=False, align='WORLD', location=(-hole_diameters[0]/2, 0, bore), scale=(1, 1, 1))
	context = bpy.context
	scene = context.scene
	cylout = scene.objects.get("Cylinder")
	cylin = scene.objects.get("Cylinder.001")
	if cylout and cylin:
		bool = cylout.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = cylin
		bool.operation = 'DIFFERENCE'
		bpy.ops.object.modifier_apply({"object": cylout}, modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cylinder.001'].select_set(True)
		bpy.ops.object.delete()
	context = bpy.context
	scene = context.scene
	cylout = scene.objects.get("Cylinder")
	flute = scene.objects.get("outer")
	if flute and cylout:
		bool = flute.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = cylout
		bool.operation = 'UNION'
		bpy.ops.object.modifier_apply(
		{"object": flute},
		modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cylinder'].select_set(True)
		bpy.ops.object.delete()	
	context = bpy.context
	scene = context.scene
	flute = scene.objects.get("outer")
	cyl = scene.objects.get("Cylinder.002")
	if flute and cyl:
		bool = flute.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = cyl
		bool.operation = 'DIFFERENCE'
		bpy.ops.object.modifier_apply(
		{"object": flute},
		modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cylinder.002'].select_set(True)
		bpy.ops.object.delete()
	bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius = 1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, od*0.5),rotation=(0,1.5708,4.7124), scale=(2, 4, 2))
	context = bpy.context
	scene = context.scene
	flute = scene.objects.get("outer")
	cyl = scene.objects.get("Cylinder")
	if flute and cyl:
		bool = flute.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = cyl
		bool.operation = 'DIFFERENCE'
		bpy.ops.object.modifier_apply(
		{"object": flute},
		modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cylinder'].select_set(True)
		bpy.ops.object.delete()
	bpy.ops.mesh.primitive_cylinder_add(vertices = 200, radius=bore*0.5, depth = total_length*0.15-hole_diameters[0], enter_editmode=False, align='WORLD', location=(-total_length*0.075-hole_diameters[0]/2, 0, 0), scale=(1, 1, 1))
	context = bpy.context
	scene = context.scene
	ob = context.object
	ob.rotation_euler = (0,math.radians(90),0)
	cyl = scene.objects.get("Cylinder")
	bpy.ops.mesh.primitive_cube_add(size = total_length*0.15-hole_diameters[0], enter_editmode=False, align='WORLD', location=(-total_length*0.075-hole_diameters[0]/2, 0, -bore*0.125+bore*0.5+(total_length*0.15-hole_diameters[0])/2), scale=(1, 1, 1))
	context = bpy.context
	scene = context.scene
	cube = scene.objects.get("Cube")
	if cyl and cube:
		bool = cyl.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = cube
		bool.operation = 'DIFFERENCE'
		bpy.ops.object.modifier_apply({"object": cyl},modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cube'].select_set(True)
		bpy.ops.object.delete()
	if flute and cyl:
		bool = flute.modifiers.new(name='booly', type='BOOLEAN')
		bool.object = cyl
		bool.operation = 'UNION'
		bpy.ops.object.modifier_apply(
		{"object": flute},
		modifier=bool.name)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects['Cylinder'].select_set(True)
		bpy.ops.object.delete()


og_directory = make_path_work(sys.argv[-2])
file_name = sys.argv[-1]
hole_diameters, hole_distances, bore, total_length, od = get_inputs("\\results.txt")
create_body(od, bore, total_length)
make_holes(hole_diameters, hole_distances, bore, total_length)
make_fipple(hole_diameters, hole_distances, bore, total_length)
file_path = og_directory + "\\" + file_name + ".blend"
bpy.ops.wm.save_as_mainfile(filepath=file_path)




