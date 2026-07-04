import heapq
import re
from collections import Counter


class SearchService:
    def __init__(self, graph, page_ranks):
        self.graph = graph
        self.page_ranks = page_ranks
        self.inverted_index = {}
        self.user_bio_words = {}
        self._build_inverted_index()

    def search(self, query, count=10):
        query_words = self._process_text(query)
        if not query_words:
            return []

        scores_by_user_id = Counter()

        self._add_username_matches(query, query_words, scores_by_user_id)
        self._add_bio_matches(query_words, scores_by_user_id)

        top_items = heapq.nlargest(
            count,
            scores_by_user_id.items(),
            key=lambda item: (item[1], self.page_ranks.get(item[0], 0)),
        )

        return [
            (self.graph.users_by_id[user_id], score, self.page_ranks.get(user_id, 0))
            for user_id, score in top_items
        ]

    def _build_inverted_index(self):
        for user in self.graph.users_by_id.values():
            words = set(self._process_text(user.bio))
            self.user_bio_words[user.id] = words

            for word in words:
                if word not in self.inverted_index:
                    self.inverted_index[word] = set()

                self.inverted_index[word].add(user.id)

    def _add_username_matches(self, query, query_words, scores_by_user_id):
        normalized_query = query.lower().strip()

        for username, user in self.graph.users_by_username.items():
            if normalized_query == username:
                scores_by_user_id[user.id] += 100
            elif normalized_query in username:
                scores_by_user_id[user.id] += 50

            for word in query_words:
                if word in username:
                    scores_by_user_id[user.id] += 5

    def _add_bio_matches(self, query_words, scores_by_user_id):
        for word in query_words:
            for user_id in self.inverted_index.get(word, set()):
                scores_by_user_id[user_id] += 1

    def _process_text(self, text):
        return re.findall(r"[a-z0-9_]+", text.lower())
