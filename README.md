# ROS 2 Inverse Kinematics & XYZ Position Tracking

Project tugas ROS 2 lanjutan untuk robot differential drive pada Gazebo.

## Fitur

- Node `inverse_kin` untuk menghitung inverse kinematics differential drive.
- Node `position_tracker` untuk melacak posisi X, Y, Z berdasarkan `/joint_states`.
- Input gerak melalui `/input_ik`.
- Robot Gazebo tetap dikendalikan melalui `/cmd_vel`.

## Parameter Robot

Parameter mengikuti model robot yang digunakan:

- Wheel radius: `0.10 m`
- Wheel separation: `0.45 m`

## Struktur

```text
simple_mover/
├── inverse_kin.py
├── position_tracker.py
└── README.md
```

File ini ditujukan untuk diletakkan di:

```text
~/ros2_ws/src/simple_mover/simple_mover/
```

## Setup `setup.py`

Tambahkan ke `console_scripts`:

```python
'inverse_kin = simple_mover.inverse_kin:main',
'position_tracker = simple_mover.position_tracker:main',
```

Contoh:

```python
entry_points={
    'console_scripts': [
        'simple_mover_node = simple_mover.simple_mover_node:main',
        'rectangle_mover = simple_mover.rectangle_mover:main',
        'inverse_kin = simple_mover.inverse_kin:main',
        'position_tracker = simple_mover.position_tracker:main',
    ],
},
```

## Dependency `package.xml`

Pastikan ada:

```xml
<depend>rclpy</depend>
<depend>geometry_msgs</depend>
<depend>std_msgs</depend>
<depend>sensor_msgs</depend>
```

## Build

```bash
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --packages-select simple_mover
source install/setup.bash
```

Cek executable:

```bash
ros2 pkg executables simple_mover
```

Harus terdapat:

```text
simple_mover inverse_kin
simple_mover position_tracker
```

## Menjalankan Gazebo

```bash
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
ros2 launch robin_bringup my_robot_gazebo.launch.py
```

## Menjalankan Position Tracker

Terminal baru:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run simple_mover position_tracker
```

Output:

```text
POSISI -> X: 0.000 m | Y: 0.000 m | Z: 0.000 m | Theta: 0.00 deg
```

## Menjalankan Inverse Kinematics

Terminal baru:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run simple_mover inverse_kin
```

## Robot Maju

```bash
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}"
```

Hentikan dengan `Ctrl+C`.

## Robot Membentuk Lingkaran

Contoh radius 0.4 m:

```bash
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.5}}"
```

Radius lintasan:

```text
R = v / omega
R = 0.2 / 0.5
R = 0.4 m
```

Lingkaran lebih cepat dengan radius sama:

```bash
ros2 topic pub -r 10 /input_ik geometry_msgs/msg/Twist "{linear: {x: 0.4}, angular: {z: 1.0}}"
```

## Reset Robot

Hentikan launch Gazebo dengan `Ctrl+C`, kemudian jalankan kembali:

```bash
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
source install/setup.bash
ros2 launch robin_bringup my_robot_gazebo.launch.py
```

Restart `position_tracker` agar koordinat kembali dimulai dari:

```text
X = 0
Y = 0
Z = 0
```

## Rumus Inverse Kinematics

Untuk differential drive:

```text
omega_L = (v - (L/2)*omega) / r
omega_R = (v + (L/2)*omega) / r
```

dengan:

```text
r = 0.10 m
L = 0.45 m
```

## Tracking Posisi

Perubahan posisi roda:

```text
ds_L = r * dtheta_L
ds_R = r * dtheta_R
```

Perpindahan robot:

```text
ds = (ds_L + ds_R) / 2
```

Perubahan orientasi:

```text
dtheta = (ds_R - ds_L) / L
```

Kemudian:

```text
X_new = X + ds*cos(theta + dtheta/2)
Y_new = Y + ds*sin(theta + dtheta/2)
Z = 0
```

> `position_tracker` menggunakan dead reckoning dari `/joint_states`, bukan ground-truth posisi Gazebo. Error dapat terakumulasi selama robot bergerak.
