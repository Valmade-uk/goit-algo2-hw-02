from typing import List, Tuple

def find_min_max(arr: List[float]) -> Tuple[float, float]:
    """
    Знаходить мінімальний та максимальний елементи масиву методом
    'розділяй і володарюй'.

    Args:
        arr: масив чисел довільної довжини

    Returns:
        (мінімум, максимум)
    """
    if not arr:
        raise ValueError("Масив не повинен бути порожнім")

    def rec(l: int, r: int) -> Tuple[float, float]:
        # Один елемент
        if l == r:
            return arr[l], arr[l]
        # Два елементи — мінімум порівнянь
        if r == l + 1:
            if arr[l] < arr[r]:
                return arr[l], arr[r]
            else:
                return arr[r], arr[l]

        mid = (l + r) // 2
        min_left, max_left = rec(l, mid)
        min_right, max_right = rec(mid + 1, r)

        return min(min_left, min_right), max(max_left, max_right)

    return rec(0, len(arr) - 1)

if __name__ == "__main__":
    print("\nПеревірка find_min_max:")
    arr = [3, 1, 7, -2, 5]
    mn, mx = find_min_max(arr)
    print("масив:", arr)
    print("мін:", mn, "макс:", mx)