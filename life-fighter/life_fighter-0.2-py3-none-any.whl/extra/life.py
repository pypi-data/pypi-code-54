DEAD = 0
ALIVE = 1

class Cell:
    "A life cell"
    
    def __init__(self, state=DEAD):
	self.state = state
	self.next_state = state

    def __str__(self):
        return str(self.state)
		
    def get_state(self):
	return self.state

    def is_alive(self):
        return self.state == ALIVE
	    
    def set_next_state(self, state):
	self.next_state = state

    def birth(self):
        self.set_next_state(ALIVE)

    def die(self):
        self.set_next_state(DEAD)
		
    def update_state(self):
	self.state = self.next_state

class Grid:
    "A life grid"
	
    def __init__(self, width, height):
	self.width = width
	self.height = height
	self.cells = {}
	for i in range(width):
            for j in range(height):
		self.cells[i,j] = Cell()
    def __str__(self):
        s = ""
        for j in range(self.height):
            for i in range(self.width):
                s += str(self.cells[i,j])
            s += "\n"
        return s
				
    def add_cells(self, cells):
	for k in cells:
            self.cells[k] = cells[k]

    def alive_neights(self, i, j):
	t = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
	count = 0
	for o,p in t:
            try:
                count += self.cells[i+o,j+p].get_state()
            except KeyError:
                pass
	return count

    def beat(self):
        cells = self.cells
	for i,j in cells:
            n = self.alive_neights(i,j)
	    c = cells[i,j]
	    if c.is_alive():
		if n <= 1 or n >= 4: c.die()
	    else:
		if n == 3: c.birth()
        for k in cells:
            cells[k].update_state()

# Text mode test

if __name__ == "__main__":
    g = Grid(14,14)
    slizer = [(1,0), (2,1), (0,2), (1,2), (2,2)]
    ds = {}
    for i,j in slizer:
        ds[i,j] = Cell(ALIVE)
    g.add_cells(ds)

    type = ""
    while type != "q":
        print str(g)
	g.beat()
	type = raw_input()
