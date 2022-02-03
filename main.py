import pygame
from pygame.locals import *
import math
import sys

class Corner:
    def __init__(self, neighbors, id, position, weight):
        self.neighbors = neighbors
        self.id = id
        self.position = position
        self.weight = weight
        # self.selected = False

    def displaySelf(self):
        print("Id is " + str(self.id) + ". My neighbors are " + str(self.neighbors))


pairs = [(0, 1, 1), (1, 2, 1), (3, 4, 1), (4, 5, 1), (6, 7, 1), (7, 8, 1), (9, 10, 1), (11, 12, 1), (13, 24, 1), (13, 14, 1), (0, 15, 1), (3, 16, 1), (6, 17, 1), (1, 18, 1), (4, 19, 1), (7, 20, 1), (9, 21, 1), (11, 22, 1), (8, 28, 1), (5, 27, 1), (2, 26, 1), (10, 29, 1), (14, 32, 1), (15, 16, 1), (16, 17, 1), (18, 19, 1), (19, 20, 1), (19, 21, 1), (21, 22, 1), (22, 23, 1), (24, 23, 1), (23, 25, 1), (26, 27, 1), (27, 28, 1), (27, 29, 1), (40, 29, 1), (29, 30, 1), (30, 31, 1), (40, 30, 1), (40, 38, 1), (38, 39, 1), (39, 30, 1), (39, 33, 1), (33, 32, 1), (32, 31, 1), (32, 44, 1), (34, 33, 1), (34, 43, 1), (34, 35, 1), (35, 36, 1), (36, 37, 1), (37, 38, 1), (37, 41, 1), (36, 42, 1)]





positions = [(173, 932), (238, 793), (262, 418), (326, 941), (382, 804), (410, 428), (429, 943), (442, 792), (488, 429), (390, 710), (425, 331), (391, 611), (427, 226), (286, 513), (324, 127), (171, 908), (335, 911), (434, 919), (239, 762), (365, 743), (443, 764), (369, 701), (367, 610), (366, 543), (278, 542), (422, 540), (279, 411), (417, 407), (491, 416), (412, 335), (413, 232), (416, 144), (292, 140), (264, 145), (204, 145), (161, 145), (149, 167), (154, 221), (233, 223), (269, 224), (239, 327), (72, 228), (67, 163), (202, 27), (292, 27)]

stairwells = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]


school = []

for i in range(len(positions)): # 1,2,3,4,5
    school.append(Corner([], i, positions[i], 1))


for corner in school:
    corner.displaySelf()

for pair in pairs:
    endpoint1 = pair[0]
    endpoint2 = pair[1]
    school[endpoint1].neighbors.append(endpoint2)
    school[endpoint2].neighbors.append(endpoint1)

print("------")

for corner in school:
    corner.displaySelf()

bellman_pairs = []
for p in pairs:
    u,v,w = p
    x1,y1 = school[u].position
    x2,y2 = school[v].position
    if u in stairwells and v in stairwells:
        w = 10
    else:
        w = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    bellman_pairs.append((u,v,w))
    bellman_pairs.append((v,u,w))





print("pygame implementation")

dimensions = (688,1000)
screen = pygame.display.set_mode(dimensions)
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)
pygame.display.set_caption("navigator")
clock = pygame.time.Clock()
selection = []

running = True

node_radius = 10
node_color = (255,255,0)
edge_color = (255,255,255)
stairwell_color = (0,255,255)
highlight_color = (255,128,255)
image2 = pygame.image.load('plan2.png').convert_alpha()


def getPath(parent, vertex):
    if vertex < 0:
        return []
    return getPath(parent, parent[vertex]) + [vertex]


# Function to run the Bellman–Ford algorithm from a given source
def bellmanFord(edges, source, dest, n):
    # distance[] and parent[] stores the shortest path (least cost/path) info
    distance = [sys.maxsize] * n
    parent = [-1] * n

    # Initially, all vertices except source vertex weight INFINITY and no parent
    distance[source] = 0

    # relaxation step (run V-1 times)
    for k in range(n - 1):
        # edge from `u` to `v` having weight `w`
        for (u, v, w) in edges:
            # if the distance to destination `v` can be shortened by taking edge (u, v)
            if distance[u] != sys.maxsize and distance[u] + w < distance[v]:
                # update distance to the new lower value
                distance[v] = distance[u] + w
                # set v's parent as `u`
                parent[v] = u

    # run relaxation step once more for n'th time to check for negative-weight cycles
    for (u, v, w) in edges:  # edge from `u` to `v` having weight `w`
        # if the distance to destination `u` can be shortened by taking edge (u, v)
        if distance[u] != sys.maxsize and distance[u] + w < distance[v]:
            print('Negative-weight cycle is found!!')
            return


    return getPath(parent, dest)



animation = 0
selection = []
highlight = []
path = bellmanFord(bellman_pairs, 1, 40, 45)
print(path)
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x,y)
            for corner in school:
                if (x-corner.position[0])**2 + (y-corner.position[1])**2 <= node_radius**2:
                    if len(selection) == 0:
                        selection = [corner.id]
                    elif len(selection) == 1:
                        if selection[0] != corner.id:
                            selection.append(corner.id)
                            path = bellmanFord(bellman_pairs, selection[0], selection[1], 45)
                            highlight = []
                            for i in range(len(path)):
                                highlight.append(school[path[i]].position)

                    else:
                        selection = [corner.id]
                    break
    screen.blit(image2, [0, 0])

    for corner in school:

        # if corner.selected == True:
        #     pygame.draw.circle(screen, (0, 255, 255), corner.position, node_radius)
        # else:
        if corner.id in selection:
            pygame.draw.circle(screen, (128, 255, 255), corner.position, node_radius)
        else:
            pygame.draw.circle(screen, node_color, corner.position, node_radius)
        textsurface = myfont.render(str(corner.id), False, (0, 0, 255))

        screen.blit(textsurface,[corner.position[0]-7, corner.position[1]-10])
        for neighbor in corner.neighbors:
            if corner.id in stairwells and school[neighbor].id in stairwells:
                pygame.draw.line(screen, stairwell_color, corner.position, school[neighbor].position)
            else:
                pygame.draw.line(screen, edge_color, corner.position, school[neighbor].position)
        if len(highlight) > 0:
            # print(highlight)
            pygame.draw.lines(screen, highlight_color, False, highlight, 5)
    pygame.display.flip()
    clock.tick(60)

