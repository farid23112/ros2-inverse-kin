# ROS 2 Differential Drive - Inverse Kinematics & XY Position Tracking

Project ROS 2 untuk robot differential-drive pada Gazebo.

## Fitur
- Inverse kinematics dari `/input_ik` ke kecepatan roda kiri/kanan.
- Meneruskan `Twist` ke `/cmd_vel` agar robot bergerak di Gazebo.
- Position tracker **X dan Y saja** menggunakan `/joint_states`.
- Dead reckoning differential-drive, tanpa `/odom`.

## Parameter Robot
- Wheel radius: `0.10 m`
- Wheel separation: `0.45 m`
- Left joint: `base_left_wheel_joint`
- Right joint: `base_right_wheel_joint`

## Build
```bash
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --packages-select simple_mover
source install/setup.bash
ros2 pkg executables simple_mover
```

## Jalankan
Gazebo:
```bash
ros2 launch robin_bringup my_robot_gazebo.launch.py
```

Position tracker:
```bash
ros2 run simple_mover position_tracker
```

Inverse kinematics:
```bash
ros2 run simple_mover inverse_kin
```

Tes gerak:
```bash
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"
```

Tes gerak melingkar:
```bash
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.5}}"
```

Tekan `Ctrl+C` pada publisher untuk berhenti.

## Catatan
Position tracker menggunakan dead reckoning dari sudut roda, sehingga error dapat terakumulasi. Posisi awal tracker adalah `(X,Y)=(0,0)`.
