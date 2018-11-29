#!bin/sh
# Updates all scripts of repository branch accordingly to recent changes

# only for gitlab required
#token=$1
#chat=$2
#bot=$3

# github
bot=$1

archive='update.tar.gz'

# gitlab
#project='53'
# github
project='greenhouse'
owner='kaulketh'

branch=develop
log='/update_bot.log'
commit_id='/lastGreenhouseCommit.id'
bot_dir='/home/pi/scripts/TelegramBot/'
wait=3

# get last commit id
# gitlab
#commit=$(curl -s --header "PRIVATE-TOKEN: "$token "https://gitlab.bekast.de/api/v4/projects/"$project"/repository/commits/"$branch | grep -Po '(?<="id":)(.*?)(?=,)' | sed "s/\"//g")
# github
commit=$(curl -s https://api.github.com/repos/$owner/$project/commits/$branch --insecure | grep -Po '(?<="sha":)(.*?)(?=,)' -m 1 | sed "s/\"//g")
# get saved commit
last_commit=$(cat $commit_id)

# function display usage
display_usage() {
echo "Failed! Paremeter is missing."
# gitlab
#echo "Using only with token for access to Gitlab, chat ID for Telegram app and bot API token!"
# github
echo "Using only with telegram bot API token!"
}

# gitlab
# if less than 3 arguments supplied, display usage
#if [ $# -le 2  ]
# github
# if less than 1 arguments supplied, display usage
if [ $# -le 0  ] 
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
# gilab
#sudo wget -q -O $archive https://gitlab.bekast.de/api/v4/projects/$project/repository/archive?private_token=$token
# github
sudo wget -q -O $archive --no-check-certificate https://github.com/$owner/$project/archive/$commit.zip
	
# extract
# gilab
#sudo tar -xvzf $archive --wildcards greenhouse-$branch-$commit/scripts/*.py -C $bot_dir
#sudo tar -xvzf $archive --wildcards greenhouse-$branch-$commit/scripts/*.sh -C $bot_dir
#sudo mv -v greenhouse-$branch-$commit/scripts/*.py $bot_dir
#sudo mv -v greenhouse-$branch-$commit/scripts/*.sh $bot_dir

# github
sudo tar -xvzf $archive --wildcards greenhouse-$commit/scripts/*.py -C $bot_dir
sudo tar -xvzf $archive --wildcards greenhouse-$commit/scripts/*.sh -C $bot_dir
sudo mv -v greenhouse-$commit/scripts/*.py $bot_dir
sudo mv -v greenhouse-$commit/scripts/*.sh $bot_dir
		
# remove tmp files
# gitlab 
#sudo rm -r -v greenhouse-$branch*
# github
sudo rm -r -v greenhouse-$commit*

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
curl -s -k https://api.telegram.org/bot$bot/sendMessage -d text="[$(date +'%F %H:%M:%S')] Updated, build: $id..., branch: $branch" -d chat_id=$chat >> /dev/null
echo "[$(date +'%F %H:%M:%S')] Updated finished, branch '$branch', commit ID '$id...' saved, system rebooted."
sudo reboot
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



