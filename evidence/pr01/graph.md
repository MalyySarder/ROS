# ROS 2 graph

## Nodes

- `/turtlesim`
- `/teleop_turtle`

## Main topics

- `/turtle1/cmd_vel`
- `/turtle1/pose`

## Pose message

`turtlesim/msg/Pose`

## Domain

`ROS_DOMAIN_ID=16`

## Communication test

The communication was intentionally broken by changing `ROS_DOMAIN_ID` from `16` to `17`.

After returning both terminals to `ROS_DOMAIN_ID=16`, `/turtle1/pose` became available again and returned a message successfully (`exit=0`).
