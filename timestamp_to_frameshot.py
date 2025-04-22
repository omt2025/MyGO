import json
import subprocess


# 读取 JSON 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 将时间戳转换为 FFmpeg 可接受的格式
def convert_timestamp_to_ffmpeg_format(timestamp):
    # 假设时间戳格式为 "0m16s"，需要转换成 "00:00:16"
    minutes, seconds = timestamp.split('m')
    seconds = seconds.rstrip('s')
    return f"00:{int(minutes):02}:{int(seconds):02}"


# 截取视频截图
def capture_screenshot(video_file, timestamp, output_file):
    # 转换时间戳格式
    ffmpeg_time = convert_timestamp_to_ffmpeg_format(timestamp)

    # 限制只处理视频的前2分钟
    duration = '00:02:00'  # 前2分钟

    # 构建 FFmpeg 命令
    command = [
        'ffmpeg',
        '-i', video_file,
        '-ss', ffmpeg_time,
        '-t', duration,  # 设置截取时间为2分钟
        '-vframes', '1',
        output_file
    ]

    # 执行命令
    subprocess.run(command)


# 主函数
def main():
    # 输入文件路径
    json_file_path = input("请输入JSON文件的路径：")
    video_file_path = input("请输入视频文件的路径：")
    output_folder = input("请输入输出目录：")

    # 读取 JSON 文件
    try:
        json_data = read_json_file(json_file_path)

        # 遍历每个时间戳并截图
        for i, item in enumerate(json_data):
            timestamp = item['timestamp']
            output_file = f"{output_folder}/screenshot_{i + 1}.jpg"
            capture_screenshot(video_file_path, timestamp, output_file)
            print(f"截图已保存: {output_file}")

    except FileNotFoundError:
        print("JSON 文件或视频文件未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()
