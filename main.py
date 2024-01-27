import json
import math
from fractions import Fraction
from itertools import product
from typing import NamedTuple, Tuple, Union, Literal, Optional

from tqdm import tqdm


class SergeevAlgorithmResponse(NamedTuple):
    condition_numbers: Tuple[
        Union[Fraction],
        Union[Fraction],
        Union[Fraction],
        Union[Fraction],
    ]
    comparison_sign: Literal["<", "=", ">"]
    iterations_count: int
    intermediate_parameters: Tuple[Tuple[Fraction, Fraction, Fraction, Fraction], ...]
    steps: Tuple[Literal[1, 2, 3], ...]


class FractionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Fraction):
            return str(obj)
        return super().default(obj)


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
            comparison_sign="=",
            iterations_count=0,
            intermediate_parameters=tuple(),
            steps=tuple(),
        )
    iterations_count = 0
    intermediate_parameters = []
    steps = []
    step_number = None

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
                sign = "="
            elif log1 > log2:
                sign = ">"
            else:
                sign = "<"
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


def format_fraction_latex(frac: Union[Fraction, int]) -> str:
    if isinstance(frac, Fraction):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
    else:
        return str(frac)


def get_log_latex(base: Union[Fraction, int], argument: Union[Fraction, int]) -> str:
    base_latex = format_fraction_latex(base)
    argument_latex = format_fraction_latex(argument)
    return f"\\log_{{{base_latex}}} {{{argument_latex}}}"


def create_latex_code_from_response(response: SergeevAlgorithmResponse) -> str:
    def format_step(
        step: int,
        step_number: int,
        logarithm_params: Tuple[Fraction, Fraction, Fraction, Fraction],
        comparison_sign: Optional[Literal["<", "=", ">"]] = None,
    ) -> str:
        a, b, c, d = logarithm_params
        log_a_b = get_log_latex(a, b)
        log_c_d = get_log_latex(c, d)
        step_number_to_roman = {0: "Condition", 1: "I", 2: "II", 3: "III"}
        comparison_sign = "\\vee" if not comparison_sign else comparison_sign
        return f"{step_number}) \\quad \\mathrm{{{step_number_to_roman[step]}}}: {log_a_b} &{comparison_sign} {log_c_d} \\\\"

    if response.comparison_sign == "=":
        lines = [
            format_step(0, 0, response.condition_numbers),
            format_step(3, 1, response.condition_numbers, comparison_sign="="),
        ]
    else:
        lines = [format_step(0, 0, response.condition_numbers)]

        for i, (step, params) in enumerate(
            zip(response.steps, response.intermediate_parameters[:-1]), start=1
        ):
            lines.append(format_step(step, i, params))
        lines.append(
            format_step(
                3,
                i + 1,
                response.intermediate_parameters[-1],
                comparison_sign=response.comparison_sign,
            )
        )

    lines = "\n".join(lines)
    latex_src = f"\\begin{{align*}}\n {lines}\n \\end{{align*}}"

    return latex_src


def is_algorithm_correct(response: SergeevAlgorithmResponse) -> bool:
    a, b, c, d = response.condition_numbers
    log1 = math.log(b, a)
    log2 = math.log(d, c)
    sign = response.comparison_sign
    if sign == ">":
        return log1 > log2
    elif sign == "<":
        return log1 < log2
    else:
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
    r = get_sergeev_algorithm_iterations_count(a, b, c, d)
    for i in r.intermediate_parameters:
        print(i)
    print(r.iterations_count)
