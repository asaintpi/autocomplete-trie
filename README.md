# Autocomplete System: Brute Force vs Trie + Heap

This repo contains my full implementation of a high performance autocomplete system, inspired by a problem I encountered in a personal journey.

**Story:**  
I had discussed and coded up a brute force solution for this, which worked but clearly wouldn’t scale. I suspected a Trie would be the right way but hadn’t built one before. After the call, I spent the evening reading up, experimenting, and ultimately implementing a production ready Trie based solution, with a min heap at each node for efficient top K prefix queries.

**What you’ll find here:**
- The brute force approach (as close as possible to what I built initially).
- The final Trie+heap solution, written and debugged from scratch.
- A full test suite with clear, realistic test cases.
- Comments and resources I actually used to learn the Trie pattern.

**Key takeaways:**  
The core design is a Trie (prefix tree), with each node maintaining a heap of the top K phrases passing through that prefix. Insertion is a bit heavier, but lookup is lightning fast.

This repo is both a technical solution and a record of how I learn and improve after hitting a gap.

*Author: Arnaud, July 31, 2025*
