# Autocomplete System: Brute Force vs Trie + Heap

This repo contains my full implementation of a high performance autocomplete system, born from a fascinating technical problem I encountered.

**Story:**  
I had discussed and coded up a brute force solution for this, which worked but clearly wouldn’t scale. I suspected a Trie would be the right way but hadn’t built one before. After the call, I spent the evening reading up, experimenting, and ultimately implementing a production ready Trie based solution, with a min heap at each node for efficient top K prefix queries.

**What you’ll find here:**
- The brute force approach (as close as possible to what I built initially).
- The final Trie+heap solution, written and debugged from scratch.
- A full test suite with clear, realistic test cases.
- Comments and resources I actually used to learn the Trie pattern.

**Key takeaways:**  
The core design is a Trie, with each node maintaining a heap of the top K phrases passing through that prefix. Insertion is a bit heavier, but lookup is lightning fast.

**Core Design Takeaway:**
The key to this system's performance is the trade off made during insertion. By augmenting each Trie node with a heap, we do more work upfront (O(L * logK)) to make query time exceptionally fast (O(P + K*logK)). This repository is both a technical solution and a record of my process for rapidly mastering and implementing a new, complex data structure.

*Author: Arnaud, July 31, 2025*
