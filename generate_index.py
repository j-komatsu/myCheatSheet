import os
import json

def load_keywords(file_path):
    """キーワード分類用のJSONファイルを読み込む"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize_pages(base_path, keywords):
    """ページを分類し、カテゴリごとにリストを作成する"""
    categorized = {key: [] for key in keywords.keys()}
    categorized["その他"] = []
    
    for file in os.listdir(base_path):
        if file.endswith(".md") and file != "Home.md":
            page_name = os.path.splitext(file)[0]
            categorized_flag = False
            
            for category, words in keywords.items():
                if any(word in page_name for word in words):
                    categorized[category].append(page_name)
                    categorized_flag = True
                    break
            
            if not categorized_flag:
                categorized["その他"].append(page_name)
    
    return categorized

def generate_index_md(categorized_pages, output_path):
    """INDEX.md を生成する"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# INDEX\n\n")
        for category, pages in categorized_pages.items():
            if pages:
                f.write(f"## {category}\n")
                for page in sorted(pages):
                    f.write(f"- [{page}]({page.replace(' ', '%20')})\n")
                f.write("\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "myCheatSheet.wiki")
    keywords_file = os.path.join(script_dir, "keywords.json")
    index_md_path = os.path.join(base_path, "INDEX.md")
    
    keywords = load_keywords(keywords_file)
    categorized_pages = categorize_pages(base_path, keywords)
    generate_index_md(categorized_pages, index_md_path)
    
    print("INDEX.md が更新されました。")

if __name__ == "__main__":
    main()
