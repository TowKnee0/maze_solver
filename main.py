import cv2
import sknw
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('maze.png')

retVal, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

thinned = cv2.ximgproc.thinning(thresh)

graph = sknw.build_sknw(thinned, multi=False)

G = nx.Graph(graph)
plt.imshow(image, cmap='gray')

# Draw Edges by 'pts'
for (s, e) in graph.edges():
    ps = graph[s][e]['pts']
    plt.plot(ps[:, 1], ps[:, 0], 'red')

# Draw Node by 'o'
node, nodes = graph.node, graph.nodes()
ps = np.array([node[i]['o'] for i in nodes])
plt.plot(ps[:, 1], ps[:, 0], 'g.')
plt.title('Skeletonize')
plt.savefig('Overlay_Maze.jpg')
plt.show()

G = nx.path_graph(len(ps))
G = nx.karate_club_graph()
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='b')

cv2.waitKey(0)
