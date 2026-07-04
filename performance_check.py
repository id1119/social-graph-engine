import sys
import time

from AutocompleteService import AutocompleteService
from GraphTraversalService import GraphTraversalService
from PageRankService import PageRankService
from RecommendationService import RecommendationService
from SearchService import SearchService
from SocialGraphRepository import SocialGraphRepository


def measure(label, function):
    start = time.perf_counter()
    result = function()
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.4f}s")
    return result


def run(dataset_dir):
    graph = measure("load_graph", lambda: SocialGraphRepository(dataset_dir).load_all())
    print(f"users: {len(graph.users_by_id)}")
    print(f"connections: {sum(graph.out_degree.values())}")
    print(f"blocked_relations: {len(graph.blocked_pairs)}")

    page_rank_service = PageRankService(graph)
    ranks = measure("pagerank", page_rank_service.calculate)
    print(f"pagerank_sum: {sum(ranks.values()):.12f}")

    search_service = measure("build_search_index", lambda: SearchService(graph, ranks))
    autocomplete_service = measure("build_trie", lambda: AutocompleteService(graph, ranks))
    traversal_service = GraphTraversalService(graph)
    recommendation_service = RecommendationService(graph, search_service.user_bio_words)

    measure("search_query", lambda: search_service.search("guildwars", 10))
    measure("autocomplete_query", lambda: autocomplete_service.autocomplete("g", 10))
    measure("bfs_level_2", lambda: traversal_service.bfs_connections_by_level(1, 2))
    measure("recommendations", lambda: recommendation_service.recommend(1, 0.7, 5))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        selected_dataset = sys.argv[1]
    else:
        selected_dataset = "dataset/small"

    run(selected_dataset)
