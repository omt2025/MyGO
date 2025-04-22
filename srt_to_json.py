import re
import json
import os

# 读取 SRT 文件内容
def read_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 计算文本相似度（示例）
def calculate_similarity(text1, text2):
    return 0.794  # 示例相似度

# 去除 HTML 标签
def remove_html_tags(text):
    return re.sub(r'<.*?>', '', text)

# SRT 转 JSON
def convert_srt_to_json(srt_content):
    srt_lines = srt_content.strip().split('\n')
    result = []
    for i in range(0, len(srt_lines), 3):
        index = srt_lines[i].strip()
        time_range = srt_lines[i + 1].strip()
        text = srt_lines[i + 2].strip()

        # 只保留 font face="Source Han Sans SC" 的文本
        if 'font face="Source Han Sans SC"' not in text:
            continue

        text = remove_html_tags(text)

        # 提取时间戳（格式: 00:00:16,320 --> 00:00:17,400）
        timestamp_match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})", time_range)
        if timestamp_match:
            start_minute = int(timestamp_match.group(2))
            start_second = int(timestamp_match.group(3))
            timestamp = f"{start_minute}m{start_second}s"
        else:
            timestamp = "Unknown"

        similarity = calculate_similarity(text, "你想要比较的文本")

        result.append({
            "timestamp": timestamp,
            "similarity": similarity,
            "text": text
        })

    return result

# 保存 JSON 文件
def save_json_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 从视频文件名提取字幕文件名
def extract_subtitle_name(video_filename):
    match = re.search(r"\] (.+? \[\d+\])", video_filename)
    if match:
        return match.group(1)
    return "subtitles"

# 读取路径并去除两端的双引号
srt_file_path = input("请输入SRT文件的路径（例如 C:\\mygo\\output_subtitles.srt）：").strip('"')
video_file_path = input("请输入原始视频文件的路径（例如 C:\\mygo\\[KitaujiSub] BanG Dream! Ave Mujica [01][WebRip][HEVC_AAC][CHS_JP&CHT_JP].mkv）：").strip('"')
output_folder = input("请输入输出目录：").strip('"')

# 使用原始字符串处理路径
srt_file_path = r"{}".format(srt_file_path)
video_file_path = r"{}".format(video_file_path)
output_folder = r"{}".format(output_folder)


try:
    # 提取字幕文件名
    video_filename = os.path.basename(video_file_path)
    subtitle_name = extract_subtitle_name(video_filename)

    # 生成 JSON 文件路径
    json_file_path = os.path.join(os.path.dirname(srt_file_path), "subtitles_output", f"{subtitle_name}.json")

    # 读取 SRT 文件
    srt_content = read_srt_file(srt_file_path)

    # 转换 SRT 为 JSON
    json_data = convert_srt_to_json(srt_content)

    # 保存 JSON 文件
    save_json_to_file(json_data, json_file_path)

    print(f"JSON 文件已保存到: {json_file_path}")

except FileNotFoundError:
    print("指定的文件路径未找到，请检查路径是否正确。")
except Exception as e:
    print(f"发生错误：{e}")
