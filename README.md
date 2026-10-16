# ROS: практические работы

Исходная ПР01 выполнена в ROS 2 Jazzy / WSL2; её evidence сохранено без изменений.
Повторение на этом ПК: Ubuntu 26.04.1, ROS 2 Lyrical, native, домены 16/17.
Журналы повторения ПР01 оставлены локально; [архив в истории GitHub](https://github.com/MalyySarder/ROS/tree/6adeb52f4e6a19cf8e18f60675eb2355b09253e6/evidence/pr01-reproduced). ПР02: `evidence/pr02/`. ПР03: `evidence/pr03/`.

## Подготовка каждого терминала

```bash
cd /home/malyysarder/Documents/ChatGPT/ДЗ/ROS
source /opt/ros/lyrical/setup.bash
export ROS_DOMAIN_ID=16
```

На Ubuntu 24.04 / Jazzy замените путь на `/opt/ros/jazzy/setup.bash`.
ROS, turtlesim, colcon, launch и launch_ros на этом ПК уже установлены.

## Повторение ПР01

В терминале A: `ros2 run turtlesim turtlesim_node`.
В B: `ros2 run turtlesim turtle_teleop_key`; стрелки вводятся в B.
В C:

```bash
ros2 node list --no-daemon --spin-time 2
ros2 topic list -t
ros2 node info /turtlesim
POSE_TYPE=$(ros2 topic type /turtle1/pose)
ros2 topic echo /turtle1/pose --once
timeout -s INT 12s ros2 topic hz /turtle1/pose
```

В B остановите teleop (Ctrl+C), задайте `export ROS_DOMAIN_ID=17`, запустите снова.
В C задайте тот же домен и выполните:

```bash
ros2 node list --no-daemon --spin-time 2
timeout 5s ros2 topic echo /turtle1/pose "$POSE_TYPE" --once
echo "exit=$?"
```

Ожидается 124. Верните B и C в домен 16, перезапустите teleop и повторите
ту же команду: поза приходит, exit=0. Остановите A и B перед ПР02.
`export` не меняет домен уже работающего процесса.

## ПР02: сборка и запуск

В свежем терминале с базовой ROS:

```bash
colcon build --symlink-install --packages-select turtle_bringup
source install/setup.bash
ros2 pkg prefix turtle_bringup
ls "$(ros2 pkg prefix turtle_bringup)/share/turtle_bringup/launch"
ros2 launch turtle_bringup sim.launch.py
```

Открывается одно окно turtlesim. Ctrl+C завершает launch и запущенный симулятор.
В другом терминале с тем же доменом (без teleop):

```bash
ros2 node list --no-daemon --spin-time 2
ros2 interface show geometry_msgs/msg/Twist
ros2 topic type /turtle1/pose
ros2 topic echo /turtle1/pose --once
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
ros2 topic echo /turtle1/pose --once
```

Дождитесь остановки. Воспроизведите ошибку:

```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

В C проверьте `ros2 topic info /cmd_vel --verbose` и
`ros2 topic info /turtle1/cmd_vel --verbose`. У неверного топика 1 издатель,
0 подписчиков. Остановите издателя, измените только имя на `/turtle1/cmd_vel`
и повторите: 1 издатель, 1 подписчик, черепаха движется. Остановите издателя.

## Проверка и сдача

Для текущей ПР03 course kit v1-w05 закреплён URL и SHA-256 в `.github/workflows/ci.yml`.
Скачайте и распакуйте его по шагу Download pinned course kit, затем:

```bash
python3 -m py_compile src/turtle_bringup/launch/sim.launch.py
python3 .course-kit/v1/tools/check_practice.py PR03 --submission .
```

GitHub Actions собирает оба пакета и выполняет тесты patrol в закреплённом официальном Jazzy-образе из
инструкции курса; локальные опыты выполнены на Lyrical. Это две отдельные
среды: внутри каждой используется только один дистрибутив. GUI проверен локально.
Старый отчёт ПР01 относится к старой версии kit и старому коммиту;
перепроверять старые отчёты ПР01/ПР02 на новом HEAD некорректно.
Для старых сдач используйте их коммиты и версии kit из соответствующих отчётов.

Для сдачи нужны SHA evidence-коммита и успешный Actions run именно этого SHA.
`report.json:commit` указывает предыдущий коммит реализации.

Условия: https://ros.lms.ci.nsu.ru/practices/pr01 и
https://ros.lms.ci.nsu.ru/practices/pr02.


## ПР03: собственная нода patrol

В свежем терминале подключите базовую ROS и соберите пакеты:

```bash
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install --packages-select turtle_bringup patrol
source install/setup.bash
export ROS_DOMAIN_ID=16
python3 -m pytest src/patrol/test -v
```

В каждом новом терминале подключайте базовую ROS, `install/setup.bash`
и домен 16. В A запустите `ros2 launch turtle_bringup sim.launch.py`.
Убедитесь, что teleop и старые издатели скорости остановлены.

В B сначала запустите ноду без remap:

```bash
ros2 run patrol patrol
```

В C проверьте граф и команду:

```bash
ros2 node info /patrol
ros2 topic echo /cmd_vel --once
ros2 topic info /cmd_vel --verbose
ros2 topic info /turtle1/cmd_vel --verbose
ros2 topic echo /turtle1/pose --once
```

Нода принимает позу, но команда уходит в `/cmd_vel`, где нет подписчика.
Остановите B (Ctrl+C), затем исправьте связь без изменения исходников:

```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

В C повторите проверку и измерьте частоту:

```bash
ros2 node info /patrol
ros2 topic info /turtle1/cmd_vel --verbose
ros2 topic echo /turtle1/cmd_vel --once
timeout --signal=INT 13s ros2 topic hz /turtle1/cmd_vel
ros2 topic echo /turtle1/pose --once
```

Ожидается около 10 Гц; код 124 у timeout означает завершение заданного интервала.
После Ctrl+C в B подождите остановки черепахи: исчезновение ноды не отправляет
нулевую команду. Проверьте нулевые скорости в `/turtle1/pose`.

Нода хранит последнюю позу в callback. Таймер 0.1 с публикует результат чистой
функции: до первой позы — нули, после — linear.x=0.5, angular.z=0.3.
В этой работе нет таймаута устаревшей позы: после первого сообщения сохраняется
последняя поза, как требует базовое задание.

Для проверки нулей до первой позы остановите симулятор и перезапустите patrol;
в C прочитайте `/cmd_vel` с явным типом `geometry_msgs/msg/Twist`.
Пакет выбирает Pose из turtlesim в Jazzy и turtlesim_msgs в Lyrical;
условные зависимости объявлены в package.xml.

Условие ПР03: https://ros.lms.ci.nsu.ru/practices/pr03.


## Состав evidence

В Git оставлены обязательные отчёты и логи сдачи. Подробные журналы отдельных
команд и вспомогательные скрипты оставлены локально и исключены из отслеживания.
Упомянутые в отчётах дополнительные файлы можно посмотреть в
[архивном коммите](https://github.com/MalyySarder/ROS/tree/6adeb52f4e6a19cf8e18f60675eb2355b09253e6/evidence).
Исходники и результаты опытов не менялись при сокращении числа файлов.


## ПР04–ПР06

Каждая работа имеет свой коммит сдачи и CI run; старые отчёты проверяются
на соответствующем коммите, поскольку код развивается от работы к работе.
ПР04: динамические параметры patrol; краткий отчёт и демонстрация —
`evidence/pr04/run.txt`, фактические наблюдения — `parameters.md`.
Текущий course kit: v1-w06. Намеренные дефекты хранятся в отдельных ветках
`codex/pr04-zero-hz-fault` и (после ПР06) `codex/pr06-lidar-parent-fault`;
CI push проверяет master, а не учебные ветки с намеренными ошибками.

ПР05: `ros2 launch course_bringup patrol.launch.py namespace:=robot_a subscriber_reliability:=best_effort record:=true bag_dir:=evidence/pr05/bag`. Демонстрация и краткий отчёт: `evidence/pr05/run.txt`. MCAP остаётся локально.
