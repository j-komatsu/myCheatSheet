import os
import re
import json

WIKI_PATH = "wiki"
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
    cleaned_title = clean_title(title)
    for category, words in keywords.items():
        if any(word.lower() in cleaned_title.lower() for word in words):
            return category
    return "その他"

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
        if filename.endswith(".md") and filename != "INDEX.md":
            title = filename.replace(".md", "")
            category = categorize(title, keywords)
            pages.append(f"- [[{title}]] ({category})\n")

    update_index(pages)  # `INDEX.md` のみ更新

if __name__ == "__main__":
    main()
