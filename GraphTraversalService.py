from collections import deque


class GraphTraversalService:
    def __init__(self, graph):
        self.graph = graph

    def bfs_connections_by_level(self, start_user_id, max_level):
        if start_user_id not in self.graph.users_by_id:
            raise ValueError(f"User with id {start_user_id} does not exist.")

        if max_level < 1:
            return {}

        visited = {start_user_id}
        queue = deque([(start_user_id, 0)])
        levels = {}

        while queue:
            current_user_id, current_level = queue.popleft()

            if current_level == max_level:
                continue

            next_level = current_level + 1

            for followed_user_id in self.graph.following[current_user_id]:
                if followed_user_id in visited:
                    continue

                visited.add(followed_user_id)

                if next_level not in levels:
                    levels[next_level] = []

                levels[next_level].append(followed_user_id)
                queue.append((followed_user_id, next_level))

        return levels
