"""
Env 2D
Copy from
"""


class Env:
    def __init__(self):
        self.x_range = 51
        self.y_range = 31
        self.motions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self) -> set:
        """
        Initialize obstacles' positions
        @rtype: set
        """
        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):
            obs.add((i, 0))  # lower bound
        for i in range(x):
            obs.add((i, y - 1))  # upper bound

        for i in range(y):
            obs.add((0, i))  # left bound
        for i in range(y):
            obs.add((x - 1, i))  # right bound

        for i in range(10, 21):
            obs.add((i, 15))  # wall
        for i in range(15):
            obs.add((20, i))
        for i in range(15, 30):
            obs.add((30, i))
        for i in range(16):
            obs.add((40, i))

        return obs
