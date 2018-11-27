#!bin/sh
# Updates all scripts from the repository master branch according to recent changes

token=$1
chat=$2
bot=$3

archive='update.tar.gz'
project='53'
branch=develop

log='/update_bot.log'
commit_id='/lastGreenhouseCommit.id'
bot_dir='/home/pi/scripts/TelegramBot/'
wait=3

# get last commit id
commit=$(curl -s --header "PRIVATE-TOKEN: "$token "https://gitlab.bekast.de/api/v4/projects/"$project"/repository/commits/"$branch | grep -Po '(?<="id":)(.*?)(?=,)' | sed "s/\"//g")
# get saved commit
last_commit=$(cat $commit_id)

# function display usage
display_usage() {
echo "Failed! Paremeter is missing."
echo "Using only with token for access to Gitlab, chat ID for Telegram app and bot API token!"
}

# if less than 3 arguments supplied, display usage
if [ $# -le 2  ] 
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
sudo rm -fv $bot_dir*.pyc
sudo rm -fv $bot_dir*.log
sudo rm -fv $bot_dir*.tmp
sudo rm -fv /cmd.tmp

# download	
echo "Download  $branch - $commit."
sudo wget -q -O $archive https://gitlab.bekast.de/api/v4/projects/$project/repository/archive?private_token=$token
	
# extract
sudo tar -xvzf $archive --wildcards greenhouse-$branch-$commit/scripts/*.py -C $bot_dir
sudo tar -xvzf $archive --wildcards greenhouse-$branch-$commit/scripts/*.sh -C $bot_dir
sudo mv -v greenhouse-$branch-$commit/scripts/*.py $bot_dir
sudo mv -v greenhouse-$branch-$commit/scripts/*.sh $bot_dir
	
# remove tmp files 
sudo rm -r -v greenhouse-$branch*
sudo rm -v $archive
	
# change owner and mode	
sudo chmod -v +x $bot_dir*.py
sudo chmod -v +x $bot_dir*.sh

# save last commit id
echo $commit > $commit_id

# update start script in /etc/init.d/
cd $bot_dir
sudo mv -vf telegrambot.sh /etc/init.d/	
sleep $wait

# reply message about update
id=${commit:0:7}
curl -s -k https://api.telegram.org/bot$bot/sendMessage -d text="Bot updated, build: $id... of branch $branch" -d chat_id=$chat >> /dev/null
echo "[$(date +'%F %H:%M:%S')] Update from branch '$branch' finished, saved last commit ID '$id...', system rebooted."
sudo reboot
}

# check if an update is required
if [[ $commit == $last_commit ]];
	then
		echo -------------------------------------------------------------------------------------------------------
		echo "[$(date +'%F %H:%M:%S')] Update not required, current version equals last commit '$last_commit'."
		exit 1
else
	curl -s -k https://api.telegram.org/bot$bot/sendMessage -d text="[$(date +'%F %H:%M:%S')] Changes detected, starting update." -d chat_id=$chat >> /dev/null
	update
fi



