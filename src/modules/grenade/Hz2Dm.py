import json
import math
import yaml
from pathlib import Path

# 读取 JSON 数据
with open("list.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 常量配置
sensitivity = 2.52
m_yaw_pitchvalue = 0.022

def convert_angles(pitch, yaw):
    result_pitch = round(pitch / (sensitivity * m_yaw_pitchvalue), 6)
    result_yaw = round(-1 * yaw / (sensitivity * m_yaw_pitchvalue), 6)
    return result_pitch, result_yaw

def ordered_dict_to_yaml(data):
    """格式化输出 YAML，保持字段顺序并添加空行"""
    lines = []
    for key, value in data.items():
        lines.append(f"{key}:")
        for field in [
            "filename", "displayname", "map", "sensitivity",
            "yaw", "pitch", "type", "throwmode", "extra", "select", "setpos"
        ]:
            v = value.get(field)
            if field in {"extra", "select", "setpos"}:
                lines.append(f"  {field}:")
                for item in v:
                    if isinstance(item, dict):
                        for k, val in item.items():
                            lines.append(f"    - {k}: \"{val}\"")
                    else:
                        lines.append(f"    - \"{item}\"")
            else:
                lines.append(f"  {field}: \"{v}\"")
        lines.append("")  # 空行分隔道具
    return "\n".join(lines)

# 构建 YML 数据结构
custom_yml_data = {}

for grenade in data["grenades"]:
    item_id = grenade["id"]
    displayname = f"{grenade['name_zh_cn']} {grenade['name_en_us']}"
    map_name = grenade["map"].capitalize()
    item_type = grenade["type"]
    raw_yaw = grenade["angle"]["yaw"]
    raw_pitch = grenade["angle"]["pitch"]
    x = grenade["position"]["x"]
    z = grenade["position"]["y"]
    y = 100  # JSON 中没有 y，填默认值

    pitch, yaw = convert_angles(raw_pitch, raw_yaw)

    throw_command = grenade.get("throw_command", "")
    throwmode = "ForwardJump" if throw_command == "hzNade_wjumpthrow_L" else "Normal"

    custom_yml_data[item_id] = {
        "filename": f"{item_id}.cfg",
        "displayname": displayname,
        "map": map_name,
        "sensitivity": str(sensitivity),
        "yaw": str(yaw),
        "pitch": str(pitch),
        "type": item_type if item_type != "HE" else "grenade",
        "throwmode": throwmode,
        "extra": [
            grenade.get("pre_throw_command", ""),
            grenade.get("post_throw_command", "")
        ],
        "select": [
            {"page": ""},
            {"slot": ""},
            {"command": ""},
            {"bind": "None"}
        ],
        "setpos": [
            {"x": str(x)},
            {"z": str(z)},
            {"y": str(y)}
        ]
    }


# 写入 custom.yml
output = ordered_dict_to_yaml(custom_yml_data)
with open("Custom.yml", "w", encoding="utf-8") as f:
    f.write(output)

print("Custom.yml 已生成")
