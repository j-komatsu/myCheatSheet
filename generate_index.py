import os
import re
import json

WIKI_PATH = "wiki"
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

def extract_sidebar():
    """_Sidebar.md の内容を読み込む"""
    if not os.path.exists(SIDEBAR_FILE):
        print(f"Error: {SIDEBAR_FILE} が見つかりません")
        return []

    with open(SIDEBAR_FILE, "r", encoding="utf-8") as f:
        return f.readlines()

def update_sidebar():
    """_Sidebar.md の「コマンドリファレンス」セクションを更新"""
    keywords = load_keywords()
    lines = extract_sidebar()

    command_references = []
    inside_section = False
    new_sidebar = []

    for line in lines:
        if "## コマンドリファレンス" in line:  # セクション開始
            inside_section = True
            new_sidebar.append(line)
            continue
        if inside_section:
            if line.startswith("## "):  # 次のセクションに入ったら終了
                inside_section = False
        if not inside_section:
            new_sidebar.append(line)

    # 更新用のページリストを取得
    for filename in os.listdir(WIKI_PATH):
        if filename.endswith(".md") and filename != "_Sidebar.md":
            title = filename.replace(".md", "")
            category = categorize(title, keywords)
            command_references.append(f"- [[{title}]] ({category})\n")

    # 「コマンドリファレンス」セクションを上書き
    new_sidebar.append("## コマンドリファレンス\n")
    if command_references:
        new_sidebar.extend(command_references)
    else:
        new_sidebar.append("コマンドリファレンスが見つかりませんでした。\n")

    # _Sidebar.md を上書き保存
    with open(SIDEBAR_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_sidebar)

    print(f"Updated {SIDEBAR_FILE}")

if __name__ == "__main__":
    update_sidebar()
