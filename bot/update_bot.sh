#!/bin/sh
# Clone from repository if required and update all, commits will compared before
# author: Thomas Kaulke, kaulketh@gmail.com

bot=$1
chat=$2
project=greenhouse
owner=kaulketh
log='/update_bot.log'
commit_id='/lastGreenhouseCommit.id'
bot_dir='/home/pi/scripts/TelegramBot/'
wait=3

# function display usage
display_usage() {
echo "Failed! Paremeter is missing."
echo "Usage only possible at least with Telegram bot API token and Chat ID!"
}

# if less than 2 arguments supplied, display usage
if [[ $# -le 1  ]]
	then 
		display_usage
		exit 1
fi

# if third arguments supplied then will set as branch
if [[ $# -eq 3  ]]
    then
        branch=$3
else
    # get default branch from repository
    branch=$(curl -s https://api.github.com/repos/${owner}/${project} --insecure | grep -Po '(?<="default_branch":)(.*?)(?=,)'| sed "s/\"//g" | sed -e 's/^[[:space:]]*//')
fi

# get last commit id
commit=$(curl -s https://api.github.com/repos/${owner}/${project}/commits/${branch} --insecure | grep -Po '(?<="sha":)(.*?)(?=,)' -m 1 | sed "s/\"//g" | sed -e 's/^[[:space:]]*//' | sed -e 's/[.]*$//')
# get saved commit
last_commit=$(cat ${commit_id})


# all output to log file
exec >> ${log}

# function update
update() {
echo -------------------------------------------------------------------------------------------------------
echo "[$(date +'%F %H:%M:%S')] Starting update..."

# go into bot directory
cd ${bot_dir}

#remove old tmp, logs and pyc
echo "[$(date +'%F %H:%M:%S')] Removing some files..."
find ${bot_dir} -name *.pyc -type f -exec rm -fv {} \;
find ${bot_dir} -name *.log -type f -exec rm -fv {} \;
find ${bot_dir} -name *.tmp -type f -exec rm -fv {} \;
rm -fv /cmd.tmp
echo 

# clone from github
echo "[$(date +'%F %H:%M:%S')] Cloning branch ${branch} from repository to '${project}' folder..."
git clone -v https://github.com/${owner}/${project}.git -b ${branch}
echo  

#change to cloned project folder
cd ${project}

# update python and shell scripts
echo "[$(date +'%F %H:%M:%S')] Updating files..."
cp -rv bot/* ${bot_dir}
# update config files
cp -v configs/motion.conf /etc/motion/motion.conf
cp -v configs/dhcpcd.conf /etc/dhcpcd.conf
#cp -v configs/ddclient.conf /etc/ddclient.conf
echo 

# back to bot directory
cd ${bot_dir}

# remove cloned not needed files and folders
echo "[$(date +'%F %H:%M:%S')] Removing unnecessary files..."
rm -rfv ${project}
echo

# change owner and mode of new files
echo "[$(date +'%F %H:%M:%S')] Setting owner and permissions..."
#chown -v root:netdev /etc/ddclient.conf
chown -v root:root /etc/motion/motion.conf
chown -v root:root /etc/dhcpcd.conf
chown -Rv root:root ${bot_dir}
chmod -Rv +x ${bot_dir}
echo 

# update start script in /etc/init.d/
echo "[$(date +'%F %H:%M:%S')] Updating start script..."
mv -vf telegrambot.sh /etc/init.d/	
echo 

# save last commit id
echo ${commit} > ${commit_id}
sleep ${wait}

# reply message about update
curl -s -k https://api.telegram.org/bot${bot}/sendMessage -d text="[$(date +'%F %H:%M:%S')] Updated, build: ${commit:0:7}, branch: $branch, rebooted" -d chat_id=${chat} >> /dev/null
echo "[$(date +'%F %H:%M:%S')] Update finished, branch '$branch', commit ID '${commit:0:7}' saved, system rebooted."
reboot
}

# check if an update is required
if [[ ${commit} == ${last_commit} ]];
	then
		curl -s -k https://api.telegram.org/bot${bot}/sendMessage -d text="[$(date +'%F %H:%M:%S')] Update checked, not required, last commit '${commit:0:7}' of branch '${branch}'." -d chat_id=${chat} >> /dev/null
		echo -------------------------------------------------------------------------------------------------------
		echo "[$(date +'%F %H:%M:%S')] Update checked, not required, current version equals last commit '${last_commit:0:7}' of branch '${branch}'."
		exit 1
else
	curl -s -k https://api.telegram.org/bot${bot}/sendMessage -d text="[$(date +'%F %H:%M:%S')] Changes detected or update was forced, starting update." -d chat_id=${chat} >> /dev/null
	update
fi
