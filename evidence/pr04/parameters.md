# ПР04: реальные команды и результаты
ROS 2 Lyrical, домен 16.

$ ros2 launch turtle_bringup sim.launch.py [background]

$ ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel [background]

$ ros2 param list /patrol

  linear_speed
  publish_hz
  start_type_description_service
  turn_rate
  use_sim_time


exit=0

$ timeout --signal=INT 12s ros2 topic hz /turtle1/cmd_vel

average rate: 9.995
	min: 0.100s max: 0.100s std dev: 0.00025s window: 9
average rate: 10.000
	min: 0.100s max: 0.100s std dev: 0.00025s window: 19
average rate: 9.999
	min: 0.100s max: 0.100s std dev: 0.00023s window: 29
average rate: 10.000
	min: 0.100s max: 0.100s std dev: 0.00023s window: 39
average rate: 10.000
	min: 0.100s max: 0.100s std dev: 0.00025s window: 49
average rate: 10.000
	min: 0.099s max: 0.100s std dev: 0.00025s window: 59
average rate: 10.000
	min: 0.099s max: 0.100s std dev: 0.00025s window: 69
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00026s window: 79
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00025s window: 89
average rate: 10.000
	min: 0.099s max: 0.101s std dev: 0.00026s window: 99


exit=124

$ ros2 param set /patrol publish_hz 5.0

Set parameter successful


exit=0

$ timeout --signal=INT 12s ros2 topic hz /turtle1/cmd_vel

average rate: 4.998
	min: 0.200s max: 0.200s std dev: 0.00014s window: 4
average rate: 5.000
	min: 0.200s max: 0.200s std dev: 0.00015s window: 9
average rate: 4.999
	min: 0.200s max: 0.200s std dev: 0.00019s window: 14
average rate: 5.000
	min: 0.200s max: 0.200s std dev: 0.00022s window: 19
average rate: 5.000
	min: 0.200s max: 0.200s std dev: 0.00021s window: 24
average rate: 5.000
	min: 0.200s max: 0.200s std dev: 0.00021s window: 29
average rate: 5.000
	min: 0.200s max: 0.200s std dev: 0.00020s window: 34
average rate: 5.000
	min: 0.200s max: 0.200s std dev: 0.00019s window: 39
average rate: 5.000
	min: 0.199s max: 0.201s std dev: 0.00021s window: 44


exit=124

$ ros2 param set /patrol publish_hz 0.0

Setting parameter failed: publish_hz must be finite and in [1.0, 30.0]


exit=0

$ ros2 param get /patrol publish_hz

Double value is: 5.0


exit=0

$ timeout --signal=INT 12s ros2 topic hz /turtle1/cmd_vel

average rate: 5.001
	min: 0.200s max: 0.200s std dev: 0.00021s window: 4
average rate: 5.001
	min: 0.200s max: 0.200s std dev: 0.00019s window: 9
average rate: 5.000
	min: 0.200s max: 0.201s std dev: 0.00023s window: 14
average rate: 5.001
	min: 0.199s max: 0.201s std dev: 0.00025s window: 19
average rate: 5.000
	min: 0.199s max: 0.201s std dev: 0.00024s window: 24
average rate: 5.001
	min: 0.199s max: 0.201s std dev: 0.00023s window: 29
average rate: 5.000
	min: 0.199s max: 0.201s std dev: 0.00023s window: 34
average rate: 5.000
	min: 0.199s max: 0.201s std dev: 0.00026s window: 39
average rate: 5.000
	min: 0.199s max: 0.201s std dev: 0.00025s window: 44
average rate: 5.000
	min: 0.199s max: 0.201s std dev: 0.00025s window: 49


exit=124

$ ros2 param set /patrol linear_speed 0.7

Set parameter successful


exit=0

$ ros2 param set /patrol turn_rate -0.4

Set parameter successful


exit=0

$ ros2 topic echo /turtle1/cmd_vel --once

linear:
  x: 0.7
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: -0.4
---


exit=0

$ ros2 service call /clear std_srvs/srv/Empty '{}'

waiting for service to become available...
requester: making request: std_srvs.srv.Empty_Request()

response:
std_srvs.srv.Empty_Response()



exit=0

$ ros2 action list -t

/turtle1/rotate_absolute [turtlesim_msgs/action/RotateAbsolute]


exit=0

background exit=0

background exit=0

Вывод: 10→5 Гц меняет поток; 0 отклонён до изменения состояния, значение и поток 5 Гц сохранены. Скорость и поворот обновляются без перезапуска. /clear — короткий запрос с одним ответом. /turtle1/rotate_absolute — длительная цель с обратной связью, результатом и возможностью отмены.

Background log:
[INFO] [launch]: All log files can be found below /home/malyysarder/.ros/log/2026-10-16-13-21-15-340993-malyysarder-Nitro-AN515-57-51865
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [turtlesim_node-1]: process started with pid [51886]
[turtlesim_node-1] [INFO] [1792131675.931555482] [turtlesim]: Starting turtlesim with node name /turtlesim
[turtlesim_node-1] [INFO] [1792131675.949479732] [turtlesim]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]
[turtlesim_node-1] [WARN] [1792131733.009196515] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.928278, y=-0.009825])
[turtlesim_node-1] [WARN] [1792131733.025687676] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.931506, y=-0.010725])
[turtlesim_node-1] [WARN] [1792131733.041255301] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.934802, y=-0.010704])
[turtlesim_node-1] [WARN] [1792131733.057708584] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.938167, y=-0.010683])
[turtlesim_node-1] [WARN] [1792131733.073209870] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.941601, y=-0.010661])
[turtlesim_node-1] [WARN] [1792131733.089733773] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.945102, y=-0.010639])
[turtlesim_node-1] [WARN] [1792131733.105460237] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.948672, y=-0.010616])
[turtlesim_node-1] [WARN] [1792131733.122050666] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.952309, y=-0.010593])
[turtlesim_node-1] [WARN] [1792131733.137565363] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.956014, y=-0.010569])
[turtlesim_node-1] [WARN] [1792131733.154118373] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.959787, y=-0.010545])
[turtlesim_node-1] [WARN] [1792131733.169849896] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.963627, y=-0.010521])
[turtlesim_node-1] [WARN] [1792131733.185289804] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.967535, y=-0.010496])
[turtlesim_node-1] [WARN] [1792131733.201775903] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.971509, y=-0.010471])
[turtlesim_node-1] [WARN] [1792131733.217321015] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.975550, y=-0.010445])
[turtlesim_node-1] [WARN] [1792131733.233791554] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.979659, y=-0.010419])
[turtlesim_node-1] [WARN] [1792131733.249145600] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.983833, y=-0.010393])
[turtlesim_node-1] [WARN] [1792131733.265445332] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.988075, y=-0.010366])
[turtlesim_node-1] [WARN] [1792131733.281873416] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.992382, y=-0.010339])
[turtlesim_node-1] [WARN] [1792131733.297489408] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=4.996756, y=-0.010311])
[turtlesim_node-1] [WARN] [1792131733.314029885] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.001195, y=-0.010283])
[turtlesim_node-1] [WARN] [1792131733.329404240] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.005700, y=-0.010254])
[turtlesim_node-1] [INFO] [1792131733.345810256] [turtlesim]: Clearing turtlesim.
[turtlesim_node-1] [WARN] [1792131733.346024171] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.010271, y=-0.010225])
[turtlesim_node-1] [WARN] [1792131733.361365005] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.014907, y=-0.010195])
[turtlesim_node-1] [WARN] [1792131733.377977110] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.019608, y=-0.010166])
[turtlesim_node-1] [WARN] [1792131733.393665734] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.024374, y=-0.010135])
[turtlesim_node-1] [WARN] [1792131733.409430790] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.029205, y=-0.010105])
[turtlesim_node-1] [WARN] [1792131733.426135165] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.034100, y=-0.010073])
[turtlesim_node-1] [WARN] [1792131733.442046570] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.039060, y=-0.010042])
[turtlesim_node-1] [WARN] [1792131733.457816029] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.044084, y=-0.010010])
[turtlesim_node-1] [WARN] [1792131733.473520849] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.049172, y=-0.009978])
[turtlesim_node-1] [WARN] [1792131733.489336853] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.054324, y=-0.009945])
[turtlesim_node-1] [WARN] [1792131733.506041987] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.059539, y=-0.009912])
[turtlesim_node-1] [WARN] [1792131733.521524036] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.064818, y=-0.009878])
[turtlesim_node-1] [WARN] [1792131733.537997089] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.070160, y=-0.009844])
[turtlesim_node-1] [WARN] [1792131733.553581642] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.075564, y=-0.009810])
[turtlesim_node-1] [WARN] [1792131733.569175762] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.081031, y=-0.009775])
[turtlesim_node-1] [WARN] [1792131733.585593654] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.086561, y=-0.009740])
[turtlesim_node-1] [WARN] [1792131733.602073743] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.092153, y=-0.009704])
[turtlesim_node-1] [WARN] [1792131733.617654459] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.097807, y=-0.009668])
[turtlesim_node-1] [WARN] [1792131733.633167179] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.103523, y=-0.009632])
[turtlesim_node-1] [WARN] [1792131733.649661012] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.109300, y=-0.009595])
[turtlesim_node-1] [WARN] [1792131733.666136239] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.115138, y=-0.009558])
[turtlesim_node-1] [WARN] [1792131733.681603260] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.121038, y=-0.009520])
[turtlesim_node-1] [WARN] [1792131733.698179693] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.126998, y=-0.009482])
[turtlesim_node-1] [WARN] [1792131733.713786202] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.133019, y=-0.009444])
[turtlesim_node-1] [WARN] [1792131733.729339065] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.139100, y=-0.009405])
[turtlesim_node-1] [WARN] [1792131733.745884014] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.145242, y=-0.009366])
[turtlesim_node-1] [WARN] [1792131733.761418797] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.151443, y=-0.009327])
[turtlesim_node-1] [WARN] [1792131733.777964074] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.157703, y=-0.009287])
[turtlesim_node-1] [WARN] [1792131733.793484603] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.164023, y=-0.009246])
[turtlesim_node-1] [WARN] [1792131733.809964807] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.170403, y=-0.009206])
[turtlesim_node-1] [WARN] [1792131733.825482568] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.176840, y=-0.009165])
[turtlesim_node-1] [WARN] [1792131733.842131318] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.183337, y=-0.009123])
[turtlesim_node-1] [WARN] [1792131733.857665984] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.189891, y=-0.009082])
[turtlesim_node-1] [WARN] [1792131733.874148783] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.196504, y=-0.009040])
[turtlesim_node-1] [WARN] [1792131733.889737317] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.203174, y=-0.008997])
[turtlesim_node-1] [WARN] [1792131733.905354498] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.209902, y=-0.008954])
[turtlesim_node-1] [WARN] [1792131733.921792913] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.216687, y=-0.008911])
[turtlesim_node-1] [WARN] [1792131733.937254509] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.223529, y=-0.008867])
[turtlesim_node-1] [WARN] [1792131733.953727658] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.230427, y=-0.008823])
[turtlesim_node-1] [WARN] [1792131733.969190705] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.237382, y=-0.008779])
[turtlesim_node-1] [WARN] [1792131733.985708029] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.244393, y=-0.008734])
[turtlesim_node-1] [WARN] [1792131734.001247516] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.251459, y=-0.008689])
[turtlesim_node-1] [WARN] [1792131734.018238059] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.258581, y=-0.008644])
[turtlesim_node-1] [WARN] [1792131734.034096535] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.265758, y=-0.008598])
[turtlesim_node-1] [WARN] [1792131734.049729348] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.272990, y=-0.008552])
[turtlesim_node-1] [WARN] [1792131734.067918256] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.280277, y=-0.008506])
[turtlesim_node-1] [WARN] [1792131734.081499481] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.287618, y=-0.008459])
[turtlesim_node-1] [WARN] [1792131734.098988355] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.295013, y=-0.008412])
[turtlesim_node-1] [WARN] [1792131734.113648817] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.302462, y=-0.008364])
[turtlesim_node-1] [WARN] [1792131734.129195841] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.309964, y=-0.008316])
[turtlesim_node-1] [WARN] [1792131734.145733946] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.317519, y=-0.008268])
[turtlesim_node-1] [WARN] [1792131734.161284446] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.325127, y=-0.008220])
[turtlesim_node-1] [WARN] [1792131734.177716788] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.332787, y=-0.008171])
[turtlesim_node-1] [WARN] [1792131734.193167567] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.340499, y=-0.008122])
[turtlesim_node-1] [WARN] [1792131734.209516939] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.348263, y=-0.008072])
[turtlesim_node-1] [WARN] [1792131734.225994248] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.356079, y=-0.008022])
[turtlesim_node-1] [WARN] [1792131734.241492305] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.363946, y=-0.007972])
[turtlesim_node-1] [WARN] [1792131734.257940622] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.371864, y=-0.007921])
[turtlesim_node-1] [WARN] [1792131734.273412154] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.379832, y=-0.007871])
[turtlesim_node-1] [WARN] [1792131734.289944937] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.387851, y=-0.007819])
[turtlesim_node-1] [WARN] [1792131734.305439564] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.395919, y=-0.007768])
[turtlesim_node-1] [WARN] [1792131734.321906174] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.404037, y=-0.007716])
[turtlesim_node-1] [WARN] [1792131734.337386453] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.412204, y=-0.007664])
[turtlesim_node-1] [WARN] [1792131734.353891234] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.420420, y=-0.007612])
[turtlesim_node-1] [WARN] [1792131734.369338973] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.428685, y=-0.007559])
[turtlesim_node-1] [WARN] [1792131734.385825996] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.436997, y=-0.007506])
[turtlesim_node-1] [WARN] [1792131734.401312588] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.445358, y=-0.007452])
[turtlesim_node-1] [WARN] [1792131734.417730266] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.453766, y=-0.007399])
[turtlesim_node-1] [WARN] [1792131734.433156758] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.462222, y=-0.007345])
[turtlesim_node-1] [WARN] [1792131734.449564462] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.470724, y=-0.007291])
[turtlesim_node-1] [WARN] [1792131734.466085582] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.479273, y=-0.007236])
[turtlesim_node-1] [WARN] [1792131734.481596120] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.487867, y=-0.007181])
[turtlesim_node-1] [WARN] [1792131734.498170284] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.496508, y=-0.007126])
[turtlesim_node-1] [WARN] [1792131734.513653020] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.505194, y=-0.007071])
[turtlesim_node-1] [WARN] [1792131734.529199387] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.513925, y=-0.007015])
[turtlesim_node-1] [WARN] [1792131734.545800963] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.522701, y=-0.006959])
[turtlesim_node-1] [WARN] [1792131734.561280086] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.531521, y=-0.006903])
[turtlesim_node-1] [WARN] [1792131734.577712719] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.540385, y=-0.006846])
[turtlesim_node-1] [WARN] [1792131734.593129741] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.549293, y=-0.006789])
[turtlesim_node-1] [WARN] [1792131734.609566380] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.558244, y=-0.006732])
[turtlesim_node-1] [WARN] [1792131734.626260128] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.567238, y=-0.006674])
[turtlesim_node-1] [WARN] [1792131734.641971221] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.576275, y=-0.006617])
[turtlesim_node-1] [WARN] [1792131734.657638904] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.585353, y=-0.006559])
[turtlesim_node-1] [WARN] [1792131734.673453208] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.594474, y=-0.006501])
[turtlesim_node-1] [WARN] [1792131734.690229020] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.603636, y=-0.006442])
[turtlesim_node-1] [WARN] [1792131734.706051529] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.612838, y=-0.006383])
[turtlesim_node-1] [WARN] [1792131734.721793668] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.622082, y=-0.006324])
[turtlesim_node-1] [WARN] [1792131734.737577806] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.631366, y=-0.006265])
[turtlesim_node-1] [WARN] [1792131734.753203249] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.640690, y=-0.006205])
[turtlesim_node-1] [WARN] [1792131734.769752396] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.650053, y=-0.006146])
[turtlesim_node-1] [WARN] [1792131734.785309125] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.659455, y=-0.006086])
[turtlesim_node-1] [WARN] [1792131734.802009592] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.668897, y=-0.006025])
[turtlesim_node-1] [WARN] [1792131734.817652383] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.678376, y=-0.005965])
[turtlesim_node-1] [WARN] [1792131734.833380818] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.687894, y=-0.005904])
[turtlesim_node-1] [WARN] [1792131734.849968530] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.697449, y=-0.005843])
[turtlesim_node-1] [WARN] [1792131734.865549360] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.707041, y=-0.005782])
[turtlesim_node-1] [WARN] [1792131734.882178278] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.716670, y=-0.005720])
[turtlesim_node-1] [WARN] [1792131734.897668027] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.726336, y=-0.005658])
[turtlesim_node-1] [WARN] [1792131734.913168804] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.736037, y=-0.005596])
[turtlesim_node-1] [WARN] [1792131734.929542567] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.745774, y=-0.005534])
[turtlesim_node-1] [WARN] [1792131734.945895431] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.755547, y=-0.005472])
[turtlesim_node-1] [WARN] [1792131734.961247374] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.765354, y=-0.005409])
[turtlesim_node-1] [WARN] [1792131734.977658904] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.775196, y=-0.005346])
[turtlesim_node-1] [WARN] [1792131734.993203820] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.785071, y=-0.005283])
[turtlesim_node-1] [WARN] [1792131735.009745146] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.794981, y=-0.005220])
[turtlesim_node-1] [WARN] [1792131735.025342546] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.804923, y=-0.005156])
[turtlesim_node-1] [WARN] [1792131735.042042469] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.814898, y=-0.005093])
[turtlesim_node-1] [WARN] [1792131735.057607225] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.824906, y=-0.005029])
[turtlesim_node-1] [WARN] [1792131735.073195688] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.834946, y=-0.004964])
[turtlesim_node-1] [WARN] [1792131735.089720262] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.845017, y=-0.004900])
[turtlesim_node-1] [WARN] [1792131735.105297715] [turtlesim]: Oh no! I hit the wall! (Clamping from [x=5.855119, y=-0.004836])
[WARNING] [launch]: user interrupted with ctrl-c (SIGINT)
[turtlesim_node-1] [INFO] [1792131735.111067759] [rclcpp]: signal_handler(signum=2)
[INFO] [turtlesim_node-1]: sending signal 'SIGINT' to process[turtlesim_node-1]
[turtlesim_node-1] [INFO] [1792131735.114433882] [rclcpp]: signal_handler(signum=2)
[INFO] [turtlesim_node-1]: process has finished cleanly [pid 51886]


Background log:
[ros2run]: Received signal:  Interrupt


## Намеренный дефект в отдельной ветке
Коммит: 0fa85cee781e804f81c10b61c60ff1683a308013
Домен 17 изолирует опыт от исправной ноды. Отключена только проверка publish_hz.
$ ros2 param set /patrol publish_hz 0.0

CLI exit=124; node exit=1
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/tmp/ros-pr04-fault/src/patrol/patrol/patrol.py", line 90, in <module>
    main()
    ~~~~^^
  File "/tmp/ros-pr04-fault/src/patrol/patrol/patrol.py", line 80, in main
    rclpy.spin(node)
    ~~~~~~~~~~^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/__init__.py", line 324, in spin
    executor.spin_once()
    ~~~~~~~~~~~~~~~~~~^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 1020, in spin_once
    self._spin_once_impl(timeout_sec)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 1012, in _spin_once_impl
    raise exception
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/task.py", line 343, in _execute_coroutine_step
    result = coro.send(None)
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 670, in handler
    await call_coroutine()
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 604, in _execute
    response = await await_or_execute(srv.callback, request, srv.srv_type.Response())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/executors.py", line 139, in await_or_execute
    return callback(*args)
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/parameter_service.py", line 142, in _set_parameters_callback
    result = node.set_parameters_atomically([param])
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 820, in set_parameters_atomically
    return self._set_parameters_atomically(parameter_list)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 840, in _set_parameters_atomically
    return self._set_parameters_atomically_common(parameter_list)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 944, in _set_parameters_atomically_common
    self._call_post_set_parameters_callback(parameter_list)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/opt/ros/lyrical/lib/python3.14/site-packages/rclpy/node.py", line 1038, in _call_post_set_parameters_callback
    callback(parameter_list)
    ~~~~~~~~^^^^^^^^^^^^^^^^
  File "/tmp/ros-pr04-fault/src/patrol/patrol/patrol.py", line 63, in apply_update
    1.0 / self.settings['publish_hz'], self.on_timer)
    ~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ZeroDivisionError: division by zero

В исправной версии та же команда отклонена, что показано выше.
