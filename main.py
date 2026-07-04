import sys

from AutocompleteService import AutocompleteService
from DidYouMeanService import DidYouMeanService
from GraphTraversalService import GraphTraversalService
from PageRankService import PageRankService
from RecommendationService import RecommendationService
from SearchService import SearchService
from SocialGraphRepository import SocialGraphRepository


def load_graph(dataset_dir="dataset/small"):
    repository = SocialGraphRepository(dataset_dir)
    return repository.load_all()


def choose_dataset():
    print("Choose dataset")
    print("1. small")
    print("2. medium")
    print("3. full")
    print("4. custom path")

    while True:
        option = input("Dataset option: ").strip()

        if option == "1":
            return "dataset/small"
        if option == "2":
            return "dataset/medium"
        if option == "3":
            return "dataset/full"
        if option == "4":
            return input("Dataset path: ").strip()

        print("Unknown dataset option.")


def print_menu():
    print("\nMenu")
    print("1. Search users")
    print("2. Show top PageRank users")
    print("3. Add follow relation")
    print("4. Show interaction history")
    print("5. Autocomplete usernames")
    print("6. BFS connections by level")
    print("7. Did you mean username")
    print("8. Recommend users")
    print("0. Exit")


def search_users(search_service):
    query = input("Search query: ").strip()
    results = search_service.search(query, 10)

    if not results:
        print("No users found.")
        return

    for position, (user, score, rank) in enumerate(results, start=1):
        print(f"{position}. {user.username} ({user.id}) - score={score}, pagerank={rank:.8f}")


def show_top_users(page_rank_service):
    count = read_int("How many users to show: ")

    for position, (user, rank) in enumerate(page_rank_service.top_users(count), start=1):
        print(f"{position}. {user.username} ({user.id}) - pagerank={rank:.8f}")


def add_follow_relation(graph, page_rank_service):
    from_id = read_int("Follower user id: ")
    to_id = read_int("Followed user id: ")

    try:
        added = graph.add_follow(from_id, to_id)
    except ValueError as error:
        print(error)
        return False

    if not added:
        print("Follow relation already exists.")
        return False

    page_rank_service.calculate()
    print("Follow relation added. PageRank recalculated.")
    return True


def show_interaction_history(graph):
    user_id = read_int("User id: ")

    try:
        history = graph.get_interaction_history(user_id)
    except ValueError as error:
        print(error)
        return

    if not history:
        print("No new interactions recorded for this user.")
        return

    for interaction in history:
        from_user = graph.users_by_id[interaction["from_id"]]
        to_user = graph.users_by_id[interaction["to_id"]]

        if interaction["from_id"] == user_id:
            print(f'{interaction["sequence"]}. followed {to_user.username} ({to_user.id})')
        else:
            print(f'{interaction["sequence"]}. followed by {from_user.username} ({from_user.id})')


def autocomplete_usernames(autocomplete_service):
    prefix = input("Username prefix: ").strip()
    results = autocomplete_service.autocomplete(prefix, 10)

    if not results:
        print("No autocomplete results.")
        return

    for position, (user, rank) in enumerate(results, start=1):
        print(f"{position}. {user.username} ({user.id}) - pagerank={rank:.8f}")


def show_bfs_connections(traversal_service):
    start_user_id = read_int("Start user id: ")
    max_level = read_int("Max level: ")

    try:
        levels = traversal_service.bfs_connections_by_level(start_user_id, max_level)
    except ValueError as error:
        print(error)
        return

    if not levels:
        print("No reachable users found for the selected level.")
        return

    for level in sorted(levels):
        print(f"\nLevel {level}:")
        for user_id in levels[level]:
            user = traversal_service.graph.users_by_id[user_id]
            print(f"- {user.username} ({user.id})")


def show_did_you_mean_suggestions(did_you_mean_service):
    username = input("Username: ").strip()
    suggestions = did_you_mean_service.suggest(username, 5)

    if not suggestions:
        print("No suggestions found.")
        return

    for position, (user, similarity, rank) in enumerate(suggestions, start=1):
        print(
            f"{position}. {user.username} ({user.id}) "
            f"- similarity={similarity:.3f}, pagerank={rank:.8f}"
        )


def show_recommendations(recommendation_service):
    user_id = read_int("User id: ")
    alpha = read_float("Alpha [0-1]: ")
    count = read_int("How many recommendations to show: ")

    try:
        recommendations = recommendation_service.recommend(user_id, alpha, count)
    except ValueError as error:
        print(error)
        return

    if not recommendations:
        print("No recommendations found.")
        return

    for position, (user, score, ppr, similarity) in enumerate(recommendations, start=1):
        print(
            f"{position}. {user.username} ({user.id}) "
            f"- score={score:.8f}, ppr={ppr:.8f}, bio_similarity={similarity:.8f}"
        )


def read_int(prompt):
    while True:
        value = input(prompt).strip()

        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


def read_float(prompt):
    while True:
        value = input(prompt).strip()

        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def run_application(dataset_dir):
    graph = load_graph(dataset_dir)
    page_rank_service = PageRankService(graph)
    page_rank_service.calculate()
    search_service = SearchService(graph, page_rank_service.ranks)
    autocomplete_service = AutocompleteService(graph, page_rank_service.ranks)
    traversal_service = GraphTraversalService(graph)
    did_you_mean_service = DidYouMeanService(graph, page_rank_service.ranks)
    recommendation_service = RecommendationService(graph, search_service.user_bio_words)

    print(f"Loaded dataset: {dataset_dir}")
    print(f"Users: {len(graph.users_by_id)}")
    print(f"Connections: {sum(graph.out_degree.values())}")
    print(f"Blocked relations: {len(graph.blocked_pairs)}")

    while True:
        print_menu()
        option = input("Choose option: ").strip()

        if option == "1":
            search_users(search_service)
        elif option == "2":
            show_top_users(page_rank_service)
        elif option == "3":
            graph_changed = add_follow_relation(graph, page_rank_service)
            if graph_changed:
                search_service = SearchService(graph, page_rank_service.ranks)
                autocomplete_service = AutocompleteService(graph, page_rank_service.ranks)
                did_you_mean_service = DidYouMeanService(graph, page_rank_service.ranks)
                recommendation_service = RecommendationService(graph, search_service.user_bio_words)
        elif option == "4":
            show_interaction_history(graph)
        elif option == "5":
            autocomplete_usernames(autocomplete_service)
        elif option == "6":
            show_bfs_connections(traversal_service)
        elif option == "7":
            show_did_you_mean_suggestions(did_you_mean_service)
        elif option == "8":
            show_recommendations(recommendation_service)
        elif option == "0":
            print("Goodbye.")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        selected_dataset = sys.argv[1]
    else:
        selected_dataset = choose_dataset()

    run_application(selected_dataset)
