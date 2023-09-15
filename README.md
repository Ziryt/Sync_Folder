# Folder Synchronization project
This CLI Python script synchronizes two folders: source and replica. The program maintains a full, identical copy of source folder at replica folder. 

# Installation
1. Clone this repository to your local machine:

    `git clone https://github.com/Ziryt/Sync_Folder`

2. Change directory to the project folder:

    `cd Sync_Folder`

3. Install the required dependencies:

    `pip install -r requirements.txt`

# Usage
Script accepts 2 required arguments: folder to sync, and path where to store backup

Usage examples: 

- This command will create and update backup folder every 2 hours according to CRON schedule

   `python main.py temp/some_folder/ other_place/backup -t "0 */2 * * *"`

- This command will create and update backup folder every Monday at 12 according to CRON schedule, it will also create log file and print logs to console

   `python main.py temp/some_folder/ other_place/backup -t "0 12 * * 1" -v -l utils/logs.log`
