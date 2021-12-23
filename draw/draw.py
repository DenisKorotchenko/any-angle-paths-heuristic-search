import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, ImageDraw
from algorithms.structures import Map, Node


def draw(grid_map: Map, start:Node=None, goal:Node=None, path=None, nodes_opened=None, nodes_expanded=None, nodes_reexpanded=None, show_in_notebook=True):
    '''
    Auxiliary function that visualizes the environment, the path and opened, expanded and reexpanded cells.
    '''
    height, width = grid_map.get_size()
    k = 2048 // max(height, width)
    h_im = height * k
    w_im = width * k
    im = Image.new('RGB', (w_im, h_im), color='white')
    draw = ImageDraw.Draw(im)

    for i in range(height):
        for j in range(width):
            if (not grid_map.traversable(i, j)):
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))

    if nodes_opened is not None:
        for node in nodes_opened:
            draw.ellipse((node.j * k - 10, node.i * k - 10, node.j * k + 10, node.i * k + 10),
                         fill=(213, 219, 219), width=0)

    if nodes_expanded is not None:
        for node in nodes_expanded:
            if type(node) is Node:
                draw.ellipse((node.j * k - k / 4, node.i * k - k / 4, node.j * k + k / 4, node.i * k + k / 4),
                             fill=(131, 145, 146), width=0)
            else:
                (i, j) = node
                draw.ellipse((j * k - k / 4, i * k - k / 4, j * k + k / 4, i * k + k / 4),
                             fill=(131, 145, 146), width=0)

    if nodes_reexpanded is not None:
        for node in nodes_reexpanded:
            draw.ellipse((node.j * k - k / 4, node.i * k - k / 4, node.j * k + k / 4, node.i * k + k / 4),
                         fill=(255, 145, 146), width=0)

    prev_step = start
    if path is not None:
        for step in path:
            if (step is not None):
                if (grid_map.traversable_step_long(step.i, step.j, prev_step.i, prev_step.j)):
                    draw.line((step.j * k, step.i * k, prev_step.j * k, prev_step.i * k), fill=(52, 152, 219), width=7)
                else:
                    draw.line((step.j * k, step.i * k, prev_step.j * k, prev_step.i * k), fill=(230, 126, 34), width=7)
                prev_step = step

    #if path is not None:
    #    for step in path:
    #        if (step is not None):
    #            draw.ellipse((step.j * k - 15, step.i * k - 15, step.j * k + 15, step.i * k + 15),
    #                         fill=(52, 152, 219), width=0)

    if (start is not None):  # and (grid_map.traversable(start.i, start.j)):
        draw.ellipse((start.j * k - 20, start.i * k - 20, start.j * k + 20, start.i * k + 20),
                     fill=(40, 180, 99), width=0)

    if (goal is not None):  # and (grid_map.traversable(goal.i, goal.j)):
        draw.ellipse((goal.j * k - 20, goal.i * k - 20, goal.j * k + 20, goal.i * k + 20),
                     fill=(231, 76, 60), width=0)

    if show_in_notebook:
        _, ax = plt.subplots(dpi=150)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.imshow(np.asarray(im))
        plt.show()
    else:
        im.show()
