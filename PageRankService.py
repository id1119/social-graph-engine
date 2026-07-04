import heapq


class PageRankService:
    def __init__(self, graph):
        self.graph = graph
        self.ranks = {}

    def calculate(self, damping_factor=0.85, epsilon=1e-6, max_iterations=100):
        user_ids = list(self.graph.users_by_id.keys())
        user_count = len(user_ids)

        if user_count == 0:
            self.ranks = {}
            return self.ranks

        if not self.ranks:
            self.ranks = {user_id: 1 / user_count for user_id in user_ids}

        base_rank = (1 - damping_factor) / user_count

        for _ in range(max_iterations):
            dangling_rank_sum = self._calculate_dangling_rank_sum()
            dangling_contribution = damping_factor * dangling_rank_sum / user_count
            new_ranks = {}
            max_difference = 0

            for user_id in user_ids:
                rank_from_followers = 0

                for follower_id in self.graph.followers[user_id]:
                    rank_from_followers += self.ranks[follower_id] / self.graph.out_degree[follower_id]

                new_rank = base_rank + dangling_contribution + damping_factor * rank_from_followers
                new_ranks[user_id] = new_rank

                difference = abs(new_rank - self.ranks[user_id])
                if difference > max_difference:
                    max_difference = difference

            self.ranks = new_ranks

            if max_difference < epsilon:
                break

        return self.ranks

    def top_users(self, count=10):
        if not self.ranks:
            self.calculate()

        top_items = heapq.nlargest(count, self.ranks.items(), key=lambda item: item[1])
        return [
            (self.graph.users_by_id[user_id], rank)
            for user_id, rank in top_items
        ]

    def _calculate_dangling_rank_sum(self):
        total = 0

        for user_id, out_degree in self.graph.out_degree.items():
            if out_degree == 0:
                total += self.ranks[user_id]

        return total
