import json
import os
import shutil
from dataclasses import dataclass, field
from typing import List

def copy_file_overwrite(src_path: str, dst_path: str):
    shutil.copyfile(src_path, dst_path)


def append_line_to_file(file_path: str, text: str):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write('\n' + text)


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

def append_resource(key,zh,en):
    zhtext = f"	\"#{key}\"										\"{zh}\"";
    entext = f"	\"#{key}\"										\"{en}\"";
    append_line_to_file("../../../resource/keybindings_schinese.txt",zhtext)
    append_line_to_file("../../../resource/keybindings_tchinese.txt",zhtext)
    append_line_to_file("../../../resource/keybindings_english.txt",entext)

def append(s,text):
    return s+'\n'+text



@dataclass(order=True)
class Grenade:
    priority: int
    command: str = field(compare=False)
    map_name: str = field(compare=False)

class GrenadeFileGenerator:
    VALID_MAPS = {"dust2", "mirage", "inferno", "nuke", "train", "anubis", "other"}
    BASE_DIR = os.path.join("..", "..", "gui", "grenade")

    def __init__(self):
        self.grenades: List[Grenade] = []

    def add_grenade(self, map_name: str, command: str, priority: int):
        if map_name not in self.VALID_MAPS:
            print(f"错误：道具 '{command}' 的地图名 '{map_name}' 无效。")
            exit(1)
        print(f'ok accept "{map_name}" "{command}" "{priority}"')
        self.grenades.append(Grenade(priority=priority, command=command, map_name=map_name))

    def generate_files(self):
        for map_name in self.VALID_MAPS:
            map_grenades = [g for g in self.grenades if g.map_name == map_name]

            # 按优先级排序
            map_grenades.sort()

            # 创建或清理目录
            dir_path = os.path.join(self.BASE_DIR, map_name)
            os.makedirs(dir_path, exist_ok=True)
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    
            if not map_grenades:
                continue

            # 写入 list.txt
            list_path = os.path.join(dir_path, "list.txt")
            with open(list_path, "w", encoding="utf-8") as f:
                for grenade in map_grenades:
                    f.write(f"{grenade.command}\n")



# 主流程
if __name__ == "__main__":
    grenades = load_grenades("list.json")  # 你的 JSON 路径
    nade_list=""

    copy_file_overwrite("../../../resource/src/keybindings_schinese.txt","../../../resource/keybindings_schinese.txt");
    copy_file_overwrite("../../../resource/src/keybindings_tchinese.txt","../../../resource/keybindings_tchinese.txt");
    copy_file_overwrite("../../../resource/src/keybindings_english.txt","../../../resource/keybindings_english.txt");

    gre = GrenadeFileGenerator();

    for g in grenades:
        ID=g['id'];
        
        append_resource(ID,g["name_zh_cn"],g["name_en_us"]);

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

        gre.add_grenade(g['map'],f'hzNade_load_{ID}',g['priority'])

        content=append(content,f'alias hzNade_info_yaw yaw {yaw} 1 1')
        content=append(content,f'alias hzNade_info_pitch pitch {pitch} 1 1')
        content=append(content,f'alias hzNade_info_pos "setpos {g['position']['x']} {g['position']['y']} 0"')
        content=append(content,f'alias hzNade_info_pre_cmd "{g['pre_throw_command']}"')
        content=append(content,f'alias hzNade_info_post_cmd "{g['post_throw_command']}"')
        content=append(content,f'alias hzNade_info_throw_cmd "{g['throw_command']}"')
        content=append(content,f'alias hzNade_info_type "+hzBind_{ty};-hzBind_{ty}"')
        write_output(content,f"data/{ID}.cfg")
        
    write_output(nade_list,f"list.cfg")
    append_line_to_file("../../../resource/keybindings_schinese.txt","}")
    append_line_to_file("../../../resource/keybindings_tchinese.txt","}")
    append_line_to_file("../../../resource/keybindings_english.txt","}")

    gre.generate_files()