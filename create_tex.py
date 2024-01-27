import sys

from main import (
    get_sergeev_algorithm_iterations_count,
    create_latex_code_from_response,
    SergeevAlgorithmResponse,
)

sys.set_int_max_str_digits(10**8)


def create_tex_file(response: SergeevAlgorithmResponse) -> None:
    preamble_linex = [
        "\\documentclass{article}",
        "\\usepackage{amsmath}",
        "\\usepackage{amsfonts}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[T2A,T1]{fontenc}",
        "\\usepackage[english,russian]{babel}",
        "\\usepackage[a4paper,margin=2cm]{geometry}",
        "\\begin{document}",
    ]
    preamble_str = "\n".join(preamble_linex)
    latex_src = create_latex_code_from_response(response)
    tex = f"{preamble_str}\n\n{latex_src}\n\n\\end{{document}}\n"
    file_name = f'sergeev-algorithm-{"_".join(map(str, [i.numerator for i in response.condition_numbers]))}'
    with open(f"{file_name}.tex", "wt") as f:
        f.write(tex)


if __name__ == "__main__":
    a, b, c, d = 77, 26, 85, 28
    a, b, c, d = 2, 5, 3, 10
    a, b, c, d = 1999, 2000, 2000, 2001
    a, b, c, d = 11, 12, 12, 13
    a, b, c, d = 10, 17, 11, 19
    response = get_sergeev_algorithm_iterations_count(a, b, c, d)
    create_tex_file(response)
