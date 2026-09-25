# ПР02: выполненные команды и результаты

Окружение: Ubuntu 26.04.1, ROS 2 Lyrical, native, rmw_fastrtps_cpp, ROS_DOMAIN_ID=16.
Teleop остановлен. Все результаты ниже получены от настоящего turtlesim.

## Три команды Linux

1. `mkdir -p src evidence/pr02 evidence/pr01-reproduced` — создаёт каталоги, включая родителей; каталоги созданы в корне workspace.
2. `source /opt/ros/lyrical/setup.bash` — подключает ROS к текущей оболочке; ros2 находит turtlesim в /opt/ros/lyrical.
3. `colcon build --symlink-install --packages-select turtle_bringup 2>&1 | tee evidence/pr02/build.txt` — собирает пакет и одновременно показывает/сохраняет объединённый вывод. Результат: 1 package finished, код 0; лог build.txt. Перед командой выполнен `set -o pipefail`.

`>` перенаправляет stdout в файл с заменой содержимого. `|` направляет stdout
на вход следующей программы. `2>&1` присоединяет stderr к текущему stdout;
`tee` пишет одновременно на экран и в файл. `pipefail` сохраняет ошибку colcon
в статусе конвейера. `source` выполняет скрипт в текущей оболочке: её переменные
меняются. Отдельная программа не может поменять окружение родительской оболочки.

## Пакет и launch

Пакет создан командой:
```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 turtle_bringup \
  --dependencies launch launch_ros turtlesim --maintainer-name Nikita \
  --maintainer-email niknikivan@gmail.com \
  --description 'Launch the standard turtlesim node for PR02'
```

Первоначальная сборка до создания launch: build-empty.txt. После добавления
launch и data_files выполнена итоговая сборка: build.txt.
`source install/setup.bash` подключает установленный пакет, но не запускает ноду.
`ros2 pkg prefix turtle_bringup` указывает install этого workspace (package-prefix.txt).
`ls "$(ros2 pkg prefix turtle_bringup)/share/turtle_bringup/launch"`
показал sim.launch.py (installed-launch.txt).

`ros2 launch turtle_bringup sim.launch.py` открыл одно окно; `ros2 node list
--no-daemon --spin-time 2` обнаружил ровно одну /turtlesim.
Остановка сигналом SIGINT (эквивалент Ctrl+C) завершила launch с кодом 0,
дочерний turtlesim завершился cleanly. В повторном node list /turtlesim отсутствует.
Логи: launch-stop-test.txt, nodes-launched.txt, nodes-stopped.txt.
Затем launch запущен повторно для опыта ниже (launch-experiment.txt).

## До / сбой / после

Ожидание: linear.x=1 задаёт движение вперёд; angular.z=0.5 — поворот против
часовой стрелки. Из исходной theta=0 координаты x и y растут, траектория — дуга.
Команда `--once` не задаёт бесконечное движение: без новых команд скорость становится нулевой.

| Стадия | x | y | theta |
|---|---:|---:|---:|
| До | 5.544445 | 5.544445 | 0.000000 |
| После --once | 6.509309 | 5.796991 | 0.504000 |
| Неверный /cmd_vel | 6.509309 | 5.796991 | 0.504000 |
| После исправления имени | 7.423817 | 8.206135 | 1.904000 |
| После остановки издателя | 6.720536 | 9.156250 | 2.504000 |

В неверный топик отправлялся тот же Twist:
```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 /cmd_vel \
  geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

Издатель обнаружен: /cmd_vel содержит 1 publisher, 0 subscriptions.
/turtle1/cmd_vel в это время содержит 0 publishers, 1 subscription (/turtlesim).
Поза не изменилась. После SIGINT издатель остановлен; CLI вернул 2,
это код прерывания этой команды в данной версии, а не сбой доставки.
Исправлено только /cmd_vel на /turtle1/cmd_vel: те же тип, скорость, частота и домен.
Теперь 1 publisher и 1 subscription, поза изменилась. После остановки
исправленного издателя и ожидания 2 с обе скорости стали 0.

Обнаружение участника DDS не означает доставку нужному подписчику. Совпадение
типа Twist недостаточно: полные имена топиков тоже должны совпасть. Домен
оставался 16; QoS совместим. Файл launch — ресурс на диске, /turtlesim —
запущенная нода, Twist — сообщение между издателем и подписчиком.

## Сохранённый вывод CLI

### `ros2 node list --no-daemon --spin-time 2`

Код: 0; файл: nodes-launched.txt

```text
/turtlesim
```

### `ros2 node list --no-daemon --spin-time 2`

Код: 0; файл: nodes-stopped.txt

```text
```

### `ros2 interface show geometry_msgs/msg/Twist`

Код: 0; файл: twist-interface.txt

```text
# This expresses velocity in free space broken into its linear and angular parts.

Vector3  linear
	float64 x
	float64 y
	float64 z
Vector3  angular
	float64 x
	float64 y
	float64 z
```

### `ros2 topic type /turtle1/pose`

Код: 0; файл: pose-type.txt

```text
turtlesim_msgs/msg/Pose
```

### `ros2 topic echo /turtle1/pose --once`

Код: 0; файл: pose-before.txt

```text
x: 5.544444561004639
y: 5.544444561004639
theta: 0.0
linear_velocity: 0.0
angular_velocity: 0.0
---
```

### `ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'`

Код: 0; файл: publish-once.txt

```text
publisher: beginning loop
publishing #1: geometry_msgs.msg.Twist(linear=geometry_msgs.msg.Vector3(x=1.0, y=0.0, z=0.0), angular=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=0.5))

```

### `ros2 topic echo /turtle1/pose --once`

Код: 0; файл: pose-after-once.txt

```text
x: 6.509308815002441
y: 5.796990871429443
theta: 0.5040000081062317
linear_velocity: 0.0
angular_velocity: 0.0
---
```

### `ros2 topic info /cmd_vel --verbose`

Код: 0; файл: topic-broken.txt

```text
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: _ros2cli_96127
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.1c.5e.7f.77.45.a6.00.00.00.00.00.00.07.03
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (10)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

Subscription count: 0

```

### `ros2 topic info /turtle1/cmd_vel --verbose`

Код: 0; файл: topic-correct-during-fault.txt

```text
Type: geometry_msgs/msg/Twist

Publisher count: 0

Subscription count: 1

Node name: turtlesim
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: SUBSCRIPTION
GID: 01.0f.1c.5e.28.76.79.44.00.00.00.00.00.00.1c.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (7)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

```

### `ros2 topic echo /turtle1/pose --once`

Код: 0; файл: pose-during-fault.txt

```text
x: 6.509308815002441
y: 5.796990871429443
theta: 0.5040000081062317
linear_velocity: 0.0
angular_velocity: 0.0
---
```

### `ros2 topic info /turtle1/cmd_vel --verbose`

Код: 0; файл: topic-fixed.txt

```text
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: _ros2cli_96250
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.1c.5e.fa.77.de.5f.00.00.00.00.00.00.07.03
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (10)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

Subscription count: 1

Node name: turtlesim
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: SUBSCRIPTION
GID: 01.0f.1c.5e.28.76.79.44.00.00.00.00.00.00.1c.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (7)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

```

### `ros2 topic echo /turtle1/pose --once`

Код: 0; файл: pose-after-fix.txt

```text
x: 7.423816680908203
y: 8.206134796142578
theta: 1.9040000438690186
linear_velocity: 1.0
angular_velocity: 0.5
---
```

### `ros2 topic echo /turtle1/pose --once`

Код: 0; файл: pose-stopped.txt

```text
x: 6.720535755157471
y: 9.15625
theta: 2.503999948501587
linear_velocity: 0.0
angular_velocity: 0.0
---
```

## Трудоёмкость

В report.time указана плановая трудоёмкость из условия: одна лабораторная пара (2 академических часа) и около 2 часов самостоятельной работы. Это не измерение времени работы агента и не заявление о посещении пары.
