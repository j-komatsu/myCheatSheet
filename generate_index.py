import json
import os
import re

WIKI_PATH = "wiki"
INDEX_FILE = os.path.join(WIKI_PATH, "INDEX.md")
SIDEBAR_FILE = os.path.join(WIKI_PATH, "_Sidebar.md")
KEYWORDS_FILE = os.path.join(WIKI_PATH, "keywords.json")

def load_keywords():
    """キーワード辞書の読み込み"""
    if not os.path.exists(KEYWORDS_FILE):
        print(f"Error: {KEYWORDS_FILE} が見つかりません")
        return {}
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize(title, keywords):
    """タイトルをカテゴリに分類"""
    for category, words in keywords.items():
        if any(word.lower() in title.lower() for word in words):
            return category
    return "その他"

def extract_command_references():
    """_Sidebar.md から 'コマンドリファレンス' の一覧を抽出"""
    if not os.path.exists(SIDEBAR_FILE):
        print(f"Error: {SIDEBAR_FILE} が見つかりません")
        return []

    with open(SIDEBAR_FILE, "r", encoding="utf-8") as f:
        content = f.readlines()

    command_references = []
    inside_section = False

    for line in content:
        if "## コマンドリファレンス" in line:  # セクションの開始
            inside_section = True
            continue
        if inside_section:
            if line.startswith("## "):  # 次のセクションに入ったら終了
                break
            match = re.search(r"\[\[(.*?)\]\]", line)  # [[ページ名]] のリンクを抽出
            if match:
                command_references.append(match.group(1))

    return command_references

def generate_index():
    """INDEX.md を生成"""
    keywords = load_keywords()
    command_refs = extract_command_references()

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("# コマンドリファレンス一覧\n\n")

        if command_refs:
            for ref in command_refs:
                category = categorize(ref, keywords)
                f.write(f"- [[{ref}]] ({category})\n")
        else:
            f.write("コマンドリファレンスが見つかりませんでした。\n")

if __name__ == "__main__":
    generate_index()
    print(f"Generated {INDEX_FILE}")
