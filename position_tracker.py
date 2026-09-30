import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class PositionTracker(Node):
    def __init__(self):
        super().__init__('position_tracker')

        self.wheel_radius = 0.10
        self.wheel_separation = 0.45

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.theta = 0.0

        self.previous_left = None
        self.previous_right = None

        self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )
        self.timer = self.create_timer(0.5, self.display_position)

        self.get_logger().info('Position Tracker aktif.')
        self.get_logger().info(
            'Tracking X, Y, Z dari /joint_states (dead reckoning).'
        )

    def joint_state_callback(self, msg):
        left_index = None
        right_index = None

        for i, name in enumerate(msg.name):
            if name == 'base_left_wheel_joint':
                left_index = i
            elif name == 'base_right_wheel_joint':
                right_index = i

        if left_index is None or right_index is None:
            return

        left = msg.position[left_index]
        right = msg.position[right_index]

        if self.previous_left is None:
            self.previous_left = left
            self.previous_right = right
            return

        dleft = left - self.previous_left
        dright = right - self.previous_right
        self.previous_left = left
        self.previous_right = right

        ds_left = self.wheel_radius * dleft
        ds_right = self.wheel_radius * dright
        ds = (ds_left + ds_right) / 2.0
        dtheta = (ds_right - ds_left) / self.wheel_separation

        theta_mid = self.theta + dtheta / 2.0
        self.x += ds * math.cos(theta_mid)
        self.y += ds * math.sin(theta_mid)
        self.theta += dtheta
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
        self.z = 0.0

    def display_position(self):
        if self.previous_left is None:
            self.get_logger().info('Menunggu /joint_states...')
            return

        self.get_logger().info(
            f'POSISI -> X: {self.x:.3f} m | '
            f'Y: {self.y:.3f} m | '
            f'Z: {self.z:.3f} m | '
            f'Theta: {math.degrees(self.theta):.2f} deg'
        )

def main(args=None):
    rclpy.init(args=args)
    node = PositionTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
