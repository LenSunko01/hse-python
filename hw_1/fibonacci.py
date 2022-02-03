from typing import List


def fibonacci(n) -> List[int]:
    fst = 0
    snd = 1
    n_fibonacci = [fst]
    for i in range(n - 1):
        tmp = fst
        fst = fst + snd
        snd = tmp
        n_fibonacci.append(fst)
    return n_fibonacci
