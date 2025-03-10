from setuptools import setup

package_name = 'demo_spacestation_gnc_rep'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='ROS2 package for space station simulation',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sdf_loader = demo_spacestation_gnc_rep.sdf_loader:main',
            'test_sdf_loader = demo_spacestation_gnc_rep.test_sdf_loader:main'
        ],
    },
)

