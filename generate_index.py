import os
import re
import json

WIKI_PATH = "wiki"
SIDEBAR_FILE = os.path.join(WIKI_PATH, "_Sidebar.md")
INDEX_FILE = os.path.join(WIKI_PATH, "INDEX.md")
KEYWORDS_FILE = os.path.join(WIKI_PATH, "keywords.json")

def load_keywords():
    """キーワード辞書の読み込み"""
    if not os.path.exists(KEYWORDS_FILE):
        print(f"Error: {KEYWORDS_FILE} が見つかりません")
        return {}
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_title(title):
    """不要なサフィックスを除去（例: `_test`, `_draft`）"""
    return re.sub(r'[_-](test|draft|backup)$', '', title, flags=re.IGNORECASE)

def categorize(title, keywords):
    """タイトルをカテゴリに分類"""
    cleaned_title = clean_title(title)  # 不要な部分を削除
    for category, words in keywords.items():
        if any(word.lower() in cleaned_title.lower() for word in words):
            return category
    return "その他"

def extract_sidebar():
    """_Sidebar.md の内容を読み込む"""
    if not os.path.exists(SIDEBAR_FILE):
        print(f"Error: {SIDEBAR_FILE} が見つかりません")
        return []
    with open(SIDEBAR_FILE, "r", encoding="utf-8") as f:
        return f.readlines()

def update_sidebar(pages):
    """_Sidebar.md の「コマンドリファレンス」セクションを更新"""
    lines = extract_sidebar()
    new_sidebar = []
    inside_section = False

    for line in lines:
        if "## コマンドリファレンス" in line:  # セクション開始
            inside_section = True
            new_sidebar.append(line)
            continue
        if inside_section and line.startswith("## "):  # 次のセクションで終了
            inside_section = False
        if not inside_section:
            new_sidebar.append(line)

    # 「コマンドリファレンス」セクションを上書き
    new_sidebar.append("## コマンドリファレンス\n")
    if pages:
        new_sidebar.extend(pages)
    else:
        new_sidebar.append("コマンドリファレンスが見つかりませんでした。\n")

    # _Sidebar.md を保存
    with open(SIDEBAR_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_sidebar)

    print(f"Updated {SIDEBAR_FILE}")

def update_index(pages):
    """INDEX.md の内容を更新"""
    index_content = ["# INDEX\n"]
    category_groups = {}

    for line in pages:
        match = re.match(r"- \[\[(.+?)\]\] \((.+?)\)", line)
        if match:
            title, category = match.groups()
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(f"- [[{title}]]\n")

    for category, links in sorted(category_groups.items()):
        index_content.append(f"\n## {category}\n")
        index_content.extend(links)

    # INDEX.md を保存
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.writelines(index_content)

    print(f"Updated {INDEX_FILE}")

def main():
    keywords = load_keywords()
    pages = []

    # ページ一覧を取得し、カテゴリ分け
    for filename in os.listdir(WIKI_PATH):
        if filename.endswith(".md") and filename not in ["_Sidebar.md", "INDEX.md"]:
            title = filename.replace(".md", "")
            category = categorize(title, keywords)
            pages.append(f"- [[{title}]] ({category})\n")

    update_sidebar(pages)
    update_index(pages)

if __name__ == "__main__":
    main()
