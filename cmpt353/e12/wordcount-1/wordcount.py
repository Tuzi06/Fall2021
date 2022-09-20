import sys
import string,re
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

def main(in_directory,out_directory):
    word = spark.read.text(in_directory)
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
    splited= word.select(functions.split(word.value,wordbreak).alias('value'))
    splited= splited.select(functions.explode(splited.value).alias('value'))
    splited = splited.select(functions.lower(splited.value).alias('word'))
    words = splited.groupby('word').count()
    words = words.sort(words['count'].desc())
    words = words.filter(words.word !=' ')
    words.write.csv(out_directory,mode='overwrite')






if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
