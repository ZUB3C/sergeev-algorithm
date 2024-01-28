import math
from itertools import product

from tqdm import tqdm

from sergeev_algorithm.types import AlgorithmResponse, ComparisonSign, FractionLike
from sergeev_algorithm.utils import convert_to_fraction


def sergeev_algorithm(
    a: FractionLike,
    b: FractionLike,
    c: FractionLike,
    d: FractionLike,
) -> AlgorithmResponse:
    a, b, c, d = map(convert_to_fraction, (a, b, c, d))
    numbers = (a, b, c, d)
    if a == c and b == d:
        # Logarithms are equals
        return AlgorithmResponse(
            condition_numbers=numbers,
            comparison_sign=ComparisonSign.EQUAL,
            iterations_count=0,
            intermediate_parameters=(),
            steps=(),
        )
    iterations_count = 0
    intermediate_parameters = []
    steps = []

    while True:
        if b > a and d > c:
            a, b, c, d = a, b / a, c, d / c
            step_number = 1
        elif b < a and d < c:
            a, b, c, d = d, c, b, a
            step_number = 2
        else:
            # break
            log1 = math.log(b, a)
            log2 = math.log(d, c)
            if log1 == log2:
                sign = ComparisonSign.EQUAL
            elif log1 > log2:
                sign = ComparisonSign.GREATER
            else:
                sign = ComparisonSign.LESS
            intermediate_parameters.append((a, b, c, d))
            step_number = 3
            steps.append(step_number)
            iterations_count += 1
            break
        intermediate_parameters.append((a, b, c, d))
        steps.append(step_number)
        iterations_count += 1

    return AlgorithmResponse(
        condition_numbers=numbers,
        comparison_sign=sign,
        iterations_count=iterations_count,
        intermediate_parameters=tuple(intermediate_parameters),
        steps=tuple(steps),
    )


def solve_first_task(start: int, stop: int) -> None:
    """Find log params with max iterations count"""
    if start >= stop:
        raise ValueError("range start is bigger or equals than range stop")

    search_range = range(start, stop)
    max_iterations_count = -1

    for a, b, c, d in tqdm(
        product(search_range, repeat=4),
        total=(stop - start) ** 4,
    ):
        response = sergeev_algorithm(a, b, c, d)
        iterations_count = response.iterations_count

        if iterations_count > max_iterations_count:
            print(f"{(a, b, c, d)}: {iterations_count}")
            max_iterations_count = iterations_count


if __name__ == "__main__":
    # a, b, c, d = 23, 6, 89, 13
    a, b, c, d = 11, 12, 12, 13
    response = sergeev_algorithm(a, b, c, d)
    for i in response.intermediate_parameters:
        print(i)
    print(f"iterations count: {response.iterations_count}")
