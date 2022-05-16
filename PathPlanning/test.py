from PathPlanning import plotting
import matplotlib.pyplot as plt
import heapq
if __name__ == "__main__":
    # s_start = (5, 5)
    # s_goal = (45, 25)
    # plot = plotting.Plotting(s_start, s_goal)
    # plot.plot_grid("BFS")
    # plt.show(block=False)
    # plt.pause(1)
    # plt.cla()
    # plot.obs.clear()
    # plot.plot_grid("BFS")
    # plt.show()
    tt = [(5,2), (1,4),(5,7),(4,2)]
    print(tt)
    heapq.heapify(tt)
    print(tt)
    # a, s = heapq.heappop(tt)
    heapq.heappush(tt, (3,3))
    print(tt)