# Графический редактор

## Лабораторная работа №1

### Тема
Генерация отрезков.

### Задание:
Разработать элементарный графический редактор, реализующий построение отрезков с
помощью алгоритма ЦДА, целочисленного алгоритм Брезенхема и алгоритма Ву. Вызов
способа генерации отрезка задается из пункта меню и доступно через панель инструментов
«Line». В редакторе кроме режима генерации отрезков в пользовательском окне должен
быть предусмотрен отладочный режим, где отображается пошаговое решение на дискретной сетке.

### Алгоритмы
#### Алгоритм ЦДА
Алгоритм DDA-линии растеризует отрезок прямой между двумя заданными точками, используя вычисления с вещественными числами. 
Аббревиатура DDA в названии этого алгоритма машинной графики происходит от англ. 
Digital Differential Analyzer (цифровой дифференциальный анализатор) — вычислительное устройство, применявшееся ранее для генерации векторов. 
Несмотря на то, что сейчас этот алгоритм практически не применяется, он позволяет понять сложности, которые встречаются при растеризации отрезка и способы их решения.

#### Алгоритм Брезенхема
Алгоритм Брезенхема (англ. Bresenham's line algorithm) — это алгоритм, определяющий, какие точки двумерного растра нужно закрасить, 
чтобы получить близкое приближение прямой линии между двумя заданными точками.

#### Алгоритм Ву Сяолиня
Алгоритм использует механизмы сглаживания при растеризации линии. При этом ступенчатые выступы на линии становятся менее заметны.

### Интерфейс
![image](https://github.com/user-attachments/assets/be317cd2-1c66-4ff2-b286-7ca7990d2661)

### Технологии
Python\
Tkinter

### Вывод
В результате реализации графического редактора, использующего алгоритмы построения отрезков (ЦДА, Брезенхема и Ву), 
реализована отрисовка отрезков с возможностью очистки доски и режимом отладки.

## Лабораторная работа №2

### Тема
Генерация кривых второго порядка.

### Задание:
Разработать элементарный графический редактор, реализующий построение линий второго порядка: окружность, эллипс, гипербола, парабола. Выбор кривой задается из пункта меню и
доступно через панель инструментов «Curve». В редакторе кроме режима генерации линий второго порядка в пользовательском окне должен быть предусмотрен
отладочный режим, где отображается пошаговое решение на дискретной сетке.

### Интерфейс
![image](https://github.com/user-attachments/assets/90a183d1-5982-4508-bcc2-d48f24197314)

### Технологии
Python\
Tkinter

### Вывод
В результате выполнения был реализован функционал для отрисовки кривых второго порядка: Круг, Элипс, Гипербола и Парабола.

## Лабораторная работа №3

### Тема
Построение кривых.

### Задание
Разработать элементарный графический редактор, реализующий построение параметрических кривых, используя форму Эрмита, форму Безье и B-сплайн. Выбор метода
задается из пункта меню и доступно через панель инструментов «Кривые». В редакторе должен быть предусмотрен режим корректировки опорных точек и состыковка сегментов. В
программной реализации необходимо реализовать базовые функции матричных вычислений.

### Интерфейс
![image](https://github.com/user-attachments/assets/400e8b26-17bd-43f9-a504-84d8a546355f)

### Технологии
Python\
Tkinter

### Вывод
В результате выполнения был реализован функционал для отрисовки кривых, используя форму Эрмита, форму Безье и B-сплайн.

## Лабораторная работа №4

### Тема
Геометрические преобразования. 

### Задание
Разработать элементарный графический редактор, реализующий геометрические преобразования в двумерном и трехмерном пространстве, а также перспективные
преобразования. Для выполнения базовых геометрических преобразований разработать панель управления. В редакторе предусмотреть отладочный режим. 

### Интерфейс
![image](https://github.com/user-attachments/assets/7272b1b5-ad26-437f-8bb7-e244defe30d5)

### Технологии
Python\
PyGame + OpenGL

### Вывод
В результате выполнения был реализован функционал рализующий геометрические преобразования в двумерном и трехмерном пространстве, а также перспективные преобразования.

## Лабораторная работа №5

### Тема
Построение полигонов. 

### Задание
Разработать элементарный графический редактор, реализующий алгоритмы построния полигонов Джарвиса и Грэхема. 
Для выполнения базовых геометрических преобразований разработать панель управления. В редакторе предусмотреть отладочный режим. 

### Интерфейс
![image](https://github.com/user-attachments/assets/6f2f193f-da26-412a-b405-6f7e5c03c195)

### Технологии
Python\
Tkinter

### Вывод
В результате выполнения был реализован функционал для отрисовки полигонов, используя алгоритмы, Джарвиса и и Грэхема.

## Лабораторная работа №6

### Тема
Реализация алгоритмов заливки. 

### Задание
Разработать элементарный графический редактор, реализующий алгоритмы заливки полигонов ET, AEL, Flood, Line-by-Line. 
Для выполнения базовых геометрических преобразований разработать панель управления. В редакторе предусмотреть отладочный режим. 

### Интерфейс
![image](https://github.com/user-attachments/assets/0b641c01-8f84-40e5-94d9-3f58191764e7)

### Технологии
Python\
Tkinter

### Вывод
В результате выполнения был реализован функционал для заливки полигонов, используя алгоритмы ET, AEL, Flood, Line-by-Line.

## Лабораторная работа №7

### Тема
Реализация алгоритмов посторения триангуляции Делоне и диаграммы Вороного.

### Задание
Разработать элементарный графический редактор, реализующий алгоритмы посторения триангуляции Делоне и диаграммы Вороного. 
Для выполнения базовых геометрических преобразований разработать панель управления. В редакторе предусмотреть отладочный режим. 

### Интерфейс
![image](https://github.com/user-attachments/assets/6b9af4d5-124b-4b5d-8100-0989ef2849d1)

### Технологии
Python\
Tkinter

### Вывод
В результате выполнения был реализован функционал для посторения триангуляции Делоне и диаграммы Вороного.
