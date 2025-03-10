#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np

def pose_to_matrix(pose):
    """ Convert pose string to transformation matrix """
    x, y, z, roll, pitch, yaw = map(float, pose.split())
    Rx = np.array([[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)], [0, 1, 0], [-np.sin(pitch), 0, np.cos(pitch)]])
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
    R = Rz @ Ry @ Rx
    return R, np.array([x, y, z]), np.array([roll, pitch, yaw])

def transform_pose(parent_pose, child_pose):
    """ Apply transformation from parent frame to child frame (including rotation) """
    R_p, T_p, rot_p = pose_to_matrix(parent_pose)
    R_c, T_c, rot_c = pose_to_matrix(child_pose)
    
    # Apply position transformation
    T_final = T_p + R_p @ T_c

    # Apply rotation transformation (accumulate yaw correctly)
    rot_final = rot_p + rot_c

    return " ".join(map(str, np.concatenate([T_final, rot_final])))

def rename_elements(model_root, model_name):
    """ Rename all elements with `ModelName::ElementName` """
    for elem in model_root.findall(".//link"):
        elem.set("name", f"{model_name}::{elem.get('name')}")
    for elem in model_root.findall(".//joint"):
        elem.set("name", f"{model_name}::{elem.get('name')}")
        elem.find("parent").text = f"{model_name}::{elem.find('parent').text}"
        elem.find("child").text = f"{model_name}::{elem.find('child').text}"
    for elem in model_root.findall(".//sensor"):
        elem.set("name", f"{model_name}::{elem.get('name')}")

def integrate_sdf(input_sdf, output_sdf):
    """ Load `spacestation.sdf`, integrate models, and output `spacestation_all.sdf` """
    tree = ET.parse(input_sdf)
    root = tree.getroot()
    model = root.find("model")
    model.set("name", "spacestation")  # 統一モデル名に変更

    base_frames = {
        "Eagle": "0 0 0 0 0 0",
        "Tiger": "0 7.0 0 0 0 1.5708",
        "Panther": "0 -7.0 0 0 0 -1.5708"
    }

    print("[INFO] Parsing joints in spacestation.sdf...")

    # `spacestation.sdf` の `<joint>` を解析し、各モジュールの `base_link` を `Eagle` 座標系で登録
    for joint in model.findall("joint"):
        parent = joint.find("parent").text
        child = joint.find("child").text
        pose = joint.find("pose").text

        if "base_link" in child and parent in base_frames:
            base_frames[child] = transform_pose(base_frames[parent], pose)
            print(f"[INFO] {child} in Eagle frame: {base_frames[child]}")

    print("[INFO] Parsing included models...")

    for include in model.findall("include"):
        module_name = include.find("name").text
        uri = include.find("uri").text.replace("model://", "sdf/")
        model_path = f"{uri}/model.sdf"

        try:
            model_tree = ET.parse(model_path)
            model_root = model_tree.getroot().find("model")

            if model_root is None:
                raise ValueError(f"No <model> element found in {model_path}")

            print(f"[INFO] Successfully loaded {module_name} from {model_path}")

            rename_elements(model_root, module_name)

            for joint in model_root.findall(".//joint"):
                child = joint.find("child").text
                pose = joint.find("pose").text

                if module_name in base_frames:
                    joint.find("parent").text = "Eagle::base_link"
                    joint.find("pose").text = transform_pose(base_frames[module_name], pose)
                    print(f"[DEBUG] Transformed joint `{joint.get('name')}` pose: {joint.find('pose').text}")

            for element in list(model_root):
                model.append(element)

        except Exception as e:
            print(f"[ERROR] Failed to process {module_name} from {model_path}: {e}")

    for include in model.findall("include"):
        model.remove(include)

    sdf_output = f'<?xml version="1.0"?>\n{ET.tostring(root, encoding="unicode")}'

    with open(output_sdf, "w") as f:
        f.write(sdf_output)

    print(f"Successfully generated {output_sdf}")

if __name__ == "__main__":
    integrate_sdf("sdf/spacestation.sdf", "sdf/spacestation_all.sdf")