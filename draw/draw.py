import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from PIL import Image, ImageDraw
from algorithms.structures import Map, Node


def draw(grid_map: Map, start:Node=None, goal:Node=None, path=None, nodes_opened=None, nodes_expanded=None, nodes_reexpanded=None, show_in_notebook=True, path2=None, path3=None, paths=None, labels=None):
    height, width = grid_map.get_size()
    k = 2048 // max(height, width)
    h_im = height * k
    w_im = width * k
    im = Image.new('RGB', (w_im, h_im), color='white')
    draw = ImageDraw.Draw(im)

    for i in range(height):
        for j in range(width):
            if not grid_map.traversable(i, j):
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

    path_colors=[(52,152,219), (218, 40, 235), (235, 228, 40), (67, 204, 147), (204, 133, 67), (139, 175, 196)]
    cmap_template = {0: [52/256, 152/256, 219/256, 1.], 1: [218/256, 40/256, 235/256, 1.], 2: [235/256, 228/256, 40/256, 1.],
            3: [67/256, 204/256, 147/256, 1.], 4: [204/256, 133/256, 67/256, 1.], 5: [139/256, 175/256, 196/256, 1.]}
    cmap = dict()

    if paths is not None:
        for i in range(min(len(paths), len(path_colors))):
            prev_step = start
            for step in paths[i]:
                if step is not None:
                    draw.line((step.j * k, step.i * k, prev_step.j * k, prev_step.i * k), fill=path_colors[i], width=7)
                    prev_step = step
            cmap[i] = cmap_template[i]
    else:
        prev_step = start
        if path is not None:
            for step in path:
                if (step is not None):
                    draw.line((step.j * k, step.i * k, prev_step.j * k, prev_step.i * k), fill=path_colors[0], width=7)
                    prev_step = step

        prev_step = start
        if path2 is not None:
            for step in path2:
                if (step is not None):
                    draw.line((step.j * k, step.i * k, prev_step.j * k, prev_step.i * k), fill=path_colors[1], width=7)
                    prev_step = step

        prev_step = start
        if path3 is not None:
            for step in path3:
                if (step is not None):
                    draw.line((step.j * k, step.i * k, prev_step.j * k, prev_step.i * k), fill=path_colors[2], width=7)
                    prev_step = step

    if start is not None:
        draw.ellipse((start.j * k - 20, start.i * k - 20, start.j * k + 20, start.i * k + 20),
                     fill=(40, 180, 99), width=0)

    if goal is not None:
        draw.ellipse((goal.j * k - 20, goal.i * k - 20, goal.j * k + 20, goal.i * k + 20),
                     fill=(231, 76, 60), width=0)

    if show_in_notebook:
        _, ax = plt.subplots(dpi=250)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.imshow(np.asarray(im))
        if paths is not None and labels is not None:
            patches = [mpatches.Patch(color=cmap[i], label=labels[i]) for i in cmap]
            plt.legend(handles=patches, loc="best", borderaxespad=0., prop={"size": 6})
        plt.show()
    else:
        im.show()
