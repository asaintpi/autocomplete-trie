"""
An implementation of a high performance autocomplete system.

This whole thing started with a problem from a technical discussion that I
couldn't get out of my head. We talked through a simple brute force approach
and even coded it out, but it was obviously not going to scale.

I was aware the solution was a Trie but I was unfamiliar with it at that moment.
My curiosity got the better of me, so I spent the evening diving into the
optimal Trie based solution we theorized about. This file is the result of that
obsession, my journey from the simple, slow approach to a design I'm actually
proud of.

Author: Arnaud
Date: July 31, 2025
"""

import heapq

# ==============================================================================
# 1: The Obvious (But slow) Brute Force Approach
# ==============================================================================

class BruteForceAutocomplete:
    """
    This is as close to what I mapped out first as I can recall. It works, but it's not good.
    You place everything into a list and scan the whole thing every
    single time. Good for a baseline, but that's about it, but not efficent at all. Requires Trie Solution.
    """
    def __init__(self):
        self.phrases = []

    def add_phrase(self, phrase: str, score: int):
        # O(1) to add  
        self.phrases.append((score, phrase))

    def get_top_k(self, prefix: str, k: int) -> list[str]:
        # Performance killer. You have to touch every single item, N,
        # then sort whatever matches M. O(N*P + M*logM). Entirely inefficient.
        matching_phrases = []
        for score, phrase in self.phrases:
            if phrase.startswith(prefix):
                matching_phrases.append((score, phrase))

        matching_phrases.sort(key=lambda x: x[0], reverse=True)
        return [phrase for score, phrase in matching_phrases[:k]]


# ==============================================================================
# 2: The Optimal Solution - Trie + Heap
# ==============================================================================

class TrieNode:
    """
    The node for the prefix tree. The 'children' dict is standard Trie implementation.
    The 'top_k_heap' is the big idea I learned from this.
    """
    def __init__(self):
        self.children = {}
        # The aha! moment was realizing I could store the best K results
        # at *every* node. A min heap is perfect for this - it lets me
        # track the "top" scores by only caring about the current smallest.
        self.top_k_heap = []

class AutocompleteSystem:
    """
    The main class. Combines the Trie and heap logic.
    The whole design philosophy here is to do the hard work on insertion  
    so that retrieval is insanely fast.
    """
    def __init__(self, k_limit: int = 10):
        self.root = TrieNode()
        self.k_limit = k_limit

    def add_phrase(self, phrase: str, score: int):
        """
        This is where the magic happened in my learnings. As we add a phrase, we update the
        heaps all the way down the tree.

        Complexity: O(L * logK). For each character, L, we do one heap
        operation, logK. This is the trade off for more efficient gets.
        """
        node = self.root
        item = (score, phrase)

        for char in phrase:
            # Standard Trie traversal/creation.
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

            # Now, we update the heap at this node.
            # If the heap isn't full, just toss the new item in.
            if len(node.top_k_heap) < self.k_limit:
                heapq.heappush(node.top_k_heap, item)
            # If the heap is full, heappushpop is an efficient way to
            # add the new item and kick out the smallest one if needed I learned.
            else:
                heapq.heappushpop(node.top_k_heap, item)

    def get_top_k(self, prefix: str) -> list[str]:
        """
        Retrieves the top K phrases. This part is dirt cheap because the
        heavy lifting is already done.

        Complexity: O(P + K*logK). Walk the prefix (P), then sort the K
        results from the heap. Basically instant.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return [] # Nothing: Prefix doesn't exist 
            node = node.children[char]

        # The heap has our top K, but they're not sorted. A final sort gives
        # us the nice descending order for the final output.
        sorted_results = sorted(node.top_k_heap, key=lambda x: x[0], reverse=True)
        return [phrase for score, phrase in sorted_results]

# ==============================================================================
# Section 3: Sanity Checks
# ==============================================================================

if __name__ == "__main__":
    # tests to make sure everything was functional.
    K = 3
    system = AutocompleteSystem(k_limit=K)

    print(f"\nAdding phrases with a top-K limit of {K}...")
    phrases_to_add = [
        ("tapestry", 100), ("tapestry api", 95), ("tapestry grid", 98),
        ("technical debt", 50), ("trie", 80), ("trie implementation", 85),
        ("system design", 90), ("tap water", 10),
    ]
    for phrase, score in phrases_to_add:
        system.add_phrase(phrase, score)
    print("Finished adding phrases.")

    # --- Test cases ---
    test_cases = {
        "tap": ['tapestry', 'tapestry grid', 'tapestry api'],
        "trie": ['trie implementation', 'trie'],
        "tapestry grid": ['tapestry grid'],
        "nonexistent": [],
        "": ['tapestry', 'tapestry grid', 'system design'],
    }

    all_passed = True
    for i, (prefix, expected) in enumerate(test_cases.items()):
        print(f"\n--- Test Case {i+1}: get_top_k('{prefix}') ---")
        actual = system.get_top_k(prefix)
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        try:
            assert actual == expected
            print("Test PASSED.")
        except AssertionError:
            print("Test FAILED.")
            all_passed = False

    print("\n" + ("All test cases passed successfully." if all_passed else "Some tests failed."))

# ==============================================================================
# Section 4: Resources & Learnings
#
# A list of the resources I used to get up to speed.
# ==============================================================================
#
# 1. Conceptual Foundations:
#    - Trie Visualization (NeetCode): https://www.youtube.com/watch?v=oobqoCJlHA0
#      (Great for the initial mental model of the structure.)
#
# 2. Implementation & Design Patterns:
#    - Python Trie Implementation Guide (GeeksforGeeks): https://www.geeksforgeeks.org/trie-insert-and-search/
#      (Used this as a baseline for the basic node/insert/search logic.)
#    - LeetCode "Design Search Autocomplete System" Discussion:
#      https://leetcode.com/problems/design-search-autocomplete-system/solutions/105374/python-solution-with-trie-and-heap/
#      (This was the key. Seeing a practical example of augmenting each Trie
#      node with another data structure was the breakthrough for the design.)
#
