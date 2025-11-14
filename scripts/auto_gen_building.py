#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def process_and_write_files(input_folder, output_folder, search_keys, insert_lines):
    """
    扫描输入文件夹中的文件，找到指定的行，在其下一行插入新内容，输出到指定文件夹

    Args:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径
        search_keys: 要查找的键值对列表，例如 ["city = yes"]
        insert_lines: 要插入的内容数组，例如 ["special_tag = yes", "another = no"]
    """
    # 确保输入路径存在
    if not os.path.isdir(input_folder):
        print(f"错误：输入路径不存在 - {input_folder}")
        return

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建输出文件夹：{output_folder}")

    file_count = 0
    total_insertions = 0

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_filepath = os.path.join(input_folder, filename)

        # 只处理文件，跳过文件夹
        if not os.path.isfile(input_filepath):
            continue

        try:
            # 读取原文件
            with open(input_filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 处理文件内容
            modified_lines = []
            insertions_in_file = 0

            for i, line in enumerate(lines):
                modified_lines.append(line)

                # 检查当前行是否匹配任何search_keys
                for search_key in search_keys:
                    if search_key in line:
                        # 在这一行后面插入新内容
                        for insert_line in insert_lines:
                            # 保持相同的缩进
                            indent = len(line) - len(line.lstrip())
                            modified_lines.append("\t" * (indent // 4) + insert_line + "\n")
                            insertions_in_file += 1
                        break  # 只匹配第一个search_key

            # 如果有修改，写入输出文件
            if insertions_in_file > 0:
                output_filepath = os.path.join(output_folder, filename)
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.writelines(modified_lines)

                print(f"✓ {filename} ({insertions_in_file} 处插入)")
                file_count += 1
                total_insertions += insertions_in_file

        except Exception as e:
            print(f"✗ 处理文件失败 {filename}：{e}")
            continue

    print(f"\n完成！")
    print(f"处理了 {file_count} 个文件，共 {total_insertions} 处插入")
    print(f"输出文件夹：{output_folder}")

def main():
    # ========== 配置部分 ==========

    # 输入文件夹路径（要扫描的文件夹）
    input_folder = "in_game/common/building_types"

    # 输出文件夹路径（生成的文件会放在这里）
    output_folder = "output/building_injections"

    # 要查找的键值对列表
    search_keys = [
        "city = yes",
        "super_metropolis = yes"
    ]

    # 要插入的内容数组（会在找到的行下一行插入）
    insert_lines = [
        "special_tag = yes",
        "another_property = no"
    ]

    # ========== 执行部分 ==========

    # 转换为绝对路径
    if not os.path.isabs(input_folder):
        input_folder = os.path.join(os.getcwd(), input_folder)

    if not os.path.isabs(output_folder):
        output_folder = os.path.join(os.getcwd(), output_folder)

    print(f"输入文件夹：{input_folder}")
    print(f"输出文件夹：{output_folder}")
    print(f"查找键值对：{search_keys}")
    print(f"插入内容：{insert_lines}")
    print("-" * 80)

    # 执行处理
    process_and_write_files(input_folder, output_folder, search_keys, insert_lines)

if __name__ == "__main__":
    main()
