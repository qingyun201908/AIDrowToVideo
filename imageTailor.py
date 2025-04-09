from PIL import Image
import os

def batch_crop_images(input_folder, output_folder, top, bottom):
    """
    批量裁剪图片（仅修改下边界，保持左右宽度不变）
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param top: 裁剪区域上边界
    :param bottom: 裁剪区域下边界
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            with Image.open(image_path) as img:
                width, height = img.size
                # 保持左右不变（left=0, right=图片宽度）
                # 动态调整下边界，确保不超过图片高度
                adjusted_bottom = min(bottom, height)
                # 裁剪区域：左=0, 上=top, 右=width, 下=adjusted_bottom
                cropped_img = img.crop((0, top, width, adjusted_bottom))
                output_path = os.path.join(output_folder, filename)
                cropped_img.save(output_path)
                print(f"裁剪并保存: {output_path}")

# 示例调用
input_folder = "D:\\BaiduNetdiskDownload\\051-100_images"
output_folder = "D:\\BaiduNetdiskDownload\\051-100_images2"
top, bottom = 0, 1225  # 仅设置上边界和下边界

batch_crop_images(input_folder, output_folder, top, bottom)