import os
import glob
import subprocess

# 支持的图片和音频扩展名
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg']

def find_audio_file(image_path):
    """查找与图片同名的音频文件"""
    base_name = os.path.splitext(image_path)[0]
    for ext in AUDIO_EXTENSIONS:
        audio_path = f"{base_name}{ext}"
        if os.path.exists(audio_path):
            return audio_path
    return None

def create_video(image_path, output_folder):
    """使用 FFmpeg 创建视频"""
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_folder, f"{base_name}.mp4")
    
    cmd = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', image_path,
    ]

    if audio_path := find_audio_file(image_path):
        cmd += ['-i', audio_path]
    else:
        cmd += [
            '-f', 'lavfi',
            '-i', 'anullsrc=cl=stereo:r=44100',
            '-t', '3'
        ]

    cmd += [
        '-vf', 
        'scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=24,format=yuv420p',  # 关键修改点
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-shortest',
        '-movflags', '+faststart',
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 错误: {e.stderr}")
        return False

def process_folder(folder_path):
    """处理整个文件夹"""
    # 收集所有图片文件
    image_files = []
    for ext in IMAGE_EXTENSIONS:
        image_files.extend(glob.glob(os.path.join(folder_path, '*' + ext)))

    # 创建输出目录
    output_folder = os.path.join(folder_path, "output_videos")
    os.makedirs(output_folder, exist_ok=True)

    # 处理每个图片文件
    for img_file in image_files:
        print(f"正在处理: {os.path.basename(img_file)}")
        if create_video(img_file, output_folder):
            print(f"成功创建: {os.path.basename(img_file)}.mp4")
        else:
            print(f"处理失败: {os.path.basename(img_file)}")
        print("-" * 50)

if __name__ == "__main__":
    target_folder = "D:\\BaiduNetdiskDownload\\001-050_images"
    
    if not os.path.exists(target_folder):
        print(f"错误: 目录不存在 - {target_folder}")
    else:
        process_folder(target_folder)
        print("全部处理完成！")