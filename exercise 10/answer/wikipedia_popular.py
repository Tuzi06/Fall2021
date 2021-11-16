import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


schema = types.StructType([
    types.StructField('page_language', types.StringType()),
    types.StructField('page_title', types.StringType()),
    types.StructField('requested', types.LongType()),
    types.StructField('bytes', types.LongType()),
])


def main(in_directory, out_directory):
    wiki = spark.read.csv(in_directory, schema=schema,sep=' ').withColumn('filename',functions.input_file_name())
    #wiki = spark.read.csv("pagecounts-1", schema=schema,sep=' ').withColumn('filename',functions.input_file_name())

    # TODO: finds the most-viewed page each hour
    #language=en
    cleaning_wiki=wiki.filter(wiki['page_language']=='en')
    #title!=Main_page
    cleaning_wiki=cleaning_wiki.filter(cleaning_wiki['page_title']!='Main_Page')
    #title!=startwith(special)
    cleaning_wiki=cleaning_wiki.filter(cleaning_wiki.page_title.startswith('Special:')==False)

    #path_to_hour=functions.udf(lambda x:functions.substring(x,-18,11),returnType=types.StringType())

    cleaning_wiki=cleaning_wiki.withColumn('date',functions.substring('filename',-18,11))
    #cleaning_wiki=cleaning_wiki.withColumn('date',cleaning_wiki['hour'].cast(types.StringType()))
    grouping_date=cleaning_wiki.groupBy('date')     
    
    result1=grouping_date.agg(functions.max(cleaning_wiki['requested']).alias('requested')).cache()
    #result2=cleaning_wiki.select(cleaning_wiki['page_title'],cleaning_wiki['requested'],cleaning_wiki['date'])
    result2=cleaning_wiki.drop('page_language','bytes','filename')

    #join_expression=result1['requested','date']==result2['requested','date']
    final_result=result1.join(result2,['requested','date'])
    #final_result=result1.join(result2,[result1.requested==result2.requested, result1.date==result2.date])
    final_result=final_result.sort('date','page_title')
    #final_result.show()
    final_result.write.csv(out_directory,mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
