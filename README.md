# maze_solver
# Required packages and their pip install commands, if any
1. Numba
   * pip install numba
2. OpenCV
   * pip install opencv-python
   * pip install opencv-contrib-python
3. Numpy
   * pip install numpy
4. Pygame
   * pip install pygame
5. Python_ta
   
Setup: Place all the .py files in one folder, create a folder called mazes and place it within the same file as the .py
files. Within the mazes folder, place the maze images.

To run the program, run the main method, main.py. The user will be greeted by the menu of the program with
the first maze loaded.

![image](https://user-images.githubusercontent.com/45114241/122686085-63f65e00-d1dd-11eb-80fe-3303da7d5d9b.png)

The user can then select their desired pathfinding algorithm (by clicking on the drop down menu) and start and
stop points by clicking the start / stop button, then the point on the maze.

![image](https://user-images.githubusercontent.com/45114241/122686198-fbf44780-d1dd-11eb-9e17-8d3df867ca40.png)

Once both points are selected (and valid, if they are not, a message warning the user will be printed to the python
console) then the visualization will start and the path the algorithm traces will be drawn in red. Once the algorithm
finds the stop point, the final path will be traced in green. To run the program again, or with a different maze and
or pathfinding algorithm, click the restart button and repeat the previous steps.

![image](https://user-images.githubusercontent.com/45114241/122686103-825c5980-d1dd-11eb-840e-5605c1fa5ba3.png)

# Using Custom Mazes
The program also supports using the users own images. To do so, find or create an image of a maze that has a white
background and black walls. The image must be of an appropriate resolution, and rectangular mazes work best (if
using a non-rectangular maze, please view the subsection, ’Using Circular / Non-Rectangular Mazes’). Place the
image into the /mazes folder. Relaunch the program, and click the drop down menu for maze selection. Pick ’other’,
and then within the text box that appears, type the name of the file, including the extension and press the ENTER
key. Once the maze loads, you may follow the steps outlined above to see your custom maze visualized!

# Using Circular / Non-Rectangular Mazes
The program supports circular / non-rectangular mazes, although the cropping algorithm used does not support
circular / non-rectangular shapes as mentioned in the computational overview. Therefore, when adding circular /
non-rectangular mazes into the /mazes folder, please make sure the name of the file begins with ’c ’, for example
’c my maze.png’. This prefix tells the program to skip the cropping step.

![image](https://user-images.githubusercontent.com/45114241/122686140-ba639c80-d1dd-11eb-9125-9ea691805ea9.png)

# Additional Information - Computational Overview
Modules / Libraries:
* opencv-python and opencv-contrib-python. The former module is used for thresholding and preprocessing
the image, and the latter module is used because it contains an implementation of the Zhang-Suen thinning
algorithm written in C++, which is essential since it is a costly algorithm (if image resolution is too large) and
would take too much time if written in Python.

* numpy for array operations

* numba’s nopython mode complies specified python code into machine code the first time it is run. This is very
important as methods like get neighbours() will be called thousands to millions of times and so running the
functions from complied code is essential to keep up with real time visualization.

* pygame for real time visualization

The program first takes the specified maze image and (if the maze is rectangular) crops the maze such that
the outer white space is removed. This is done by finding the contours of the image, and assuming that the two
longest lines will be borders of the maze (usually this is the case for rectangular mazes, so the assumption is okay).
The program does work with any shape maze, however, the white space around the maze may lead to weird paths.
Otsu’s binarization is then applied to isolate the maze from the image, and then the maze is thinned to 1 pixel using
1Zhang-Suen algorithm to preserve connectivity. The perseverance of maze connectivity is integral to the program
since any ”holes” in the maze will alter the path the program finds. The resultant thinned maze is then stored into
a 2d array which represents a graph where each pixel of the maze is a vertex, and the edges are the valid path nodes
from of the neighboring 8 pixels.
The MatrixGraph class stores this array, and has various methods that are useful for graphs. For instance, getting
the neighbors of a vertex, finding the euclidean distance between two vertices within the graph, and calculating the
closest point of a path in relation to a specific point.
The PathfindingAlgorithms class within the algorithms.py module has various path finding algorithms as methods:

**Breadth First Search**: This version of breadth first search is implemented iteratively. The algorithm starts at the designated start
point, adds that vertex to a queue and marks it as visited, along with all its neighbors and then loops through
the queue until it is empty, or the target is found. The loop checks if the first vertex in the queue is the target
vertex, if it is not, then the vertex is removed from the queue and the vertex’s neighbors are added to the queue
if they have not been previously visited. Additionally, at each iteration of the loop, the path searched is drawn
in red. The function also keeps track of the path that is searched, so the final path can be drawn in green and
returned. The breadth first search algorithm searches each vertex in a first in first out order according to the
queue. This allows the path to quickly spread across the entire graph.

**Depth First Search**: This version of depth first search is implemented iteratively. The algorithm starts at the designated start
point, and adds that point to a stack. The function then loops until the stack is empty, or the target is found.
At each iteration of the loop, the top vertex of the stack is checked to see if it is the target vertex, if it is not,
the vertex is popped and it’s neighbors are pushed into the stack if they had not been previously discovered.
Additionally, at each iteration of the loop the path searched is drawn in red. The function also keeps track
of the path that is searched, so the final path can be drawn in green and is returned. The depth first search
algorithm searches each vertex in a last in first out order according to the stack. This allows for the algorithm
to cover a large distance but skips over side paths.

**A***: An unweighted implementation of the A* search using the Euclidean Distance heuristic is implemented. The
reason we opted for euclidean distance over Manhattan distance is because the method used to crop the maze
is limited to rectangular mazes; everything else works with any kind of maze. Thus, diagonal lines in mazes
are possible and so Manhattan distance is less accurate in these situations.

All visualization within the program is done via Pygame. The following modules all utilize Pygame in order to
convey data to the user, and allow for user input. We utilize the following:

* button.py: This module contains the Button and ToggleButton class that allows the user select the start and
stop points of the maze, along with reset the inputs.

* clock.py: This module contains the Timer class which allows the user to inspect how long the specified algorithm
has been running for.

* text box.py: This module contains the TextBox class which allows the user to manually input the filename of
a maze via the keyboard.

* drop down.py: This module contains the DropDown class which allows the user to select which pathfinding
algorithm and maze they want to see the program run with.

* algorithms.py: This module contains the PathfindingAlgorithms class which as previously mentioned stores
the pathfinding algorithms our program utilzes, however it also contains methods such as draw loop iterations
which allows the user to note how many nodes have been searched at any given point.
