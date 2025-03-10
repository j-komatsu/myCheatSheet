import os
import json

def load_keywords(file_path):
    """キーワード分類用のJSONファイルを読み込む"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize_pages(base_path, keywords):
    """ページをカテゴリごとに分類する"""
    categorized = {key: [] for key in keywords.keys()}
    categorized["その他"] = []
    
    for file in os.listdir(base_path):
        if file.endswith(".md") and file != "INDEX.md":  # INDEX.md を除外
            page_name = os.path.splitext(file)[0]
            page_name_lower = page_name.lower()
            categorized_flag = False
            
            for category, words in keywords.items():
                if any(word.lower() in page_name_lower for word in words):  # 大文字小文字を無視して比較
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
                f.write(f"## {category}\n\n")
                for page in sorted(pages):
                    f.write(f"- [{page}]({page.replace(' ', '%20')})\n")
                f.write("\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))  # リポジトリのルートを取得
    wiki_path = os.path.join(repo_root, "wiki")  # wikiフォルダのパス
    keywords_file = os.path.join(repo_root, "keywords.json")  # JSONファイルのパス
    index_md_path = os.path.join(wiki_path, "INDEX.md")  # INDEX.mdのパス

    # デバッグ用出力
    print(f"script_dir: {script_dir}")
    print(f"repo_root: {repo_root}")
    print(f"wiki_path: {wiki_path}")
    print(f"index_md_path: {index_md_path}")

    if not os.path.exists(wiki_path):
        print(f"エラー: 指定されたwikiフォルダが見つかりません: {wiki_path}")
        return

    keywords = load_keywords(keywords_file)
    categorized_pages = categorize_pages(wiki_path, keywords)
    generate_index_md(categorized_pages, index_md_path)

    # `INDEX.md` の確認
    if os.path.exists(index_md_path):
        print(f"INDEX.md の生成に成功: {index_md_path}")
        os.system(f"ls -l {index_md_path}")
    else:
        print("エラー: INDEX.md が生成されていません")
    
    print("INDEX.md が更新されました。")

if __name__ == "__main__":
    main()

