# DiscordMessageHandler:
DiscordMessageHandler is a script that handles and helps you organize all the messages from your Discord account that you've ever sent.

# Data:
To get the file with your discord data, go to Discord/USER SETTINGS/Privacy & Safety/Request all of my Data (It can take many hours-days for discord to email you the data, depends of how old-active is the account).

# Usage Instructions:
## Installing DiscordMessageHandler:

1. Download the executable or the source files (requires Python).
2. Download the "package.zip" file sent to your email by Discord.
3. Unzip the Discord data from the "package.zip" file

## Running DiscordMessageHandler:
1. Open the command line in the directory containing the source files or executable.
2. Type the following command
```
DiscordMessageHandler --directory="Your-directory/package/messages"
```
or 
```
python main.py --directory="Your-directory/package/messages"
```
(Make sure to replace "Your-directory" with your actual directory.)

## Output: 
If everything goes right, a text file named "data.txt" will be generated. This file contains all the Discord messages you've ever sent.

## Customization:
You can customize the output data according to your needs using the following arguments.

# Arguments:
* -h, --help: Displays the help message and exits.

* -v, --version: Shows the version number of the program and exits.

* -a, --attachment: Optional argument. If provided, includes only attachments in the output.

* --key: Optional argument. Sets a key to search for specific data. Default value is an empty string. (Type: string)

* --limit: Optional argument. Limits the number of messages per conversation in the output. Default value is -1 (no limit). (Type: int)

* --output: Optional argument. Changes the output directory for the data file. Default is the current directory. (Type: string)

* -u: Optional argument. Disables sorting the output by time.

* -r: Optional argument. Sorts the output in reverse order (descending).

* --directory: Optional argument. Changes the directory for the input data. Default is the current directory. (Type: string)

* --name: Optional argument. Sets a custom name for the output file. Default is "data". (Type: string)

* -i, --index: Optional argument. Adds an index to every message in the output.

* -t, --time: Optional argument. Removes timestamps from every message in the output.

* -c, --console: Optional argument. Displays the data in the console instead of writing them to a file. Not recommended for large datasets.
