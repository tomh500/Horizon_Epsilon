import json
import os

# 加载 JSON 文件（支持数组 or 对象结构）
def load_grenades(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'grenades' in data:
        return data['grenades']
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Invalid JSON structure")

# 格式化每个投掷物（示例处理）
def format_grenade(g):
    name = g.get("name_en_us", g.get("id", "unknown"))
    map_name = g["map"]
    throw_cmd = g["throw_command"]
    angle = g["angle"]
    return f"[{name}] ({map_name})\nCommand: {throw_cmd}\nAngle: pitch={angle['pitch']}, yaw={angle['yaw']}\n"

# 写入文件（相对路径）
def write_output(content, relative_path):
    full_path = os.path.abspath(relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✔ 写入成功: {full_path}")

def append(s,text):
    return s+'\n'+text

# 主流程
if __name__ == "__main__":
    grenades = load_grenades("list.json")  # 你的 JSON 路径
    nade_list=""
    for g in grenades:
        ID=g['id'];

        sens = 2.52
        m_yaw = 0.022
        m_pitch = 0.022

        yaw = g['angle']['yaw']
        pitch = g['angle']['pitch']

        yaw = (-yaw)/(sens*m_yaw)
        pitch = pitch/(sens*m_pitch)

        priority = g['priority']
        ty = g['type']

        content=""

        nade_list=append(nade_list,f'alias hzNade_load_{ID} exec Horizon/src/modules/grenade/data/{ID}.cfg')

        content=append(content,f'alias hzNade_info_yaw yaw {yaw} 1 1')
        content=append(content,f'alias hzNade_info_pitch pitch {pitch} 1 1')
        content=append(content,f'alias hzNade_info_pos "setpos {g['position']['x']} {g['position']['y']} 0"')
        content=append(content,f'alias hzNade_info_pre_cmd "{g['pre_throw_command']}"')
        content=append(content,f'alias hzNade_info_post_cmd "{g['post_throw_command']}"')
        content=append(content,f'alias hzNade_info_throw_cmd "{g['throw_command']}"')
        content=append(content,f'alias hzNade_info_type "+hzBind_{ty};-hzBind_{ty}"')
        write_output(content,f"data/{ID}.cfg")
    write_output(nade_list,f"list.cfg")
