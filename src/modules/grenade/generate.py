import json
import os
import shutil
from dataclasses import dataclass, field
from typing import List


# 工具函数部分 ----------------------------------------------------------------

def copy_file_with_overwrite(src: str, dst: str):
    shutil.copyfile(src, dst)


def append_line(filepath: str, line: str):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write('\n' + line)


def load_grenade_data(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'grenades' in data:
        return data['grenades']
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Invalid JSON structure: expected list or object with 'grenades' key")


def format_grenade_description(grenade: dict) -> str:
    name = grenade.get("name_en_us", grenade.get("id", "unknown"))
    map_name = grenade["map"]
    cmd = grenade["throw_command"]
    angle = grenade["angle"]
    return f"[{name}] ({map_name})\nCommand: {cmd}\nAngle: pitch={angle['pitch']}, yaw={angle['yaw']}\n"


def write_text_file(content: str, relative_path: str):
    abs_path = os.path.abspath(relative_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✔ 写入成功: {abs_path}")


def append_keybinding_resource(key: str, zh: str, en: str):
    zh_entry = f'\t"#{key}"\t\t\t\t\t\t\t\t\t"{zh}"'
    en_entry = f'\t"#{key}"\t\t\t\t\t\t\t\t\t"{en}"'

    append_line("../../../resource/keybindings_schinese.txt", zh_entry)
    append_line("../../../resource/keybindings_tchinese.txt", zh_entry)
    append_line("../../../resource/keybindings_english.txt", en_entry)


def append_text(base: str, line: str) -> str:
    return base + '\n' + line


# 数据结构与文件生成类 ------------------------------------------------------

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

    def add(self, map_name: str, command: str, priority: int):
        if map_name not in self.VALID_MAPS:
            print(f"错误：地图名无效 -> {map_name}（道具命令: {command}）")
            exit(1)
        print(f'ok accept "{map_name}" "{command}" "{priority}"')
        self.grenades.append(Grenade(priority=priority, command=command, map_name=map_name))

    def generate_map_cfg_files(self):
        for map_name in self.VALID_MAPS:
            grenades_in_map = [g for g in self.grenades if g.map_name == map_name]
            grenades_in_map.sort()

            dir_path = os.path.join(self.BASE_DIR, map_name)
            os.makedirs(dir_path, exist_ok=True)

            # 清理旧文件
            for fname in os.listdir(dir_path):
                file_path = os.path.join(dir_path, fname)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            if not grenades_in_map:
                continue

            list_txt_path = os.path.join(dir_path, "list.txt")
            with open(list_txt_path, "w", encoding="utf-8") as f:
                for grenade in grenades_in_map:
                    f.write(f"{grenade.command}\n")


# 主程序流程 -----------------------------------------------------------------

if __name__ == "__main__":
    grenade_data = load_grenade_data("list.json")
    alias_list = ""

    # 复制源绑定文件
    copy_file_with_overwrite("../../../resource/src/keybindings_schinese.txt", "../../../resource/keybindings_schinese.txt")
    copy_file_with_overwrite("../../../resource/src/keybindings_tchinese.txt", "../../../resource/keybindings_tchinese.txt")
    copy_file_with_overwrite("../../../resource/src/keybindings_english.txt", "../../../resource/keybindings_english.txt")

    generator = GrenadeFileGenerator()

    for entry in grenade_data:
        grenade_id = entry['id']
        append_keybinding_resource(grenade_id, entry["name_zh_cn"], entry["name_en_us"])

        # 计算视角角度
        sensitivity = 2.52
        m_yaw = 0.022
        m_pitch = 0.022

        yaw = -entry['angle']['yaw'] / (sensitivity * m_yaw)
        pitch = entry['angle']['pitch'] / (sensitivity * m_pitch)

        grenade_type = entry['type']
        grenade_map = entry['map']
        grenade_priority = entry['priority']

        alias_name = f"hzNade_load_{grenade_id}"
        alias_list = append_text(alias_list, f'alias {alias_name} exec Horizon/src/modules/grenade/data/{grenade_id}.cfg')
        generator.add(grenade_map, alias_name, grenade_priority)

        config_content = ""
        config_content = append_text(config_content, f'alias hzNade_info_yaw yaw {yaw} 1 1')
        config_content = append_text(config_content, f'alias hzNade_info_pitch pitch {pitch} 1 1')
        config_content = append_text(config_content, f'alias hzNade_info_pos "setpos {entry["position"]["x"]} {entry["position"]["y"]} 0"')
        config_content = append_text(config_content, f'alias hzNade_info_pre_cmd "{entry["pre_throw_command"]}"')
        config_content = append_text(config_content, f'alias hzNade_info_post_cmd "{entry["post_throw_command"]}"')
        config_content = append_text(config_content, f'alias hzNade_info_throw_cmd "{entry["throw_command"]}"')
        config_content = append_text(config_content, f'alias hzNade_info_type "+hzBind_{grenade_type};-hzBind_{grenade_type}"')

        write_text_file(config_content, f"data/{grenade_id}.cfg")

    write_text_file(alias_list, "list.cfg")

    for lang in ["schinese", "tchinese", "english"]:
        append_line(f"../../../resource/keybindings_{lang}.txt", "}")

    generator.generate_map_cfg_files()
