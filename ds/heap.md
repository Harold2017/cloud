#

## Heap

[wiki](https://en.wikipedia.org/wiki/Heap_(data_structure))

```bash

Operation         find-min    delete-min    insert       decrease-key    meld
Binary            Θ(1)        Θ(log n)      O(log n)     O(log n)        Θ(n)
Leftist           Θ(1)        Θ(log n)      Θ(log n)     O(log n)        Θ(log n)
Binomial          Θ(1)        Θ(log n)      Θ(1)[b]      Θ(log n)        O(log n)[c]
Fibonacci         Θ(1)        O(log n)[b]   Θ(1)         Θ(1)[b]         Θ(1)
Pairing           Θ(1)        O(log n)[b]   Θ(1)         o(log n)[b][d]  Θ(1)
Brodal[e]         Θ(1)        O(log n)      Θ(1)         Θ(1)            Θ(1)
Rank-pairing      Θ(1)        O(log n)[b]   Θ(1)         Θ(1)[b]         Θ(1)
Strict Fibonacci  Θ(1)        O(log n)      Θ(1)         Θ(1)            Θ(1)
2-3 heap          O(log n)    O(log n)[b]   O(log n)[b]  Θ(1)            ?


a. Each insertion takes O(log(k)) in the existing size of the heap, thus ΣO(log(k)) [k=1 to n]. Since log(n/2) = log(n) - 1, a constant factor (half) of these insertions are within a constant factor of the maximum, so asymptotically we can assume k = n; formally the time is n * O(log(n)) - O(n) = O(n * log(n)). This can also be readily seen from Stirling's approximation.
b. [a b c d e f g h i] Amortized time.
c. n is the size of the larger heap.
d. Lower bound of Omega(log log n), upper bound of O(2^{2 * {sqrt {log log n}}}).
e. Brodal and Okasaki later describe a persistent variant with the same bounds except for decrease-key, which is not supported. Heaps with n elements can be constructed bottom-up in O(n).[15]
```

## My implementation

- Binary Heap
  - [wiki](https://en.wikipedia.org/wiki/Binary_heap)
  - [implementation](https://github.com/Harold2017/golina/tree/master/container/tree/bheap)
- Fibonacci Heap
  - [wiki](https://en.wikipedia.org/wiki/Fibonacci_heap)
  - [implementation](https://github.com/Harold2017/golina/tree/master/container/heap/fibonacci)
  - [why fibonacci heap](https://stackoverflow.com/questions/19508526/what-is-the-intuition-behind-the-fibonacci-heap-data-structure?lq=1)
  - [why called fibonacci](https://stackoverflow.com/questions/14333314/why-is-a-fibonacci-heap-called-a-fibonacci-heap)
