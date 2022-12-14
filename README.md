# game_of_life
## Установка игры:

### 1.1 Через командную строку:

1) Скопировать ссылку на репозиторий;
![image](https://user-images.githubusercontent.com/113696995/206867588-e525501f-52b5-431a-87cd-2fe2d35a56e1.png)
2) В командной строке набрать "git clone [вставить ссылку]";
3) Дождаться установки;
4) По окончании установки набрать в командной строке "main.exe";
5) Наслаждаться игрой. (См. пункты 2 "Взаимодействие с полем" и 3 "Правила игры") 

### 1.2 Через архив:
1) Скачать zip-файл;
![image](https://user-images.githubusercontent.com/113696995/206867567-0a261607-693f-4b38-90b3-e82e7a65aee3.png)
2) Распаковать его в любую папку;
3) Запустить файл "main.exe";
4) Наслаждаться игрой. (См. пункты 2 "Взаимодействие с полем" и 3 "Правила игры") 

### 2 Взаимодействие с полем:
1) При входе в игру Вы увидете окно с полем клеток и тремя кнопками: "СТАРТ", "СТОП" и "ОЧИСТИТЬ".
2)  Нажатие кнопки "СТАРТ" запускает расчет новых поколений клеток по правилам (см. пункт 3 "Правила игры").
3)  Нажатие кнопки "СТОП" приостанавливает расчет новых поколений клеток.
4)  Нажатие кнопки "ОЧИСТИТЬ" очищает всё поле, все клетки становятся пустыми.

### 3 Правила игры:
1) Место действия игры — размеченная на клетки плоскость.
2) Каждая клетка на этой поверхности имеет восемь соседей, окружающих её, и может находиться в двух состояниях: быть «живой» (заполненной) или «мёртвой» (пустой).
3) Распределение живых клеток в начале игры называется первым поколением. Каждое следующее поколение рассчитывается на основе предыдущего по таким правилам: 
в пустой (мёртвой) клетке, с которой соседствуют три живые клетки, зарождается жизнь;
если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; 
в противном случае (если живых соседей меньше двух или больше трёх) клетка умирает («от одиночества» или «от перенаселённости»).
4) Игрок не принимает активного участия в игре. Он лишь расставляет или генерирует начальную конфигурацию «живых» клеток, которые затем изменяются согласно правилам. 

# Приятной игры!
