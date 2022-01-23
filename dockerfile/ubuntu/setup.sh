# docker のビルド時にこれを実行すると入力操作を伴う問い合わせをされて
# ビルドが止まってしまうので、ビルドではなく起動時の初期化処理で
# タイムゾーンに関するインストールを実施する
apt install -y tzdata

cd /data/StockAnalyzer
python3 downloader.py &

cd /data/SteamAnalyzer
python3 downloader.py &

cd /data/CoconaraAnalyzer
python3 downloader.py &

systemctl start cron

while :
do
    sleep 1
done
