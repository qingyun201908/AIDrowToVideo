import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder):
    """
    从PDF文件中提取所有图片并按顺序保存到指定文件夹
    
    参数:
        pdf_path (str): PDF文件路径
        output_folder (str): 图片保存目录
    """
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)
    
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    
    # 初始化图片计数器
    image_count = 0
    
    # 遍历每一页
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # 获取当前页所有图片列表
        image_list = page.get_images(full=True)
        
        # 遍历当前页的图片
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]  # 获取图片xref
            base_image = doc.extract_image(xref)  # 提取图片信息
            image_data = base_image["image"]      # 获取图片二进制数据
            ext = base_image["ext"]               # 获取图片扩展名
            
            # 生成图片文件名
            image_filename = f"image_{image_count + 1}.{ext}"
            image_path = os.path.join(output_folder, image_filename)
            
            # 保存图片
            with open(image_path, "wb") as img_file:
                img_file.write(image_data)
            
            image_count += 1
    
    print(f"成功提取 {image_count} 张图片到目录: {output_folder}")

if __name__ == "__main__":
    # 配置参数（根据实际情况修改）
    pdf_file = "D:\\BaiduNetdiskDownload\\一-人-之-下第051-100话.pdf"  # PDF文件路径
    
    # 自动生成输出文件夹路径（PDF文件名 + _images）
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]  # 去除扩展名
    folder_name = f"{base_name}_images"  # 生成文件夹名称
    output_dir = os.path.join(os.path.dirname(pdf_file), folder_name)  # 完整输出路径
    
    # 执行提取
    extract_images_from_pdf(pdf_file, output_dir)