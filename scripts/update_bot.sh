#!bin/sh
# updates all scripts from the repository according to last changes

token=$1
archive='greenhouse.tar.gz'
project='53'
log='/update.bot'
commit_id='/lastGreenhouseCommit.id'
bot_dir='/home/pi/scripts/TelegramBot/'
wait=3

# get last commit id
commit=$(curl -s --header "PRIVATE-TOKEN: "$token "https://gitlab.bekast.de/api/v4/projects/"$project"/repository/commits/master" | grep -Po '(?<="id":)(.*?)(?=,)' | sed "s/\"//g")
# get saved commit
last_commit=$(cat $commit_id)

# all output to log file
exec >> $log

# function display usage
display_usage() {
echo
echo "Use it with token for acces to gitlab!"
echo "ie: $BASH_SOURCE  eXe4NA6xq2WQeg3DHFBd"
}

# function update
update() {
echo -------------------------------------------------------------------------------------------------------
echo "$(date +'%F %H:%M:%S') : Update started."
#remove old tmp, logs and pyc
sudo rm -fv $bot_dir*.pyc
sudo rm -fv $bot_dir*.log
sudo rm -fv $bot_dir*.tmp
sudo rm -fv /*.log
sudo rm -fv /cmd.tmp
echo "Download last commit: "$commit
sudo wget -q -O $archive https://gitlab.bekast.de/api/v4/projects/$project/repository/archive?private_token=$token
# extract
sudo tar -xvzf $archive --wildcards greenhouse-master-$commit/scripts/*.py -C $bot_dir
sudo tar -xvzf $archive --wildcards greenhouse-master-$commit/scripts/*.sh -C $bot_dir
sudo mv -v greenhouse-master-$commit/scripts/*.py $bot_dir
sudo mv -v greenhouse-master-$commit/scripts/*.sh $bot_dir
# remove tmp files and chown and chmod 
sudo rm -r -v greenhouse-master*
sudo rm -v *.gz
sudo chmod -v +x $bot_dir*.py
sudo chmod -v +x $bot_dir*.sh
# save last commit id
echo $commit > $commit_id
sleep $wait
echo "$(date +'%F %H:%M:%S') : Update finished, last commit id: $commit saved, whole system rebooted."
sudo reboot
}

# if less than one argument supplied, display usage
if [ $# -le 0  ] 
	then 
		display_usage
		exit 1
fi

# if commit was not changed nothing will be updated
if [[ $commit == $last_commit ]];
	then
		echo -------------------------------------------------------------------------------------------------------
		echo "$(date +'%F %H:%M:%S') : No new changes, nothing to update!"
		exit 1
else
	update
fi
