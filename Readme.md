# docker コンテナ環境の構築手順

## 1. 含まれるコンテナ

- mysql
  - DB本体
- phpMyAdmin
  - DB制御補助
- nodered
  - 各種サーバ制御
- superset
  - BIツール

## 2. ディレクトリ構造

|-- mount  
|　|-- db (mysql 関連のマウント先)  
|　|　|-- data (db 本体が格納される)  
|　|　|　|-- .gitignore (data ディレクトリをリポジトリに残すためだけに設置。)  
|　|　|  
|　|　|-- my.cnf (文字コードなどを設定する)  
|　|　|-- sql (データベースの初期化関連)  
|　|　　|-- 001-create-tables.sql (初期化時に実行するクエリを格納)  
|　|　　|-- init-database.sh　(初期化処理のためのスクリプト)  
|　|  
|　|-- nodered  
|　|　|-- settings.js  
|　|　|-- package.json   
|　|　|-- node_modules (mysql やemail など最低限のノードを格納)   
|　|　|-- (フローファイル、暗号化済み認証情報)  
|　|  
|　|-- nginx  
|　|　|-- public  
|　|　|-- index.html  
|　|  
|　|-- superset
|　|  
|　|-- metabase
|  
|-- docker-compose.yml  
|-- .env  
|-- Readme.md  

## 3. 構築手順

### 3.0. ラズパイの設定

熱暴走を抑えるため、/boot/config.txt に

```
temp_limit=75
```

を追記しておく。

### 3.1. 環境変数の設定

.env を編集してください。

| カテゴリ   | 環境変数名          | 概要                                                    |
| ---------- | ------------------- | ------------------------------------------------------- |
| common     | CONTAINER_BASE_NAME | コンテナの頭につけるプロジェクト名                      |
| node-red   | NODE_RED_PORT       | コンテナ外からアクセスするときのnode-red のポート番号   |
| node-red   | NODE_RED_FLOW       | 最初にアクセスされるフローのフロー名                    |
|node-red|NODE_RED_CREDENTIAL_SECRET|認証文字列（nodered のフローで記録するパスワード等の暗号化に使用）|
| mysql      | MYSQL_PORT          | コンテナ外からアクセスするときのmysql のポート番号      |
| mysql      | MYSQL_DATABASE      | 最初に生成するデータベース名                            |
| mysql      | MYSQL_ROOT_PASSWORD | root ユーザの初期パスワード                             |
| mysql      | MYSQL_USER          | 通常アクセスするときのためのユーザ名                    |
| mysql      | MYSQL_PASSWORD      | 上記ユーザ名に対する初期パスワード                      |
| phpMyAdmin | PMA_PORT            | コンテナ外からアクセスするときのphpMyAdmin のポート番号 |
| phpMyAdmin | PMA_USER            | mysql にアクセスするためのユーザ名。MYSQL_USER の設定値と同じにしておく |
| phpMyAdmin | PMA_PASSWORD        | 上記ユーザ名に対する初期パスワード。MYSQL_PASSWORD の設定値と同じにしておく。 |
| superset      | SUPERSET_PORT          | コンテナ外からアクセスするときのsuperset のポート番号      |
| metabase      | METABASE_PORT          | コンテナ外からアクセスするときのmetabase のポート番号      |
| nginx      | NGINX_PORT          | コンテナ外からアクセスするときのnginx のポート番号      |

### 3.2. コンテナ群の生成及び起動

```
sudo docker-compose up -d
```

### 3.3. superset の初期化

#### 3.3.1. アカウントを初期化する

```
docker-compose exec superset superset fab create-admin --username (adminユーザ名) --firstname (名前) --lastname (苗字) --email (メールアドレス) --password (adminパスワード)
```

- (adminユーザ名)
- (名前)
- (苗字)
- (メールアドレス)
- (adminパスワード)

の部分は適宜置き換えてください。

例：
```
docker-compose exec superset superset fab create-admin --username admin --firstname name --lastname sample --email sample@sample.com --password password
```

#### 3.3.2. DBを初期化する

```
docker-compose exec superset superset db upgrade
```

#### 3.3.3. サンプルを読みこむ（この手順はスキップ可）

```
docker-compose exec superset superset load_examples
```

#### 3.3.4. ロールを初期化する

```
docker-compose exec superset superset init
```

ユーザ名やパスワードその他もろもろ聞かれるので設定する。

### 3.4. metabase のアカウント初期化

![metabase初期化画面](.\images\metabase000.png)

最初にアクセスすると、上記画面のように2 Add your data の画面で色々聞かれるので、以下の内容をそれぞれ入力する。

| 項目              | 概要                               |
| ----------------- | ---------------------------------- |
| (データベース)    | MySQL を選択する                   |
| Name              | 好きな名前を入力する               |
| Host              | db で固定                          |
| Port              | 3306 で固定                        |
| Database name     | 環境変数 MYSQL_DATABASE に合わせる |
| Database username | 環境変数MYSQL_USER に合わせる      |
| Database password | 環境変数MYSQL_PASSWORD に合わせる  |


## 4. 注意事項

### 4.1. NodeRED のmysql ノードからmysql database にアクセスする場合

ノードで設定するホスト名をdb, ポート番号を3306 にしておくこと(MYSQL_PORT ではなく3306 にする)。

ホスト名はlocalhost や127.0.0.1 ではダメ。db というのは、docker-compose.yml に記載したmysql のサービス名であり、docker コンテナをまたいでネットワークアクセスする時にホスト名として使用する。

### 4.2. superset でdata source を追加するときのSQLAlchemy URI の書き方

```
 mysql://${MYSQL_USER}:${MYSQL_PASSWORD}@db:3306/(database名)
```



と記述する。${MYSQL_USER} と${MYSQL_PASSWORD} は.env で設定したものに置き換える。

db はmysql のホスト名であり、4.1. と同じ理由によりlocalhost や127.0.0.1 ではなくdb を指定する。


## 5. 参考情報
- node-red & docker:
  - https://nodered.jp/docs/getting-started/docker




