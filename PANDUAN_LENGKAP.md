# PANDUAN LENGKAP TUGAS ROS 2: INVERSE KINEMATICS + TRACKING XYZ

## 1. Parameter robot yang sudah dicek
Workspace: ~/ros2_ws
Package program: simple_mover
Package Gazebo: robin_bringup
Launch: my_robot_gazebo.launch.py

Parameter model:
- wheel radius = 0.10 m
- wheel separation = 0.45 m

Topic yang tersedia:
- /cmd_vel
- /joint_states
- /tf
- /tf_static

Tidak tersedia /odom.

## 2. Salin file program
Salin inverse_kin.py dan position_tracker.py ke:
~/ros2_ws/src/simple_mover/simple_mover/

## 3. Ubah setup.py
Tambahkan di console_scripts:
'inverse_kin = simple_mover.inverse_kin:main',
'position_tracker = simple_mover.position_tracker:main',

## 4. Ubah package.xml
Pastikan ada:
<depend>rclpy</depend>
<depend>geometry_msgs</depend>
<depend>std_msgs</depend>
<depend>sensor_msgs</depend>

## 5. Build
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --packages-select simple_mover
source install/setup.bash

Cek:
ros2 pkg executables simple_mover

## 6. Buka Gazebo
Terminal 1:
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
ros2 launch robin_bringup my_robot_gazebo.launch.py

## 7. Jalankan tracker
Terminal 2:
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run simple_mover position_tracker

## 8. Jalankan inverse kinematics
Terminal 3:
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run simple_mover inverse_kin

## 9. Robot maju
Terminal 4:
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"

Hentikan publisher dengan Ctrl+C.

## 10. Robot lingkaran
Radius lintasan R = v / omega.

Contoh radius 0.4 m:
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.5}}"

Lingkaran lebih cepat tetapi radius sama:
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.4}, angular: {z: 1.0}}"

## 11. Reset robot
Hentikan launch Gazebo dengan Ctrl+C, lalu jalankan lagi:
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
ros2 launch robin_bringup my_robot_gazebo.launch.py

Restart position_tracker agar X,Y,Theta kembali ke 0.

## 12. Rumus
Inverse kinematics:
omega_L = (v - (L/2)*omega) / r
omega_R = (v + (L/2)*omega) / r

Tracking:
ds_L = r*dtheta_L
ds_R = r*dtheta_R
ds = (ds_L + ds_R)/2
dtheta = (ds_R - ds_L)/L

X_new = X + ds*cos(theta + dtheta/2)
Y_new = Y + ds*sin(theta + dtheta/2)
Z = 0

Catatan: tracker memakai dead reckoning dari /joint_states, bukan ground-truth Gazebo.
