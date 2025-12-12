from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import ExecuteProcess
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('arm_v1_0_0_description')

    xacro_file = os.path.join(share_dir, 'urdf', 'arm_v1_0_0.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_urdf},
            {'use_sim_time': True}
        ],
        output='screen'
    )

    gazebo_server = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-v', '4', 'empty.sdf'],
        output='screen'
    )

    urdf_spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'arm_v1_0_0',
            '-topic', 'robot_description'
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_server,
        urdf_spawn_node,
    ])
