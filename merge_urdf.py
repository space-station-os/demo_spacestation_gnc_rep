import os
import xml.etree.ElementTree as ET

# Directory containing the module URDF files
# modules_dir = '/home/yuyuqq/ros2_ws/src/demo_spacestation_gnc_rep/urdf'
modules_dir = './urdf'

# Path to the SDF file
# sdf_file = '/home/yuyuqq/ros2_ws/src/demo_spacestation_gnc_rep/sdf/spacestation.sdf'
sdf_file = './sdf/spacestation.sdf'

# Path to the output merged URDF file
output_file = os.path.join(modules_dir, 'spacestation.urdf')

# Initialize the content of the merged URDF file
urdf_content = '<?xml version="1.0"?>\n<robot name="spacestation">\n'

# Function to add origin tag with pose
def add_origin(pose):
    pose_values = pose.split()
    return f'<origin xyz="{pose_values[0]} {pose_values[1]} {pose_values[2]}" rpy="{pose_values[3]} {pose_values[4]} {pose_values[5]}"/>'

# Parse the SDF file
tree = ET.parse(sdf_file)
root = tree.getroot()

# Process each included model
for include in root.findall('.//include'):
    uri = include.find('uri').text
    name = include.find('name').text
    module_name = uri.split('model://')[-1]
    module_file = os.path.join(modules_dir, f'{module_name}.urdf')
    
    with open(module_file, 'r') as f:
        module_content = f.read()
        # Extract and append only the contents inside the <robot> tag
        module_content = module_content.split('<robot name="')[1]
        module_content = module_content.split('</robot>')[0]
        # Replace the module name with the instance name
        module_content = module_content.replace(module_name, name)
        # Prefix link names and joint names with instance names to ensure uniqueness
        module_content = module_content.replace('<link name="', f'<link name="{name}_')
        module_content = module_content.replace('<parent link="', f'<parent link="{name}_')
        module_content = module_content.replace('<child link="', f'<child link="{name}_')
        module_content = module_content.replace('<joint name="', f'<joint name="{name}_')
        # Add color to visual elements if material is present
        material = include.find('material')
        if material is not None:
            color = material.find('color').text
            color_tag = f'<material name="{name}_color"><color rgba="{color}"/></material>'
            module_content = module_content.replace('<visual>', f'<visual>{color_tag}', 1)

        # Add origin tag if pose is present
        pose = include.find('pose')
        if pose is not None:
            origin_tag = add_origin(pose.text)
            module_content = module_content.replace('<collision>', f'<collision>{origin_tag}', 1)
            module_content = module_content.replace('<visual>', f'<visual>{origin_tag}', 1)

        # Extract the root link of the module
        urdf_content += module_content

# Process each joint
for joint in root.findall('.//joint'):
    name = joint.get('name')
    joint_type = joint.get('type')
    parent = joint.find('parent').text.replace("::", "_")
    child = joint.find('child').text.replace("::", "_")
    pose = joint.find('pose')
    joint_pose = ""
    if pose is not None:
        joint_pose = add_origin(pose.text)
    
    urdf_content += f'<joint name="{name}" type="{joint_type}">\n'
    urdf_content += f'  <parent link="{parent}"/>\n'
    urdf_content += f'  <child link="{child}"/>\n'
    urdf_content += joint_pose + '\n'
    urdf_content += '</joint>\n'

# Close the <robot> tag in the merged URDF content
urdf_content += '</robot>\n'

# Save the merged URDF content to the output file
with open(output_file, 'w') as f:
    f.write(urdf_content)

print(f'URDF file is seved in {output_file} ')
