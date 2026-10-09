import json, os, pathlib, re, shlex, signal, subprocess, time
import yaml
out=pathlib.Path('evidence/pr03'); children=[]; records=[]
def run(args, filename, timeout=20, allowed=(0,)):
    r=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
    (out/filename).write_text(r.stdout)
    records.append({'command':shlex.join(args),'file':filename,'exit':r.returncode})
    assert r.returncode in allowed,(args,r.returncode,r.stdout)
    return r.stdout

def start(args,filename):
    f=(out/filename).open('w')
    p=subprocess.Popen(args,stdout=f,stderr=f,start_new_session=True)
    children.append((p,f))
    records.append({'command':shlex.join(args),'file':filename,'event':'start'})
    time.sleep(2)
    assert p.poll() is None,(args,p.returncode)
    return p

def stop(p):
    os.killpg(p.pid,signal.SIGINT)
    p.wait(timeout=10)
    records.append({'event':'SIGINT','pid':p.pid,'exit':p.returncode})
    assert p.returncode==0,p.returncode

def pose(filename):
    return yaml.safe_load(run(['ros2','topic','echo','/turtle1/pose','--once'],filename).split('---')[0])

def same(a,b):
    return all(abs(a[k]-b[k])<1e-5 for k in ['x','y','theta'])

try:
    patrol=start(['ros2','run','patrol','patrol'],'patrol-no-remap.txt')
    zero=yaml.safe_load(run(['ros2','topic','echo','/cmd_vel','geometry_msgs/msg/Twist','--once'],'command-without-pose.txt').split('---')[0])
    assert all(v==0 for axis in zero.values() for v in axis.values()),zero
    sim=start(['ros2','launch','turtle_bringup','sim.launch.py'],'simulator.txt')
    run(['ros2','topic','type','/turtle1/pose'],'pose-type.txt')
    run(['ros2','node','list','--no-daemon','--spin-time','2'],'nodes-broken.txt')
    run(['ros2','node','info','/patrol'],'patrol-info-broken.txt')
    before=pose('pose-before.txt')
    command=yaml.safe_load(run(['ros2','topic','echo','/cmd_vel','geometry_msgs/msg/Twist','--once'],'command-broken.txt').split('---')[0])
    assert command['linear']['x']==0.5 and command['angular']['z']==0.3
    info=run(['ros2','topic','info','/cmd_vel','--verbose'],'topic-broken.txt')
    assert 'Publisher count: 1' in info and 'Subscription count: 0' in info
    info=run(['ros2','topic','info','/turtle1/cmd_vel','--verbose'],'topic-target-before-remap.txt')
    assert 'Publisher count: 0' in info and 'Subscription count: 1' in info
    broken=pose('pose-broken.txt');assert same(before,broken)
    stop(patrol)
    patrol=start(['ros2','run','patrol','patrol','--ros-args','-r','cmd_vel:=/turtle1/cmd_vel'],'patrol-remapped.txt')
    run(['ros2','node','info','/patrol'],'patrol-info-fixed.txt')
    info=run(['ros2','topic','info','/turtle1/cmd_vel','--verbose'],'topic-fixed.txt')
    assert 'Publisher count: 1' in info and 'Subscription count: 1' in info
    fixed_command=yaml.safe_load(run(['ros2','topic','echo','/turtle1/cmd_vel','--once'],'command-fixed.txt').split('---')[0])
    assert fixed_command==command
    hz=run(['timeout','--signal=INT','13s','ros2','topic','hz','/turtle1/cmd_vel'],'frequency.txt',timeout=18,allowed=(124,))
    rates=[float(x) for x in re.findall(r'average rate:\s*([\d.]+)',hz)]
    assert len(rates)>=10 and 8<rates[-1]<12,rates
    moved=pose('pose-fixed.txt');assert not same(broken,moved)
    stop(patrol)
    time.sleep(2)
    stopped=pose('pose-stopped.txt')
    assert stopped['linear_velocity']==0 and stopped['angular_velocity']==0,stopped
    time.sleep(1)
    later=pose('pose-stopped-later.txt');assert same(stopped,later)
    nodes=run(['ros2','node','list','--no-daemon','--spin-time','2'],'nodes-after-stop.txt');assert '/patrol' not in nodes
    info=run(['ros2','topic','info','/turtle1/cmd_vel','--verbose'],'topic-after-stop.txt');assert 'Publisher count: 0' in info
    (out/'measurements.json').write_text(json.dumps({'before':before,'broken':broken,'fixed':moved,'stopped':stopped,'stopped_later':later,'frequency_duration_seconds':13,'average_rates_hz':rates,'assertions':'passed'},indent=2))
    stop(sim)
    print('Live checks passed; last average frequency:',rates[-1])
finally:
    for p,f in children:
        if p.poll() is None:
            os.killpg(p.pid,signal.SIGINT)
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL)
        f.close()
    (out/'executed-commands.json').write_text(json.dumps(records,indent=2))
