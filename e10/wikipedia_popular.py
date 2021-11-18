import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

page_schema = types.StructType([
        types.StructField('language', types.StringType()),
        types.StructField('title',types.StringType()),
        types.StructField('times',types.LongType()),
        types.StructField('byte',types.LongType()),
])
    
def main(in_directory, out_directory):
    source = spark.read.csv(in_directory, schema = page_schema, sep=' ').withColumn('filename',functions.input_file_name())

    data = source.filter(source['language'] == 'en')
    data = data.filter(data['title'] != 'Main_Page')
    data = data.filter(data['title'].startswith('Special:')==False)

    def convert(s):
        return re.search('\d+\-[0-9]{2}', s).group(0)
    
    path_to_hour = functions.udf(convert,returnType=types.StringType())
    data = data.withColumn('date',path_to_hour(data['filename']))
    data = data.cache()
    group = data.groupby('date')
    r1 = group.agg(functions.max(data['times']).alias('times'))

    r2 = data.drop('language','filename','byte')

    r = r1.join(data,on = ['date','times'])
    r = r.sort('date','title')
    r = r.select('date','title','times')
    r.write.csv(out_directory,mode='overwrite')

    
if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
