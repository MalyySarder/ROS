# Одометрия и TF — ПР07

Gazebo выдаёт `/model/course_ackermann/odometry`. Мост переносит сообщение в
`/vehicle/odom_gz` с исходными `header.frame_id="course_ackermann/odom"` и
`child_frame_id="course_ackermann/base_link"`.

`course_simulation/odom_adapter` принимает только эту пару frames и только
конечные значения pose, quaternion, twist и обеих covariance. Он копирует всё
сообщение и меняет ровно две строки на `odom` и `base_link`, публикуя результат
в `/vehicle/odom`. Повторная нормализация уже нормализованного сообщения запрещена.
Одновременно публикуется `TransformStamped`: тот же stamp, pose.position и
pose.orientation. Подстановка времени получения вместо исходного stamp не делается.

## Владельцы

- `odom → base_link`: только `/robot_a/odom_adapter`, динамический `/tf`.
- `base_link → camera_link`, `base_link → lidar_link`, `base_link → imu_link`:
  `/robot_a/robot_state_publisher`, `/tf_static`, reliable + transient local.
- У robot_state_publisher также существует издатель `/tf` для подвижных сочленений.
  Поэтому два DDS-издателя самого топика `/tf` допустимы: проверяется уникальность
  владельца конкретного ребра. В этом запуске joint_states колёс не передаются;
  их реальное вращение проверено через Gazebo dynamic_pose, а не выдуманные TF.
- Встроенный Gazebo `/model/course_ackermann/tf` в ROS не мостится.

Все узлы запускаются с `use_sim_time=true`. Namespace узлов — `robot_a`;
контрактные имена топиков и frames сохраняются.

## Проверки

В unit-тесте исходный stamp `123 s + 456789 ns`, ненулевые pose/twist и разные
массивы covariance после нормализации полностью совпадают с входом. Исходное
сообщение не изменяется; TF повторяет stamp/pose результата. Отдельные тесты
отклоняют чужие frames, уже нормализованные frames, NaN/inf, в том числе covariance.

В живом запуске сопоставлены 30 одинаковых stamps сразу на `/vehicle/odom_gz`,
`/vehicle/odom` и `/tf`: полное равенство полей и ожидаемое преобразование frames.
По DDS publisher GID подтверждён один источник ребра `odom → base_link`:
`odom_adapter`. Все три fixed-связи имеют смещение `[0.28, 0, 0.38]` от base_link.
RViz с Fixed Frame=base_link показал корпус и сенсоры, Global Status: Ok.
Без joint_states у RobotModel остаются предупреждения о подвижных колёсных frames;
это не используется как доказательство их физического движения.

MCAP содержит нормализованную одометрию, динамический и статический TF.
При воспроизведении в ПР08 адаптер одометрии и RSP повторно запускать не нужно:
используются сохранённые `/tf` и `/tf_static`, чтобы не создавать дубликаты.
