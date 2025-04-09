import easyocr
import cv2
import os
import torch
from gc import collect  # 内存回收

# ------------------- 配置区域 -------------------
input_folder = r'D:\BaiduNetdiskDownload\051-100_images2'
languages = ['ch_sim', 'en']
supported_exts = ['.jpg', '.jpeg', '.png']
# ----------------------------------------------

# GTX 1050Ti 优化参数
config = {
    'batch_size': 4,           # 显存有限，建议4-6
    'workers': 2,              # 避免过多线程竞争
    'fp16': False,             # 1050Ti不支持Tensor Core，关闭半精度
    'model_load': 'balanced'   # 显存优化模式
}

def merge_paragraphs(results):
    """轻量级段落合并算法"""
    if not results:
        return []
    
    # 按Y坐标排序
    sorted_results = sorted(results, key=lambda x: x[0][0][1])
    
    # 合并逻辑（简化版）
    paragraphs = []
    current_para = []
    prev_bottom = -100  # 初始间距
    
    for box, text, _ in sorted_results:
        top = box[0][1]
        # 行间距超过50像素视为新段落（根据漫画排版调整）
        if (top - prev_bottom) > 50:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        current_para.append(text.strip())
        prev_bottom = box[3][1]  # 更新底部坐标
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs

def process_image(reader, image_path, output_path):
    """处理单张图片并管理显存"""
    try:
        # 读取图片
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("图片读取失败")
        
        # 显存优化策略
        torch.cuda.empty_cache()
        
        # 执行OCR
        results = reader.readtext(
            img,
            batch_size=config['batch_size'],
            workers=config['workers'],
            detail=1,          # 必须为1才能获取坐标
            paragraph=False    # 禁用内置段落合并（使用自定义算法）
        )
        
        # 合并段落
        paragraphs = merge_paragraphs(results)
        
        # 保存结果
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(paragraphs))
        
        return True
    except Exception as e:
        print(f"处理失败: {str(e)}")
        return False
    finally:
        collect()  # 强制回收内存

if __name__ == "__main__":
    # 验证CUDA
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA不可用，请检查驱动")
    
    # 初始化Reader（显存优化配置）
    reader = easyocr.Reader(
        lang_list=languages,
        gpu=True,
        detector=True,
        recognizer=True,
        model_storage_directory=None,
        download_enabled=False,
        user_network_directory=None
    )
    
    # 遍历处理
    total = len([f for f in os.listdir(input_folder) if any(f.endswith(ext) for ext in supported_exts)])
    processed = 0
    
    for filename in os.listdir(input_folder):
        if not any(filename.lower().endswith(ext) for ext in supported_exts):
            continue
        
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(
            input_folder,
            f"{os.path.splitext(filename)[0]}.txt"
        )
        
        print(f"处理中 [{processed+1}/{total}]: {filename[:20]}...", end='', flush=True)
        
        if process_image(reader, image_path, output_path):
            print(" ✓")
            processed += 1
        else:
            print(" ✗")
    
    print(f"\n完成！成功处理 {processed}/{total} 张图片")  