import os
import subprocess

def merge_videos(folder_path, output_file):
    # 获取所有视频文件
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    video_files.sort()  # 根据名称排序，确保顺序正确

    # 生成 FFmpeg 需要的输入列表文件
    list_file = os.path.join(folder_path, 'file_list.txt')
    with open(list_file, 'w', encoding='utf-8') as f:
        for video in video_files:
            f.write(f"file '{os.path.join(folder_path, video)}'\n")

    # FFmpeg 合并视频
    ffmpeg_cmd = f'ffmpeg -f concat -safe 0 -i "{list_file}" -c copy "{output_file}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

    # 清理文件
    os.remove(list_file)
    print(f"合并完成：{output_file}")

# 使用示例
merge_videos("D:\\BaiduNetdiskDownload\\001-050_images\\output_videos", "output.mp4")
