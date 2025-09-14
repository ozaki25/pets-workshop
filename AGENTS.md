# Pet Shelter Agent Instructions

## プロジェクト概要

このプロジェクトは、犬の保護施設向けのWebアプリケーションです。人々が里親募集中の犬を検索・閲覧できる機能を提供します。

## アーキテクチャ

- **モノレポ構造**: サーバーとクライアントが同一リポジトリ内に配置
- **バックエンド**: Flask + SQLAlchemy + SQLite
- **フロントエンド**: Astro + Svelte + TypeScript
- **データベース**: SQLite (`server/dogshelter.db`)

## ディレクトリ構造

```
pets-workshop/
├── server/                 # Flask バックエンド
│   ├── app.py             # メインアプリケーション
│   ├── dogshelter.db      # SQLite データベース
│   ├── models/            # データベースモデル
│   │   ├── dog.py         # Dog モデル
│   │   ├── breed.py       # Breed モデル
│   │   ├── dogs.csv       # 犬データ
│   │   └── breeds.csv     # 犬種データ
│   └── utils/
│       └── seed_database.py
├── client/                # Astro + Svelte フロントエンド
│   ├── src/
│   │   ├── components/    # Svelte コンポーネント
│   │   ├── pages/         # Astro ページ
│   │   └── layouts/       # レイアウトファイル
│   └── e2e-tests/         # E2E テスト
└── content/               # ドキュメント
```

## データベース設計

### Dogs テーブル
- `id`: 主キー
- `name`: 犬の名前
- `breed_id`: 犬種ID（外部キー）
- `age`: 年齢
- `description`: 説明
- `gender`: 性別
- `status`: ステータス（Available, Adopted等）

### Breeds テーブル
- `id`: 主キー  
- `name`: 犬種名

## API エンドポイント

- `GET /api/dogs` - 全ての犬のリスト取得
- `GET /api/dogs/<id>` - 特定の犬の詳細取得
- `GET /api/breeds` - 全ての犬種のリスト取得

## 開発ガイドライン

### バックエンド（Python/Flask）
- **型ヒントを使用**: 全ての関数とメソッドでPython型ヒントを適用
- **SQLAlchemy**: データベース操作にはSQLAlchemyのORMを使用
- **エラーハンドリング**: 404エラー等の適切なHTTPステータスコードを返す
- **レスポンス形式**: JSON形式でデータを返す

### フロントエンド（TypeScript/Astro/Svelte）
- **TypeScript**: アロー関数を使用（`function`キーワードではなく）
- **ダークモード**: モダンでダークモードのデザインを採用
- **コンポーネント**: 再利用可能なSvelteコンポーネントを作成

### テスト
- **E2Eテスト**: Playwrightを使用してE2Eテストを実装
- **テストファイル**: `e2e-tests/`ディレクトリ内に配置

## 環境設定

### サーバー起動
```bash
cd server
source venv/bin/activate
python3 app.py  # ポート5100で起動
```

### クライアント起動
```bash
cd client
npm run dev
```

## 機能要件

### 現在の機能
- 犬一覧の表示
- 犬の詳細表示
- 犬種一覧の取得

### 実装予定/拡張可能な機能
- 犬種によるフィルタリング
- ステータスによるフィルタリング
- 検索機能
- テーマ切り替え
- アニメーション効果

## タスク実行時の注意点

### ファイル編集時
- 既存のコード構造とスタイルに従う
- 型安全性を保つ
- エラーハンドリングを適切に実装

### 新機能追加時
- API仕様とフロントエンド仕様の整合性を確保
- テストケースの追加を検討
- データベースの変更が必要な場合は適切にマイグレーションを考慮

### デバッグ・トラブルシューティング
- ターミナル出力を確認してエラーの原因を特定
- ブラウザの開発者ツールでフロントエンドのエラーを確認
- SQLiteファイルの存在と権限を確認
