class Grid:
    """
    Represents a 2d grid of things, whatever they might be
    This would mainly be used to represent a grid of some sort in a game
        Input: grid - 2d list
    """
    def __init__(self, grid = None):
        #placeholder for the 2d list
        self.grid = None

        #How many items wide and tall is the grid
        self.width = 0
        self.height = 0
        if grid:
            self.set_grid(grid)

    def set_grid(self, grid):
        """
        Sets the grid and calculates its width and height
        """
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def get_grid(self):
        return list(self.grid)

    def get_cell(self, x, y):
        """
        Returns whatever element is at the x, y position in the grid
        If its an invalid index, we return None
        """
        try:
            return self.grid[y][x]
        except IndexError:
            return None

    def to_string(self):
        string = []
        for y in range(self.height):
            for x in range(self.width):
                string.append(self.grid[y][x])
            string.append("\n")
        return ", ".join(string)

    def get_neighbors(self, x, y):
        y_top = y - 1
        y_bottom = y + 1
        x_left = x - 1
        x_right = x + 1
        top_left = self.get_cell(x_left, y_top)
        top = self.get_cell(x, y_top)
        top_right = self.get_cell(x_right, y_top)
        left = self.get_cell(x_left, y)
        right = self.get_cell(x_right, y)
        bottom_left = self.get_cell(x_left, y_bottom)
        bottom = self.get_cell(x, y_bottom)
        bottom_right = self.get_cell(x_right, y_bottom)
        return [
            ((x_left, y_top), top_left), 
            ((x, y_top), top), 
            ((x_right, y_top), top_right),
            ((x_left, y), left), 
            ((x_right, y), right),
            ((x_left, y_bottom), bottom_left), 
            ((x, y_bottom), bottom), 
            ((x_right, y_bottom), bottom_right)
        ]
