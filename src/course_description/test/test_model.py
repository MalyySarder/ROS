"""Check geometry, topology and sensor parents, beyond URDF syntax."""

import math
import os
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
import xacro

MODEL = Path(os.environ.get('PR06_MODEL', str(
    Path(__file__).resolve().parents[1] / 'urdf' / 'vehicle.urdf.xacro')))


def model(**mappings):
    return ET.fromstring(xacro.process_file(
        str(MODEL), mappings={k: str(v) for k, v in mappings.items()}).toxml())


def joint(root, name):
    return root.find(f"joint[@name='{name}']")


def xyz(element):
    return tuple(float(v) for v in element.find('origin').get('xyz').split())


def test_tree_connected_acyclic():
    root = model()
    links = {link.get('name') for link in root.findall('link')}
    assert len(links) == 10
    parents = {}
    for j in root.findall('joint'):
        child, parent = j.find('child').get('link'), j.find('parent').get('link')
        assert child in links and parent in links and child not in parents
        parents[child] = parent
    assert links - parents.keys() == {'base_link'}
    for child in links:
        seen = set()
        while child in parents:
            assert child not in seen
            seen.add(child)
            child = parents[child]
        assert child == 'base_link'


def test_lidar_parent():
    j = joint(model(), 'lidar_joint')
    assert j.find('parent').get('link') == 'base_link'
    assert xyz(j) == pytest.approx((0.28, 0.0, 0.38))


def test_sensor_contract():
    root = model()
    for sensor in ['camera', 'lidar', 'imu']:
        j = joint(root, sensor + '_joint')
        assert j.get('type') == 'fixed'
        assert j.find('parent').get('link') == 'base_link'
        assert xyz(j) == pytest.approx((0.28, 0, 0.38))


@pytest.mark.parametrize('base,track,radius', [(0.8, 0.62, 0.12), (1.0, 0.8, 0.15)])
def test_parameterized_geometry(base, track, radius):
    root = model(wheelbase=base, track=track, wheel_radius=radius)
    for side, sign in [('left', 1), ('right', -1)]:
        assert xyz(joint(root, f'front_{side}_steering_joint')) == pytest.approx(
            (base / 2, sign * track / 2, 0))
        assert xyz(joint(root, f'rear_{side}_wheel_joint')) == pytest.approx(
            (-base / 2, sign * track / 2, 0))
    for name in ['front_left', 'front_right', 'rear_left', 'rear_right']:
        j = joint(root, name + '_wheel_joint')
        assert j.get('type') == 'continuous'
        assert j.find('axis').get('xyz') == '0 1 0'
        link = root.find(f"link[@name='{name}_wheel']")
        for kind in ['visual', 'collision']:
            cylinder = link.find(kind + '/geometry/cylinder')
            assert float(cylinder.get('radius')) == radius
            assert float(cylinder.get('length')) == 0.07


def test_shapes_and_physical_numbers():
    root = model()
    body = root.find("link[@name='base_link']")
    assert body.find('visual/geometry/box').get('size') == '1.05 0.52 0.22'
    for link in root.findall('link'):
        assert link.find('visual/geometry') is not None
        assert link.find('collision/geometry') is not None
        mass = float(link.find('inertial/mass').get('value'))
        assert math.isfinite(mass) and mass > 0
        inertia = link.find('inertial/inertia')
        diag = [float(inertia.get(k)) for k in ['ixx', 'iyy', 'izz']]
        assert all(math.isfinite(v) and v > 0 for v in diag)
        assert 2 * max(diag) <= sum(diag) + 1e-12
        assert all(float(inertia.get(k)) == 0 for k in ['ixy', 'ixz', 'iyz'])
    for j in root.findall("joint[@type='revolute']"):
        limit = j.find('limit')
        assert float(limit.get('lower')) < float(limit.get('upper'))
        assert float(limit.get('effort')) > 0 and float(limit.get('velocity')) > 0
    assert not root.findall('.//plugin')
