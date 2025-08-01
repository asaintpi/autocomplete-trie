"""
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

# =============================================================
# My original obvious (but slow) brute force approach
# =============================================================

class BruteForceAutocomplete:
    """
    This is as close to what I mapped out first as I can recall. It works, but it's not good.
    You place everything into a list and scan the whole thing every
    single time. Good for a baseline, but that's about it, not efficent at all. Requires Trie Solution.
    """
    def __init__(self):
        self.phrases = []
        self.maxLen = 0

    def add_phrase(self, phrase: str, score: int):
        # O(1)  
        self.phrases.append((score, phrase))
        self.maxLen = max(self.maxLen, len(phrase))

    def get_top_k(self, prefix: str, k: int) -> list[str]:
        # Here we touched every single item, N
        # then sort whatever matches M 
        # O(N*P + M*logM). Entirely inefficient.
        preLen = len(prefix)
        matching_phrases = []
        
        if preLen > self.maxLen:
            return matching_phrases
            
        for score, phrase in self.phrases:
            if phrase[:preLen]:
                matching_phrases.append((score, phrase))

        matching_phrases.sort(key=lambda x: x[0]).reverse()
        return [phrase for score, phrase in matching_phrases[:k]]


# ==============================================================================
# The optimal solution - Using Trie + Heap now
# ==============================================================================

class TrieNode:
    """
    The node for the prefix tree. The 'children' dict is standard Trie implementation.
    The 'top_k_heap' is the big idea I learned from this.
    """
    def __init__(self):
        self.children = {}
        # The aha! moment was realizing I could store the best K results
        # at *every* node with a min heap
        self.top_k_heap = []

class AutocompleteSystem:
    """
    Combining the Trie and heap logic.
    The whole design here is to do the hard work on insertion  
    so that retrieval is insanely fast.
    """
    def __init__(self, k_limit: int = 10):
        self.root = TrieNode()
        self.k_limit = k_limit

    def add_phrase(self, phrase: str, score: int):
        """
        This is where the magic happened in my learnings, as we add a phrase, we update the
        heaps all the way down the tree.

        O(L * logK). For each character, L, we do one heap
        operation, logK. This is the trade off for more efficient gets.
        """
        node = self.root
        item = (score, phrase)

        for char in phrase:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            if len(node.top_k_heap) < self.k_limit:
                heapq.heappush(node.top_k_heap, item)
            # heappushpop is an efficient way to add the new item and kick out the smallest one if needed I learned.
            else:
                heapq.heappushpop(node.top_k_heap, item)

    def get_top_k(self, prefix: str) -> list[str]:
        """
        Retrieves the top K phrases. This part is dirt cheap because the
        heavy lifting is already done.

        O(P + K*logK). Go through prefix and sort the K
        results from the heap, instant.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return [] 
            node = node.children[char]

        sorted_results = sorted(node.top_k_heap, key=lambda x: x[0], reverse=True) # corrected how I perform my reverse on sorts
        return [phrase for score, phrase in sorted_results]

# =======================================================================
# Basic test cases
# =======================================================================

if __name__ == "__main__":
    # tests to make sure everything was functional.
    K = 3
    system = AutocompleteSystem(K)

    phrases_to_add = [
        ("tape", 100), ("tape api", 95), ("tape grid", 98),
        ("technical debt", 50), ("trie", 80), ("trie implementation", 85),
        ("system design", 90), ("tap water", 10),
    ]
    for phrase, score in phrases_to_add:
        system.add_phrase(phrase, score)

    test_cases = {
        "tap": ['tape', 'tape grid', 'tapeapi'],
        "trie": ['trie implementation', 'trie'],
        "tape grid": ['tape grid'],
        "nonexistent": [],
        "": ['tape', 'tape grid', 'system design'],
    }

    all_passed = True
    for i, (prefix, expected) in enumerate(test_cases.items()):
        actual = system.get_top_k(prefix)
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        try:
            assert actual == expected
            print("Test PASSED!")
        except AssertionError:
            print("Test FAILED!!")
            all_passed = False

    print("\n" + ("All test cases passed successfully." if all_passed else "Some tests failed."))

# ==============================================================================
# Section 4: Resources & Learnings
#
# A list of the resources I used to get up to speed. My first task was understanding/implementing a Trie regularly first.
# ==============================================================================
#
# 1. Conceptual Foundations:
#    - Trie Visualization (NeetCode): https://www.youtube.com/watch?v=oobqoCJlHA0
#      (Great for me for the initial mental model of the structure.)
#
# 2. Implementation & Design Patterns:
#    - Python Trie Implementation Guide (GeeksforGeeks): https://www.geeksforgeeks.org/trie-insert-and-search/
#      (Used this as a baseline for the basic node/insert/search logic.)
#    - LeetCode "Design Search Autocomplete System" Discussion:
#      https://leetcode.com/problems/design-search-autocomplete-system/solutions/105374/python-solution-with-trie-and-heap/
#      (This was the key. Seeing a practical example of augmenting each Trie
#      node with another data structure was the breakthrough for the design.)
#
