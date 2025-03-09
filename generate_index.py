import json
import os

# キーワード辞書の読み込み
def load_keywords(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# カテゴライズ関数
def categorize(title, keywords):
    for category, words in keywords.items():
        if any(word.lower() in title.lower() for word in words):
            return category
    return "その他"

# インデックス生成
def generate_index(base_path, keywords):
    index = {}
    output_path = os.path.join(base_path, "INDEX.md")  # 出力先を明確に指定

    # デバッグ出力: ファイル生成場所を確認
    print(f"Generating INDEX.md at: {output_path}")

    # ベースパスが存在するか確認
    if not os.path.exists(base_path):
        print(f"Error: Base path does not exist: {base_path}")
        exit(1)

    for file in os.listdir(base_path):
        if file.endswith(".md"):
            title = file.replace(".md", "")
            category = categorize(title, keywords)
            index.setdefault(category, []).append(title)

    with open(output_path, "w", encoding="utf-8") as f:
        for category, pages in sorted(index.items()):
            f.write(f"## {category}\n")
            for page in sorted(pages):
                f.write(f"- [{page}]({page.replace(' ', '%20')}.md)\n")

# メイン処理（スクリプトのテスト実行用）
if __name__ == "__main__":
    # 現在のスクリプトディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = script_dir  # 出力先ディレクトリをスクリプト実行ディレクトリに設定
    keywords_file = os.path.join(script_dir, "keywords.json")  # キーワード辞書ファイルの絶対パス

    # デバッグ出力: 実行ディレクトリと参照するファイルのパスを確認
    print(f"Script directory: {script_dir}")
    print(f"Base path: {base_path}")
    print(f"Keywords file: {keywords_file}")

    # キーワード辞書をロード
    if not os.path.exists(keywords_file):
        print(f"Error: Keywords file not found at {keywords_file}")
        exit(1)

    keywords = load_keywords(keywords_file)

    # インデックス生成
    generate_index(base_path, keywords)
