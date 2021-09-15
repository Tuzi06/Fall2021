import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('weather ETL').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.4' # make sure we have Spark 2.4+

observation_schema = types.StructType([
    types.StructField('station', types.StringType()),
    types.StructField('date', types.StringType()),
    types.StructField('observation', types.StringType()),
    types.StructField('value', types.IntegerType()),
    types.StructField('mflag', types.StringType()),
    types.StructField('qflag', types.StringType()),
    types.StructField('sflag', types.StringType()),
    types.StructField('obstime', types.StringType()),
])


def main(in_directory, out_directory):
    #Read the input directory of .csv.gz files.
    weather = spark.read.csv(in_directory, schema=observation_schema)
    
    #Keep only the records we care about:
    #field qflag (quality flag) is null; (Hint)
    cleaned_data = weather.filter(weather.qflag.isNull())
 
    #the station starts with 'CA'; (Hint option 1; Hint option 2)
    cleaned_data = cleaned_data.filter(cleaned_data.station.startswith('CA'))

    #the observation is 'TMAX'.
    cleaned_data = cleaned_data.filter(cleaned_data['observation'] == 'TMAX')

    #Divide the temperature by 10 so it's actually in °C, and call the resulting column tmax.
    cleaned_data = cleaned_data.withColumn('tmax', cleaned_data['value'] / 10)

    #Keep only the columns station, date, and tmax.
    cleaned_data = cleaned_data.select(cleaned_data['station'], cleaned_data['date'], cleaned_data['tmax'])

    #Write the result as a directory of JSON files GZIP compressed (in the Spark one-JSON-object-per-line way).
    cleaned_data.write.json(out_directory, compression='gzip', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
