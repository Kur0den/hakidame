read -p "dev環境からのアップデートを実行しますか? (y/n): " answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    git stash
    if [ $? -ne 0 ]; then
        echo "Error stashing changes"
        exit 1
    fi
    result=$(git pull)
    if [ $? -ne 0 ]; then
        echo "Error pulling changes"
        git stash pop
        exit 1
    fi
    git stash pop
    if [ $? -ne 0 ]; then
        echo "Error popping stash"
        exit 1
    fi

    if [[ $result == *"Already up to date."* ]]; then
        echo "No changes to pull"
        exit 0
    fi

    author=$(whoami)
    echo "Pull successful"
    python3 ./pull-notifications.py "$result" "$author"
fi
