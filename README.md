# README.md

## Purpose of this demo
- To show an example of how to organize space station modules to create your space station model in the SDF format 
- To demo to convert from SDF to URDF for ROS 2 use.
- 
## File organization

```plaintext
demo_spacestation_gnc_rep/
├── CMakeLists.txt
├── package.xml
├── merge_urdf.py			# See Procedures Step4
├── launch/
│   └── display_spacestation.launch.py
├── sdf/				# Create these files to design space station 
│   ├── spacestation_module_typeA/ 	# Defining a module_typeA for demo
│   │   ├── model.config
│   │   └── model.sdf
│   ├── spacestation_module_typeB/	# Defining a module_typeB for demo
│   │   ├── model.config
│   │   └── model.sdf
│   └── spacestation.sdf		# Defining a spacestation for demo
├── urdf/				# See (Note) below
│   ├── spacestation_module_typeA.urdf
│   ├── spacestation_module_typeB.urdf
│   └── spacestation.urdf
└── rviz/
    └── spacestation.rviz
```

(Note) 
The URDF files in this directory are intended to be generated from SDF files 
by following the instructions in README.md in the root directory. 
They are left here for comparison purposes.


## Procedures 
### Step1. Creating sdf file for space station module (before combining)
```
cd /path/to/demo_spacestation_gnc_rep
```
See the files in sdf/spacestation_module_typeA/ and sdf/spacestation_module_typeB/

### Step2. Generating urdf file for space station module (before combining)

```
sdf2urdf sdf/spacestation_module_typeA/model.sdf > urdf/spacestation_module_typeA.urdf
sdf2urdf sdf/spacestation_module_typeB/model.sdf > urdf/spacestation_module_typeB.urdf
```
Memo: This seems also work
export GAZEBO_MODEL_PATH=path/to/demo_spacestation_gnc_rep/urdf:$GAZEBO_MODEL_PATH
gz sdf -p urdf/spacestation.sdf > urdf/spacestation.urdf

### Step3. Creating sdf file for combined space station 

See the files in sdf/spacestation.sdf. 
Edit the file as needed for change the configuration.

### Step4. Creating urdf file for combined space station 
The inputs are space station module urdf files (from Step2) and space station sdf file (from Step3).
```
python3 merge_urdf.py
```
### Step5. Build
```
cd /path/to/compile/ros2
colcon build
source install/setup.bash
```

### Step6. Run
```
ros2 launch demo_spacestation_gnc_rep display_spacestation.launch.py
```
A rviz window will be launched. 

## Discussions
- Is it good to start with .sdf files to design and configure a space station? Please give us alternative ideas. 
- It would be preferable if there is a pre-developed generation method to conbine sub-modules (spacestation_module_typeX.urdf) and conficulation sdf file (spacestation.sdf) to generate spacestation.urdf.  

## TODO
- Support sensors



