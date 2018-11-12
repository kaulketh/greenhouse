#!bin/sh
# updates all scripts from the repository according to last changes


archive='greenhouse.tar.gz'
project='53'

# get last commit id
commit=$(curl --header "PRIVATE-TOKEN: "$1 "https://gitlab.bekast.de/api/v4/projects/"$project"/repository/commits/master" | grep -Po '(?<="id":)(.*?)(?=,)' | sed "s/\"//g")
# get saved commit
last_commit = $(cat /lastGreenhouseCommit.id)

exec >> /update.bot

# function display usage
display_usage() {
echo
echo "Use it with your token for acces to gitlab!"
echo "ie: $BASH_SOURCE  eXe4NA6xq2WQeg3DHFBd"
}


# function update
update() {
echo -------------------------------------------------------------------------------------------------------
echo "$(date +'%F %H:%M:%S') : Update started."
echo
echo "Remove old compilation, tmp and log files..."
sudo rm -v /home/pi/scripts/TelegramBot/*.pyc
sudo rm -v /home/pi/scripts/TelegramBot/*.log
sudo rm -v /home/pi/scripts/TelegramBot/*.tmp
sudo rm -v /*.log
sudo rm -v /cmd.tmp
echo
echo "Download last commit: "$commit
sudo wget -O $archive https://gitlab.bekast.de/api/v4/projects/$project/repository/archive?private_token=$1
echo
echo "Extracting..."
sudo tar -xvzf $archive --wildcards greenhouse-master-$commit/scripts/*.py -C /home/pi/scripts/TelegramBot/
sudo tar -xvzf $archive --wildcards greenhouse-master-$commit/scripts/*.sh -C /home/pi/scripts/TelegramBot/
echo
echo "Moving files..."
sudo mv -v greenhouse-master-$commit/scripts/*.py /home/pi/scripts/TelegramBot/
sudo mv -v greenhouse-master-$commit/scripts/*.sh /home/pi/scripts/TelegramBot/
echo
echo "Removing temporary files..."
sudo rm -r -v greenhouse-master*
sudo rm -v *.gz
echo
echo "Change mode of new files..."
sudo chmod -v +x /home/pi/scripts/TelegramBot/*.py
sudo chmod -v +x /home/pi/scripts/TelegramBot/*.sh
echo
echo "$(date +'%F %H:%M:%S') : Update finished."
# save last commit id
echo $commit > /lastGreenhouseCommit.id
sleep 2
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
		echo "$(date +'%F %H:%M:%S') : No changes detected, nothing to update!"
		exit 1
else
	update
fi
