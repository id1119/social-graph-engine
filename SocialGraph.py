class SocialGraph:
    def __init__(self):
        self.users_by_id = {}
        self.users_by_username = {}
        self.following = {}
        self.followers = {}
        self.out_degree = {}
        self.blocked_by_user = {}
        self.blocked_pairs = set()
        self.following_history = {}
        self.follower_history = {}
        self._interaction_sequence = 0

    def add_user(self, user):
        self.users_by_id[user.id] = user
        self.users_by_username[user.username.lower()] = user
        self.following[user.id] = set()
        self.followers[user.id] = set()
        self.out_degree[user.id] = 0
        self.blocked_by_user[user.id] = set()
        self.following_history[user.id] = []
        self.follower_history[user.id] = []

    def add_follow(self, from_id, to_id, record_history=True, enforce_blocks=True):
        if from_id not in self.users_by_id:
            raise ValueError(f"User with id {from_id} does not exist.")

        if to_id not in self.users_by_id:
            raise ValueError(f"User with id {to_id} does not exist.")

        if from_id == to_id:
            raise ValueError("User cannot follow itself.")

        if enforce_blocks and self.is_blocked_between(from_id, to_id):
            raise ValueError("Follow relation is not allowed because blocking exists between users.")

        if to_id in self.following[from_id]:
            return False

        self.following[from_id].add(to_id)
        self.followers[to_id].add(from_id)
        self.out_degree[from_id] += 1

        if record_history:
            self._record_follow_interaction(from_id, to_id)

        return True

    def add_block(self, blocker_id, blocked_id):
        if blocker_id not in self.users_by_id:
            raise ValueError(f"User with id {blocker_id} does not exist.")

        if blocked_id not in self.users_by_id:
            raise ValueError(f"User with id {blocked_id} does not exist.")

        if blocker_id == blocked_id:
            raise ValueError("User cannot block itself.")

        if blocked_id in self.blocked_by_user[blocker_id]:
            return False

        self.blocked_by_user[blocker_id].add(blocked_id)
        self.blocked_pairs.add((blocker_id, blocked_id))
        return True

    def is_blocked_between(self, first_user_id, second_user_id):
        return (
            (first_user_id, second_user_id) in self.blocked_pairs
            or (second_user_id, first_user_id) in self.blocked_pairs
        )

    def get_interaction_history(self, user_id):
        if user_id not in self.users_by_id:
            raise ValueError(f"User with id {user_id} does not exist.")

        history = self.following_history[user_id] + self.follower_history[user_id]
        return sorted(history, key=lambda interaction: interaction["sequence"])

    def _record_follow_interaction(self, from_id, to_id):
        self._interaction_sequence += 1
        interaction = {
            "sequence": self._interaction_sequence,
            "from_id": from_id,
            "to_id": to_id,
        }

        self.following_history[from_id].append(interaction)
        self.follower_history[to_id].append(interaction)
