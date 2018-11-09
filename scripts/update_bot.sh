#!bin/sh
# updates the scripts from the repository in current directory


archive='greenhouse.tar.gz'
project='53'

echo "Get last commit from repository..."
commit = curl --header "PRIVATE-TOKEN: $1" "https://gitlab.bekast.de/api/v4/projects/$project/repository/commits/master" | grep -Po '(?<="id":)(.*?)(?=,)'

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
echo
echo "Before execute update make sure that access file with the right settings is in the current directory!"
echo "Waiting 7 seconds, maybe u will break execution of this script..."
sleep 7
echo
echo "Remove old compilation and log files..."
sudo rm -v *.pyc
sudo rm -v *.log
echo
echo "Download from repository..."
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
sudo chmod -v +x *.py
sudo chmod -v +x *.sh
echo
echo "Bot updated!"
echo "Restart whole system in 5 seconds! Login later manually again if required!"
sleep 5
sudo reboot
