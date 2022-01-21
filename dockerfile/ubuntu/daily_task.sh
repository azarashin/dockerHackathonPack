echo "Daily task start." > /data/last_update.log
date >> /data/last_update.log

echo "Start StockAnalyzer." >> /data/last_update.log
cd /data/StockAnalyzer
python3 analyzer.py

echo "Finish StockAnalyzer." >> /data/last_update.log
date >> /data/last_update.log

echo "Start SteamAnalyzer" >> /data/last_update.log

cd /data/SteamAnalyzer
python3 packer.py && python3 database_updator.py

echo "Finish SteamAnalyzer" >> /data/last_update.log
date >> /data/last_update.log



