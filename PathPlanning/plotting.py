"""
Plot tools 2D
from github
"""


import os
import sys
import matplotlib.pyplot as plt

# sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../..")

from PathPlanning import env


class Plotting:
    def __init__(self, xI: tuple, xG: tuple):
        """
        @param xI: starting point(x, y)
        @param xG: goal point (x, y)
        """
        self.xI = xI
        self.xG = xG
        self.env = env.Env()
        self.obs = self.env.obs_map()  # is it necessary?

    def update_obs(self, obs):
        self.obs = obs

    def animation(self, path, visited, name):
        self.plot_grid(name)
        self.plot_visited(visited)
        self.plot_path(path)
        plt.show()

    def plot_grid(self, name: str):
        """
        plot the map
        @param name: graph title, string
        """
        obs_x = [x[0] for x in self.obs]  # obs = ((1,0), (2,0), ...)
        obs_y = [x[1] for x in self.obs]

        plt.plot(self.xI[0], self.xI[1], "bs")  # the starting point
        plt.plot(self.xG[0], self.xG[1], "gs")  # the goal point
        plt.plot(obs_x, obs_y, "ks")
        plt.title(name)
        plt.axis("equal")

    def plot_visited(self, visited: list, cl='gray'):
        if self.xI in visited:
            visited.remove(self.xI)
        if self.xG in visited:
            visited.remove(self.xG)

        count = 0

        for x in visited:
            count += 1
            plt.plot(x[0], x[1], color=cl, marker='o')
            plt.gcf().canvas.mpl_connect('key_release_event', lambda event: [exit(0) if event.key == 'escape' else None])

            if count < len(visited) / 3:
                length = 20
            elif count < len(visited) * 2 / 3:
                length = 30
            else:
                length = 40

            if count % length == 0:
                plt.pause(0.001)  # small pause between each new visited point plotted

        plt.pause(0.01)

    def plot_path(self, path: list, cl='r', flag=False):
        """

        @param path: [(x1, y1), (x2, y2), ...]
        @param cl:
        @param flag:
        """
        path_x = [path[i][0] for i in range(len(path))]
        path_y = [path[i][1] for i in range(len(path))]

        if not flag:
            plt.plot(path_x, path_y, linewidth='3', color='r')
        else:
            plt.plot(path_x, path_y, linewidth='3', color=cl)

        # maybe not necessary
        # plt.plot(self.xI[0], self.xI[1], "bs")  # the starting point
        # plt.plot(self.xG[0], self.xG[1], "gs")  # the goal point

        plt.pause(0.01)
