# A simple task scheduler 

This is a simple task scheduler utility implemented in python3

It allows to schedule console commands to be run at specific interval.
The results of execution can later be viewed in the application, also they are sent via email.

## Install:

Clone project with git or download source archive.

From the project root folder run:

`pip install .`

This will install all dependencies and create binary `schedulr` somewhere in system path.

## Usage

Running `schedulr` will start the schduler application. 
While it is running, it will execute the programs you schedule.
It offers command-line interface to enter commands.

The supported commands are:

 * Add new command with running interval: `add <run interval in seconds> <command>`
 * Add new command with crontab-like schedule: `add <* * * * *> <command>`
 * Show executed commands: `log <number of commands to show, default 10>`
 * Show commands to be executed: `backlog <number of commands to show, default 10>`
 * Help: `help` or `?`
 * Exit: `q` or OS-specific EOF (`Ctrl-D` or `Ctrl-Z` + `Enter`)

Example:
```
root@790f5d4f8af1:/data# schedulr
Python task scheduler. Type help or ? to list commands
schedulr: add 10 pwd
Added job with command "pwd"
schedulr: log
Showing last 2 reports
03/10/22 08:56:38 -- 03/10/22 08:56:38  "pwd"  /

03/10/22 08:56:48 -- 03/10/22 08:56:48  "pwd"  /

schedulr: backlog 5
Showing upcoming 5 jobs
03/10/22 08:57:28 "pwd"
03/10/22 08:57:38 "pwd"
03/10/22 08:57:48 "pwd"
03/10/22 08:57:58 "pwd"
03/10/22 08:58:08 "pwd"
```

## Configuration

Email notifications will not work without correct configuration.
SMTP server address, port and credentials need to be set, as well as sender and recipient email addresses. 
This configuration is read from file `config.cfg` in current working directory. 
Another file can be specified by command-line argument, i.e. `schedulr --cfg ~/config.txt`.
If `--cfg` is not provided and there is no `config.cfg` in current directory, hard-coded defaults are used.

Example `config.cfg` is in root of the project. 
The format of the file is INI-like and is self-explanatory.

You can test email functionality by starting python's built-in SMTP server by 
```
python -m smtpd -n -c DebuggingServer localhost:1025
```

Default configuration will connect to this server.
Note that it does not support username/password, so leave them empty in config.

