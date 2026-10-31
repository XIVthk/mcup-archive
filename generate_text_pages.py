#!/usr/bin/env python3
import os
import shutil
import html
import markdown
from jinja2 import Template

SOURCE_DIR = "novels"
TEMPLATE_FILE = "templates/text_reading_template.html"
OUTPUT_DIR = "reading"

def generate_reading_pages():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()
    template = Template(template_content)

    supported_extensions = ('.txt', '.md')
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(supported_extensions)]
    
    for filename in files:
        print(f"处理中: {filename}")

        base_name = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]
        file_path = os.path.join(SOURCE_DIR, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        if file_ext == '.md':
            html_content = markdown.markdown(raw_content, extensions=[
                'extra', 'codehilite', 'toc', 'nl2br'
            ])
            final_content = f'<div class="markdown-body">{html_content}</div>'
        else:
            escaped = html.escape(raw_content)
            final_content = f'<div class="plain-text">{escaped.replace(chr(10), "<br>")}</div>'

        html_output = template.render(
            title=base_name,
            content=final_content,
        )

        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)

        print(f"✅ 已生成: {output_path}")

    print(f"\n🎉 完成！共处理 {len(files)} 个文件。")

if __name__ == '__main__':
    generate_reading_pages()