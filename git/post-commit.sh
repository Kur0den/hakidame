#!/bin/bash

# 変更されたファイルのリストを取得
files=$(git diff-tree -r --name-only --no-commit-id HEAD)

# 各ファイルのパーミッションを変更
for file in $files; do
    chmod g+rwx "$file"
done

# コミットされたファイルの一覧とそのステータスを取得
files=$(git diff-tree -r --name-status --no-commit-id HEAD)

# コミットしたユーザーの名前とメールアドレスを取得
author=$(git log -1 --pretty=format:'%an <%ae>')

# コミットのハッシュを取得
commit_hash=$(git rev-parse HEAD)

# コミット全体での容量変化を取得
diff_stats=$(git diff --numstat ${commit_hash}^! --)
added_bytes=0
deleted_bytes=0

while IFS=$'\t' read -r added deleted filename; do
  added_bytes=$((added_bytes + added))
  deleted_bytes=$((deleted_bytes + deleted))
done <<< "$diff_stats"

# コミットメッセージを取得
message=commit_message=$(git log -1 --pretty=format:'%s')

# Pythonスクリプトにファイル一覧とステータスを渡す
python3 .git/hooks/commit-notifications.py "$commit_hash" "$files" "$added_bytes" "$deleted_bytes" "$author" "$message"
