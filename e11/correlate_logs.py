import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import math
spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        hostName = m.group(1)
        num_byte =m.group(2)
        return Row(hostname = hostName, num_bytes = num_byte)
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    log = log_lines.map(line_to_row).filter(not_none).collect()
    return log

def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    # TODO: calculate r.
    logs = logs.groupBy('hostname')
    num_request = logs.count()
    sum_bytes = logs.agg(functions.sum('num_bytes').alias('sum_bytes'))
    log = num_request.join(sum_bytes,'hostname')
    
    n = log.count()

    log = log.select(
        log['count'].alias('xi'),
        log['sum_bytes'].alias('yi'),
        (log['count']*log['count']).alias('xi^2'),
        (log['sum_bytes']*log['sum_bytes']).alias('yi^2'),
        (log['count']*log['sum_bytes']).alias('xiyi')
    )

    xi = log.agg(functions.sum('xi')).first()[0]
    yi = log.agg(functions.sum('yi')).first()[0]
    xi2 = log.agg(functions.sum('xi^2')).first()[0]
    yi2 = log.agg(functions.sum('yi^2')).first()[0]
    xiyi = log.agg(functions.sum('xiyi')).first()[0]

    r = (n*xiyi-xi*yi)/((math.sqrt(n*xi2-xi**2))*(math.sqrt(n*yi2-yi**2)))
    # r = 0 # TODO: it isn't zero.
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
