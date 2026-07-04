import heapq


class TrieNode:
    def __init__(self):
        self.children = {}
        self.user_id = None


class AutocompleteService:
    def __init__(self, graph, page_ranks):
        self.graph = graph
        self.page_ranks = page_ranks
        self.root = TrieNode()
        self._build_trie()

    def autocomplete(self, prefix, count=10):
        normalized_prefix = prefix.lower().strip()
        if not normalized_prefix:
            return []

        node = self._find_node(normalized_prefix)
        if node is None:
            return []

        user_ids = []
        self._collect_user_ids(node, user_ids)

        top_user_ids = heapq.nlargest(
            count,
            user_ids,
            key=lambda user_id: self.page_ranks.get(user_id, 0),
        )

        return [
            (self.graph.users_by_id[user_id], self.page_ranks.get(user_id, 0))
            for user_id in top_user_ids
        ]

    def _build_trie(self):
        for user in self.graph.users_by_id.values():
            self._insert(user.username, user.id)

    def _insert(self, username, user_id):
        node = self.root

        for character in username.lower():
            if character not in node.children:
                node.children[character] = TrieNode()

            node = node.children[character]

        node.user_id = user_id

    def _find_node(self, prefix):
        node = self.root

        for character in prefix:
            if character not in node.children:
                return None

            node = node.children[character]

        return node

    def _collect_user_ids(self, node, user_ids):
        if node.user_id is not None:
            user_ids.append(node.user_id)

        for child in node.children.values():
            self._collect_user_ids(child, user_ids)
