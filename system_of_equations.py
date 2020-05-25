import sys
import random
import string

def get_variables(n=1, level=1):
    '''
    Generate variables for equation.

    Parameters
    ----------
    n : int or dict or list or tuple
        number of variables or equations to solve

    level : int
        difficulty of problem to solve
        1 or 'babe' - lowest, values between 0 and 9
        2 or 'kido' - positive values between 0 and 20
        3 or 'novice' - values between -20 and 20
        4 or 'pupil' - values between -100 and 100
        5 or 'smart' - values between -200 and 200
        6 or 'smartass' - possible fractions as answer

    Returns
    -------
    dictionary
        keys: names of variables
        values: values of variables

    TODO: 1. smartass
    '''
    assert isinstance(n, int) and n > 0, "n is a positive int"

    level_names = ('babe', 'kido', 'novice', 'pupil', 'smart', 'smartass')
    if isinstance(level, int) and (0 < level < 7):
        level -= 1  # just to meet level names in level_names tuple
    elif isinstance(level, str):
        if level in level_names:
            level = level_names.index(level)
        elif level in [str(i) for i in range(1, 7)]:
            level = int(level) - 1
    else:
        raise TypeError("level must be int from 1 to 6 or str")

    if level == 0:
        a, b = 1, 9
        name_start = 23  # x, y, z
    elif level == 1:
        a, b = 1, 20
        name_start = 23  # x, y, z
    elif level == 2:
        a, b = -20, 20
        name_start = random.choice([0, 23]) # a, b, c or x, y, z
    elif level == 3:
        a, b = -100, 100
        name_start = random.choice([0, 23]) # a, b, c or x, y, z
    elif level == 4 or level == 5:
        a, b = -200, 200
        name_start = random.randint(0, 25)
    elif level == 5:
        a, b = -200, 200
        name_start = random.randint(0, 25)

    # naming convention
    alphabet = string.ascii_lowercase
    variable_names = alphabet[name_start:] + alphabet[:name_start]

    ret = {'n': n}
    ret['level'] = level
    ret['variables'] = variable_names[:n]
    for i in range(n):
        ret[variable_names[i]] = random.randint(a, b)

    ret['coefficients'] = [random.randint(a, b) for i in range(n * n)]

    return ret


def add_coefficient(c):
    if c == 1:
        return ''
    if c < 0:
        return f'- {abs(c)}'
    elif c > 0:
        return f'+ {c}'
    else:
        return ''


def add_element(c, v, elem, lhs):
    c = add_coefficient(c)

    if c == '':
        return ''

    ret = c + v
    if lhs == '':
        if ret[0] == '+':
            ret = ret[2:]
    else:
        ret = " " + ret

    return ret


def add_latex_line(txt, indent=0):
    return ' ' * 2 * indent + txt + '\n'


def latexify(eqs):
    import subprocess
    latex = get_latex_doc(eqs)
    with open('out.tex', 'w') as f:
        f.write(latex)
    subprocess.run(["pdflatex", "out.tex"])
    subprocess.run(["rm", "out.log", "out.aux", "out.tex"])


def get_latex_doc(eqs):
    ret = add_latex_line(r'\documentclass[12pt, a4paper]{article}')
    ret += add_latex_line(r'\usepackage[margin=0.5in]{geometry}')
    ret += add_latex_line(r'\usepackage[fleqn]{amsmath}')
    ret += add_latex_line(r'\usepackage{multicol}')
    ret += add_latex_line(r'\begin{document}')
    ret += add_latex_line(r'\begin{multicols}{2}')

    for txt in eqs:
        ret += add_latex_line(r'\begin{equation}', indent=2)
        ret += add_latex_line(r'\begin{cases}', indent=3)
        for line in txt.split('\n'):
            ret += add_latex_line(r'' + line + r'\\', indent=4)
        ret = add_latex_line(ret[:-3])
        ret +=  add_latex_line(r'\end{cases}', indent=3)
        ret += add_latex_line(r'\end{equation}', indent=2)
        ret += add_latex_line(r' ', indent=2)

    ret += add_latex_line(r'\end{multicols}')
    ret += add_latex_line(r'\end{document}')

    return ret


def get_system_of_equations(N=1, n=1, level=1, latex=True):
    "..."

    rets = []
    for eq in range(N):
        d = get_variables(n, level)

        ret = ''
        for z in range(n):

            rhs = 0
            lhs = ''
            for elem in range(n):
                c = d['coefficients'][elem + z * n]
                v = d['variables'][elem]

                element = add_element(c, v, elem, lhs)
                lhs += element
                rhs += c * d[v]

            ret += f'{lhs} = {rhs}'
            if z < n - 1:
                ret += '\n'
        rets.append(ret)

    if latex:
        rets = latexify(rets)

    return rets


if __name__ == "__main__":
    N = int(sys.argv[1])
    n = int(sys.argv[2])
    level = sys.argv[3]
    t = get_system_of_equations(N, n, level)
    print(t)
