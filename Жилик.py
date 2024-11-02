import sympy as sympy
from sympy.calculus.util import maximum, minimum


def maximum_function_on_diff(f_x, symbol_x, number, distance):  # Ищет максимум производной n-го порядка на [a;b]
    diff_func = sympy.diff(f_x, symbol_x, number)
    diff_func_max = abs(maximum(diff_func, x, distance))
    diff_func_min = abs(minimum(diff_func, x, distance))

    if diff_func_max < diff_func_min:                       # Это на тот случай если минимум оказался больше
        diff_func_max = diff_func_min

    return diff_func_max


function = "x/2*log(x^2/2)"                             # Исходная функция
function = sympy.sympify(function)                      # sympify - переводит нашу строку в понятный Питону синтаксис
a = 1
b = 3
n = 10
Rh = 0
x = sympy.Symbol('x')                                   # Для Питона, чтобы понимал в какую переменную надо подставлять
interval = sympy.Interval(a, b)                         # Создали интервал

print("-----------------------------Исходный интеграл---------------------------------------")
Integral_function = sympy.integrate(function, (x, a, b))
print("Значение интеграла =", Integral_function, "=", end=" ")
Integral_function = sympy.N(Integral_function)
print(sympy.N(Integral_function), "\n")                 # sympy.N() как видно досчитывает логарифмы
print("--------------------------Интеграл методом трапеций----------------------------------")

h = (b - a) / n                                         # Считаем шаг сетки
nodes = [a]                                             # Задаем сначала нулевой элемент
for i in range(1, n+1):
    nodes.append(nodes[i-1] + h)                        # Заполняем список с шагом h в данном интервале

                                                        # Помним что применили sympify теперь .subs будет работать
y0 = sympy.N(function.subs(x, nodes[0]))               # Подставляем в функцию границы a и b
yn = sympy.N(function.subs(x, nodes[n]))

first_sum = (y0 + yn) / 2
next_sums = 0
for i in range(1, n):                                   # Считаем значение функции внутри промежутка a и b
    next_sums += sympy.N(function.subs(x, nodes[i]))

Integral_function_new = h * (first_sum + next_sums)

print("Значение интеграла:", Integral_function_new)
print("Ошибка составила", abs(Integral_function - Integral_function_new))

M_2 = maximum_function_on_diff(function, x, 2, interval)  # Находим вторую производную

Rh = (-(b - a) / 12) * (M_2 * h**2)                     # По формуле
print("Остаточный член R(h):", Rh, "\n")
print("Количество точек: ", n)
print("Взят шаг h = ", h)

print("---------------------------Интеграл методом Симсона----------------------------------")

mult_next = y0 + yn

for i in range(1, n):
    if i % 2 == 0:
        mult_next += 2 * function.subs(x, nodes[i])
    else:
        mult_next += 4 * function.subs(x, nodes[i])

Integral_function_new = (h / 3) * mult_next

print("Значение интеграла:", Integral_function_new)
print("Ошибка составила", abs(Integral_function - Integral_function_new))

M_4 = maximum_function_on_diff(function, x, 4, interval)        # Находим четвертую производную

Rh = (-(b - a) / 180) * M_4 * pow(h, 4)
print("Остаточный член R(h):", Rh, "\n")
print("Количество точек: ", n)
print("Взят шаг h = ", h)

print("-------------------------Интеграл методом три восьмых---------------------------------")

n = 9
h = (b - a) / n
nodes = [a]
for i in range(1, n+1):
    nodes.append(nodes[i-1] + h)

sum_first = y0 + yn
sum_second = 0
sum_third = 0

for i in range(1, n):
    if i % 3 != 0:
        sum_second += function.subs(x, nodes[i])
    else:
        sum_third += function.subs(x, nodes[i])

Integral_function_new = 3 / 8 * h * (sum_first + 3 * sum_second + 2 * sum_third)

print("Значение интеграла:", Integral_function_new)
print("Ошибка составила", abs(Integral_function - Integral_function_new))

Rh = (-(b - a) / 80) * M_4 * pow(h, 4)

print("Остаточный член R(h):", Rh, "\n")
print("Количество точек: ", n)
print("Взят шаг h = ", h)

print("----------------------------Интеграл методом Гаусса-----------------------------------")

n = 4
h = (b - a) / n
nodes = [a]
for i in range(1, n+1):
    nodes.append(nodes[i-1] + h)

M_8 = maximum_function_on_diff(function, x, 8, interval)  # Находим восьмую производную

ai = 0
summa = 0

for i in range(n):
    xi = (b + a) / 2
    if i == 0:
        xi += -0.86113631 * ((b - a) / 2)
        ai = 0.34785484
    if i == 1:
        xi += -0.33998104 * ((b - a) / 2)
        ai = 0.65214516
    if i == 2:
        xi += 0.33998104 * ((b - a) / 2)
        ai = 0.65214516
    if i == 3:
        xi += 0.86113631 * ((b - a) / 2)
        ai = 0.34785484
    fxi = function.subs(x, xi)
    summa += ai * fxi

Rh = pow((b-a)/2, 2*n) * 2.88 * pow(10, -7) * M_8
    
Integral_function_new = (b - a) / 2 * summa

print("Значение интеграла:", Integral_function_new)
print("Ошибка составила", abs(Integral_function - Integral_function_new))

print("Остаточный член R(h):", Rh, "\n")
print("Количество точек: ", n)
print("Взят шаг h = ", h)

print("--------------------Интеграл методом левых прямоугольников-----------------------------")

n = 100                                   # Если взять n = 100, то получим 1.5314066, что логично
h = (b - a) / n
nodes = [a]
for i in range(1, n+1):
    nodes.append(nodes[i-1] + h)

M_1 = maximum_function_on_diff(function, x, 1, interval)  # Находим производную

Integral_function_new = 0
for i in range(n):
    Integral_function_new += function.subs(x, nodes[i])

Integral_function_new *= h

print("Значение интеграла:", sympy.N(Integral_function_new))
print("Ошибка составила", abs(Integral_function - sympy.N(Integral_function_new)))

Rh = M_1 / 2 * (b - a) * h

print("Остаточный член R(h):", sympy.N(Rh), "\n")
print("Количество точек: ", n)
print("Взят шаг h = ", h)

# Первое задание правильно. Дальше пока не уверен.
print("-------------------Интеграл методом трапеций с уменьшением шага-------------------------")

print("Значение исходного интеграла =", Integral_function)

Epsilon = pow(10, -6)
print("Epsilon = ", Epsilon)

while True:
    Rh = (b - a) / 12 * M_2 * h * h
    if abs(Rh) < Epsilon:
        break
    h -= 0.001
    n = int(round((b - a) / h))
    nodes = [a]
    for i in range(1, n + 1):
        nodes.append(nodes[i - 1] + h)
    Rh = 0

y0 = sympy.N(function.subs(x, nodes[0]))               # Подставляем в функцию границы a и b
yn = sympy.N(function.subs(x, nodes[n]))

first_sum = (y0 + yn) / 2
next_sums = 0
for i in range(1, n):                                   # Считаем значение функции внутри промежутка a и b
    next_sums += sympy.N(function.subs(x, nodes[i]))

Integral_function_new = h * (first_sum + next_sums)

print("Значение полученного интеграла:", Integral_function_new)
print("Ошибка составила", abs(Integral_function - Integral_function_new))

print("Остаточный член R(h):", sympy.N(Rh), "\n")
print("Взят шаг h = ", h)

print("----------------Интеграл методом трапеций с уменьшением интервала---------------------")

n = 10

h = (b - a) / n
nodes = [a]
for i in range(1, n + 1):
    nodes.append(nodes[i - 1] + h)

while True:
    y0 = sympy.N(function.subs(x, nodes[0]))
    yn = sympy.N(function.subs(x, nodes[n]))

    first_sum = (y0 + yn) / 2
    next_sums = 0
    for i in range(1, n):
        next_sums += sympy.N(function.subs(x, nodes[i]))

    Integral_function_new = h * (first_sum + next_sums)

    n *= 2

    h = (b - a) / n
    nodes = [a]
    for i in range(1, n + 1):
        nodes.append(nodes[i - 1] + h)

    y0 = sympy.N(function.subs(x, nodes[0]))
    yn = sympy.N(function.subs(x, nodes[n]))

    first_sum = (y0 + yn) / 2
    next_sums = 0
    for i in range(1, n):
        next_sums += sympy.N(function.subs(x, nodes[i]))

    Integral_function_new_2 = h * (first_sum + next_sums)

    if abs(Integral_function_new_2 - Integral_function_new) <= Epsilon:
        break

print("Значение полученного интеграла:", Integral_function_new)
print("Ошибка составила", abs(Integral_function - Integral_function_new))

print("Остаточный член R(h):", Rh, "\n")
print("Взят шаг h = ", h)
