# README

## 前提

Dockerのインストール、gitの初期設定を行っていること


## ローカル環境構築

以下を実施してください。

1. リポジトリをローカルにclone: `git clone [URL]`
2. docker立ち上げ: `docker-compose up -d --build`　※-dを外すとコンソールにログを表示しながら開発できます
3. ブラウザで、`http://localhost:8080`を開き "OK" と表示されたら完了

## マイグレーション　　※docker起動時に実行されます

1. dockerに入る: `docker-compose exec api bash`
2. ディレクトリ移動: `cd database`
3. マイグレーションファイル生成: `alembic revision --autogenerate -m "※ファイル名、下記の補足参照"`
4. ローカルを確認すると、app/database/versions に新規ファイルが作成されているので、中身を編集する
5. マイグレーション実行: `alembic upgrade head`

※補足: マイグレーションファイル名は、[Create/Alter/Drop +テーブル名]としてください
　例）alter_products

## 初期データ登録(seed)　　※docker起動時に実行されます

1. app/seed.py を編集　※docker起動時に毎回実行される為、データが増えすぎない書き方にする必要がある（コーディング規約参照）
2. dockerに入る: `docker-compose exec api bash`
3. seed実行　`python seed.py`

## API設計書の自動生成

ブラウザで、`http://localhost:8080/docs`を開くと、実装したAPIの仕様書が自動生成されています
仕様書の`Try it out`ボタン > `Execute`ボタンより、APIを実行できます

## テスト実施

1. dockerに入る: `docker-compose exec api bash`
2. 1ファイルのみテスト: `pytest [※テスト対象のフォルダ名/ファイル名]`
3. 全ファイルテスト: `pytest tests`
4. カバレッジ確認: `pytest -v --cov=[※テスト対象のフォルダ名/ファイル名] --cov-report=term-missing`

カバレッジ確認について補足
- テスト対象のフォルダ名の例）app/apis/
- 結果に、網羅されていない行番号が表示されます

> apis/product.py       47     22    53%   27, 32-40, 56-63, 68-71

- カバレッジは、以下の方法で **HTML出力** もできます。
    - `pytest -v --cov=[※テスト対象のフォルダ/ファイル名] --cov-report=html`
    - app/htmlcov/index.htmlが生成されるので、ブラウザで開く
