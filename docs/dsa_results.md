
# Data Structures & Algorithms (DSA) Comparison Results

## Results
We conducted a comparison between **Linear Search** and **Dictionary Lookup** to determine the efficiency of searching for transactions by ID. The results are as follows:

- **Linear Search Time:** 0.002861 milliseconds
- **Dictionary Lookup Time:** 0.001192 milliseconds
- **Comparison:** Dictionary Lookup is **2.40 times faster** than Linear Search for this test.

## Reflection
### Why is Dictionary Lookup Faster?
We observed that dictionary lookup is faster because it uses a hash table to directly access the transaction by its key (`transaction_id`), resulting in an average time complexity of **O(1)**. In contrast, linear search scans each transaction sequentially, resulting in a time complexity of **O(n)**.

### Alternative Data Structures
We considered other data structures that could be useful in different scenarios:
- **Binary Search Tree (BST):** If transaction IDs were sorted, a BST could provide a search time of **O(log n)**.
- **Trie:** If transaction IDs had common prefixes, a trie could be used for efficient prefix-based searches.
