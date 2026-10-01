from setuptools import find_packages, setup

package_name = 'simple_mover'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Farid Surya Wardana',
    maintainer_email='farid@example.com',
    description='ROS 2 inverse kinematics and XY position tracking.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'inverse_kin = simple_mover.inverse_kin:main',
            'position_tracker = simple_mover.position_tracker:main',
        ],
    },
)
