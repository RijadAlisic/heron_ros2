import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import subprocess


def generate_launch_description():

    pkg_heron_gazebo = get_package_share_directory('heron_gazebo')
    pkg_heron_description = get_package_share_directory('heron_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Launch arguments
    x_arg = DeclareLaunchArgument('x', default_value='0.0')
    y_arg = DeclareLaunchArgument('y', default_value='0.0')
    z_arg = DeclareLaunchArgument('z', default_value='0.1')
    yaw_arg = DeclareLaunchArgument('yaw', default_value='0.0')

    # Paths
    world_path = os.path.join(pkg_heron_gazebo, 'worlds', 'simple_water.sdf')
    urdf_path = os.path.join(pkg_heron_gazebo, 'urdf', 'heron_harmonic.urdf.xacro')

    ## Process URDF using command-line xacro
    xacro_cmd = ['xacro', urdf_path]
    robot_description_raw = subprocess.check_output(xacro_cmd).decode('utf-8')
    
    # Replace package:// paths with file:// for Gazebo
    meshes_path = os.path.join(pkg_heron_description, 'meshes')
    robot_description = robot_description_raw.replace(
        'package://heron_description/meshes',
        f'file://{meshes_path}'
    )

    # Gazebo
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': world_path}.items(),
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
    )

    # Spawn Heron
    spawn_heron = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_heron',
        output='screen',
        arguments=[
            '-name', 'heron',
            '-topic', 'robot_description',
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
            '-Y', LaunchConfiguration('yaw'),
        ],
    )
    
    # ROS ↔ Gazebo bridge for thrusters
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        arguments=[
            # Map ROS topics to Gazebo's actual topic names
            '/heron/right_engine_joint/cmd_vel@std_msgs/msg/Float64]gz.msgs.Double',
            '/heron/left_engine_joint/cmd_vel@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/heron/joint/right_engine_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/heron/joint/left_engine_joint/cmd_thrust@std_msgs/msg/Float64]gz.msgs.Double',
            '/heron/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        remappings=[
            ('/heron/right_engine_joint/cmd_vel', '/model/heron/joint/right_engine_joint/cmd_thrust'),
            ('/heron/left_engine_joint/cmd_vel', '/model/heron/joint/left_engine_joint/cmd_thrust'),
        ]
    )

    return LaunchDescription([
        x_arg, y_arg, z_arg, yaw_arg,
        gz_sim,
        robot_state_publisher,
        spawn_heron,
        bridge,
    ])
