#Code made by::
#Luis Sanchez --> Ci: 26.781.211
#Juan Zabala --> Ci: 26.900.042
#Alejandro Sanchez --> Ci: 27.242.594


from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpHprInterval, Func, Sequence
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task
from math import pi, sin, cos
from direct.gui.OnscreenText import OnscreenText,TextNode

import sys


# Pantalla completa
#loadPrcFileData("", """fullscreen 1
#win-size 1920 1080""")

def crearCubo(parent, x, y, z, posicion, cuboEstado, walls):
	# getV3n3cp() retorna un formato de vértice estándar con un color empaquetado, una normal de 3 componentes y una posición de vértice de 3 componentes.
	vformat = GeomVertexFormat.getV3n3cp()
	# GeomVertexData() se usa para almacenar incofmacion del vertice en tablas, cada columna es un dato del certice y la fila un nuevo vertice
	vdata = GeomVertexData("cubo_data", vformat, Geom.UHStatic)
	#Geom.UHStatic indica con que frecuencia se espera modificar los vertices, renderizando muchos cubos sin  cambiar vertices
	tris = GeomTriangles(Geom.UHStatic)
	# GeomTriangles almacena cualquier numero de triangulos conectados o no
	# GeomVertexWriter genera un puntero al objeto vdata para escribir datos en el
	posWriter = GeomVertexWriter(vdata, "vertex")
	colWriter = GeomVertexWriter(vdata, "color")
	normalWriter = GeomVertexWriter(vdata, "normal")

	vcount = 0
	contador = 0

	for direccion in (1, -1):
		for i in range(3):
			normal = VBase3()
			normal[i] = direccion
			rgb = [0., 0., 0.]

			#Colores del cubo
			if direccion == -1:
				#color =  (255, 0, 0	, 1.) #dejar aqui por sia
				if i == 0:
					color = (1, .5, .0, 1.) #Naranja
				elif i == 1:
					color =  (.024, .235, 1, 1.) #Azul
				elif i == 2:
					contador = contador + 1
					if contador == 1:
						color =  (255, 255, 0, 1.) #Amarillo

			elif i == 1:
				color = (0, 1, 0, 1) #verde
			elif i == 0:
				color = (255, 0, 0	, 1.) #rojo
			elif i == 2:
				color = (255, 255, 255, 1.) #Blanco
			else:
				pass


			for a, b in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
				pos = VBase3()
				pos[i] = direccion
				pos[(i + direccion) % 3] = a
				pos[(i + direccion * 2) % 3] = b

				posWriter.addData3f(pos)
				colWriter.addData4f(color)
				normalWriter.addData3f(normal)

			vcount += 4

			tris.addVertices(vcount - 2, vcount - 3, vcount - 4)
			tris.addVertices(vcount - 4, vcount - 1, vcount - 2)

	geom = Geom(vdata)
	# Geom es un objeto que recopila un geomVertexdata y uno o mas objetos GeomPrimitive para hacer una sola pueza geometrica
	geom.addPrimitive(tris)
	# GeomNode es un nodo que mantiene objeos geom renderizables de geometria
	node = GeomNode("cubo_node")
	node.addGeom(geom)
	cubo = parent.attachNewNode(node)
	cubo.setScale(.48)
	cubo.setPos(x, y, z)
	estado = set()  # the walls this cube belongs to
	posicion[cubo] = [x, y, z]
	cuboEstado[cubo] = estado
	# En Panda3D, el eje X apunta directamente a la derecha.
	# El eje Y va perpendicular a la pantalla.
	# El eje Z está apuntando hacia arriba.

	if x == 1:
		walls["right"].append(cubo)
		estado.add("right")
	elif x == -1:
		walls["left"].append(cubo)
		estado.add("left")
	elif x == 0:
		walls["center"].append(cubo)
		estado.add("center")

	if y == 1:
		walls["back"].append(cubo)
		estado.add("back")
	elif y == -1:
		walls["front"].append(cubo)
		estado.add("front")
	elif y == 0:
		walls["standing"].append(cubo)
		estado.add("standing")

	if z == -1:
		walls["down"].append(cubo)
		estado.add("down")
	elif z == 1:
		walls["up"].append(cubo)
		estado.add("up")
	elif z == 0:
		walls["equator"].append(cubo)
		estado.add("equator")

	return cubo


class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		# Presione Esc para salir del programa
		self.accept("escape", sys.exit)

		#Tiempo de que dura la pantalla de carga
		for i in range(0,15):
			self.loadscreen()

		

		# Instrucciones y teclas en la ventana generada
		info = OnscreenText(text="TECLAS:",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .90), scale=.07)
		up = OnscreenText(text="-Arriba: U, shift-U",
		                  style=1, fg=(1, 1, 1, 1), pos=(-1.1, .80), scale=.05)
		down = OnscreenText(text="-Abajo: D, shift-D",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .70), scale=.05)
		left = OnscreenText(text="    -Izquierda: L, shift-L",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .60), scale=.05)
		right = OnscreenText(text="    -Derecha: R, shift-R",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, .50), scale=.05)
		front = OnscreenText(text="-Frente: F, shift-F",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, .40), scale=.05)
		back = OnscreenText(text="-Fondo: B, shift-B",
		                    style=1, fg=(1, 1, 1, 1), pos=(-1.1, .30), scale=.05)
		equator = OnscreenText(text="    - Centro-E: E, shift-E",
		                       style=1, fg=(1, 1, 1, 1), pos=(-1.1, .20), scale=.05)
		standing = OnscreenText(text="   - Centro-S: S, shift-S",
		                        style=1, fg=(1, 1, 1, 1), pos=(-1.1, .10), scale=.05)
		center = OnscreenText(text="   - Centro-C: C, shift-C",
		                      style=1, fg=(1, 1, 1, 1), pos=(-1.1, .0), scale=.05)
		vista = OnscreenText(text="- Reinciar Vista: K",
		                      style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.10), scale=.05)
		voltear = OnscreenText(text="- Voltear Vista: Z",
		                      style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.20), scale=.05)
		info2 = OnscreenText(text="         INSTRUCCIONES:",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.60), scale=.07)
		inst1 = OnscreenText(text="                  Presionar teclas necesarias",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.70), scale=.05)
		inst2 = OnscreenText(text="          luego pulsar Enter para",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.80), scale=.05)
		inst3 = OnscreenText(text="     ejecutar la secuencia.",
		                     style=1, fg=(1, 1, 1, 1), pos=(-1.1, -.90), scale=.05)
		info3 = OnscreenText(text="PRESIONE ESC PARA SALIR",
		                     style=1, fg=(1, 1, 1, 1), pos=(1, -.90), scale=.05)
		integrantes =  OnscreenText(text="INTEGRANTES:\n "
		                                 "Alejandro Sánchez\n"
		                                 "Juan Zabala\n"
		                                 "Luis Sánchez",
		                    style=1, fg=(1, 1, 1, 1), pos=(1.08, .90), scale=.05)
		# Load background image
		try:
			b = OnscreenImage(parent=render2d, image="multimedia/bg.jpg")
		except:
			pass
		walls = {}
		pivotes = {}
		rotaciones = {}
		posicion = {}
		cuboEstado = {}
		# La división ecuatorial es la división entre las caras hacia arriba y hacia abajo,
		#  la división central entre las caras izquierda y derecha, la división en pie la izquierda
		wallIDs = ("front", "back", "left", "right", "down", "up", "equator", "center", "standing")
		giros = {}
		# VBase(Z,X,Y) Si gira alrededor de el eje Z, VBase3(90., 0., 0.).
		# El grado es positivo siguendo la regla de la mano derecha.
		giros["right"] = VBase3(0., -90., 0.)
		giros["center"] = VBase3(0., -90., 0.)  # La dirección de la rotacion de la sección "center" sigue la cara "right".
		giros["left"] = VBase3(0., 90., 0.)
		giros["back"] = VBase3(0., 0., -90.)
		giros["front"] = VBase3(0., 0., 90.)
		giros["standing"] = VBase3(0., 0., 90.)  # La dirección de la rotacion de la seccion de pie sigue la cara "front".
		giros["down"] = VBase3(90., 0., 0.)
		giros["up"] = VBase3(-90., 0., 0.)
		giros["equator"] = VBase3(-90., 0., 0.)  # La direccion de rotacion del centro "ecuator" sigue la cara "up".
		wallRotacion = {}
		wallNegRotacion = {}
		# Cada rotacion es una matriz.
		# La rotacion positiva "front" y la rotacion negativa "back" tienen la misma matriz.
		# El slice "stading" sigue las reglas de la cara "front".

		wallRotacion["right"] = wallRotacion["center"] = wallNegRotacion["left"] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
		wallRotacion["left"] = wallNegRotacion["right"] = wallNegRotacion["center"] = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

		wallRotacion["back"] = wallNegRotacion["standing"] = wallNegRotacion["front"] = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
		wallRotacion["front"] = wallRotacion["standing"] = wallNegRotacion["back"] = [[0, 0, -1], [0, 1, 0], [1, 0, 0]]

		wallRotacion["up"] = wallRotacion["equator"] = wallNegRotacion["down"] = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
		wallRotacion["down"] = wallNegRotacion["equator"] = wallNegRotacion["up"] = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]

		for wallID in wallIDs:
			walls[wallID] = []
			pivotes[wallID] = self.render.attachNewNode('pivot_%s' % wallID)
			rotaciones[wallID] = {"hpr": giros[wallID]}
		# print walls
		# print pivots
		# print rotations
		for x in (-1, 0, 1):
			for y in (-1, 0, 1):
				for z in (-1, 0, 1):
					crearCubo(self.render, x, y, z, posicion, cuboEstado, walls)
		# Configuracion de camara y visualizacion
		self.cam.setPos(7, -10, 6)
		self.cam.lookAt(0., 0., 0.)


		def reparentCubos(wallID):
			pivote = pivotes[wallID]
			children = pivote.getChildren()
			children.wrtReparentTo(self.render)
			pivote.clearTransform()
			children.wrtReparentTo(pivote)
			for cubo in walls[wallID]:
				cubo.wrtReparentTo(pivote)

		def actualizarEstadoCubo(wallID, negRotacion=False):
			for cubo in walls[wallID]:
				estadoAnterior = cuboEstado[cubo]
				#print("Estado Anterior:", estadoAnterior)
				#print("Posicion Anterior", posicion[cubo])
				estadoActualizado = set()
				cuboEstado[cubo] = estadoActualizado

				# Coordenada X
				newPos = 0
				if not negRotacion:
					for j in range(3):
						newPos = newPos + int(posicion[cubo][j]) * int(wallRotacion[wallID][j][0])
				else:
					for j in range(3):
						newPos = newPos + int(posicion[cubo][j]) * int(wallNegRotacion[wallID][j][0])

				if newPos == 1:
					estadoActualizado.add("right")
				elif newPos == -1:
					estadoActualizado.add("left")
				elif newPos == 0:
					estadoActualizado.add("center")
				newPosX = newPos

				# Coordenada Y
				newPos = 0
				if not negRotacion:
					for j in range(3):
						newPos = newPos + int(posicion[cubo][j]) * int(wallRotacion[wallID][j][1])
				else:
					for j in range(3):
						newPos = newPos + int(posicion[cubo][j]) * int(wallNegRotacion[wallID][j][1])

				if newPos == 1:
					estadoActualizado.add("back")
				elif newPos == -1:
					estadoActualizado.add("front")
				elif newPos == 0:
					estadoActualizado.add("standing")
				newPosY = newPos

				# Coordenada Z
				newPos = 0
				if not negRotacion:
					for j in range(3):
						newPos = newPos + int(posicion[cubo][j]) * int(wallRotacion[wallID][j][2])
				else:
					for j in range(3):
						newPos = newPos + int(posicion[cubo][j]) * int(wallNegRotacion[wallID][j][2])

				if newPos == 1:
					estadoActualizado.add("up")
				elif newPos == -1:
					estadoActualizado.add("down")
				elif newPos == 0:
					estadoActualizado.add("equator")
				newPosZ = newPos

				posicion[cubo] = [newPosX, newPosY, newPosZ]
				#print("Estado Actualizado:", estadoActualizado)
				#print("Posicion Actualizada:", posicion[cubo])
				#print("*******************")

				for antWallID in estadoAnterior - estadoActualizado:
					walls[antWallID].remove(cubo)
				for actWallID in estadoActualizado - estadoAnterior:
					walls[actWallID].append(cubo)

		self.sec = Sequence()




		def aggIntervalo(wallID, negRotacion=False):
			self.sec.append(Func(reparentCubos, wallID))
			rot = rotaciones[wallID]["hpr"]
			if negRotacion:
				rot = rot * -1.
			# 1.0 es la velocidad de rotación, 2.5 es más lenta.
			self.sec.append(LerpHprInterval(pivotes[wallID], 0.5, rot))
			self.sec.append(Func(actualizarEstadoCubo, wallID, negRotacion))

		def aceptarInput():  # Revision: top-->up, bottom-->down. Reverse rotation: back,up,right
			# <F> agrega rotacion positiva "Front"
			self.accept("f", lambda: aggIntervalo("front"))
			# <Shift+F> agrega rotacion negativa "front
			self.accept("shift-f", lambda: aggIntervalo("front", True))
			# <B> agregra rotacion positiva "back"
			self.accept("b", lambda: aggIntervalo("back"))
			# <Shift+B> gregra rotacion negativa "back"
			self.accept("shift-b", lambda: aggIntervalo("back", True))

			# <L> agrega rotacion positiva "left"
			self.accept("l", lambda: aggIntervalo("left"))
			# <Shift+L> agrega rotacion negativa "left"
			self.accept("shift-l", lambda: aggIntervalo("left", True))
			# <R> agrega rotacion positiva "right"
			self.accept("r", lambda: aggIntervalo("right"))
			# <Shift+R> agrega rotacion negativa "right"
			self.accept("shift-r", lambda: aggIntervalo("right", True))
			# <D> agrega rotacion positiva "down"
			self.accept("d", lambda: aggIntervalo("down"))
			# <Shift+D> agrega rotacion negativa "down"
			self.accept("shift-d", lambda: aggIntervalo("down", True))
			# <U> adds a positive Up rotation
			self.accept("u", lambda: aggIntervalo("up"))
			# <Shift+U> adds a negative Up rotation
			self.accept("shift-u", lambda: aggIntervalo("up", True))

			# Rivision: to rotate the center slice
			# <C> adds a positive Back rotation
			self.accept("c", lambda: aggIntervalo("center"))
			# <Shift+C> adds a negative Back rotation
			self.accept("shift-c", lambda: aggIntervalo("center", True))
			# Rivision: to rotate the equator slice
			# <E> adds a positive Back rotation
			self.accept("e", lambda: aggIntervalo("equator"))
			# <Shift+E> adds a negative Back rotation
			self.accept("shift-e", lambda: aggIntervalo("equator", True))
			# Rivision: to rotate the standing slice
			# <S> adds a positive Back rotation
			self.accept("s", lambda: aggIntervalo("standing"))
			# <Shift+S> adds a negative Back rotation
			self.accept("shift-s", lambda: aggIntervalo("standing", True))

			# <Enter> Arranca la secuencia
			self.accept("enter", comenzarSec)

		

		def ignoraInput():
			self.ignore("f")
			self.ignore("shift-f")
			self.ignore("b")
			self.ignore("shift-b")
			self.ignore("l")
			self.ignore("shift-l")
			self.ignore("r")
			self.ignore("shift-r")
			self.ignore("d")
			self.ignore("shift-d")
			self.ignore("u")
			self.ignore("shift-u")
			self.ignore("enter")

		def comenzarSec():
			# No permitir entrada de secuencia durante la secuencia principal
			ignoraInput()
			# ...Aceptar entrada cuando se finaliza la secuencia
			self.sec.append(Func(aceptarInput))
			self.sec.start()
			#print("Secuancia comenzada")
			# Crear una nueva secuencia, so no new intervals will be appended to the started one
			self.sec = Sequence()

		aceptarInput()

		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")	

		#Funcion de reiniciar la vista del cubo 
		def reset():
			self.trackball.node().setHpr(0, 0, 0)
		#Funcion de vista inversa del cubo
		def inverso():
			self.trackball.node().setHpr(180, 0, 0)
		
		#Al presionar la "k" se reinicia la vista
		self.accept("k",reset)
		#Al presionar la "z" se volteara la vista
		self.accept("z",inverso)

	#Funcion la cual fija la camara en la posicion
	def spinCameraTask(self, task):
		self.camera.setPos(0,0,0)
		return Task.cont
		
	#Funcion de Pantalla de Carga
	def loadscreen(self):
		loadingText=OnscreenText("GenerandoCubo...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
		self.graphicsEngine.renderFrame() #render a frame otherwise the screen will remain black
		self.graphicsEngine.renderFrame() #idem dito
		self.graphicsEngine.renderFrame() #you need to do this because you didn't yet call run()
		self.graphicsEngine.renderFrame() #run() automatically renders the frames for you

app = MyApp()
# configurar el cubo en el scene graph
app.cam.node().getDisplayRegion(0).setSort(20)
app.run()

