import sys
from fractions import Fraction
from os import PathLike
from pathlib import Path
from typing import Optional, Tuple

from sergeev_algorithm import sergeev_algorithm
from sergeev_algorithm.types import AlgorithmResponse, ComparisonSign, FractionLike

sys.set_int_max_str_digits(10**8)


def __format_fraction(frac: FractionLike) -> str:
    if isinstance(frac, Fraction):
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
    return str(frac)


def __format_logarithm(base: FractionLike, argument: FractionLike) -> str:
    log_base = __format_fraction(base)
    log_argument = __format_fraction(argument)
    return f"\\log_{{{log_base}}} {{{log_argument}}}"


def __format_iteration_step(
    step: int,
    step_number: int,
    logarithm_params: Tuple[Fraction, Fraction, Fraction, Fraction],
    comparison_sign: Optional[ComparisonSign] = None,
) -> str:
    a, b, c, d = logarithm_params
    log_a_b = __format_logarithm(a, b)
    log_c_d = __format_logarithm(c, d)
    step_number_to_roman = {0: "Condition", 1: "I", 2: "II", 3: "III"}
    comparison_sign_str: str = comparison_sign.value if comparison_sign else "\\vee"
    return (
        f"{step_number}) \\quad \\mathrm{{{step_number_to_roman[step]}}}: {log_a_b}"
        f"&{comparison_sign_str} {log_c_d} \\\\"
    )


def generate_steps_tex(response: AlgorithmResponse) -> str:
    if response.comparison_sign == ComparisonSign.EQUAL:
        lines = [
            __format_iteration_step(0, 0, response.condition_numbers),
            __format_iteration_step(
                3, 1, response.condition_numbers, comparison_sign=ComparisonSign.EQUAL
            ),
        ]
    else:
        lines = [__format_iteration_step(0, 0, response.condition_numbers)]

        for i, (step, params) in enumerate(
            zip(response.steps, response.intermediate_parameters[:-1]), start=1
        ):
            lines.append(__format_iteration_step(step, i, params))
        lines.append(
            __format_iteration_step(
                step=3,
                step_number=i + 1,
                logarithm_params=response.intermediate_parameters[-1],
                comparison_sign=response.comparison_sign,
            )
        )

    lines_str: str = "\n".join(lines)
    return f"\\begin{{align*}}\n{lines_str}\n\\end{{align*}}"


def generate_tex_file(
    response: AlgorithmResponse, filename: Optional[PathLike[str]] = None
) -> None:
    preamble = (
        "\\documentclass{article}\n"
        "\\usepackage{amsmath}\n"
        "\\usepackage{amsfonts}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T2A,T1]{fontenc}\n"
        "\\usepackage[english,russian]{babel}\n"
        "\\usepackage[a4paper,margin=2cm]{geometry}\n"
    )
    steps_tex = generate_steps_tex(response)
    document_tex = f"{preamble}\\begin{{document}}\n\n{steps_tex}\n\n\\end{{document}}\n"

    filename = filename or Path(
        "sergeev-algorithm-"
        f"{'_'.join([str(i.numerator) for i in response.condition_numbers])}"
        ".tex"
    )
    filepath: PathLike[str] = Path(__file__).parent.parent.joinpath(filename)
    with open(filepath, "wt") as file:
        file.write(document_tex)


if __name__ == "__main__":
    # a, b, c, d = 77, 26, 85, 28
    # a, b, c, d = 2, 5, 3, 10
    # a, b, c, d = 1999, 2000, 2000, 2001
    # a, b, c, d = 11, 12, 12, 13
    a, b, c, d = 10, 17, 11, 19
    response = sergeev_algorithm(a, b, c, d)
    generate_tex_file(response)
