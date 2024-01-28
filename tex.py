import sys
from fractions import Fraction
from typing import Optional, Tuple, Union

from custom_types import ComparisonSign, SergeevAlgorithmResponse
from main import (
    get_sergeev_algorithm_iterations_count,
)

sys.set_int_max_str_digits(10**8)


def format_fraction_latex(frac: Union[Fraction, int]) -> str:
    if isinstance(frac, Fraction):
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
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
        comparison_sign: Optional[ComparisonSign] = None,
    ) -> str:
        a, b, c, d = logarithm_params
        log_a_b = get_log_latex(a, b)
        log_c_d = get_log_latex(c, d)
        step_number_to_roman = {0: "Condition", 1: "I", 2: "II", 3: "III"}
        comparison_sign_str: str = comparison_sign.value if comparison_sign else "\\vee"
        return (
            f"{step_number}) \\quad \\mathrm{{{step_number_to_roman[step]}}}: {log_a_b}"
            f"&{comparison_sign_str} {log_c_d} \\\\"
        )

    if response.comparison_sign == ComparisonSign.EQUAL:
        lines = [
            format_step(0, 0, response.condition_numbers),
            format_step(3, 1, response.condition_numbers, comparison_sign=ComparisonSign.EQUAL),
        ]
    else:
        lines = [format_step(0, 0, response.condition_numbers)]

        for i, (step, params) in enumerate(
            zip(response.steps, response.intermediate_parameters[:-1]), start=1
        ):
            lines.append(format_step(step, i, params))
        lines.append(
            format_step(
                step=3,
                step_number=i + 1,
                logarithm_params=response.intermediate_parameters[-1],
                comparison_sign=response.comparison_sign,
            )
        )

    lines_str: str = "\n".join(lines)
    return f"\\begin{{align*}}\n{lines_str}\n\\end{{align*}}"


def create_tex_file(response: SergeevAlgorithmResponse) -> None:
    preamble = (
        "\\documentclass{article}\n"
        "\\usepackage{amsmath}\n"
        "\\usepackage{amsfonts}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T2A,T1]{fontenc}\n"
        "\\usepackage[english,russian]{babel}\n"
        "\\usepackage[a4paper,margin=2cm]{geometry}\n"
    )
    latex_src = create_latex_code_from_response(response)
    tex = f"{preamble}\\begin{{document}}\n\n{latex_src}\n\n\\end{{document}}\n"
    file_name = (
        f'sergeev-algorithm-{"_".join([str(i.numerator) for i in response.condition_numbers])}'
    )
    with open(f"{file_name}.tex", "wt") as f:
        f.write(tex)


if __name__ == "__main__":
    # a, b, c, d = 77, 26, 85, 28
    # a, b, c, d = 2, 5, 3, 10
    # a, b, c, d = 1999, 2000, 2000, 2001
    # a, b, c, d = 11, 12, 12, 13
    a, b, c, d = 10, 17, 11, 19
    response = get_sergeev_algorithm_iterations_count(a, b, c, d)
    create_tex_file(response)
