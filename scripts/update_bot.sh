#!bin/sh
# Clone from repository if required, commits will compared before

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

# clone from github
cd $bot_dir
echo Clone from git repository in \'$project\' folder
git clone -v https://github.com/$owner/$project.git

# update python and shell scripts
cd $project
mv -vf scripts/*.py $bot_dir
mv -vf scripts/*.sh $bot_dir

# update config files
mv -vf configs/motion.conf /etc/motion/motion.conf
mv -vf configs/dhcpcd.conf /etc/dhcpcd.conf
mv -vf configs/ddclient.conf /etc/ddclient.conf

# change owner and mode of files
chown -v root:netdev /etc/ddclient.conf
chown -v root:root /etc/motion/motion.conf
chown -v root:root /etc/dhcpcd.conf
chown -v root:root $bot_dir*.py

chmod -v +x $bot_dir*.py
chmod -v +x $bot_dir*.sh

# update start script in /etc/init.d/
cd $bot_dir
mv -vf telegrambot.sh /etc/init.d/	

# remove cloned files and folder
echo Remove cloned files
rm -rf greenhouse

# save last commit id
echo $commit > $commit_id
echo Saved:  $(cat $commit_id)
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

