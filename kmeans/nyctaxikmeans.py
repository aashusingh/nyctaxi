from pyspark.mllib.clustering import KMeans
from numpy import array
from math import sqrt
from pyspark import SparkContext


sc = SparkContext("local","NYC Taxi")

# Load and parse the data
# data = sc.textFile("trip_small.csv").map(lambda line: line.split(","))
dataFile = sc.textFile("triptest")


#Run on AWS
#dataFile = ("s3n://accesskey:secretkey@rep-name/repos")


data = sc.textFile(dataFile).cache()
parsedData = data.map(lambda line: array([float(x) for x in line.split(',')]))

#data = sc.textFile("data/mllib/kmeans_data.txt")
#parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))

# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 60, maxIterations=10,
        runs=10, initializationMode="random")

# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))
