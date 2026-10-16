# ПР03. Первая нода: поза и команда

> Дополнительные журналы, названные ниже, оставлены локально и доступны в [архиве этой работы](https://github.com/MalyySarder/ROS/tree/6adeb52f4e6a19cf8e18f60675eb2355b09253e6/evidence/pr03). В текущей версии Git сохранены обязательные файлы сдачи; наблюдения не изменены.

## Среда и реализация

Локально: Ubuntu 26.04 / ROS 2 Lyrical, домен 16, native. Pose имеет тип
`turtlesim_msgs/msg/Pose` (вывод сохранён в pose-type.txt).
Пакет turtle_bringup из ПР02 сохранён. Рядом создан ament_python-пакет patrol:

```bash
ros2 pkg create --build-type ament_python --node-name patrol patrol \
  --dependencies rclpy geometry_msgs --license Apache-2.0 \
  --maintainer-name Nikita --maintainer-email niknikivan@gmail.com \
  --description 'Pose subscription and timed velocity publisher for PR03'
```

В package.xml добавлены условные зависимости на turtlesim_msgs (Lyrical)
и turtlesim (Jazzy); CI использует Jazzy, как и в ПР02. Одна среда импортирует
один соответствующий тип Pose. Команда запуска установлена через console_scripts.

Сначала реализован минимальный init/Node/spin без подписки и таймера.
Сборка: build-minimal.txt; исходник этого этапа: minimal-node.py.txt;
`ros2 node list --no-daemon --spin-time 2` обнаружил /patrol (minimal-nodes.txt).
После этого добавлены подписка и таймер, итоговая сборка — build.txt.

## Как работает нода

- `rclpy.init()` инициализирует контекст ROS и обрабатывает ROS-аргументы, включая remap.
- Создание `Patrol` регистрирует /patrol, подписку на /turtle1/pose,
  издатель в относительный cmd_vel и таймер с периодом 0.1 с.
- `rclpy.spin(node)` обслуживает executor: ожидает события и вызывает готовые callbacks.
- Callback подписки только сохраняет последнее сообщение в latest_pose.
  Объект подписки хранится в поле pose_subscription.
- Callback таймера публикует результат чистой функции command_from_pose.
  Она не обращается к ROS-графу: до первой позы возвращает все нули,
  после первой позы — linear.x=0.5, angular.z=0.3, остальные компоненты 0.
  Каждый вызов возвращает новый Twist и не меняет входную позу.
- Ctrl+C вызывает завершение spin. finally освобождает ноду и контекст.
  Нода при завершении не отправляет отдельный тормозной Twist: нужно дождаться
  таймаута команды в turtlesim. Это проверено по скорости и двум последовательным позам.

Последняя поза хранится до следующего сообщения. Таймаут устаревшей позы,
динамические параметры и маршрут мышью в обязательную часть не добавлялись.

## Сборка и тесты

```bash
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install --packages-select patrol
source install/setup.bash
python3 -m pytest src/patrol/test -v
```

Вывод — tests.txt. Четыре теста поведения проверяют отсутствие позы, обычное
сообщение без изменения входа, допустимость нулевой позы и отсутствие общего
изменяемого состояния между командами. Остальные проверки: copyright,
flake8, mypy, pep257, xmllint. Линтеры ограничены каталогом пакета через
conftest.py, поэтому команда из корня workspace не проверяет build/install
и сохранённые журналы прошлых работ.

## Живой опыт: до / сбой / после

В каждом терминале подключены базовая ROS, install/setup.bash и ROS_DOMAIN_ID=16.
Старые издатели и teleop не работали.

1. Запущен `ros2 run patrol patrol` без симулятора. Чтение
   `ros2 topic echo /cmd_vel geometry_msgs/msg/Twist --once` показало нулевой Twist:
   команда публикуется таймером даже до первой позы.
2. Запущен `ros2 launch turtle_bringup sim.launch.py`. /patrol подписана на позу,
   после её получения публикует (0.5, 0.3), но в /cmd_vel.
3. `ros2 topic info /cmd_vel --verbose` показывает 1 издателя и 0 подписчиков.
   `/turtle1/cmd_vel` имеет 0 издателей и 1 подписчика (/turtlesim).
   В node info /patrol видна подписка /turtle1/pose, значит причина не в отсутствии позы.
   Две позы подтверждают отсутствие движения.
4. Patrol остановлена SIGINT (тот же сигнал, что Ctrl+C), затем запущена так:

```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

Изменено только сопоставление имени: исходный код, домен, скорости, период
и симулятор не менялись. Относительное cmd_vel в корневом namespace разрешалось
в /cmd_vel; remap направил тот же издатель в /turtle1/cmd_vel.
Теперь 1 publisher и 1 subscription; команды до/после имеют одинаковые значения,
а черепаха движется. Наличие издателя в графе не означает доставку подписчику
другого топика даже при одинаковом типе Twist.

5. Выполнен `timeout --signal=INT 13s ros2 topic hz /turtle1/cmd_vel`.
   Код 124 — ожидаемое завершение по времени; вывод frequency.txt содержит
   больше 10 секунд наблюдения после обнаружения издателя.
6. После SIGINT patrol подождали 2 секунды, прочитали позу, затем повторили
   измерение после дополнительной секунды. Скорости нулевые, поза не меняется;
   /patrol исчезла из node list, число издателей cmd_vel стало 0.
   Затем остановлен launch. Журналы завершения: patrol-remapped.txt, simulator.txt.

Последняя средняя частота: **10.000 Гц**, диапазон средних в журнале 9.997–10.000 Гц.

| Стадия | x | y | theta | linear_velocity | angular_velocity |
|---|---:|---:|---:|---:|---:|
| До | 5.544445 | 5.544445 | 0.000000 | 0.000000 | 0.000000 |
| Без remap | 5.544445 | 5.544445 | 0.000000 | 0.000000 | 0.000000 |
| С remap | 5.536469 | 5.544445 | -0.004785 | 0.500000 | 0.300000 |
| После остановки patrol | 6.116346 | 5.647100 | 0.350415 | 0.000000 | 0.000000 |
| Повтор после ожидания | 6.116346 | 5.647100 | 0.350415 | 0.000000 | 0.000000 |

За время измерения черепаха прошла почти полный круг: финальная точка близка
к исходной, но отличается; в момент измерения скорости равны 0.5 и 0.3.
После остановки patrol черепаха ещё успела пройти участок до прекращения команды,
поэтому точка окончательной остановки отличается от позы при работающей ноде.

## Сырые результаты

Список выполненных команд с кодами завершения — executed-commands.json.
Ниже ключевые наблюдения, без замены результата ожидаемым выводом.

### ros2 topic echo /cmd_vel geometry_msgs/msg/Twist --once (до симулятора)

```text
linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

### ros2 node info /patrol (без remap)

```text
/patrol
  Subscribers:
    /turtle1/pose: turtlesim_msgs/msg/Pose
  Publishers:
    /cmd_vel: geometry_msgs/msg/Twist
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
  Service Servers:
    /patrol/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /patrol/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /patrol/get_parameters: rcl_interfaces/srv/GetParameters
    /patrol/get_type_description: type_description_interfaces/srv/GetTypeDescription
    /patrol/list_parameters: rcl_interfaces/srv/ListParameters
    /patrol/set_parameters: rcl_interfaces/srv/SetParameters
    /patrol/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
  Service Clients:

  Action Servers:

  Action Clients:
```

### ros2 topic info /cmd_vel --verbose

```text
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: patrol
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.1c.5e.48.33.6b.e2.00.00.00.00.00.00.14.03
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

### ros2 topic info /turtle1/cmd_vel --verbose (до remap)

```text
Type: geometry_msgs/msg/Twist

Publisher count: 0

Subscription count: 1

Node name: turtlesim
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: SUBSCRIPTION
GID: 01.0f.1c.5e.b5.33.7d.aa.00.00.00.00.00.00.1c.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (7)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite
```

### ros2 topic info /turtle1/cmd_vel --verbose (после remap)

```text
Type: geometry_msgs/msg/Twist

Publisher count: 1

Node name: patrol
Node namespace: /
Topic type: geometry_msgs/msg/Twist
Topic type hash: RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a
Endpoint type: PUBLISHER
GID: 01.0f.1c.5e.58.35.ed.2e.00.00.00.00.00.00.14.03
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
GID: 01.0f.1c.5e.b5.33.7d.aa.00.00.00.00.00.00.1c.04
QoS profile:
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (7)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite
```

### timeout --signal=INT 13s ros2 topic hz /turtle1/cmd_vel

```text
average rate: 9.997
	min: 0.100s max: 0.100s std dev: 0.00013s window: 9
average rate: 9.997
	min: 0.100s max: 0.100s std dev: 0.00018s window: 19
average rate: 9.998
	min: 0.100s max: 0.100s std dev: 0.00019s window: 29
average rate: 9.998
	min: 0.100s max: 0.100s std dev: 0.00019s window: 39
average rate: 9.999
	min: 0.099s max: 0.100s std dev: 0.00021s window: 49
average rate: 9.999
	min: 0.099s max: 0.100s std dev: 0.00020s window: 59
average rate: 9.999
	min: 0.099s max: 0.100s std dev: 0.00020s window: 69
average rate: 9.999
	min: 0.099s max: 0.100s std dev: 0.00022s window: 79
average rate: 9.999
	min: 0.099s max: 0.100s std dev: 0.00023s window: 89
average rate: 10.000
	min: 0.099s max: 0.100s std dev: 0.00023s window: 99
average rate: 10.000
	min: 0.099s max: 0.100s std dev: 0.00023s window: 109
```

### ros2 topic echo /turtle1/pose --once (после остановки)

```text
x: 6.1163458824157715
y: 5.64709997177124
theta: 0.3504146933555603
linear_velocity: 0.0
angular_velocity: 0.0
---
```

## Сдача

Course kit: v1-w05, SHA-256 bca214e3de6f90f9513049dfa0f36fee65ad834da502dc3f3f8fb443517b5197.
В report.commit записывается коммит реализации; этот отчёт добавляется следующим
коммитом. CI собирает пакеты и выполняет tests/checker для текущей ПР03.
В report.time указана плановая трудоёмкость из условия: одна пара (2 академических
часа) и около 2 часов самостоятельной доработки; это не измерение времени агента.
