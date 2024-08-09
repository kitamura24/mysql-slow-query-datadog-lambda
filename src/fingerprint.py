import re

def fingerprint(query):

    # コメント部分を除外するためのプレースホルダーを設定
    comments = []
    def replace_comments(match):
        comments.append(match.group(0))
        return f"__SQL_COMMENT_{len(comments) - 1}__"

    # コメント部分をプレースホルダーに置き換える
    query = re.sub(r'/\*.*?\*/', replace_comments, query, flags=re.DOTALL)

    query = query.strip().lower() # プレースホルダーも小文字に変換

    query = re.sub(r'\\["\']', '', query)
    query = re.sub(r'[ \n\t\r\f]+', ' ', query)
    query = re.sub(r'\bnull\b', '?', query)
    query = re.sub(r'\b\d+\b', '?', query)

    # "str" => ?
    query = re.sub(r'".*?"', '?', query)
    # 'str' => ?
    query = re.sub(r"'.*?'", '?', query)

    query = re.sub(r'\b(in|values)([\s,]*\([\s?,]*\))+', '\\1(?+)', query)
    query = re.sub(r'\blimit \?(, ?\?| offset \?)?', 'limit ?', query)

    # プレースホルダーを元のコメントに戻す
    # プレースホルダーも小文字に変換されているので、小文字で置換する
    for i, comment in enumerate(comments):
        query = query.replace(f"__sql_comment_{i}__", comment)

    return query
