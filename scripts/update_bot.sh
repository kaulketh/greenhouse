#!bin/sh
# updates all scripts from the repository according to the last commit

exec >> /update.bot
echo -------------------------------------------------------------------------------------------------------
echo "Start update: $(date +'%F %H:%M:%S')"

archive='greenhouse.tar.gz'
project='53'

# function display usage
display_usage() {
echo
echo "Use it with your token for acces to gitlab!"
echo "ie: $BASH_SOURCE  eXe4NA6xq2WQeg3DHFBd"
}

# if less than one argument supplied, display usage
if [ $# -le 0  ] 
	then 
		display_usage
		exit 1
fi

echo "Get last commit from repository..."
commit=$(curl --header "PRIVATE-TOKEN: "$1 "https://gitlab.bekast.de/api/v4/projects/"$project"/repository/commits/master" | grep -Po '(?<="id":)(.*?)(?=,)' | sed "s/\"//g")
echo $commit > /lastGreenhouseCommit.id 
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
echo "Files updated: $(date +'%F %H:%M:%S')"
sleep 2
sudo reboot
