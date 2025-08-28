import json
import os
import shutil
from dataclasses import dataclass, field
from typing import List
import math
import re
import subprocess

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
    zh_entry = f'\t"{key}"\t\t\t\t\t\t\t\t\t"{zh}"'
    en_entry = f'\t"{key}"\t\t\t\t\t\t\t\t\t"{en}"'

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
    VALID_MAPS = {"dust2", "mirage", "inferno", "nuke", "train", "anubis", "ancient","other"}
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

            # if not grenades_in_map:
            #     continue

            list_txt_path = os.path.join(dir_path, "list.txt")
            with open(list_txt_path, "w", encoding="utf-8") as f:
                for grenade in grenades_in_map:
                    f.write(f"{grenade.command}\n")
            print(list_txt_path)
            generate_gui_files(list_txt_path)
            # generate_gui_files(os.path.join(dir_path, "list1.txt"))

# 生成 gui 文件
def truncate_path_from_horizon(relative_path: str) -> str:
    # 获取绝对路径
    abs_path = os.path.dirname(os.path.abspath(relative_path))
    # 分割路径为组件列表
    parts = abs_path.replace('\\', '/').split('/')
    # 查找 Horizon 出现的位置
    if "Horizon" in parts:
        index = parts.index("Horizon")
        # 从 Horizon 开始重组成路径
        truncated = '/'.join(parts[index:])
        return truncated
    else:
        raise ValueError("路径中未包含 'Horizon' 文件夹")
def generate_gui_files(txt_path):
    # 读取 grenade id 列表
    with open(txt_path, 'r', encoding='utf-8') as f:
        grenade_ids = [line.strip() for line in f if line.strip()]

    fpath=truncate_path_from_horizon(txt_path)

    # 计算分页数量，每页15个有效槽位
    total_ids = len(grenade_ids)
    pages = max(math.ceil(total_ids / 15),1)

    # 补齐至每页15个（用 "none" 占位）
    grenade_ids += ['none'] * (pages * 15 - total_ids)

    # 获取当前目录
    directory = os.path.dirname(os.path.abspath(txt_path))

    # 清除已有 gui_i_cmd.cfg 和 gui_i_txt.cfg 文件
    pattern = re.compile(r'^gui_\d+_(cmd|txt)\.cfg$')
    for filename in os.listdir(directory):
        if pattern.match(filename):
            os.remove(os.path.join(directory, filename))

    # 槽位顺序：2, 1, 0；每个槽位编号顺序：1-8
    slot_order = [1,2, 0]
    reserved_indices = {1, 2, 8}  # 1-based编号
    positions_per_slot = 8

    for page in range(pages):
        cmd_lines = []
        txt_lines = []

        # 当前页的15个 grenade id
        page_ids = grenade_ids[page * 15 : (page + 1) * 15]
        id_index = 0  # 当前分配的 grenade id 索引

        for slot in slot_order:
            for idx in range(1, positions_per_slot + 1):
                cvar = f'cl_radial_radio_tab_{slot}_text_{idx}'
                if idx in reserved_indices:
                    if idx == 1:
                        cmd_lines.append(f'{cvar} cmd";alias hzGUI_grenade_setTXT exec Horizon_Epsilon/src/gui/grenade/gui_1_txt.cfg;alias hzGUI_grenade_setCMD exec Horizon_Epsilon/src/gui/grenade/gui_1_cmd.cfg;\n')
                        txt_lines.append(f'{cvar} "#CFG_Function_LstMenu"\n')
                    elif idx==8:
                        if slot==0:
                            cmd_lines.append(f'{cvar} cmd";\n')
                            txt_lines.append(f'{cvar} "#CFG_Function_WheelPrePage"\n')
                        elif slot==1:
                            cmd_lines.append(f'{cvar} cmd";\n')
                            txt_lines.append(f'{cvar} "#CFG_Function_WheelPrePage"\n')
                        else:
                            if page==0:
                                cmd_lines.append(f'{cvar} cmd";\n')
                                txt_lines.append(f'{cvar} "#CFG_Function_IsPrePage"\n')
                            else:
                                cmd_lines.append(f'{cvar} cmd";alias hzGUI_grenade_setTXT exec {fpath}/gui_{page}_txt.cfg;alias hzGUI_grenade_setCMD exec {fpath}/gui_{page}_cmd.cfg;\n')
                                txt_lines.append(f'{cvar} "#CFG_Function_PrePage"\n')
                                
                    else:
                        if slot==0:
                            if page+1==pages:
                                cmd_lines.append(f'{cvar} cmd";\n')
                                txt_lines.append(f'{cvar} "#CFG_Function_IsNxtPage"\n')
                            else:
                                cmd_lines.append(f'{cvar} cmd";alias hzGUI_grenade_setTXT exec {fpath}/gui_{page+2}_txt.cfg;alias hzGUI_grenade_setCMD exec {fpath}/gui_{page+2}_cmd.cfg;\n')
                                txt_lines.append(f'{cvar} "#CFG_Function_NxtPage"\n')
                        elif slot==1:
                            cmd_lines.append(f'{cvar} cmd";\n')
                            txt_lines.append(f'{cvar} "#CFG_Function_WheelNxtPage"\n')
                        else:
                            cmd_lines.append(f'{cvar} cmd";\n')
                            txt_lines.append(f'{cvar} "#CFG_Function_WheelNxtPage"\n')
                else:
                    gid = page_ids[id_index]
                    id_index += 1
                    cmd_lines.append(f'{cvar} cmd";hzNade_load_{gid};\n')
                    txt_lines.append(f'{cvar} "#{gid}"\n')
            cmd_lines.append("\n");
            txt_lines.append("\n");

        # 写入文件
        with open(os.path.join(directory, f'gui_{page+1}_cmd.cfg'), 'w', encoding='utf-8') as f_cmd:
            f_cmd.writelines(cmd_lines)
        with open(os.path.join(directory, f'gui_{page+1}_txt.cfg'), 'w', encoding='utf-8') as f_txt:
            f_txt.writelines(txt_lines)

    print(f'已生成 {pages} 页，共 {pages * 2} 个 GUI 文件。')


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
        pitch = (entry['angle']['pitch']-89.00) / (sensitivity * m_pitch)

        grenade_type = entry['type']
        grenade_map = entry['map']
        grenade_priority = entry['priority']

        alias_name = f"{grenade_id}"
        alias_list = append_text(alias_list, f'alias hzNade_load_{alias_name} exec Horizon_Epsilon/src/modules/grenade/data/{grenade_id}.cfg')
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
    subprocess.run([os.path.abspath("../../../install.bat")], shell=True)


