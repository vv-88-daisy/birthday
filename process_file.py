import os
import argparse

def rename_files_continuous(folder_path, target_ext=None, start_num=1, prefix="p"):
    """
    强制按连续序号重命名（从start_num开始，无缺失，带p前缀）
    :param folder_path: 目标文件夹路径
    :param target_ext: 重命名后的扩展名（None保留原扩展名）
    :param start_num: 起始序号（默认1）
    :param prefix: 前缀（默认p）
    """
    # 验证文件夹
    if not os.path.isdir(folder_path):
        print(f"❌ 错误：文件夹 '{folder_path}' 不存在！")
        return

    # 步骤1：获取所有文件，过滤出目标类型，按文件名排序（避免乱序）
    file_list = []
    for filename in os.listdir(folder_path):
        file_full_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_full_path):
            # 筛选扩展名（如果指定）
            if target_ext is None or filename.lower().endswith(target_ext.lower().lstrip(".")):
                file_list.append(filename)
    
    # 按文件名排序（保证遍历顺序固定）
    file_list.sort()

    if not file_list:
        print(f"⚠️  文件夹中未找到符合条件的文件")
        return

    # 步骤2：强制分配连续序号（忽略原有文件名，从start_num开始）
    renamed_count = 0
    for seq in range(start_num, start_num + len(file_list)):
        # 取当前要处理的文件（按排序后的顺序）
        old_name = file_list[seq - start_num]
        old_full_path = os.path.join(folder_path, old_name)

        # 确定最终扩展名
        _, old_ext = os.path.splitext(old_name)
        final_ext = target_ext if target_ext is not None else old_ext
        if final_ext and not final_ext.startswith("."):
            final_ext = f".{final_ext}"
        
        # 生成连续序号的新文件名（p1、p2、p3...）
        new_name = f"{prefix}{seq}{final_ext}"
        new_full_path = os.path.join(folder_path, new_name)

        # 执行重命名（可选：覆盖/跳过已存在的文件）
        try:
            # 方案A：覆盖已存在的文件（推荐，保证序号连续）
            os.rename(old_full_path, new_full_path)
            print(f"✅ 重命名：{old_name} → {new_name}")
            renamed_count += 1

            # 方案B：跳过已存在的文件（取消下面注释，注释方案A）
            # if not os.path.exists(new_full_path):
            #     os.rename(old_full_path, new_full_path)
            #     print(f"✅ 重命名：{old_name} → {new_name}")
            #     renamed_count += 1
            # else:
            #     print(f"⚠️  跳过 {old_name}：{new_name} 已存在")
        except Exception as e:
            print(f"❌ 失败 {old_name}：{str(e)}")

    print(f"\n📊 完成！共处理 {renamed_count}/{len(file_list)} 个文件，序号范围：{start_num}~{start_num + len(file_list) - 1}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="强制连续序号重命名（带p前缀）")
    parser.add_argument("folder", help="目标文件夹路径")
    parser.add_argument("-e", "--ext", help="重命名后的扩展名（如 txt、jpg）")
    parser.add_argument("-s", "--start", type=int, default=1, help="起始序号（默认1）")
    parser.add_argument("-p", "--prefix", default="p", help="前缀（默认p）")
    args = parser.parse_args()

    rename_files_continuous(args.folder, args.ext, args.start, args.prefix)