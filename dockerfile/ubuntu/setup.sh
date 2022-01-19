cd /data/StockAnalyzer
python3 downloader.py &

cd /data/SteamAnalyzer
python3 downloader.py &

systemctl start cron

while :
do
    sleep 1
done
