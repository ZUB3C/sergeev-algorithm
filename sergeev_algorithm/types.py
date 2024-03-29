from enum import Enum
from fractions import Fraction
from typing import NamedTuple, Tuple, TypeAlias, Union

FractionLike: TypeAlias = Union[Fraction, int]


class ComparisonSign(Enum):
    LESS = "<"
    EQUAL = "="
    GREATER = ">"
    UNKNOWN = "V"


class AlgorithmResponse(NamedTuple):
    condition_numbers: Tuple[
        Fraction,
        Fraction,
        Fraction,
        Fraction,
    ]
    comparison_sign: ComparisonSign
    iterations_count: int
    intermediate_parameters: Tuple[Tuple[Fraction, Fraction, Fraction, Fraction], ...]
    steps: Tuple[int, ...]
