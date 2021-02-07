#!/usr/local/bin/python3
from flask import Flask
from flask import jsonify, request
from calendar import timegm
from datetime import datetime
import sqlite3

app = Flask(__name__)

SQLITE_DATABASE_FILE = '/tmp/monitor.db'
MONITOR_TABLE = 'packet_latency'
COMPONENT_LIST = ['min_latency', 'avg_latency',
                  'max_latency', 'stddev_latency']


############# Helper methods #############
def convert_to_time_sec(timestamp):
    """Convert a Grafana timestamp to unixtimestamp in seconds
    Args:
        timestamp (str): time in datetime from Grafana
            Example: '2019-06-16T08:00:05.331Z'
    Returns:
        int: time in epoc
            Example: 1560672005
        """
    return timegm(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())


def get_all_data(column, start_time_epoc, end_time_epoc):
    """Fetch data from database

    Args:
        column (str): column of table
        start_time_epoc (int): Start time
        end_time_epoc (int): end time

    Returns:
        list: list of datapoints
            Example: [(22.433, 1612557720000), (1.72, 1612557780000), (31.101, 1612557840000), (21.248, 1612557901000)]
    """
    conn = sqlite3.connect(SQLITE_DATABASE_FILE)

    cursor = conn.cursor()
    cursor.execute(
        f'SELECT {column},epoc*1000 from {MONITOR_TABLE} where epoc >= {start_time_epoc} and epoc <= {end_time_epoc}')
    result = cursor.fetchall()
    conn.close()
    return result


############# Routes #############
@app.route('/')
def hello():
    return "OK"


@app.route('/search', methods=['POST'])
def list_options():
    return jsonify(COMPONENT_LIST)


@app.route('/query', methods=['POST'])
def query_data():
    final_result = []

    if request.json['targets'][0]['type'] == 'table':
        print("table not supported")
        return jsonify("No Data :(")
    else:
        start, end = request.json['range']['from'], request.json['range']['to']
        series = request.json['targets'][0]['target']

        if series == 'min_latency':
            output_data = get_all_data(
                'min', convert_to_time_sec(start), convert_to_time_sec(end))
            for each_epoc in output_data:
                final_result.append(list(each_epoc))
        elif series == 'avg_latency':
            output_data = get_all_data(
                'avg', convert_to_time_sec(start), convert_to_time_sec(end))
            for each_epoc in output_data:
                final_result.append(list(each_epoc))
        elif series == 'max_latency':
            output_data = get_all_data(
                'max', convert_to_time_sec(start), convert_to_time_sec(end))
            for each_epoc in output_data:
                final_result.append(list(each_epoc))
        elif series == 'stddev_latency':
            output_data = get_all_data(
                'stddev', convert_to_time_sec(start), convert_to_time_sec(end))
        else:
            output_data = []
            print("Invalid Choice")

    for each_epoc in output_data:
        final_result.append(list(each_epoc))
    print(final_result)
    return jsonify(
        [
            {
                "target": series,
                "datapoints": final_result
            }
        ]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
