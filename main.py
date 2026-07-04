
import sys

from PageRankService import PageRankService
from SocialGraphRepository import SocialGraphRepository


def load_graph(dataset_dir="dataset/small"):
    repository = SocialGraphRepository(dataset_dir)
    return repository.load_all()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        selected_dataset = sys.argv[1]
    else:
        selected_dataset = "dataset/small"

    graph = load_graph(selected_dataset)

    print(f"Loaded dataset: {selected_dataset}")
    print(f"Users: {len(graph.users_by_id)}")
    print(f"Connections: {sum(graph.out_degree.values())}")
    print(f"Blocked relations: {len(graph.blocked_pairs)}")

    page_rank_service = PageRankService(graph)
    page_rank_service.calculate()

    print("\nTop 10 users by PageRank:")
    for position, (user, rank) in enumerate(page_rank_service.top_users(10), start=1):
        print(f"{position}. {user.username} ({user.id}) - {rank:.8f}")
