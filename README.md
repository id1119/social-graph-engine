# Social Graph Engine

A Python social-network simulation built around directed graphs, search, ranking and recommendation algorithms.

The project models users as graph nodes and follow relationships as directed edges, then layers discovery features on top of that graph: PageRank, search, autocomplete, graph traversal and personalized recommendations.

## Highlights

- Iterative **PageRank** with dangling-node handling
- **Personalized PageRank** for user-specific recommendations
- Hybrid recommendation score combining PPR and biography similarity
- **Inverted index** for user/bio search
- **Trie-based autocomplete** for usernames
- **BFS traversal** for multi-hop connection discovery
- "Did you mean" username suggestions
- Follow/block relationship management
- Performance benchmarks across multiple dataset sizes

## Architecture

The project separates graph storage from the services that operate on it:

```text
SocialGraph.py               # Graph state and relationships
SocialGraphRepository.py     # Dataset loading
PageRankService.py           # Global ranking
SearchService.py             # Indexed search
AutocompleteService.py       # Trie autocomplete
GraphTraversalService.py     # BFS traversal
RecommendationService.py     # Personalized recommendations
DidYouMeanService.py         # Fuzzy username suggestions
performance_check.py         # Benchmarks
main.py                      # Interactive CLI
```

## Recommendation model

Recommendations combine graph structure with profile similarity:

```text
score = alpha * PersonalizedPageRank + (1 - alpha) * content_similarity
```

Content similarity is based on Jaccard similarity between user biographies. Existing follows, blocked users and the current user are filtered from the candidate set.

## Running the project

```bash
python3 main.py
```

Or select a dataset directly:

```bash
python3 main.py dataset/small
python3 main.py dataset/medium
python3 main.py dataset/full
```

Each dataset contains:

```text
users.txt
connections.txt
blocked.txt
```

## Features available from the CLI

1. Search users
2. Show top PageRank users
3. Add follow relationships
4. Show interaction history
5. Autocomplete usernames
6. Explore connections with BFS
7. Suggest similar usernames
8. Recommend users

## Performance

The implementation includes a benchmark script for graph loading, PageRank, index construction, autocomplete, BFS and recommendations:

```bash
python3 performance_check.py dataset/medium
```

The repository includes datasets ranging from thousands to tens of thousands of users, making it useful for comparing how the algorithms scale.

## Tech stack

- Python
- Graph algorithms
- PageRank / Personalized PageRank
- Trie
- BFS
- Inverted indexes
- Heap-based top-k selection

## Status

Academic algorithm/data-structures project, maintained as a portfolio implementation of graph-based search and recommendation systems.
