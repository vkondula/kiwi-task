#!/bin/python2.7
import argparse
import sys
import datetime
import re
from copy import copy

COLLUMS = 5
DELIMITER = ","


def parse_args():
    """
    Handles CLI options using argparse
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        help="Read from this file instead of stdin",
        type=str
    )
    parser.add_argument(
        "--output",
        help="Write to this file instead of stdout",
        type=str
    )
    args = parser.parse_args()
    retval = {}
    if args.output in ("-", None):
        retval["output"] = sys.stdout
    else:
        retval["output"] = open(args.output, "w")
    if args.input in ("-", None):
        retval["input"] = sys.stdin
    else:
        retval["input"] = open(args.input, "r")
    return retval


class FlightParser(object):
    date_pattern = r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})$"

    def __init__(self, input):
        self.input = input
        self.collums = None
        self.flights = []
        self.airports = set()
        self.comp = re.compile(self.date_pattern)

    def _get_row(self):
        row = self.input.readline().replace("\n", "")
        if not row:
            return None
        return row.split(DELIMITER)

    def set_collums(self):
        """Set order of collums defined by 1st line"""
        row = self._get_row()
        if not row:
            raise Exception("Empty input")
        self.collums = row

    def read_line(self):
        """Parse line, convert time information and save to dictionery"""
        row = self._get_row()
        if not row:
            return None
        flight = {}
        for c in zip(self.collums, row):
            if c[0] in ("source", "destination"):
                self.airports.add(c[1])
            if c[0] in ("departure", "arrival"):
                flight[c[0]] = self.convert_time(c[1])
                continue
            flight[c[0]] = c[1]
        if len(flight) != COLLUMS:
            raise Exception("Invalid input")
        return flight

    def read_all(self):
        """Read all lines from input"""
        while True:
            flight = self.read_line()
            if not flight:
                break
            self.flights.append(flight)
        return self.flights

    def get_flights(self):
        return self.flights

    def get_airports(self):
        return self.airports

    def convert_time(self, time):
        """Parsing time information with regex"""
        result = self.comp.match(time)
        try:
            timestamp = datetime.datetime(
                year=int(result.group(1)),
                month=int(result.group(2)),
                day=int(result.group(3)),
                hour=int(result.group(4)),
                minute=int(result.group(5)),
                second=int(result.group(6)),
            )
        except Exception:
            raise Exception("Invalid time format")
        return timestamp


class FlightSearcher(object):

    def __init__(self, flights, airports):
        self.flights = flights
        self.airports = airports
        self.path = []
        self.cache_airport = {}

    def get_all_combinations(self):
        """
        Backtracking algorithm
        Basically:
        1) put 1st airport to the stack
        2) pop one from stack and put it to the path
        3) verify path (for duplicity segments)
            a) if ok generate following flights and put them to stack
        4) if len > 3 yield the path
        5) if stack not empty go to 2nd step

        """
        for source in self.airports:
            open_stack = [(source, None, 1, None), ]
            self.path = []
            while open_stack:
                airport, arrival, depth, f_number = open_stack.pop()
                while len(self.path) >= depth:
                    self.path.pop()
                self.path.append((airport, f_number))
                if not self.verify_path():
                    continue
                for f in self.get_next_flights(airport, arrival):
                    open_stack.append(
                        (
                            f["destination"],
                            f["arrival"],
                            depth + 1,
                            f["flight_number"],
                        )
                    )
                if len(self.path) > 2:
                    yield copy(self.path)

    def get_all_flights_from_airport(self, airport):
        """
        Get list of all flights from airport.
        Time consuming operation thar runs very often,
        so cache was addded.
        """
        if airport in self.cache_airport:
            return self.cache_airport[airport]
        else:
            flights = filter(lambda f:  f["source"] == airport, self.flights)
            self.cache_airport[airport] = flights
            return flights

    def get_next_flights(self, airport, time, min=60, max=240):
        """Get list of all possible flights from airport in time window"""
        if not time:
            return self.get_all_flights_from_airport(airport)
        minimum = time + datetime.timedelta(minutes=min)
        maximum = time + datetime.timedelta(minutes=max)
        flights = []
        for f in self.get_all_flights_from_airport(airport):
            if f['departure'] > minimum and f['departure'] < maximum:
                flights.append(f)
        return flights

    def verify_path(self):
        """Check for repeating segments"""
        if len(self.path) < 3:
            return True
        current = self.path[-1][0]
        last = self.path[-2][0]
        for counter in range(1, len(self.path) - 1):
            if (
                self.path[counter][0] == current and
                self.path[counter-1][0] == last
            ):
                return False
        return True


def formater(journey):
    """
    journey is list of tuples!
    example: [(aiport1, None), (airport2, flight1), (airport3, flight2)]
    1) double for statement
    2) ignore None
    3) invert touples so flight between airports is visible
    """
    segments = [
        i for flight in journey for i in flight[::-1] if i
    ]
    return DELIMITER.join(segments) + "\n"


def main(args):
    parser = FlightParser(args["input"])
    parser.set_collums()
    flights = parser.read_all()
    if not flights:
        raise Exception("No flights defined")
    iterator = FlightSearcher(
        flights,  # all flights
        parser.get_airports(),  # all airports
    )
    for journey in iterator.get_all_combinations():
        args["output"].write(formater(journey))
    return 0


if __name__ == "__main__":
    args = parse_args()
#    try:
    retval = main(args)
#   except Exception as e:
#        sys.stderr.write(e.message)
#        sys.exit(1)
    sys.exit(retval)
