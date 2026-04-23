# Heron USV Simulator — ROS 2 Jazzy + Gazebo Harmonic

A working port of the [Clearpath Heron USV](https://github.com/heron/heron) simulator from ROS 1 (Gazebo Classic + UUV Simulator) to **ROS 2 Jazzy** with **Gazebo Harmonic**.

## Features

- Realistic water buoyancy physics (Gazebo Harmonic native)
- Differential thrust control (2× thrusters)
- Odometry publishing
- Visual water surface (VRX `coast_waves` model)
- Full ROS 2 integration

## Requirements

- Ubuntu 24.04 (Noble)
- ROS 2 Jazzy
- Gazebo Harmonic

## Dependencies

```bash
sudo apt install -y \
  ros-jazzy-ros-gz \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  python3-colcon-common-extensions
```

## Installation

```bash
mkdir -p ~/heron_ws/src
cd ~/heron_ws/src

# Clone this repository
git clone https://github.com/RijadAlisic/heron_ros2.git

# Clone VRX (required for water surface model)
git clone https://github.com/osrf/vrx.git -b jazzy

cd ~/heron_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

> **Note:** `vrx` is not included in this repo due to its size. It must be cloned separately as shown above.

## Usage

### Launch

```bash
ros2 launch heron_gazebo heron_world.launch.py
```

Optional arguments:

```bash
ros2 launch heron_gazebo heron_world.launch.py x:=10.0 y:=5.0 z:=0.5 yaw:=1.57
```

### Control

The Heron uses differential thrust. Publish `Float64` to the thruster topics directly:

```bash
# Move forward
ros2 topic pub /model/heron/joint/right_engine_joint/cmd_thrust std_msgs/msg/Float64 "{data: 5.0}" &
ros2 topic pub /model/heron/joint/left_engine_joint/cmd_thrust std_msgs/msg/Float64 "{data: 5.0}"

# Turn right (differential thrust)
ros2 topic pub /model/heron/joint/right_engine_joint/cmd_thrust std_msgs/msg/Float64 "{data: -5.0}" &
ros2 topic pub /model/heron/joint/left_engine_joint/cmd_thrust std_msgs/msg/Float64 "{data: 5.0}"

# Stop
ros2 topic pub /model/heron/joint/right_engine_joint/cmd_thrust std_msgs/msg/Float64 "{data: 0.0}" &
ros2 topic pub /model/heron/joint/left_engine_joint/cmd_thrust std_msgs/msg/Float64 "{data: 0.0}"
```

Thrust range: `-10.0` to `10.0` (Newtons)

### Monitor

```bash
ros2 topic echo /heron/odometry
```

## Package Structure

```
src/
├── heron/
│   ├── heron_control/             # Teleop and navigation config (ROS 1, not yet ported)
│   ├── heron_description/         # URDF and meshes (converted to ROS 2)
│   └── heron_msgs/                # Custom messages (converted to ROS 2)
├── heron_simulator/
│   ├── heron_gazebo/              # Main simulator package
│   │   ├── launch/
│   │   │   └── heron_world.launch.py      # Active ROS 2 launch file
│   │   ├── urdf/
│   │   │   └── heron_harmonic.urdf.xacro  # Gazebo Harmonic URDF
│   │   └── worlds/
│   │       ├── simple_water.sdf           # Active water world
│   │       ├── ocean_surface.world        # Legacy ROS 1 (not used)
│   │       └── lake.world                 # Legacy ROS 1 (not used)
│   └── heron_simulator/           # Metapackage
└── vrx/                           # External dependency — clone separately
    └── vrx_gz/
        └── models/coast_waves/    # Water surface visual used by simple_water.sdf
```

## ROS 2 Topics

| Topic | Type | Direction |
|---|---|---|
| `/model/heron/joint/right_engine_joint/cmd_thrust` | `std_msgs/Float64` | → Gazebo |
| `/model/heron/joint/left_engine_joint/cmd_thrust` | `std_msgs/Float64` | → Gazebo |
| `/heron/odometry` | `nav_msgs/Odometry` | ← Gazebo |
| `/joint_states` | `sensor_msgs/JointState` | ← Gazebo |

## Migration Notes

Key changes from ROS 1:

| ROS 1 | ROS 2 / Gazebo Harmonic |
|---|---|
| `libuuv_underwater_object_ros_plugin.so` | `gz-sim-buoyancy-system` (world-level) |
| `libuuv_thruster_ros_plugin.so` | `gz-sim-thruster-system` |
| `libuuv_joint_state_publisher.so` | `gz-sim-joint-state-publisher-system` |
| `libgazebo_ros_p3d.so` | `gz-sim-odometry-publisher-system` |
| XML launch files | Python launch files |
| `catkin` build system | `ament_cmake` |
| `map()` in xacro | `list(map())` for Python 3 |

### Buoyancy Tuning

- Collision volume: `1.0 × 0.6 × 0.12 = 0.072 m³`
- Max buoyant force: `1000 × 0.072 × 9.81 = 706 N`
- Mass: `47 kg` → weight `461 N` → floats at ~65% submerged

## Known Limitations

- Boat oscillates slightly on water surface (stable and acceptable — hydrodynamics plugin caused NaN instability and was removed)
- Thruster commands must be published directly to Gazebo topic names (ROS bridge remapping not yet wired)
- Sensors (GPS, IMU, magnetometer) not yet ported from original `heron_description`
- `heron_control` package not yet converted to ROS 2

## Contributing

PRs welcome! Priority areas:

- [ ] ROS bridge with friendly topic remapping (`cmd_vel` interface)
- [ ] Port sensors (GPS, IMU, magnetometer) to Gazebo Harmonic
- [ ] Convert `heron_control` to ROS 2
- [ ] Joystick teleoperation node
- [ ] Integration with VRX competition worlds

## Credits

- Original Heron: [Clearpath Robotics](https://clearpathrobotics.com)
- ROS 2 Port: MIT
- Water simulation: [VRX Competition](https://github.com/osrf/vrx)

## License

BSD (matching original Clearpath Heron packages)

This is an independent ROS 2 port, not affiliated with Clearpath Robotics