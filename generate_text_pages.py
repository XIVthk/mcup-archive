#!/usr/bin/env python3
import os
import shutil
from jinja2 import Template

# 【配置区域】
TXT_SOURCE_DIR = "novels"       # 您的TXT文件存放目录
PDF_SOURCE_DIR = "novels"        # 您的PDF文件存放目录
TEMPLATE_FILE = "templates/text_reading_template.html"
OUTPUT_DIR = "reading"           # 生成的阅读页存放目录

def generate_reading_pages():
    # 0. 确保输出目录存在（清空旧的）
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. 读取模板
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()
    template = Template(template_content)

    # 2. 遍历所有TXT文件
    for filename in os.listdir(TXT_SOURCE_DIR):
        if not filename.endswith('.txt'):
            continue  # 跳过非TXT文件

        print(f"处理中: {filename}")

        # 3. 准备模板变量
        base_name = filename.replace('.txt', '')
        txt_url = f"../{TXT_SOURCE_DIR}/{filename}"
        pdf_url = f"../{PDF_SOURCE_DIR}/{base_name}.pdf"

        # 4. 渲染HTML
        html_content = template.render(
            title=base_name,
            txt_url=txt_url,
            pdf_url=pdf_url
        )

        # 5. 写入文件
        output_filename = f"{base_name}.html"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ 已生成: {output_path}")

    print("\n🎉 所有文本阅读页生成完毕！")

if __name__ == '__main__':
    generate_reading_pages()