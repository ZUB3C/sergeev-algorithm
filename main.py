import math
from fractions import Fraction
from itertools import product
from typing import Union

from tqdm import tqdm

from custom_types import ComparisonSign, SergeevAlgorithmResponse


def convert_to_fraction(value: Union[Fraction, int]) -> Fraction:
    if isinstance(value, int):
        return Fraction(value)
    return value


def get_sergeev_algorithm_iterations_count(
    a: Union[Fraction, int],
    b: Union[Fraction, int],
    c: Union[Fraction, int],
    d: Union[Fraction, int],
) -> SergeevAlgorithmResponse:
    a, b, c, d = [convert_to_fraction(i) for i in (a, b, c, d)]
    numbers = (a, b, c, d)
    if a == c and b == d:
        # Logarithms are equals
        return SergeevAlgorithmResponse(
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

    return SergeevAlgorithmResponse(
        condition_numbers=numbers,
        comparison_sign=sign,
        iterations_count=iterations_count,
        intermediate_parameters=tuple(intermediate_parameters),
        steps=tuple(steps),
    )


def is_algorithm_correct(response: SergeevAlgorithmResponse) -> bool:
    a, b, c, d = response.condition_numbers
    log1 = math.log(b, a)
    log2 = math.log(d, c)
    sign = response.comparison_sign
    if sign == ComparisonSign.GREATER:
        return log1 > log2
    if sign == ComparisonSign.LESS:
        return log1 < log2
    return log1 == log2


def find_log_params_with_max_iterations_count() -> None:
    max_iterations_count = -float("inf")

    search_range = range(10, 101)

    for a, b, c, d in tqdm(
        product(search_range, repeat=4),
        total=(search_range.stop - search_range.start) ** 4,
    ):
        response = get_sergeev_algorithm_iterations_count(a, b, c, d)
        iterations_count = response.iterations_count

        if iterations_count > max_iterations_count:
            print(f"{(a, b, c, d)}: {iterations_count}")
            max_iterations_count = iterations_count


if __name__ == "__main__":
    # a, b, c, d = 23, 6, 89, 13
    a, b, c, d = 11, 12, 12, 13
    response = get_sergeev_algorithm_iterations_count(a, b, c, d)
    for i in response.intermediate_parameters:
        print(i)
    print(response.iterations_count)
