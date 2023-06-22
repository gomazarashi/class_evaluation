# class_evaluation

`class_evaluation` は、岡山大学の授業評価アンケートへの回答を自動化するためのプログラムです。現在開発中であり、次回(2学期末)の授業評価アンケートに対応する予定です。

## 特徴
- seleniumを用いたブラウザの自動操作
- ログイン情報を保持しない設計
- 複数の授業評価アンケートを一括で回答可能
- 一度評価したアンケートはスキップ

## デモ
(準備中)

## インストール
[github](https://github.com/gomazarashi/class_evaluation)からcloneするか、zipファイルをダウンロードしてください。使用には`selenium`が必要であるため、以下のコマンドでインストールしてください。
```
pip install selenium
```
また、`Chrome Driver`をダウンロードし、`class_evaluation.py`と同じディレクトリに配置するか、環境変数PATHに追加してください。

## 使い方
cmdなどでclass_evaluation.pyを以下のように実行します。
```
python class_evaluation.py
```
その後、指示に従って岡大ID、パスワードおよび対象の授業の学期を半角数字で入力し、エンターキーを押すと自動で授業評価アンケートへの回答が行われます。

## 開発に参加する
追加したい機能やバグの報告はissueにお願いします。また、開発の際はdevelopブランチからforkして行ってください。プルリクエストはdevelopブランチにお願いします。


