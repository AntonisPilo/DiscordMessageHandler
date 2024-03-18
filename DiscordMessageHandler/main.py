import argparse,os,sys
from data import Data


def main():
    ap = argparse.ArgumentParser(description="Process data with customizable options.")
    ap.add_argument("-v", "--version", version=Data.version, action="version", help="Show program's version number and exit.")
    ap.add_argument("-a", "--attachment", required=False, help="Include only attachments in the output.", action="store_true")
    ap.add_argument("--key", required=False, help="Set a key to search for specific data.", type=str, default="")
    ap.add_argument("--limit", required=False, help="Limit the number of messages per conversation in the output.", type=int, default=-1)
    ap.add_argument("--output", required=False, help="Change the output directory for the data file. Default is the current directory.", type=str, default=os.getcwd())
    ap.add_argument("-u", required=False, help="Disable sorting the output by time.", action="store_false")
    ap.add_argument("-r", required=False, help="Sort the output in reverse order (descending).", action="store_true")
    ap.add_argument("--directory", required=False, help="Change the directory for the input data. Default is the current directory.", type=str, default=os.getcwd())
    ap.add_argument("--name", required=False, help="Set a custom name for the output file. Default is 'data'.", type=str, default="data")
    ap.add_argument("-i", "--index", required=False, help="Add an index to every message in the output.", action="store_true", default=False)
    ap.add_argument("-t", "--time", required=False, help="Remove timestamps from every message in the output.", action="store_false", default=True)
    ap.add_argument("-c", "--console", required=False, help="Display the data in the console instead of writing them to a file. Not recommended for large datasets.", action="store_true", default=False)

    argv = ap.parse_args()

    data = Data(argv.directory)

    timestamps,messages = data.get_messages(argv.key,argv.limit,argv.u,argv.r,argv.attachment)

    data.output(timestamps,messages,argv.name,argv.output,argv.index,argv.time,argv.console)


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(1)