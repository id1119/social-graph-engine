import heapq


class RecommendationService:
    def __init__(self, graph, user_bio_words):
        self.graph = graph
        self.user_bio_words = user_bio_words

    def recommend(self, user_id, alpha, count=10):
        if user_id not in self.graph.users_by_id:
            raise ValueError(f"User with id {user_id} does not exist.")

        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha must be between 0 and 1.")

        personalized_ranks = self._calculate_personalized_page_rank(user_id)
        candidate_scores = []

        for candidate_id in self.graph.users_by_id:
            if not self._is_valid_candidate(user_id, candidate_id):
                continue

            content_similarity = self._jaccard_similarity(user_id, candidate_id)
            combined_score = (
                alpha * personalized_ranks.get(candidate_id, 0)
                + (1 - alpha) * content_similarity
            )

            candidate_scores.append(
                (
                    candidate_id,
                    combined_score,
                    personalized_ranks.get(candidate_id, 0),
                    content_similarity,
                )
            )

        top_candidates = heapq.nlargest(
            count,
            candidate_scores,
            key=lambda item: item[1],
        )

        return [
            (
                self.graph.users_by_id[candidate_id],
                combined_score,
                personalized_rank,
                content_similarity,
            )
            for candidate_id, combined_score, personalized_rank, content_similarity in top_candidates
        ]

    def _calculate_personalized_page_rank(self, start_user_id, damping_factor=0.85, epsilon=1e-6, max_iterations=100):
        user_ids = list(self.graph.users_by_id.keys())
        user_count = len(user_ids)

        if user_count == 0:
            return {}

        ranks = {user_id: 0 for user_id in user_ids}
        ranks[start_user_id] = 1

        for _ in range(max_iterations):
            dangling_rank_sum = 0

            for user_id in user_ids:
                if self.graph.out_degree[user_id] == 0:
                    dangling_rank_sum += ranks[user_id]

            new_ranks = {user_id: 0 for user_id in user_ids}
            new_ranks[start_user_id] = 1 - damping_factor
            dangling_contribution = damping_factor * dangling_rank_sum / user_count
            max_difference = 0

            for user_id in user_ids:
                new_ranks[user_id] += dangling_contribution

                for follower_id in self.graph.followers[user_id]:
                    new_ranks[user_id] += damping_factor * ranks[follower_id] / self.graph.out_degree[follower_id]

            for user_id in user_ids:
                difference = abs(new_ranks[user_id] - ranks[user_id])
                if difference > max_difference:
                    max_difference = difference

            ranks = new_ranks

            if max_difference < epsilon:
                break

        return ranks

    def _jaccard_similarity(self, first_user_id, second_user_id):
        first_words = self.user_bio_words.get(first_user_id, set())
        second_words = self.user_bio_words.get(second_user_id, set())

        if not first_words and not second_words:
            return 0

        union_size = len(first_words | second_words)
        if union_size == 0:
            return 0

        intersection_size = len(first_words & second_words)
        return intersection_size / union_size

    def _is_valid_candidate(self, user_id, candidate_id):
        if candidate_id == user_id:
            return False

        if candidate_id in self.graph.following[user_id]:
            return False

        if self.graph.is_blocked_between(user_id, candidate_id):
            return False

        return True
