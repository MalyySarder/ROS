# Типы сообщений ПР02

> Дополнительные журналы, названные ниже, оставлены локально и доступны в [архиве этой работы](https://github.com/MalyySarder/ROS/tree/6adeb52f4e6a19cf8e18f60675eb2355b09253e6/evidence/pr02). В текущей версии Git сохранены обязательные файлы сдачи; наблюдения не изменены.

| Топик | Тип | Назначение |
|---|---|---|
| /turtle1/cmd_vel | geometry_msgs/msg/Twist | Команда скорости, подписчик /turtlesim |
| /turtle1/pose | turtlesim_msgs/msg/Pose | Положение и фактические скорости, издатель /turtlesim |

Тип Pose подтверждён `ros2 topic type /turtle1/pose` (pose-type.txt).
В исходном Jazzy он назывался turtlesim/msg/Pose; здесь используется Lyrical.

Twist содержит два Vector3: linear.{x,y,z} — линейная скорость (м/с),
angular.{x,y,z} — угловая (рад/с). В плоском turtlesim используем linear.x
для движения вперёд и angular.z для поворота; другие компоненты команды равны 0.
В опыте linear.x=1.0 и angular.z=0.5 (положительный поворот против часовой стрелки).
Структура подтверждена `ros2 interface show geometry_msgs/msg/Twist` (twist-interface.txt).
Pose: x,y — координаты, theta — угол (рад), linear_velocity и angular_velocity — скорости.

Ошибочный /cmd_vel тоже имеет geometry_msgs/msg/Twist, но без подписчиков.
Соответствие одного типа не связывает разные полные имена топиков.
