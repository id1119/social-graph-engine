# Social Graph Engine

A Python social-network engine built around directed graphs, ranking, indexed search and personalized recommendation algorithms.

The project loads a social graph once and builds reusable data structures for PageRank, search, autocomplete, multi-hop traversal and recommendations.

## Highlights

- Iterative **PageRank** with damping and dangling-node handling
- **Personalized PageRank** for user-specific relevance
- Hybrid recommendations combining graph relevance and biography similarity
- **Inverted index** for profile-text search
- **Trie-based autocomplete** for usernames
- **BFS traversal** for multi-hop connection discovery
- Ranked username correction suggestions
- Heap-based top-k result selection
- Performance benchmarks across multiple dataset sizes

## Graph model

Users are nodes in a directed graph and follow relationships are directed edges. The graph maintains fast lookup structures for users, outgoing relationships, incoming relationships, out-degree values and relationship constraints.

## PageRank

The implementation uses iterative PageRank with a damping factor of `0.85`, convergence threshold `1e-6`, and redistribution of rank from dangling nodes.

Top users are selected with a heap, avoiding a full sort when only the highest-ranked results are needed.

## Ranked search

Biography terms are normalized and stored in an inverted index:

```text
term -> { user_id, user_id, ... }
```

Search scores username and biography matches, then uses PageRank as an additional ranking signal for similarly relevant results.

## Trie autocomplete

Usernames are inserted into a trie at initialization. Prefix queries traverse directly to the matching trie node, collect candidate users and return the highest-ranked completions according to PageRank.

## Personalized recommendations

Recommendations combine Personalized PageRank with Jaccard similarity between normalized biography word sets:

```text
score = alpha * PersonalizedPageRank
      + (1 - alpha) * JaccardSimilarity
```

The `alpha` parameter controls the balance between graph-based and content-based relevance. Existing relationships and disallowed candidates are removed from the recommendation set.

## Multi-hop traversal

Breadth-First Search explores the graph level by level:

```text
Level 1 -> direct connections
Level 2 -> one intermediary
Level 3 -> two intermediaries
...
```

A visited set ensures each user is processed at most once during a traversal.

## Username suggestions

The project includes a "Did you mean" service that compares an unknown username with existing usernames and ranks the closest candidates, with PageRank available as an additional ordering signal.

## Architecture

```text
User.py                     User model
SocialGraph.py              Directed graph state
SocialGraphRepository.py    Dataset loading
PageRankService.py          Global PageRank
SearchService.py            Inverted-index search
AutocompleteService.py      Trie autocomplete
GraphTraversalService.py    BFS traversal
RecommendationService.py    Personalized recommendations
DidYouMeanService.py        Username suggestions
performance_check.py        Benchmarks
main.py                     Interactive CLI
```

## Dataset format

The application supports `small`, `medium` and `full` datasets. Each dataset contains:

```text
users.txt
connections.txt
blocked.txt
```

with user records, directed follow edges and relationship constraints used by the application.

## Running

Requires Python 3.

```bash
python3 main.py
```

Or choose a dataset explicitly:

```bash
python3 main.py dataset/small
python3 main.py dataset/medium
python3 main.py dataset/full
```

## CLI features

1. Search users
2. Show top PageRank users
3. Add follow relationships
4. Show interaction history
5. Autocomplete usernames
6. Explore connections with BFS
7. Suggest similar usernames
8. Recommend users

## Performance benchmark

```bash
python3 performance_check.py dataset/medium
```

The benchmark measures graph loading, PageRank, index construction, trie construction, search, autocomplete, BFS and recommendation execution.

## What this project demonstrates

- directed graph modeling
- iterative ranking algorithms
- graph traversal
- personalized ranking
- inverted-index information retrieval
- trie-based prefix search
- top-k selection with heaps
- hybrid recommendation systems
- performance-oriented data structures

## Status

Complete algorithms-and-data-structures project maintained as a portfolio implementation of graph search, ranking and recommendation systems.
