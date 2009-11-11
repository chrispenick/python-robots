# -*- coding: utf-8 -*-

import time, Queue, thread, random

# ==========================================================

class direction:
	
	dd = [
		'Top',
		'Right',
		'Bottom',
		'Left',
		]
	
	def __init__(self, d=0):
		if d < len(self.dd):
			self.d = d
		else:
			self.d = self.dd.index(d)
	
	def __str__(self):
		return self.dd[self.d]
	
	def __repr__(self):
		return '<direction %s>' % self.__str__()
	
	def __eq__(self, one):
		return self.d == one.d
	
	def __neg__(self):
		return self.__add__(2)
	
	def __add__(self, one):
		return direction((self.d + one) % 4)

	def __sub__(self, one):
		return self.__add__(-one)
	
	def __hash__(self):
		return self.d
		

directionTop    = direction(0)
directionRight  = direction(1)
directionBottom = direction(2)
directionLeft   = direction(3)

# ==========================================================

class posDifferentSizes(Exception):
	pass

class posExceptionValue(Exception):
	pass

# ----------------------

class position:
	
	def __init__(self, x, y, width=0, height=0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		if width and (x < 0 or x > width):
			raise posExceptionValue('X = %d' % x)
		if height and (y < 0 or y > height):
			raise posExceptionValue('Y = %d' % y)
	
	def __str__(self):
		if self.width and self.height:
			return '%d, %d (%d, %d)' % (self.x, self.y, self.width, self.height)
		return '%d, %d' % (self.x, self.y)
	
	def __repr__(self):
		return '<position %s>' % self.__str__()
	
	def __eq__(self, one):
		return self.x == one.x and self.y == one.y
	
	def __neg__(self):
		return position(-self.x, -self.y)
	
	def __add__(self, one):
		if self.width and one.width and self.width != one.width:
			raise posDifferentSizes('%d != %d' % (self.width, one.width))
		if self.height and one.height and self.height != one.height:
			raise posDifferentSizes('%d != %d' % (self.height, one.height))
		return position(
					self.x + one.x,
					self.y + one.y,
					self.width or one.width,
					self.height or one.height
					)

	def __sub__(self, one):
		return self.__add__(-one)

# ----------------------

def stepForward(pos, dr):
	return {
		directionTop:    position(0, -1),
		directionRight:  position(1, 0),
		directionBottom: position(0, 1),
		directionLeft:   position(-1, 0),
		}[dr] + pos

# ==========================================================

class landUnbroken(Exception):
	pass

# ----------------------

class land:
	
	char = '?'
	name = '?'
	patency = True
	shoot = True
	visibility = True
	broken = None
	
	def __init__(self):
		pass

	def __eq__(self, one):
		return (self.patency == one.patency) and (self.shoot == one.shoot) and (self.visibility == one.visibility)

	def __repr__(self):
		return '<land %s>' % self.__str__()
	
	def demolish(self):
		if not self.broken:
			raise landUnbroken(self.name)
		self.char       = self.broken.char
		self.name       = self.broken.name
		self.patency    = self.broken.patency
		self.shoot      = self.broken.shoot
		self.visibility = self.broken.visibility
		self.broken     = self.broken.broken

# ----------------------

class landFloor(land):
	char = ' '
	name = 'Gender'

class landWall(land):
	char = '#'
	name = 'Wall'
	patency = False
	shoot = False
	visibility = False
	broken = landFloor

class landBarrier(landWall):
	char = 'X'
	name = 'Barrier'
	broken = False

class landWater(land):
	char = '~'
	name = 'Water'
	patency = False

class landTree(land):
	char = 'T'
	name = 'Tree'
	visibility = False

# ----------------------

landChars = dict([ (x.char, x) for x in (landFloor, landWall, landBarrier, landWater, landTree) ])

# ==========================================================

class preObjectUse(Exception):
	pass

class objAbsence(Exception):
	pass

# ----------------------

class obj:
	
	name = 'preObject'
	char = '?'
	
	def __init__(self, pos):
		self.pos = pos
	
	def use(self, unit):
		raise preObjectUse()

# ----------------------

class objMedKit(obj):
	
	name = 'MedKit'
	char = 'M'
	
	def use(self, unit):
		unit.health = unit.maxHealth

class objChucks(obj):
	
	name = 'Chucks'
	char = 'A'
	
	def use(self, unit):
		unit.ammo = unit.maxAmmo

# ==========================================================

class unitAbsence(Exception):
	pass

class unitCantStep(Exception):
	pass

class unitNoAmmo(Exception):
	pass

# ----------------------

class unit:
	
	def getChar(self):
		return {
			directionTop: '^',
			directionRight: '>',
			directionBottom: 'v',
			directionLeft: '<',
			}[self.dt]
	
	char = property(getChar)
	
	def __init__(self, map, health, ammo, pos, dt=direction()):
		self.map = map
		self.maxHealth = health
		self.health = health
		self.maxAmmo = ammo
		self.ammo = ammo
		self.pos = pos
		self.dt = dt
		self.queue = Queue.Queue(1)
	
	def __str__(self):
		if self.health < 1:
			return 'DEAD'
		return 'H:%2d A:%2d pos:%5s dt:%s' % (self.health, self.ammo, self.pos, self.dt)
	
	def __repr__(self):
		return '<unit %s>' % self.__str__()
	
	def wound(self):
		self.health -= 1
		if self.health < 1:
			self.suicide()
	
	def suicide(self):
		self.map.units.remove(self)
	
	# ------------------
	
	def canStep(self, dt=None):
		if not dt:
			dt = self.dt
		
		try:
			p = stepForward(self.pos, dt)
		except posExceptionValue:
			return False
		
		try:
			self.map.getUnit(p)
			return False
		except unitAbsence:
			try:
				return self.map.getLand(p).patency
			except IndexError:
				return False
	
	def fireLook(self, dt=None):
		if not dt:
			dt = self.dt
		
		p = self.pos
		while 1:

			try:
				p = stepForward(p, dt)
			except posExceptionValue:
				return None
			
			try:
				return self.map.getUnit(p)
			except unitAbsence:
				try:
					l = self.map.getLand(p)
					if not l.shoot: #visibility?
						return l
				except IndexError:
					pass
	
	def fireLookUnit(self, dt=None):
		x = self.fireLook(dt)
		if x and issubclass(x.__class__, unit):
			return x
	
	# ------------------
	
	def turnLeft(self):
		self.dt -= 1
		self.queue.get()

	def turnRight(self):
		self.dt += 1
		self.queue.get()
	
	def step(self):
		if not self.canStep():
			raise unitCantStep('%s : %s' % (self.pos, self.dt))
		self.pos = stepForward(self.pos, self.dt)
		try:
			o = self.map.getObject(self.pos)
			o.use(self)
			self.map.objects.remove(o)
		except objAbsence:
			pass
		
		self.queue.get()
	
	def fire(self):
		if not self.ammo:
			raise unitNoAmmo()
		self.ammo -= 1
		x = self.fireLook()
		if x :
			if issubclass(x.__class__, unit):
				x.wound()
			elif issubclass(x.__class__, land) and x.broken:
				x.demolish()
		self.queue.get()
	
	# ------------------
	
	def cycle(self):
		self.queue.get()
		while 1:
			if self.health < 1:
				return
			self.do()
	
	def do(self):
		while 1:
			time.sleep(10000)

# ==========================================================

class tank(unit):

	def do(self):
		self.turnRight()
		while self.canStep():
			if self.fireLook() and self.ammo:
				self.fire()
			if random.randint(0, 3) == 0:
				break
			self.step()

# ==========================================================

class map:
	
	def __init__(self):
		self.objects = []
		self.units = []
	
	def makeMap(self, height, width):
		pass
	
	def fromString(self, str):
		ll = str.split('\n')
		self.height = len(ll)
		self.width = len(ll[0])
		self.m = [ [ landChars[y]() for y in x ] for x in ll ]
	
	def __str__(self):
		n = 10
		v = []
		for y in range(self.height):
			vv = []
			for x in range(self.width):
				pos = position(x, y)
				try:
					vv.append(self.getUnit(pos).char)
				except unitAbsence:
					try:
						vv.append(self.getObject(pos).char)
					except objAbsence:
						vv.append(self.getLand(pos).char)
			v.append( ' '*n+'|'+''.join(vv)+'|' )
		return '\n'.join([' '*n+'+'+'-'*self.width+'+']+v+[' '*n+'+'+'-'*self.width+'+'])
	
		#return '\n'.join([' '*10+'+'+'-'*self.width+'+']
		#				+[ ''.join([' '*10+'|']+[ y.char for y in x ]+['|']) for x in self.m ]
		#				+[' '*10+'+'+'-'*self.width+'+'])
	
	def getLand(self, pos):
		return self.m[pos.y][pos.x]
	
	def getObject(self, pos):
		for x in self.objects:
			if x.pos == pos:
				return x
		raise objAbsence(str(pos))
	
	def getUnit(self, pos):
		for x in self.units:
			if x.pos == pos:
				return x
		raise unitAbsence(str(pos))
	
	def addObject(self, one):
		self.objects.append(one)
	
	def addUnit(self, one):
		self.units.append(one)
	
	def __getitem__(self, xy):
		return getLand(*xy)
	
	def cycle(self):
		for x in self.units:
			thread.start_new_thread(x.cycle, ())
		while 1:
			for x in self.units:
				x.queue.put(1)
				time.sleep(0.2)
				for x in self.units:
					print repr(x)
				print '\n\n', self, '\n\n'
			time.sleep(.3)
	
# ==========================================================

firstMap = map()
firstMap.fromString(
				'             \n'
				' # # # # # # \n'
				' # # # # # # \n'
				' # # #X# # # \n'
				' # #     # # \n'
				'     # #     \n'
				'X ##     ## X\n'
				'             \n'
				' # # ### # # \n'
				' # # # # # # \n'
				' # #     # # \n'
				'             '
				)

firstMap.addObject( objMedKit(position(6, 6, firstMap.width, firstMap.height)) )
firstMap.addObject( objChucks(position(6, 4, firstMap.width, firstMap.height)) )
firstMap.addObject( objChucks(position(6, 9, firstMap.width, firstMap.height)) )

firstMap.addUnit( tank(firstMap, 3, 30, position(0, 0, firstMap.width, firstMap.height), directionTop) )
firstMap.addUnit( tank(firstMap, 3, 30, position(6, 0, firstMap.width, firstMap.height), directionTop) )
firstMap.addUnit( tank(firstMap, 3, 30, position(12, 0, firstMap.width, firstMap.height), directionTop) )

firstMap.addUnit( tank(firstMap, 3, 30, position(0, 11, firstMap.width, firstMap.height), directionTop) )
firstMap.addUnit( tank(firstMap, 3, 30, position(6, 11, firstMap.width, firstMap.height), directionTop) )
firstMap.addUnit( tank(firstMap, 3, 30, position(12, 11, firstMap.width, firstMap.height), directionTop) )

firstMap.cycle()



