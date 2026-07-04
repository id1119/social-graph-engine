from pathlib import Path

from SocialGraph import SocialGraph
from User import User


class SocialGraphRepository:
    USERS_FILE = "users.txt"
    CONNECTIONS_FILE = "connections.txt"
    BLOCKED_FILE = "blocked.txt"

    def __init__(self, dataset_dir):
        self.dataset_dir = Path(dataset_dir)

    def load_all(self):
        graph = SocialGraph()
        self._load_users(graph)
        self._load_connections(graph)
        self._load_blocked(graph)
        return graph

    def save_all(self, graph):
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        self._save_users(graph)
        self._save_connections(graph)
        self._save_blocked(graph)

    def _load_users(self, graph):
        with self._path(self.USERS_FILE).open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|", 2)
                if len(parts) != 3:
                    raise ValueError(f"Invalid users.txt line {line_number}: {line}")

                user_id_text, username, bio = parts
                graph.add_user(User(int(user_id_text), username, bio))

    def _load_connections(self, graph):
        with self._path(self.CONNECTIONS_FILE).open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                from_id, to_id = self._parse_id_pair(line, self.CONNECTIONS_FILE, line_number)
                graph.add_follow(from_id, to_id, record_history=False, enforce_blocks=False)

    def _load_blocked(self, graph):
        with self._path(self.BLOCKED_FILE).open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                blocker_id, blocked_id = self._parse_id_pair(line, self.BLOCKED_FILE, line_number)
                graph.add_block(blocker_id, blocked_id)

    def _save_users(self, graph):
        with self._path(self.USERS_FILE).open("w", encoding="utf-8") as file:
            for user_id in sorted(graph.users_by_id):
                user = graph.users_by_id[user_id]
                file.write(f"{user.id}|{user.username}|{user.bio}\n")

    def _save_connections(self, graph):
        with self._path(self.CONNECTIONS_FILE).open("w", encoding="utf-8") as file:
            for from_id in sorted(graph.following):
                for to_id in sorted(graph.following[from_id]):
                    file.write(f"{from_id}|{to_id}\n")

    def _save_blocked(self, graph):
        with self._path(self.BLOCKED_FILE).open("w", encoding="utf-8") as file:
            for blocker_id, blocked_id in sorted(graph.blocked_pairs):
                file.write(f"{blocker_id}|{blocked_id}\n")

    def _path(self, file_name):
        return self.dataset_dir / file_name

    def _parse_id_pair(self, line, file_name, line_number):
        parts = line.split("|")
        if len(parts) != 2:
            raise ValueError(f"Invalid {file_name} line {line_number}: {line}")

        first_id, second_id = parts
        return int(first_id), int(second_id)
