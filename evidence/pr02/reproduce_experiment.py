import subprocess as s, pathlib, time, signal, os, json
out=pathlib.Path('evidence/pr02'); records=[]; children=[]
def run(args,name,timeout=20):
 p=s.run(args,stdout=s.PIPE,stderr=s.STDOUT,text=True,timeout=timeout)
 (out/name).write_text(p.stdout);records.append({'command':__import__('shlex').join(args),'file':name,'exit':p.returncode}); assert p.returncode==0,(args,p.stdout);return p.stdout
def start(args,name):
 f=(out/name).open('w');p=s.Popen(args,stdout=f,stderr=s.STDOUT,start_new_session=True);children.append((p,f));time.sleep(2);assert p.poll() is None;return p
def stop(p, allowed=(0,)):
 os.killpg(p.pid,signal.SIGINT);p.wait(timeout=10); assert p.returncode in allowed,p.returncode

def pose(name):
 text=run(['ros2','topic','echo','/turtle1/pose','--once'],name)
 return {k:float(v) for line in text.splitlines() if ': ' in line for k,v in [line.split(': ',1)]}
def same(a,b):return all(abs(a[k]-b[k])<1e-5 for k in ['x','y','theta'])
try:
 p=start(['ros2','launch','turtle_bringup','sim.launch.py'],'launch-stop-test.txt')
 nodes=run(['ros2','node','list','--no-daemon','--spin-time','2'],'nodes-launched.txt');assert nodes.split().count('/turtlesim')==1
 stop(p);time.sleep(1)
 nodes=run(['ros2','node','list','--no-daemon','--spin-time','2'],'nodes-stopped.txt');assert '/turtlesim' not in nodes
 p=start(['ros2','launch','turtle_bringup','sim.launch.py'],'launch-experiment.txt')
 run(['ros2','interface','show','geometry_msgs/msg/Twist'],'twist-interface.txt')
 run(['ros2','topic','type','/turtle1/pose'],'pose-type.txt')
 a=pose('pose-before.txt')
 twist='{linear: {x: 1.0}, angular: {z: 0.5}}'
 run(['ros2','topic','pub','--once','/turtle1/cmd_vel','geometry_msgs/msg/Twist',twist],'publish-once.txt')
 time.sleep(2);b=pose('pose-after-once.txt');assert not same(a,b)
 pub=['ros2','topic','pub','--rate','1','--wait-matching-subscriptions','0']
 bad=start(pub+['/cmd_vel','geometry_msgs/msg/Twist',twist],'publish-broken.txt')
 info=run(['ros2','topic','info','/cmd_vel','--verbose'],'topic-broken.txt');assert 'Subscription count: 0' in info and 'Publisher count: 1' in info
 run(['ros2','topic','info','/turtle1/cmd_vel','--verbose'],'topic-correct-during-fault.txt')
 c=pose('pose-during-fault.txt');assert same(b,c)
 stop(bad, (0, 2))
 good=start(pub+['/turtle1/cmd_vel','geometry_msgs/msg/Twist',twist],'publish-fixed.txt')
 info=run(['ros2','topic','info','/turtle1/cmd_vel','--verbose'],'topic-fixed.txt');assert 'Subscription count: 1' in info and 'Publisher count: 1' in info
 d=pose('pose-after-fix.txt');assert not same(c,d)
 stop(good, (0, 2));time.sleep(2);e=pose('pose-stopped.txt');assert e['linear_velocity']==0 and e['angular_velocity']==0
 stop(p)
 (out/'measurements.json').write_text(json.dumps({'before':a,'once':b,'broken':c,'fixed':d,'stopped':e,'assertions':'passed'},indent=2))
finally:
 for p,f in children:
  if p.poll() is None:
   os.killpg(p.pid,signal.SIGINT)
   try:p.wait(timeout=10)
   except s.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL)
  f.close()
 (out/'executed-commands.json').write_text(json.dumps(records,indent=2))
