"""
A* 2D
From github
"""

from PathPlanning import plotting, env
import math
import heapq

class AStar:
    """
    AStar set the cost + heuristics as the priority
    """
    def __init__(self, s_start: tuple, s_goal: tuple, heuristic_type):
        self.s_start = s_start
        self.s_goal = s_goal
        self.heuristic_type = heuristic_type

        self.Env = env.Env()

        self.u_set = self.Env.motions  # action space
        self.obs = self.Env.obs  # position of obstacles

        self.OPEN = []  # priority queue
        self.CLOSED = []  # visited order
        self.PARENT = dict()  # recorded node relations: {'child_node', parent_node}
        self.g = dict()  # cost

    def searchingo(self):
        """
        A_star Searching.
        :return: path, visited order
        """

        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN,
                       (self.f_value(self.s_start), self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:  # stop condition
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]:  # conditions for updating Cost
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (self.f_value(s_n), s_n))

        return self.extract_path(self.PARENT), self.CLOSED

    def searching(self):
        """
        A_star searching
        @return:
        """
        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN, (self.f_value(self.s_start), self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]:
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (self.f_value(s_n), s_n))

        return self.extract_path(self.PARENT), self.CLOSED

    def get_neighbor(self, s: tuple):
        return [(s[0] + u[0], s[1] + u[1]) for u in self.u_set]

    def cost(self, current_state, next_sate):
        if self.is_collisions(current_state, next_sate):
            return math.inf

        diff_x = next_sate[0] - current_state[0]
        diff_y = next_sate[1] - current_state[1]
        return math.hypot(diff_x, diff_y)

    def is_collisions(self, s_start, s_end):
        """
        check if the movement collision with env
        @param s_start:
        @param s_end:
        @return:
        """
        if s_start in self.obs or s_end in self.obs:
            return True
        if s_start[0] != s_end[0] and s_start[1] != s_end[1]:
            if s_end[0] - s_start[0] == s_start[1] - s_end[1]:
                s1 = (min(s_start[0], s_end[0]), min(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
            else:
                s1 = (min(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), min(s_start[1], s_end[1]))

            if s1 in self.obs or s2 in self.obs:
                return True
        return False

    def extract_path(self, parent):
        """
        extract the optimal path from self.PARENT
        @param parent:
        @return: a list contains each node
        """
        path = [self.s_goal]
        s = self.s_goal
        while True:
            s = parent[s]
            path.append(s)

            if s == self.s_start:
                break
        return list(path)

    def f_value(self, s):
        """
        f = g + h
        @param s:
        @return:
        """
        return self.g[s] + self.heuristic(s)

    def heuristic(self, s):
        """
        Calculate heuristic
        @param s: current state [x, y]
        @return: heuristic value
        """
        diff_x = self.s_goal[0] - s[0]
        diff_y = self.s_goal[1] - s[1]
        if self.heuristic_type == "manhattan":
            return abs(diff_x) + abs(diff_y)
        else:
            return math.sqrt(diff_x ** 2 + diff_y ** 2)

if __name__ == "__main__":
    s_start = (5, 5)
    s_goal = (42, 25)

    astar = AStar(s_start, s_goal, "euclidean")
    plot = plotting.Plotting(s_start, s_goal)

    path, visited = astar.searching()
    plot.animation(path, visited, "A*")
