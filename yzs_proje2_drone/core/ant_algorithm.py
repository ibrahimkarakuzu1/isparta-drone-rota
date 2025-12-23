# core/ant_algorithm.py
import numpy as np

class AntColonyOptimizer:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances + 1e-10
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = list(range(len(distances)))
        self.n_ants = int(n_ants)
        self.n_best = int(n_best)
        self.n_iterations = int(n_iterations)
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        history = []
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=all_time_shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay
            history.append(all_time_shortest_path[1])
        return all_time_shortest_path, history

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def pick_move(self, pheromone, dist, visited):
        try:
            pheromone = np.copy(pheromone)
            pheromone[list(visited)] = 0
            row = (pheromone ** self.alpha) * ((1.0 / dist) ** self.beta)
            row[np.isnan(row)] = 0
            row[np.isinf(row)] = 0
            if row.sum() == 0: return self._random_pick(visited)
            norm_row = row / row.sum()
            return np.random.choice(self.all_inds, 1, p=norm_row)[0]
        except:
            return self._random_pick(visited)

    def _random_pick(self, visited):
        unvisited = [i for i in self.all_inds if i not in visited]
        if not unvisited: return self.all_inds[0]
        return np.random.choice(unvisited)