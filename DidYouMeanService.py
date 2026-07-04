from difflib import SequenceMatcher


class DidYouMeanService:
    def __init__(self, graph, page_ranks):
        self.graph = graph
        self.page_ranks = page_ranks

    def suggest(self, username, count=5):
        normalized_username = username.lower().strip()
        if not normalized_username:
            return []

        if normalized_username in self.graph.users_by_username:
            user = self.graph.users_by_username[normalized_username]
            return [(user, 1.0, self.page_ranks.get(user.id, 0))]

        suggestions = []

        for existing_username, user in self.graph.users_by_username.items():
            similarity = SequenceMatcher(None, normalized_username, existing_username).ratio()

            if similarity > 0:
                suggestions.append((user, similarity, self.page_ranks.get(user.id, 0)))

        suggestions.sort(key=lambda item: (item[1], item[2]), reverse=True)
        return suggestions[:count]
