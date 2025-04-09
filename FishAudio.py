import os
import logging
from fish_audio_sdk import Session, TTSRequest, ReferenceAudio

# 配置日志记录异常
logging.basicConfig(
    filename='tts_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_directory(target_dir: str):
    """处理指定目录下的文本文件
    
    Args:
        target_dir: 包含文本文件和生成音频文件的目录
    """
    session = Session("")
    
    processed = 0
    skipped = 0
    errors = 0

    for filename in os.listdir(target_dir):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(target_dir, filename)
        base_name = os.path.splitext(filename)[0]
        audio_path = os.path.join(target_dir, f"{base_name}.mp3")

        try:
            # 读取文本内容
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()

            # 跳过空文件
            if not text:
                logging.info(f"跳过空文件: {filename}")
                skipped += 1
                continue

            # 生成语音文件
            with open(audio_path, "wb") as f:
                for chunk in session.tts(TTSRequest(
                    reference_id="7f92f8afb8ec43bf81429cc1c9199cb1",
                    text=text
                )):
                    f.write(chunk)

            print(f"生成成功: {filename} -> {os.path.basename(audio_path)}")
            processed += 1

        except Exception as e:
            logging.error(f"文件 {filename} 处理失败: {str(e)}", exc_info=True)
            print(f"错误: {filename} 转换失败，详见日志")
            errors += 1

    # 输出统计报告
    print(f"\n处理完成: 成功 {processed} 个 | 跳过 {skipped} 个 | 失败 {errors} 个")

if __name__ == "__main__":
    # 使用示例：处理当前目录下的文件
    process_directory(target_dir="D:\\BaiduNetdiskDownload\\001-050_images")