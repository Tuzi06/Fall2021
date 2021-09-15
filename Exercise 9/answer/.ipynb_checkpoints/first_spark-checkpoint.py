{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "455585b7",
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "from pyspark.sql import SparkSession, functions, types"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "e6374c8d",
   "metadata": {},
   "outputs": [
    {
     "ename": "Exception",
     "evalue": "Java gateway process exited before sending its port number",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mException\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-2-27d2d41ea7f5>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mspark\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mSparkSession\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mbuilder\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mappName\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'first Spark app'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mgetOrCreate\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[0mspark\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msetLogLevel\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'WARN'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Roaming\\Python\\Python38\\site-packages\\pyspark\\sql\\session.py\u001b[0m in \u001b[0;36mgetOrCreate\u001b[1;34m(self)\u001b[0m\n\u001b[0;32m    226\u001b[0m                             \u001b[0msparkConf\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mset\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mvalue\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    227\u001b[0m                         \u001b[1;31m# This SparkContext may be an existing one.\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 228\u001b[1;33m                         \u001b[0msc\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mgetOrCreate\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0msparkConf\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    229\u001b[0m                     \u001b[1;31m# Do not update `SparkConf` for existing `SparkContext`, as it's shared\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    230\u001b[0m                     \u001b[1;31m# by all sessions.\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Roaming\\Python\\Python38\\site-packages\\pyspark\\context.py\u001b[0m in \u001b[0;36mgetOrCreate\u001b[1;34m(cls, conf)\u001b[0m\n\u001b[0;32m    382\u001b[0m         \u001b[1;32mwith\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_lock\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    383\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_active_spark_context\u001b[0m \u001b[1;32mis\u001b[0m \u001b[1;32mNone\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 384\u001b[1;33m                 \u001b[0mSparkContext\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mconf\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mconf\u001b[0m \u001b[1;32mor\u001b[0m \u001b[0mSparkConf\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    385\u001b[0m             \u001b[1;32mreturn\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_active_spark_context\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    386\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Roaming\\Python\\Python38\\site-packages\\pyspark\\context.py\u001b[0m in \u001b[0;36m__init__\u001b[1;34m(self, master, appName, sparkHome, pyFiles, environment, batchSize, serializer, conf, gateway, jsc, profiler_cls)\u001b[0m\n\u001b[0;32m    142\u001b[0m                 \" is not allowed as it is a security risk.\")\n\u001b[0;32m    143\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 144\u001b[1;33m         \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_ensure_initialized\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mgateway\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mgateway\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mconf\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mconf\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    145\u001b[0m         \u001b[1;32mtry\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    146\u001b[0m             self._do_init(master, appName, sparkHome, pyFiles, environment, batchSize, serializer,\n",
      "\u001b[1;32m~\\AppData\\Roaming\\Python\\Python38\\site-packages\\pyspark\\context.py\u001b[0m in \u001b[0;36m_ensure_initialized\u001b[1;34m(cls, instance, gateway, conf)\u001b[0m\n\u001b[0;32m    329\u001b[0m         \u001b[1;32mwith\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_lock\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    330\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_gateway\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 331\u001b[1;33m                 \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_gateway\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mgateway\u001b[0m \u001b[1;32mor\u001b[0m \u001b[0mlaunch_gateway\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mconf\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    332\u001b[0m                 \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_jvm\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mSparkContext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_gateway\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mjvm\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    333\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\AppData\\Roaming\\Python\\Python38\\site-packages\\pyspark\\java_gateway.py\u001b[0m in \u001b[0;36mlaunch_gateway\u001b[1;34m(conf, popen_kwargs)\u001b[0m\n\u001b[0;32m    106\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    107\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[0mos\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0misfile\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mconn_info_file\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 108\u001b[1;33m                 \u001b[1;32mraise\u001b[0m \u001b[0mException\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"Java gateway process exited before sending its port number\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    109\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    110\u001b[0m             \u001b[1;32mwith\u001b[0m \u001b[0mopen\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mconn_info_file\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m\"rb\"\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0minfo\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mException\u001b[0m: Java gateway process exited before sending its port number"
     ]
    }
   ],
   "source": [
    "spark = SparkSession.builder.appName('first Spark app').getOrCreate()\n",
    "spark.sparkContext.setLogLevel('WARN')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c7240606",
   "metadata": {},
   "outputs": [],
   "source": [
    "assert sys.version_info >= (3, 5) # make sure we have Python 3.5+\n",
    "assert spark.version >= '2.3' # make sure we have Spark 2.3+"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ae7d0e88",
   "metadata": {},
   "outputs": [],
   "source": [
    "schema = types.StructType([\n",
    "    types.StructField('id', types.IntegerType()),\n",
    "    types.StructField('x', types.FloatType()),\n",
    "    types.StructField('y', types.FloatType()),\n",
    "    types.StructField('z', types.FloatType()),\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "59e7b891",
   "metadata": {},
   "outputs": [],
   "source": [
    "def main(in_directory, out_directory):\n",
    "    # Read the data from the JSON files\n",
    "    xyz = spark.read.json(in_directory, schema=schema)\n",
    "    #xyz.show(); return\n",
    "\n",
    "    # Create a DF with what we need: x, (soon y,) and id%10 which we'll aggregate by.\n",
    "    with_bins = xyz.select(\n",
    "        xyz['x'],\n",
    "        # TODO: also the y values\n",
    "        xyz['y'],\n",
    "        (xyz['id'] % 10).alias('bin'),\n",
    "    )\n",
    "    #with_bins.show(); return\n",
    "\n",
    "    # Aggregate by the bin number.\n",
    "    grouped = with_bins.groupBy(with_bins['bin'])\n",
    "    groups = grouped.agg(\n",
    "        functions.sum(with_bins['x']),\n",
    "        # TODO: output the average y value. Hint: avg\n",
    "        function.avg(with_bins['y']),\n",
    "        functions.count('*'))\n",
    "\n",
    "    # We know groups has <=10 rows, so it can safely be moved into two partitions.\n",
    "    groups = groups.sort(groups['bin']).coalesce(2)\n",
    "    groups.write.csv(out_directory, compression=None, mode='overwrite')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4066f025",
   "metadata": {},
   "outputs": [],
   "source": [
    "if __name__=='__main__':\n",
    "    in_directory = sys.argv[1]\n",
    "    out_directory = sys.argv[2]\n",
    "#     in_directory = \"xyz-1\"\n",
    "#     out_directory = \"output\"\n",
    "    main(in_directory, out_directory)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
