# Повторение ПР01 на новом ПК — 2026-09-25

Согласованное отличие: native Ubuntu 26.04.1 / Lyrical вместо Jazzy / WSL2.
Исходная сдача в ../pr01 сохранена. Это журнал повторения, не новая сдача ПР01.

Запущены `ros2 run turtlesim turtlesim_node` и `ros2 run turtlesim turtle_teleop_key`.
Стрелка вверх передана в настоящий PTY teleop. Первый замер позы сделан уже
после начала движения, поэтому это не исходная точка спавна.
В домене 16 x вырос с 5.6084447 до 7.5604444; после перевода teleop в 17
повторная стрелка не изменила позу. После возврата teleop в 16 x=9.5764446.

Симулятор публикует /turtle1/pose (turtlesim_msgs/msg/Pose), teleop публикует
/turtle1/cmd_vel (geometry_msgs/msg/Twist), симулятор подписан на cmd_vel.
Частота: последние средние 62.500 Гц, `timeout -s INT 12s ros2 topic hz /turtle1/pose`.
Экспорт домена действует на новые процессы: teleop перезапущен, turtlesim не менялся.

Команды наблюдения и сырые результаты:

## `ros2 node list --no-daemon --spin-time 2`

```text
/teleop_turtle
/turtlesim
```

## `ros2 topic list -t`

```text
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim_msgs/msg/Color]
/turtle1/pose [turtlesim_msgs/msg/Pose]
```

## `ros2 node info /turtlesim`

```text
/turtlesim
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /turtle1/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /turtle1/color_sensor: turtlesim_msgs/msg/Color
    /turtle1/pose: turtlesim_msgs/msg/Pose
  Service Servers:
    /clear: std_srvs/srv/Empty
    /kill: turtlesim_msgs/srv/Kill
    /reset: std_srvs/srv/Empty
    /spawn: turtlesim_msgs/srv/Spawn
    /turtle1/set_pen: turtlesim_msgs/srv/SetPen
    /turtle1/teleport_absolute: turtlesim_msgs/srv/TeleportAbsolute
    /turtle1/teleport_relative: turtlesim_msgs/srv/TeleportRelative
    /turtlesim/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /turtlesim/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /turtlesim/get_parameters: rcl_interfaces/srv/GetParameters
    /turtlesim/get_type_description: type_description_interfaces/srv/GetTypeDescription
    /turtlesim/list_parameters: rcl_interfaces/srv/ListParameters
    /turtlesim/set_parameters: rcl_interfaces/srv/SetParameters
    /turtlesim/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
  Service Clients:

  Action Servers:
    /turtle1/rotate_absolute: turtlesim_msgs/action/RotateAbsolute
  Action Clients:

```

## `ROS_DOMAIN_ID=17 ros2 node list --no-daemon --spin-time 2`

```text
/teleop_turtle
```

## `ROS_DOMAIN_ID=17 timeout 5s ros2 topic echo /turtle1/pose turtlesim_msgs/msg/Pose --once`

```text
exit=124
```

## `ROS_DOMAIN_ID=16 ros2 node list --no-daemon --spin-time 2`

```text
/teleop_turtle
/turtlesim
```

## `ROS_DOMAIN_ID=16 timeout 5s ros2 topic echo /turtle1/pose turtlesim_msgs/msg/Pose --once`

```text
x: 9.576444625854492
y: 5.544444561004639
theta: 0.0
linear_velocity: 0.0
angular_velocity: 0.0
---
exit=0
```
