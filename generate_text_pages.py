#!/usr/bin/env python3
import os
import shutil
import markdown  # 需要先安装: pip install markdown
from jinja2 import Template

# 【配置区域】
SOURCE_DIR = "novels"           # 源文件目录（支持 .txt 和 .md）
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

    # 2. 遍历所有支持的文件（.txt 和 .md）
    supported_extensions = ('.txt', '.md')
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(supported_extensions)]
    
    for filename in files:
        print(f"处理中: {filename}")

        # 获取基础名称（不含扩展名）
        base_name = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]
        file_path = os.path.join(SOURCE_DIR, filename)
        
        # 读取原始内容
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # 根据扩展名决定是否渲染 Markdown
        if file_ext == '.md':
            # 将 Markdown 转换为 HTML
            html_content = markdown.markdown(raw_content, extensions=[
                'extra',        # 表格、脚注等扩展
                'codehilite',   # 代码高亮（可选）
                'toc',          # 目录
                'nl2br',        # 换行转 <br>
            ])
            content_type = 'markdown'
        else:
            # TXT 文件：保持纯文本，但保留换行
            html_content = f'<div class="plain-text">{raw_content.replace(chr(10), "<br>")}</div>'
            content_type = 'plain'
        
        # 准备模板变量
        txt_url = f"../{SOURCE_DIR}/{filename}"
        pdf_url = f"../{SOURCE_DIR}/{base_name}.pdf"
        
        # 检查 PDF 是否存在
        pdf_exists = os.path.exists(os.path.join(SOURCE_DIR, f"{base_name}.pdf"))

        # 渲染 HTML
        html_output = template.render(
            title=base_name,
            content=html_content,
            content_type=content_type,
            txt_url=txt_url,
            pdf_url=pdf_url if pdf_exists else "#",
            pdf_exists=pdf_exists
        )

        # 写入文件
        output_filename = f"{base_name}.html"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)

        print(f"✅ 已生成: {output_path} (类型: {content_type})")

    print(f"\n🎉 所有阅读页生成完毕！共处理 {len(files)} 个文件。")

if __name__ == '__main__':
    generate_reading_pages()