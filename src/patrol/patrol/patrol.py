# Copyright 2026 Nikita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Store the latest turtle pose and publish a command every 0.1 seconds."""

from geometry_msgs.msg import Twist
from patrol.control import command_from_pose
from patrol.parameters import LIMITS, validate_settings
from patrol.pose_type import Pose
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class Patrol(Node):
    """Publish to relative cmd_vel so the destination can be remapped."""

    def __init__(self):
        super().__init__('patrol')
        self.latest_pose = None
        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.declare_parameter('publish_hz', 10.0)
        self.settings = {name: self.get_parameter(name).value for name in LIMITS}
        validate_settings(self.settings)
        self.add_on_set_parameters_callback(self.validate_update)
        self.add_post_set_parameters_callback(self.apply_update)
        self.pose_subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.on_pose, 10)
        self.command_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.command_timer = self.create_timer(1.0 / self.settings['publish_hz'], self.on_timer)

    def validate_update(self, parameters):
        """Check the complete candidate before committing any state."""
        candidate = dict(self.settings)
        candidate.update({p.name: p.value for p in parameters if p.name in LIMITS})
        try:
            validate_settings(candidate)
        except ValueError as error:
            return SetParametersResult(successful=False, reason=str(error))
        return SetParametersResult(successful=True)

    def apply_update(self, parameters):
        """Apply only a committed update; replace the old timer if needed."""
        previous_hz = self.settings['publish_hz']
        self.settings.update({p.name: p.value for p in parameters if p.name in LIMITS})
        if self.settings['publish_hz'] != previous_hz:
            self.command_timer.cancel()
            self.destroy_timer(self.command_timer)
            self.command_timer = self.create_timer(
                1.0 / self.settings['publish_hz'], self.on_timer)

    def on_pose(self, pose):
        """Keep only the newest pose; publishing belongs to the timer."""
        self.latest_pose = pose

    def on_timer(self):
        """Publish zero before the first pose, otherwise a fixed velocity."""
        self.command_publisher.publish(command_from_pose(
            self.latest_pose, self.settings['linear_speed'], self.settings['turn_rate']))


def main(args=None):
    """Initialize ROS, process callbacks and release resources on Ctrl+C."""
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
