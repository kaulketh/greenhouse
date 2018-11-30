#!bin/sh
# Updates all scripts of repository branch accordingly to recent changes

bot=$1
chat=$2
project=greenhouse
owner=kaulketh
branch=develop
log='/update_bot.log'
commit_id='/lastGreenhouseCommit.id'
bot_dir='/home/pi/scripts/TelegramBot/'
wait=3

# get last commit id
commit=$(curl -s https://api.github.com/repos/$owner/$project/commits/$branch --insecure | grep -Po '(?<="sha":)(.*?)(?=,)' -m 1 | sed "s/\"//g" | sed -e 's/^[[:space:]]*//' | sed -e 's/[.]*$//')
# get saved commit
last_commit=$(cat $commit_id)

# function display usage
display_usage() {
echo "Failed! Paremeter is missing."
echo "Using only with Telegram bot API token and Chat ID!"
}

# if less than 2 arguments supplied, display usage
if [ $# -le 1  ] 
	then 
		display_usage
		exit 1
fi

# all output to log file
exec >> $log

# function update
update() {
echo -------------------------------------------------------------------------------------------------------
echo "[$(date +'%F %H:%M:%S')] Update started."

#remove old tmp, logs and pyc
rm -fv $bot_dir*.pyc
rm -fv $bot_dir*.log
rm -fv $bot_dir*.tmp
rm -fv /cmd.tmp

# download
echo Download: $branch $commit
wget -q --no-check-certificate https://github.com/$owner/$project/archive/$branch.zip
	
# extract
echo Extract: $branch.zip
#unzip $branch.zip greenhouse-$branch/configs/*.sh -d $bot_dir
#unzip $branch.zip greenhouse-$branch/scripts/*.py -d $bot_dir
#unzip $branch.zip greenhouse-$branch/scripts/*.sh -d $bot_dir
unzip $branch.zip greenhouse-$branch/* -d $bot_dir

# update python and shell scripts
mv -vf greenhouse-$branch/scripts/*.py $bot_dir
mv -vf greenhouse-$branch/scripts/*.sh $bot_dir

# update configs
mv -vf greenhous-$branch/configs/motion.conf /etc/motion/motion.conf
mv -vf greenhous-$branch/configs/ddclient.conf /etc/ddclient.conf
mv -vf greenhous-$branch/configs/dhcpcd.conf /etc/dhcpcd.conf

# change owner and mode of files
chown root:netdev /etc/ddclient.conf
chown root:root /etc/motion/motion.conf
chown root:root /etc/dhcpcd.conf
chown root:root $bot_dir/*.py

chmod -v +x $bot_dir*.py
chmod -v +x $bot_dir*.sh

# update start script in /etc/init.d/
mv -vf telegrambot.sh /etc/init.d/	

# remove tmp and downloaded files
rm -v *.zip
cd $bot_dir
rm -rf -v greenhouse-$branch*

# save last commit id
echo $commit > $commit_id

sleep $wait

# reply message about update
id=${commit:0:7}
curl -s -k https://api.telegram.org/bot$bot/sendMessage -d text="[$(date +'%F %H:%M:%S')] Updated, build: $id..., branch: $branch, rebooted" -d chat_id=$chat >> /dev/null
echo "[$(date +'%F %H:%M:%S')] Updated finished, branch '$branch', commit ID '$id...' saved, system rebooted."
reboot
}

# check if an update is required
if [[ $commit == $last_commit ]];
	then
		curl -s -k https://api.telegram.org/bot$bot/sendMessage -d text="[$(date +'%F %H:%M:%S')] Update checked, not required, recent changes are included." -d chat_id=$chat >> /dev/null
		echo -------------------------------------------------------------------------------------------------------
		echo "[$(date +'%F %H:%M:%S')] Update checked, not required, current version equals last commit '$last_commit'."
		exit 1
else
	curl -s -k https://api.telegram.org/bot$bot/sendMessage -d text="[$(date +'%F %H:%M:%S')] Changes detected, starting update." -d chat_id=$chat >> /dev/null
	update
fi

