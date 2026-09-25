# ROS: практические работы

Исходная ПР01 выполнена в ROS 2 Jazzy / WSL2; её evidence сохранено без изменений.
Повторение на этом ПК: Ubuntu 26.04.1, ROS 2 Lyrical, native, домены 16/17.
Результаты повторения: `evidence/pr01-reproduced/`. ПР02: `evidence/pr02/`.

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

Course kit v1-w03 закреплён URL и SHA-256 в `.github/workflows/ci.yml`.
Скачайте и распакуйте его по шагу Download pinned course kit, затем:

```bash
python3 -m py_compile src/turtle_bringup/launch/sim.launch.py
python3 .course-kit/v1/tools/check_practice.py PR02 --submission .
```

GitHub Actions собирает пакет в закреплённом официальном Jazzy-образе из
инструкции курса; локальные опыты выполнены на Lyrical. Это две отдельные
среды: внутри каждой используется только один дистрибутив. GUI проверен локально.
Старый отчёт ПР01 относится к старой версии kit и старому коммиту;
перепроверять его checker-ом ПР02 на новом HEAD некорректно.

Для сдачи нужны SHA evidence-коммита и успешный Actions run именно этого SHA.
`report.json:commit` указывает предыдущий коммит реализации.

Условия: https://ros.lms.ci.nsu.ru/practices/pr01 и
https://ros.lms.ci.nsu.ru/practices/pr02.
