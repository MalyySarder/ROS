# ПР06: фреймы, владельцы и геометрия

Модель взята по размерам из `.course-kit/v1/models/course_ackermann/model.sdf`,
kit v1-w06. Геометрия в метрах; X вперёд, Y влево, Z вверх.
База 0.8, колея 0.62, радиус колеса 0.12, ширина 0.07.
Корпус 1.05×0.52×0.22, visual/collision центр (0,0,0.12).
Корневой base_link находится на уровне осей колёс; мировая pose SDF в URDF не переносится.
У сенсоров в исходном SDF нет visual: маленькие коробки в URDF — только наглядное
обозначение. Их frames совпадают (0.28,0,0.38) согласно исходнику, не разнесены произвольно.

| Parent | Child | Joint / тип | Translation при q=0 | Ось |
|---|---|---|---|---|
| base_link | camera_link | camera_joint / fixed | 0.28,0,0.38 | — |
| base_link | lidar_link | lidar_joint / fixed | 0.28,0,0.38 | — |
| base_link | imu_link | imu_joint / fixed | 0.28,0,0.38 | — |
| base_link | front_left_knuckle | front_left_steering_joint / revolute | 0.4,0.31,0 | Z |
| base_link | front_right_knuckle | front_right_steering_joint / revolute | 0.4,-0.31,0 | Z |
| front_left_knuckle | front_left_wheel | front_left_wheel_joint / continuous | 0,0,0 | Y |
| front_right_knuckle | front_right_wheel | front_right_wheel_joint / continuous | 0,0,0 | Y |
| base_link | rear_left_wheel | rear_left_wheel_joint / continuous | -0.4,0.31,0 | Y |
| base_link | rear_right_wheel | rear_right_wheel_joint / continuous | -0.4,-0.31,0 | Y |

При q=0 все joint rotations — identity; cylinder visual/collision отдельно
повёрнут на pi/2 вокруг X, чтобы ось колеса лежала вдоль Y.
Рулевые пределы ±0.55 рад. Xacro аргументы меняют расстояния и радиусы,
тест проверяет и штатные параметры, и (1.0,0.8,0.15).

Владелец ВСЕХ преобразований таблицы — единственный `/robot_state_publisher`.
Fixed связи идут в `/tf_static` reliable/transient_local, подвижные — в `/tf`
volatile после `/joint_states`. Демонстрационный CLI только публикует JointState,
сам tf не публикует. map/odom не существуют на этом этапе; Fixed Frame RViz=base_link.
Штампы JointState задаются `header: auto`; static tf имеет время 0 и не устаревает
как динамический. Показатель rate=10000 у static в view_frames — служебное
представление статического буфера, не измеренная частота сети.

## Проверено

Сначала проверены корпус и фиксированный lidar, затем добавлены остальные звенья.
Полная модель: 10 links, 9 joints, дерево связно и ациклично, допустимые массы
и положительные физически допустимые диагональные инерции; visual/collision отдельно.
RViz открыт и визуально проверен: Global Status: Ok, корпус, колёса и сенсоры отображаются.
Получены check_urdf и 6 pytest проверок модели, а также colcon test.
У KDL есть предупреждение об инерции root link; URDF валиден, RSP и RViz работают.
Это описание/визуализация, а не динамическая симуляция Ackermann-контроллера.

## Дефект и исправление

В ветке `codex/pr06-lidar-parent-fault` изменён только parent lidar_joint:
base_link → camera_link. Offset остался (0.28,0,0.38).
check_urdf продолжает принимать связное дерево, но test_lidar_parent падает.
Фактический tf base_link→lidar_link стал (0.56,0,0.76) из-за сложения offsets.
В master parent восстановлен: тот же тест проходит и тот же tf2_echo показывает
(0.28,0,0.38). Неверную геометрию нельзя диагностировать одной проверкой синтаксиса.

## Фактическое дерево view_frames

```text
[INFO] [1792132312.200121481] [view_frames]: Listening to tf data for 5.0 seconds...
[INFO] [1792132317.207379537] [view_frames]: Generating graph...
[INFO] [1792132317.211662708] [view_frames]: Result:tf2_msgs.srv.FrameGraph_Response(frame_yaml="front_left_knuckle: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10.200\n  most_recent_transform: 1792132317.204316\n  oldest_transform: 1792132312.204209\n  buffer_length: 5.000\nfront_left_wheel: \n  parent: 'front_left_knuckle'\n  broadcaster: 'default_authority'\n  rate: 10.200\n  most_recent_transform: 1792132317.204316\n  oldest_transform: 1792132312.204209\n  buffer_length: 5.000\nfront_right_knuckle: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10.200\n  most_recent_transform: 1792132317.204316\n  oldest_transform: 1792132312.204209\n  buffer_length: 5.000\nfront_right_wheel: \n  parent: 'front_right_knuckle'\n  broadcaster: 'default_authority'\n  rate: 10.200\n  most_recent_transform: 1792132317.204316\n  oldest_transform: 1792132312.204209\n  buffer_length: 5.000\nrear_left_wheel: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10.200\n  most_recent_transform: 1792132317.204316\n  oldest_transform: 1792132312.204209\n  buffer_length: 5.000\nrear_right_wheel: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10.200\n  most_recent_transform: 1792132317.204316\n  oldest_transform: 1792132312.204209\n  buffer_length: 5.000\ncamera_link: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10000.000\n  most_recent_transform: 0.000000\n  oldest_transform: 0.000000\n  buffer_length: 0.000\nimu_link: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10000.000\n  most_recent_transform: 0.000000\n  oldest_transform: 0.000000\n  buffer_length: 0.000\nlidar_link: \n  parent: 'base_link'\n  broadcaster: 'default_authority'\n  rate: 10000.000\n  most_recent_transform: 0.000000\n  oldest_transform: 0.000000\n  buffer_length: 0.000\n")
[INFO] [1792132317.221983522] [view_frames]: Exporting graph in /tmp/pr06-frames.pdf file...

```

Дефект зафиксирован коммитом `78eb6be` в отдельной ветке. Исправная модель — `2996920`.
Сырые результаты того же теста и tf2_echo до/после находятся в model-check.txt.
