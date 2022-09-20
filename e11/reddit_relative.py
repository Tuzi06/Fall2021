import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)

    # TODO
    groups=comments.groupBy('subreddit')
    averages = groups.agg(functions.avg(comments['score'])).cache()
    
    averages = averages. filter(averages['avg(score)']>0)

    average_collection = averages.join(functions.broadcast(comments), on = 'subreddit')
    # average_collection = averages.join(comments, on = 'subreddit')
    average_collection = average_collection.withColumn('rel_score',average_collection['score']/average_collection['avg(score)']).cache()
    
    max_relative_score = average_collection.groupby('subreddit').agg(functions.max(average_collection['rel_score']).alias('rel_score'))

    best_comments = comments.groupby('subreddit').agg(functions.max('score').alias('score'))
    best_comments = best_comments.join(functions.broadcast(comments), on =['subreddit','score'])
    # best_comments = best_comments.join(comments, on =['subreddit','score'])
    best_comments = best_comments.sort('score')

    best_author = best_comments.join(functions.broadcast(max_relative_score), on='subreddit')
    # best_author = best_comments.join(max_relative_score, on='subreddit')
    best_author = best_author.select('subreddit','author','rel_score')
    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
