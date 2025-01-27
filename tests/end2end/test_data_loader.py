from pathlib import Path
from typing import List

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

data_path = Path(__file__).parent / 'test_data'
data = [str(data_path / f"{i}.txt") for i in range(5)]
print(data)

A = gmt.create_metamorphic_relation(
    name='A',
    data=data
)

counter = 0


def data_loader(filepath: str) -> int:
    global counter
    counter += 1
    return int(Path(filepath).read_text())


@gmt.transformation(A)
def add(x: int):
    return x + 10


@gmt.relation(A)
def greate(source: int, follow_up: int) -> bool:
    return source < follow_up


@gmt.system_under_test(A, data_loader=data_loader)
def test_non_batched(batch: int) -> int:
    assert isinstance(batch, int)
    return batch


@gmt.system_under_test(A, data_loader=data_loader, batch_size=2)
def test_batched(batch: List[int]) -> List[int]:
    assert all(isinstance(x, int) for x in batch)
    return batch


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 5 * 2
    assert test_results[KEY]['number_of_failed_tests'] == 0

    assert counter == 5 * 2
