# maze_solver
Instructions for running the program:
Required packages and their pip install command:
1. Numba - pip install numba
2. OpenCV - pip install opencv-python, pip install opencv-contrib-python
3. Numpy - pip install numpy
4. Pygame - pip install pygame
5. Python_ta

Setup: Place all the .py files in one folder, create a folder called mazes and place it within the same file as the .py
files. Within the mazes folder, place the maze images.

To run the program, run the main method, main.py. The user will be greeted by the menu of the program with
the first maze loaded.

# Program
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
