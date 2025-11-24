from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера
    (жадібний алгоритм).
    """
    jobs = [PrintJob(**j) for j in print_jobs]
    cons = PrinterConstraints(**constraints)

    # Перевірка коректності
    for j in jobs:
        if j.volume <= 0 or j.print_time <= 0:
            raise ValueError(f"Некоректні дані у завданні {j.id}")
        if j.priority not in (1, 2, 3):
            raise ValueError(f"Некоректний пріоритет у завданні {j.id}")
        if j.volume > cons.max_volume:
            raise ValueError(
                f"Модель {j.id} має об'єм {j.volume}, що перевищує max_volume={cons.max_volume}"
            )

    # Стабільне сортування за пріоритетом (вищий раніше)
    jobs.sort(key=lambda x: x.priority)

    print_order: List[str] = []
    total_time = 0

    current_group: List[PrintJob] = []
    current_volume = 0.0

    def close_group():
        nonlocal total_time, current_group, current_volume
        if not current_group:
            return
        # час групи = max часу моделей
        group_time = max(j.print_time for j in current_group)
        total_time += group_time
        print_order.extend(j.id for j in current_group)

        current_group = []
        current_volume = 0.0

    for job in jobs:
        can_add = (
            len(current_group) < cons.max_items and
            current_volume + job.volume <= cons.max_volume
        )

        if can_add:
            current_group.append(job)
            current_volume += job.volume
        else:
            close_group()
            current_group.append(job)
            current_volume = job.volume

    close_group()

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування з умови
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму (загальне, не індивідуальне)
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()