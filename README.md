This bot the userIDs in database the role automaticly on join and scans the current members if they are in the list. if they are, bot will give them the role.

This bot is very useful for people that wanna move their staff to another server,
just add their user IDS in db.

If you already know everything about hosting a bot, you can skip this text file.
If not, I'll quickly run through the process of creating a Discord Bot account with you so you can get started with your own custom Discord bot.
Also I'll give you a brief overview of the possible ways to host a bot.


== 1) CREATING A DISCORD BOT ACCOUNT ==
You need a Discord bot account to be able to run the code I've written for you.
- Make sure you're logged on the Discord *website* here: https://discord.com/
- Open up this page in your web browser: https://discord.com/developers/applications
- Click the "New Application" button on the top right.
- Give your application a name and then click "Create".
- Create a Bot account by navigating to the "Bot" tab and clicking "Add Bot".
- If you want your bot to be able to invited by others, tick the "Public Bot" checkbox.
- Copy the Token using the "Copy" button.
- Replace TOKEN in the config.json with the bot token you just copied.
WARNING: Do not UNDER ANY CIRCUMSTANCES share this Token with anyone as it's like a password for your bot. A Discord employee will never ask for it. Also, if your Bot is public and someone gets hold of the Token, they can wreak havoc on any server that the bot is on, including potentially deleting all messages. If your Token got leaked, make sure to click "Regnerate" as fast as possible to minimize the damage.


== 2) INVITING THE BOT TO YOUR SERVER ==
Now that your bot has been created, you can invite it to your server.
- Now click the "OAuth2" tab on the application page you were on for creating your bot.
- Tick the "bot" checkbox under "Scopes"
- Tick the permissions your bot will need to function properly. You can find the necessary permissions in the text file called "Needed permissions.txt" - you can also give your bot the Administrator permission, but keep in mind that this means that the bot has every possible permission.
- In the "Scopes" section you will find the link to invite your bot to any server that you have the "Manage Server" permission on.


== 3) HOSTING THE BOT ==
There are in general two ways to host your bot: Either you host the bot yourself on your computer (or any other local machine you have physical access to like a Raspberry Pi or even a smartphone) or you host it on a VPS (= Virtual Private Server), which is basically a small, cheap server that runs 24/7.
Both have advantages and disadvantages:
- When you host the bot on a local device, it's way easier to setup the bot and get running quickly, yet you have to keep that device powered on all the time, which might be undesirable.
- A cheap VPS will cost you a few bucks monthly and you have to use SSH to connect to it and set it up, but it will be powered on 24/7 and will usually be a better overall solution for such a bot.


== 3a) HOSTING THE BOT ON A LOCAL DEVICE ==
To run the bot on a local device, you need to have Python installed and install the necessary modules for Python. You can download the newest version of Python here: https://www.python.org/. Make sure to let the installer include Python in $PATH.
Now install the modules. You can do that on Windows by navigating into the folder where this text document is, pressing Shift + Right click anywhere in the folder, clicking "Open in PowerShell" and running this command:
python -m pip install -r requirements.txt
The steps should be very similar on Linux and macOS.
If it says something along the lines of "'python' not found", try it with python3 instead or without "python -m" entirely and if it still doesn't work, your Python installation might be screwed up. Try reinstalling Python.
To run your bot, just run "python main.py" (without quotation marks); "python3" instead of "python" might work too. If you get a message that looks like "python: can't open file 'main.py': [Errno 2] No such file or directory", you're probably not in the right folder with your command prompt.


== 3b) HOSTING THE BOT ON A VPS ==
The process of hosting your bot on a VPS is more complicated and will inevitably require you to do most of the research on your own, but I can boil it down to the following steps (considering that your VPS runs some Linux distribution like Debian or CentOS - if it runs Windows, install a Linux distribution).
In general:
- First of all, get the VPS up and running and establish a connection to it via SSH* (native on Linux and Mac, use PuTTY on Windows for that) on your machine.
- Transfer the whole folder with the bot over to the VPS over e.g. SFTP (you could use FileZilla for that and don't use normal FTP, it's not secure).
- Configure the VPS to your needs (like installing Python and other needed programs and libraries).
- Get a supervisor running (you could use supervisord for that) and let it take care of running your bot.
- Take security measures like closing unneeded ports, using keyfiles for SSH, not allowing root connections with SSH etc.
- Think of a good backup strategy, in case something happens to the valuable data on your VPS.
If you're using a VPS, it's very easy to screw something up (like not properly securing the SSH connection with keyfiles), so please do *A LOT* of research on how to run and maintain a VPS, otherwise you might end up having your database leaked or something similar.
If you have further questions about hosting a Discord bot, just hit me up, I'll be glad to help.
But I will not host your bot.
* SSH = Secure Shell, a way to securely build up a remote connection to a server and use the command line in it, also includes SFTP for file transfer


== 4) VPS CHOICE ==
The discord.py community recommends the following VPS providers:
- https://scaleway.com/ - Incredibly cheap but powerful VPSes, owned by https://online.net/, based in Europe.
- https://digitalocean.com/ - US-based cheap VPSes. The gold standard. Locations available world wide.
- https://ovh.co.uk/ - Cheap VPSes, used by many people. France and Canadian locations available.
- https://time4vps.eu/ - Cheap VPSes, seemingly based in Lithuania.
- https://linode.com/ - More cheap VPSes!
- https://vultr.com/ - US-based, DigitalOcean-like.
- https://galaxygate.net/ - A reliable, affordable, and trusted host, Used by Dank Memer, Rythm, and many other people.
Using one of the cheaper options is usually a good start and will do just fine for small bots (up to a around hundred servers) and most providers will give you a way to smoothly upgrade your current plan. But it of course also depends on what your bot can do: Does it save a lot (= many gigabytes) data, is it usually in many voice channels, does it do image/video manipulation a lot?
But there are lots of other providers, just do a Google search and you'll be sure to find the right one.
Be wary of free hosting providers like Heraku, those services are not made to host Discord bots and you'll run into issues when trying to do so (believe me, I've fallen for them myself).
If you have a spare Raspberry Pi, you can theoretically use it, but it will have subpar performance (especially if it's older or weaker than the Raspberry Pi 3B+).


That's about it, hopefully this helped you. If there's something wrong with your bot or something's not working, contact me.
- Mikael.
