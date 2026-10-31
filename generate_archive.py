import os
import glob

LOCAL_NOVELS_DIR = "novels"
TEMPLATE_PATH = "templates/archive_template.html"
OUTPUT_PATH = "archive.html"

def main():
    # 扫描 txt 和 md，去重（同名只取一个）
    source_files = glob.glob(os.path.join(LOCAL_NOVELS_DIR, "*.txt")) + \
                   glob.glob(os.path.join(LOCAL_NOVELS_DIR, "*.md"))
    
    # 按基础名去重
    seen = set()
    unique_files = []
    for f in sorted(source_files):
        base = os.path.splitext(os.path.basename(f))[0]
        if base not in seen:
            seen.add(base)
            unique_files.append(f)
    
    table_rows = []
    for file_path in unique_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        web_file_path = f"reading/{base_name}.html"
        
        row_html = f"""
        <tr>
            <td><strong>《{base_name}》</strong></td>
            <td><a href="{web_file_path}" class="chapter-link">在线阅读</a></td>
        </tr>
        """
        table_rows.append(row_html)
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    final_html = template_content.replace('<!-- TABLE_ROWS -->', '\n'.join(table_rows))
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ 成功生成！共 {len(unique_files)} 部作品。")

if __name__ == '__main__':
    main()