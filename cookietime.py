import csv
import datetime
import getopt
import os
import sys

# Exception Classes for ease of reading instead of generic exception name.
class FileEmpty(Exception):
    pass


class NoLogsInFile(Exception):
    pass


class TooFewParams(Exception):
    pass


class FileFormatError(Exception):
    pass


# CookieTime class implemented to store record as a datatype


class CookieTime:
    def __init__(self, cookiename, timestamp):
        self.cookiename = cookiename
        self.timestamp = timestamp

    def __repr__(self):
        return str(self.timestamp) + " " + str(self.cookiename)


# Computes the number of records for given date and returns max cookie count
def compute(file, date):
    """
    compute function to check for number of records for the given date and
    returns cookie name for onlymaximum occurance in the date
    Args:
    filename(str): in relative path to code
    date(datetime.date): date to determine max
    Returns(list(str)):
    ['0'] if no records match criteria
    ['abc','xyz'] if multiple entries have max length
    ['abc'] if one match the criteria.
    """
    if os.path.getsize(file) == 0:
        raise FileEmpty("The file is empty")
    with open(file, "r") as f:
        result = {}
        reader = csv.reader(f)
        header = next(reader)
        if not (header and "cookie" == header[0] and "timestamp" == header[1]):
            raise FileFormatError("HeaderMissing")
        for row in reader:
            if row:
                cookietime = CookieTime(
                    row[0].strip(), datetime.datetime.fromisoformat(row[1].strip())
                )
                if cookietime.timestamp.date() == date:
                    if cookietime.cookiename not in result:
                        result[cookietime.cookiename] = (1, [cookietime.timestamp])
                    else:
                        result[cookietime.cookiename][1].append(cookietime.timestamp)
                        result[cookietime.cookiename] = (
                            result[cookietime.cookiename][0] + 1,
                            result[cookietime.cookiename][1],
                        )
    if result:
        max_hits = max([x[0] for x in result.values()])
        return [x[0] for x in result.items() if x[1][0] == max_hits]
    if not result:
        return ["0"]


# Driver function
def driver():
    """
    Driver code to process commandline arguement and
    file management and calling the max_hits cookiename code.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:", ["filename =", "date ="])
    except Exception as e:
        print(e)

    filename, arg_date = "", ""
    for opt, arg in opts:
        if opt in ("-f", "--filename"):
            filename = os.getcwd() + "/" + arg
        elif opt in ("-d", "--date"):
            try:
                arg_date = datetime.date.fromisoformat(arg)
            except Exception as e:
                print("The code halted due to the following issue: " + str(e))
                exit(1)

    if not (filename and arg_date):
        if not filename:
            raise TooFewParams("Please enter the filename")
        else:
            raise TooFewParams("Please enter the date")
    else:
        print(*compute(filename, arg_date), sep="\n")


if __name__ == "__main__":
    driver()
