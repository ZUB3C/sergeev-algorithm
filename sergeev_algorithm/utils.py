import math
from fractions import Fraction

from sergeev_algorithm.types import AlgorithmResponse, ComparisonSign, FractionLike


def convert_to_fraction(value: FractionLike) -> Fraction:
    if isinstance(value, int):
        return Fraction(value)
    return value


def is_algorithm_correct(response: AlgorithmResponse) -> bool:
    a, b, c, d = response.condition_numbers
    log1 = math.log(b, a)
    log2 = math.log(d, c)
    sign = response.comparison_sign
    if sign == ComparisonSign.GREATER:
        return log1 > log2
    if sign == ComparisonSign.LESS:
        return log1 < log2
    return log1 == log2
