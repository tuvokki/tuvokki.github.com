import argparse, datetime, unicodedata, re

def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

parser = argparse.ArgumentParser(description='Create a new post.')

parser.add_argument('-title', help='Title of the post', required=True)
parser.add_argument('-date', help='Date of the post formatted [yyyy-mm-dd] (defaults to today)', required=False)
parser.add_argument('-draft', help='Draft post (defaults to false)', required=False, action='store_true')

args = parser.parse_args()
dateformat = "%Y-%m-%d"
today = datetime.datetime.today()

filedate = today.strftime(dateformat)

if args.date:
  try:
    t = datetime.datetime.strptime(args.date, dateformat)
    filedate = t.strftime(dateformat)
  except Exception:
    print("Not a valid date, using today", filedate)

filename = filedate + '-' + slugify(args.title) + '.md'

f = open(filename, 'w')

print("---", file=f)
print("layout: post", file=f)
print("title: " + args.title, file=f)
if args.draft:
  print("published: false", file=f)
if args.date:
  print("date: " + filedate, file=f)
print("---", file=f)
