import sys
from pyspark.sql import SparkSession, functions, types, Row
import re

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
        return Row(hostname=m.group(1),bytes=m.group(2))
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
    log_rows=log_lines.map(line_to_row)
    log_rows=log_rows.filter(not_none)
    return log_rows


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    # TODO: calculate r.
    #2. group by hostname	
    logs_host=logs.groupby('hostname').count().alias('count_requests')
    logs_bytes=logs.groupby('hostname').agg(functions.sum('bytes').alias('sum_request_bytes'))
    log=logs_host.join(logs_bytes,'hostname')


    #3.
#x_i=log.select(log['count'])
#y_i=log.select(log['sum_request_bytes'])
#x_i2=log.select(log['count']*log['count'])
#y_i2=log.select(log['sum_request_bytes']*log['sum_request_bytes'])
#x_iy_i=log.select(log['sum_request_bytes']*log['count'])

    value=log.select(
    log['count'].alias('x_i'),log['sum_request_bytes'].alias('y_i'),
    (log['count']*log['count']).alias('x_i^2'),(log['sum_request_bytes']*log['sum_request_bytes']).alias('y_i^2'),
    (log['sum_request_bytes']*log['count']).alias('x_iy_i'))

    n=log.count()
    sum_x_i=value.agg(functions.sum('x_i')).first()[0]
    sum_y_i=value.agg(functions.sum('y_i')).first()[0]
    sum_x_i2=value.agg(functions.sum('x_i^2')).first()[0]
    sum_y_i2=value.agg(functions.sum('y_i^2')).first()[0]
    sum_x_iy_i=value.agg(functions.sum('x_iy_i')).first()[0]
    print()
    #4.
    import math
    r=(n*sum_x_iy_i-(sum_x_i*sum_y_i))/(math.sqrt(n*sum_x_i2-(sum_x_i**2))*math.sqrt(n*sum_y_i2-(sum_y_i**2)))

    # TODO: it isn't zero.
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
