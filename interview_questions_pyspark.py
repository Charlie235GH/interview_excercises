"""
50 Technical PySpark Interview Questions for Data Management Positions
Ordered by ascending skill level (Beginner → Intermediate → Advanced)
Each question designed to be solved in under 5 minutes

Focus Areas: DataFrames, RDDs, SQL, Data Processing, Performance Optimization,
Streaming, Data Quality, ETL Operations

Author: Interview Preparation - PySpark Edition
Date: December 11, 2025
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, count, max as spark_max, sum as spark_sum, min as spark_min, 
    when, lit, concat, upper, lower, length, substring, trim, to_date, 
    current_date, current_timestamp, year, month, datediff, first, last,
    row_number, rank, lag, lead, ntile, percent_rank, stddev, 
    percentile_approx, collect_list, from_json, window, split, regexp_replace,
    rand, broadcast, udf
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, 
    BooleanType, TimestampType, DateType
)
from pyspark.sql.window import Window
from pyspark import SparkContext, SparkConf
import pyspark.sql.functions as F

# Initialize Spark Session (for demonstration)
def get_spark_session():
    """Initialize Spark Session with common configurations."""
    return SparkSession.builder \
        .appName("PySpark Interview Questions") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

# Sample data creation helper functions
def create_sample_data(spark):
    """Create sample DataFrames for testing."""
    # Employee data
    employees_data = [
        (1, "Alice", "Engineering", 75000, "2020-01-15"),
        (2, "Bob", "Sales", 65000, "2019-03-20"),
        (3, "Charlie", "Engineering", 80000, "2021-06-10"),
        (4, "Diana", "Marketing", 70000, "2020-11-05"),
        (5, "Eve", "Sales", 72000, "2018-09-12")
    ]
    
    employees_schema = StructType([
        StructField("emp_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("department", StringType(), True),
        StructField("salary", IntegerType(), True),
        StructField("hire_date", StringType(), True)
    ])
    
    return spark.createDataFrame(employees_data, employees_schema)

print("PySpark Interview Questions - Data Management Focus")
print("="*60)

# =============================================================================
# BEGINNER LEVEL (Questions 1-15)
# =============================================================================

# Question 1: Create a Spark Session
def create_spark_session():
    """Q1: How do you create a Spark Session with custom configurations?"""
    spark = SparkSession.builder \
        .appName("DataProcessingApp") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()
    return spark

print("Q1 - Spark Session created with custom configurations")

# Question 2: Read CSV file
def read_csv_file(spark, file_path):
    """Q2: How do you read a CSV file with headers and infer schema?"""
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(file_path)
    return df

print("Q2 - Read CSV with header and schema inference")

# Question 3: Show DataFrame info
def show_dataframe_info(df):
    """Q3: How do you display DataFrame schema, count, and sample data?"""
    print("Schema:")
    df.printSchema()
    print(f"Row count: {df.count()}")
    print("Sample data:")
    df.show(5)

print("Q3 - DataFrame information display methods")

# Question 4: Select specific columns
def select_columns(df, columns):
    """Q4: How do you select specific columns from a DataFrame?"""
    return df.select(*columns)

print("Q4 - Select specific columns")

# Question 5: Filter DataFrame
def filter_dataframe(df, condition):
    """Q5: How do you filter DataFrame rows based on conditions?"""
    # Example: df.filter(col("salary") > 70000)
    return df.filter(condition)

print("Q5 - Filter DataFrame with conditions")

# Question 6: Add new column
def add_calculated_column(df):
    """Q6: How do you add a calculated column to DataFrame?"""
    return df.withColumn("annual_bonus", col("salary") * 0.1)

print("Q6 - Add calculated column")

# Question 7: Rename columns
def rename_columns(df, column_mapping):
    """Q7: How do you rename multiple columns?"""
    for old_name, new_name in column_mapping.items():
        df = df.withColumnRenamed(old_name, new_name)
    return df

print("Q7 - Rename multiple columns")

# Question 8: Drop columns
def drop_columns(df, columns_to_drop):
    """Q8: How do you drop columns from DataFrame?"""
    return df.drop(*columns_to_drop)

print("Q8 - Drop columns")

# Question 9: Handle null values
def handle_null_values(df):
    """Q9: How do you handle null values in DataFrame?"""
    # Drop rows with any null values
    df_clean = df.na.drop()
    
    # Fill null values with defaults
    df_filled = df.na.fill({"salary": 0, "department": "Unknown"})
    
    return df_clean, df_filled

print("Q9 - Handle null values")

# Question 10: Group by and aggregate
def group_by_aggregate(df):
    """Q10: How do you perform group by operations with aggregations?"""
    return df.groupBy("department") \
        .agg(
            avg("salary").alias("avg_salary"),
            count("*").alias("emp_count"),
            spark_max("salary").alias("max_salary")
        )

print("Q10 - Group by with aggregations")

# Question 11: Sort DataFrame
def sort_dataframe(df):
    """Q11: How do you sort DataFrame by multiple columns?"""
    return df.orderBy(col("department").asc(), col("salary").desc())

print("Q11 - Sort by multiple columns")

# Question 12: Write DataFrame to file
def write_dataframe(df, output_path, format_type="parquet"):
    """Q12: How do you write DataFrame to different file formats?"""
    df.write \
        .mode("overwrite") \
        .option("header", "true") \
        .format(format_type) \
        .save(output_path)

print("Q12 - Write DataFrame to file")

# Question 13: Basic SQL operations
def sql_operations(spark, df):
    """Q13: How do you perform SQL operations on DataFrame?"""
    df.createOrReplaceTempView("employees")
    
    result = spark.sql("""
        SELECT department, AVG(salary) as avg_salary
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 70000
    """)
    
    return result

print("Q13 - SQL operations on DataFrame")

# Question 14: Union DataFrames
def union_dataframes(df1, df2):
    """Q14: How do you union two DataFrames?"""
    return df1.union(df2)

print("Q14 - Union DataFrames")

# Question 15: Distinct values
def get_distinct_values(df, column):
    """Q15: How do you get distinct values from a column?"""
    return df.select(column).distinct()

print("Q15 - Get distinct values")

# =============================================================================
# INTERMEDIATE LEVEL (Questions 16-35)
# =============================================================================

# Question 16: Join operations
def join_dataframes(df1, df2, join_key, join_type="inner"):
    """Q16: How do you perform different types of joins?"""
    return df1.join(df2, join_key, join_type)

print("Q16 - Join DataFrames")

# Question 17: Window functions
def window_functions(df):
    """Q17: How do you use window functions for ranking and analytics?"""
    window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
    
    return df.withColumn("rank", row_number().over(window_spec)) \
        .withColumn("salary_rank", rank().over(window_spec)) \
        .withColumn("running_total", spark_sum("salary").over(window_spec))

print("Q17 - Window functions")

# Question 18: UDF (User Defined Function)
def create_udf_example(spark):
    """Q18: How do you create and use UDFs?"""
    from pyspark.sql.functions import udf
    
    def salary_grade(salary):
        if salary >= 80000:
            return "Senior"
        elif salary >= 70000:
            return "Mid"
        else:
            return "Junior"
    
    salary_grade_udf = udf(salary_grade, StringType())
    
    return salary_grade_udf

print("Q18 - User Defined Functions")

# Question 19: Data type conversions
def data_type_conversions(df):
    """Q19: How do you convert data types in DataFrame?"""
    return df.withColumn("hire_date", to_date(col("hire_date"), "yyyy-MM-dd")) \
        .withColumn("salary", col("salary").cast(DoubleType())) \
        .withColumn("emp_id", col("emp_id").cast(StringType()))

print("Q19 - Data type conversions")

# Question 20: String operations
def string_operations(df):
    """Q20: How do you perform string operations on DataFrame columns?"""
    return df.withColumn("name_upper", upper(col("name"))) \
        .withColumn("name_length", length(col("name"))) \
        .withColumn("dept_abbr", substring(col("department"), 1, 3)) \
        .withColumn("name_clean", trim(col("name")))

print("Q20 - String operations")

# Question 21: Date/Time operations
def datetime_operations(df):
    """Q21: How do you work with date/time columns?"""
    return df.withColumn("hire_date", to_date(col("hire_date"), "yyyy-MM-dd")) \
        .withColumn("hire_year", year(col("hire_date"))) \
        .withColumn("hire_month", month(col("hire_date"))) \
        .withColumn("days_employed", datediff(current_date(), col("hire_date")))

print("Q21 - Date/Time operations")

# Question 22: Pivoting data
def pivot_data(df):
    """Q22: How do you pivot DataFrame data?"""
    return df.groupBy("department") \
        .pivot("name") \
        .agg(first("salary"))

print("Q22 - Pivot data")

# Question 23: Broadcasting variables
def broadcast_example(spark, df):
    """Q23: How do you use broadcast variables for optimization?"""
    dept_mapping = {"Engineering": "ENG", "Sales": "SAL", "Marketing": "MKT"}
    broadcast_mapping = spark.sparkContext.broadcast(dept_mapping)
    
    def map_department(dept):
        return broadcast_mapping.value.get(dept, dept)
    
    map_dept_udf = udf(map_department, StringType())
    
    return df.withColumn("dept_code", map_dept_udf(col("department")))

print("Q23 - Broadcast variables")

# Question 24: Accumulator usage
def accumulator_example(spark, df):
    """Q24: How do you use accumulators for distributed counters?"""
    high_salary_counter = spark.sparkContext.accumulator(0)
    
    def count_high_salary(salary):
        if salary > 75000:
            high_salary_counter.add(1)
        return salary
    
    count_salary_udf = udf(count_high_salary, IntegerType())
    result_df = df.withColumn("salary_checked", count_salary_udf(col("salary")))
    
    return result_df, high_salary_counter

print("Q24 - Accumulator usage")

# Question 25: Partitioning strategies
def partitioning_strategies(df, output_path):
    """Q25: How do you partition data for optimal performance?"""
    # Partition by department
    df.write \
        .mode("overwrite") \
        .partitionBy("department") \
        .parquet(output_path)

print("Q25 - Data partitioning")

# Question 26: Bucketing
def bucketing_example(df, output_path):
    """Q26: How do you implement bucketing for better query performance?"""
    df.write \
        .mode("overwrite") \
        .bucketBy(4, "emp_id") \
        .sortBy("salary") \
        .saveAsTable("employees_bucketed")

print("Q26 - Bucketing implementation")

# Question 27: Cache and persist
def caching_strategies(df):
    """Q27: How do you optimize DataFrame performance using caching?"""
    # Cache in memory
    df_cached = df.cache()
    
    # Persist with specific storage level
    from pyspark import StorageLevel
    df_persisted = df.persist(StorageLevel.MEMORY_AND_DISK)
    
    return df_cached, df_persisted

print("Q27 - Caching strategies")

# Question 28: Repartitioning
def repartitioning_example(df):
    """Q28: How do you repartition DataFrame for better performance?"""
    # Increase partitions
    df_more_partitions = df.repartition(8)
    
    # Decrease partitions
    df_fewer_partitions = df.coalesce(2)
    
    # Repartition by column
    df_by_dept = df.repartition("department")
    
    return df_more_partitions, df_fewer_partitions, df_by_dept

print("Q28 - Repartitioning strategies")

# Question 29: Error handling
def error_handling_example(spark, file_path):
    """Q29: How do you implement error handling in PySpark?"""
    try:
        df = spark.read.csv(file_path, header=True, inferSchema=True)
        return df
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        # Return empty DataFrame with schema
        schema = StructType([StructField("error", StringType(), True)])
        return spark.createDataFrame([("File not found",)], schema)

print("Q29 - Error handling")

# Question 30: Complex aggregations
def complex_aggregations(df):
    """Q30: How do you perform complex aggregations with multiple conditions?"""
    return df.groupBy("department") \
        .agg(
            avg("salary").alias("avg_salary"),
            stddev("salary").alias("salary_stddev"),
            percentile_approx("salary", 0.5).alias("median_salary"),
            spark_sum(when(col("salary") > 75000, 1).otherwise(0)).alias("high_earners"),
            collect_list("name").alias("employee_names")
        )

print("Q30 - Complex aggregations")

# Question 31: Schema enforcement
def schema_enforcement(spark):
    """Q31: How do you enforce schema when reading data?"""
    schema = StructType([
        StructField("emp_id", IntegerType(), False),
        StructField("name", StringType(), False),
        StructField("department", StringType(), True),
        StructField("salary", DoubleType(), True)
    ])
    
    df = spark.read \
        .schema(schema) \
        .option("mode", "FAILFAST") \
        .csv("employee_data.csv", header=True)
    
    return df

print("Q31 - Schema enforcement")

# Question 32: Data quality checks
def data_quality_checks(df):
    """Q32: How do you implement data quality validations?"""
    # Check for nulls
    null_counts = df.select([count(when(col(c).isNull(), c)).alias(c) 
                            for c in df.columns])
    
    # Check for duplicates
    duplicate_count = df.count() - df.dropDuplicates().count()
    
    # Data validation
    invalid_salaries = df.filter(col("salary") < 0).count()
    
    return null_counts, duplicate_count, invalid_salaries

print("Q32 - Data quality checks")

# Question 33: Delta Lake operations (conceptual)
def delta_lake_operations():
    """Q33: How would you implement Delta Lake operations?"""
    operations = {
        "read": "df = spark.read.format('delta').load('/path/to/delta-table')",
        "write": "df.write.format('delta').mode('overwrite').save('/path/to/delta-table')",
        "merge": "delta_table.merge(updates_df, 'target.id = source.id').whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()",
        "time_travel": "df = spark.read.format('delta').option('timestampAsOf', '2021-01-01').load('/path')"
    }
    return operations

print("Q33 - Delta Lake operations")

# Question 34: Streaming basics
def streaming_example(spark):
    """Q34: How do you set up basic streaming operations?"""
    # Read stream
    stream_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "input-topic") \
        .load()
    
    # Process stream
    processed = stream_df.select(
        col("value").cast("string").alias("message"),
        current_timestamp().alias("processing_time")
    )
    
    # Write stream
    query = processed.writeStream \
        .format("console") \
        .outputMode("append") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    return query

print("Q34 - Streaming operations")

# Question 35: Performance monitoring
def performance_monitoring(spark, df):
    """Q35: How do you monitor and optimize Spark job performance?"""
    # Enable SQL metrics
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
    
    # Explain query plan
    df.explain(True)
    
    # Check partition count
    partition_count = df.rdd.getNumPartitions()
    
    return partition_count

print("Q35 - Performance monitoring")

# =============================================================================
# ADVANCED LEVEL (Questions 36-50)
# =============================================================================

# Question 36: Custom partitioner
def custom_partitioner_example(spark):
    """Q36: How do you implement custom partitioning logic?"""
    from pyspark.sql.functions import col, when
    
    def partition_by_salary_range(df):
        return df.withColumn("salary_partition",
            when(col("salary") < 60000, "low")
            .when(col("salary") < 80000, "medium")
            .otherwise("high")
        )
    
    return partition_by_salary_range

print("Q36 - Custom partitioner")

# Question 37: Advanced window functions
def advanced_window_functions(df):
    """Q37: How do you implement complex window operations?"""
    # Define multiple window specifications
    dept_window = Window.partitionBy("department").orderBy("salary")
    global_window = Window.orderBy("salary")
    
    return df.withColumn("dept_salary_rank", rank().over(dept_window)) \
        .withColumn("global_percentile", percent_rank().over(global_window)) \
        .withColumn("salary_lag", lag("salary", 1).over(dept_window)) \
        .withColumn("salary_lead", lead("salary", 1).over(dept_window)) \
        .withColumn("salary_ntile", ntile(4).over(dept_window))

print("Q37 - Advanced window functions")

# Question 38: Graph processing with GraphFrames
def graph_processing_example():
    """Q38: How would you implement graph processing operations?"""
    # This is conceptual as GraphFrames requires additional setup
    operations = {
        "create_graph": """
            from graphframes import GraphFrame
            vertices = spark.createDataFrame([("a", "Alice"), ("b", "Bob")], ["id", "name"])
            edges = spark.createDataFrame([("a", "b", "friend")], ["src", "dst", "relationship"])
            graph = GraphFrame(vertices, edges)
        """,
        "page_rank": "graph.pageRank(resetProbability=0.15, maxIter=10)",
        "connected_components": "graph.connectedComponents()",
        "shortest_paths": "graph.shortestPaths(landmarks=['a', 'b'])"
    }
    return operations

print("Q38 - Graph processing")

# Question 39: MLlib integration
def mllib_integration_example(df):
    """Q39: How do you integrate with MLlib for machine learning?"""
    from pyspark.ml.feature import VectorAssembler, StandardScaler
    from pyspark.ml.clustering import KMeans
    from pyspark.ml import Pipeline
    
    # Feature engineering
    assembler = VectorAssembler(inputCols=["salary"], outputCol="features")
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
    kmeans = KMeans(k=3, featuresCol="scaledFeatures")
    
    # Create pipeline
    pipeline = Pipeline(stages=[assembler, scaler, kmeans])
    
    # This would be fitted and transformed in practice
    return pipeline

print("Q39 - MLlib integration")

# Question 40: Advanced data skew handling
def handle_data_skew(df, skewed_column):
    """Q40: How do you handle data skew in large datasets?"""
    # Add salt to skewed keys
    from pyspark.sql.functions import rand, concat, lit
    
    # Add random salt
    salted_df = df.withColumn("salt", (rand() * 10).cast("int")) \
        .withColumn("salted_key", concat(col(skewed_column), lit("_"), col("salt")))
    
    # Alternative: Use broadcast join for smaller skewed data
    def broadcast_join_skew_fix(large_df, small_df, join_key):
        from pyspark.sql.functions import broadcast
        return large_df.join(broadcast(small_df), join_key)
    
    return salted_df

print("Q40 - Data skew handling")

# Question 41: Custom data source
def custom_data_source_example():
    """Q41: How would you implement a custom data source?"""
    # This is a conceptual example of reading from custom format
    custom_reader = {
        "implementation": """
            class CustomDataSource:
                def __init__(self, spark):
                    self.spark = spark
                
                def read_custom_format(self, path):
                    # Custom logic to read proprietary format
                    rdd = self.spark.sparkContext.textFile(path)
                    # Parse and transform data
                    return self.spark.createDataFrame(rdd.map(self.parse_line))
                
                def parse_line(self, line):
                    # Custom parsing logic
                    return tuple(line.split('|'))
        """,
        "usage": "custom_source = CustomDataSource(spark); df = custom_source.read_custom_format('path')"
    }
    return custom_reader

print("Q41 - Custom data source")

# Question 42: Dynamic partition pruning
def dynamic_partition_pruning(spark):
    """Q42: How do you optimize queries with dynamic partition pruning?"""
    spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")
    spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.useStats", "true")
    
    # Example query that benefits from DPP
    query = """
        SELECT l.*, s.name 
        FROM large_partitioned_table l
        JOIN small_dimension_table s ON l.department_id = s.id
        WHERE s.active = true
    """
    
    return query

print("Q42 - Dynamic partition pruning")

# Question 43: Adaptive query execution
def adaptive_query_execution(spark):
    """Q43: How do you configure Adaptive Query Execution (AQE)?"""
    configs = {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true",
        "spark.sql.adaptive.skewJoin.enabled": "true",
        "spark.sql.adaptive.localShuffleReader.enabled": "true",
        "spark.sql.adaptive.advisoryPartitionSizeInBytes": "64MB",
        "spark.sql.adaptive.coalescePartitions.minPartitionNum": "1"
    }
    
    for key, value in configs.items():
        spark.conf.set(key, value)
    
    return configs

print("Q43 - Adaptive Query Execution")

# Question 44: Memory management
def memory_management_optimization():
    """Q44: How do you optimize memory usage in Spark applications?"""
    configs = {
        "driver_memory": "spark.driver.memory=4g",
        "executor_memory": "spark.executor.memory=8g",
        "memory_fraction": "spark.sql.shuffle.partitions=200",
        "garbage_collection": "spark.executor.extraJavaOptions=-XX:+UseG1GC",
        "off_heap": "spark.sql.columnVector.offHeap.enabled=true",
        "tungsten": "spark.sql.codegen.wholeStage=true"
    }
    
    return configs

print("Q44 - Memory management")

# Question 45: Security implementation
def security_implementation():
    """Q45: How do you implement security in Spark applications?"""
    security_configs = {
        "authentication": "spark.authenticate=true",
        "encryption": "spark.network.crypto.enabled=true",
        "ssl": "spark.ssl.enabled=true",
        "acls": "spark.acls.enable=true",
        "kerberos": "spark.security.credentials.hbase.enabled=true",
        "data_encryption": "spark.sql.execution.arrow.pyspark.enabled=true"
    }
    
    return security_configs

print("Q45 - Security implementation")

# Question 46: Cost-based optimization
def cost_based_optimization(spark):
    """Q46: How do you enable and configure cost-based optimization?"""
    # Enable CBO
    spark.conf.set("spark.sql.cbo.enabled", "true")
    spark.conf.set("spark.sql.cbo.joinReorder.enabled", "true")
    spark.conf.set("spark.sql.cbo.planStats.enabled", "true")
    
    # Collect statistics
    collect_stats_query = """
        ANALYZE TABLE employees COMPUTE STATISTICS FOR ALL COLUMNS
    """
    
    return collect_stats_query

print("Q46 - Cost-based optimization")

# Question 47: Multi-cluster deployment
def multi_cluster_deployment():
    """Q47: How do you design for multi-cluster Spark deployment?"""
    deployment_strategies = {
        "yarn_cluster": {
            "mode": "--deploy-mode cluster",
            "queue": "--queue production",
            "resources": "--num-executors 10 --executor-cores 4 --executor-memory 8g"
        },
        "kubernetes": {
            "master": "--master k8s://https://kubernetes-api-server",
            "image": "--conf spark.kubernetes.container.image=spark:latest",
            "namespace": "--conf spark.kubernetes.namespace=spark-jobs"
        },
        "standalone": {
            "master": "--master spark://master:7077",
            "total_cores": "--total-executor-cores 40"
        }
    }
    
    return deployment_strategies

print("Q47 - Multi-cluster deployment")

# Question 48: Real-time analytics pipeline
def realtime_analytics_pipeline(spark):
    """Q48: How do you build a real-time analytics pipeline?"""
    # Stream processing with stateful operations
    pipeline_code = """
        # Read from Kafka
        input_stream = spark.readStream \\
            .format("kafka") \\
            .option("kafka.bootstrap.servers", "localhost:9092") \\
            .option("subscribe", "events") \\
            .load()
        
        # Parse JSON and extract fields
        parsed_stream = input_stream.select(
            from_json(col("value").cast("string"), event_schema).alias("event")
        ).select("event.*")
        
        # Windowed aggregations
        windowed_counts = parsed_stream \\
            .withWatermark("timestamp", "10 minutes") \\
            .groupBy(
                window(col("timestamp"), "5 minutes", "1 minute"),
                col("event_type")
            ) \\
            .count()
        
        # Output to multiple sinks
        query = windowed_counts.writeStream \\
            .outputMode("update") \\
            .format("delta") \\
            .option("checkpointLocation", "/tmp/checkpoint") \\
            .trigger(processingTime="30 seconds") \\
            .start()
    """
    
    return pipeline_code

print("Q48 - Real-time analytics pipeline")

# Question 49: Data lineage and governance
def data_lineage_governance():
    """Q49: How do you implement data lineage and governance?"""
    governance_framework = {
        "metadata_tracking": """
            # Track data transformations
            def track_lineage(df, operation, source_tables):
                lineage_info = {
                    'timestamp': datetime.now(),
                    'operation': operation,
                    'source_tables': source_tables,
                    'output_schema': df.schema.json(),
                    'row_count': df.count()
                }
                return lineage_info
        """,
        "data_quality_rules": """
            def apply_quality_rules(df, rules):
                for rule in rules:
                    if rule['type'] == 'not_null':
                        df = df.filter(col(rule['column']).isNotNull())
                    elif rule['type'] == 'range_check':
                        df = df.filter(
                            col(rule['column']).between(rule['min'], rule['max'])
                        )
                return df
        """,
        "cataloging": """
            # Register tables with metadata
            spark.sql('''
                CREATE TABLE IF NOT EXISTS data_catalog (
                    table_name STRING,
                    schema_json STRING,
                    created_date TIMESTAMP,
                    owner STRING,
                    description STRING
                )
            ''')
        """
    }
    
    return governance_framework

print("Q49 - Data lineage and governance")

# Question 50: Enterprise ETL architecture
def enterprise_etl_architecture():
    """Q50: How do you design an enterprise-grade ETL architecture with PySpark?"""
    architecture = {
        "layered_approach": {
            "bronze_layer": "Raw data ingestion with minimal transformations",
            "silver_layer": "Cleaned and validated data with business rules",
            "gold_layer": "Aggregated and business-ready analytics data"
        },
        "error_handling": """
            class ETLPipeline:
                def __init__(self, spark):
                    self.spark = spark
                    self.logger = self.setup_logging()
                
                def run_with_retry(self, operation, max_retries=3):
                    for attempt in range(max_retries):
                        try:
                            return operation()
                        except Exception as e:
                            if attempt == max_retries - 1:
                                self.logger.error(f"Operation failed after {max_retries} attempts: {e}")
                                raise
                            self.logger.warning(f"Attempt {attempt + 1} failed, retrying: {e}")
        """,
        "monitoring": """
            def setup_monitoring(spark):
                # Custom metrics
                spark.sparkContext.statusTracker()
                
                # Integration with monitoring systems
                spark.conf.set("spark.sql.streaming.metricsEnabled", "true")
                spark.conf.set("spark.metrics.conf.driver.source.jvm.class", 
                              "org.apache.spark.metrics.source.JvmSource")
        """,
        "configuration_management": """
            class ConfigManager:
                def __init__(self, env):
                    self.config = self.load_config(env)
                
                def get_spark_config(self):
                    return {
                        "spark.app.name": self.config['app_name'],
                        "spark.sql.adaptive.enabled": self.config['adaptive_query'],
                        "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
                    }
        """
    }
    
    return architecture

print("Q50 - Enterprise ETL architecture")

print("\n" + "="*80)
print("All 50 PySpark questions completed!")
print("Key areas covered:")
print("- DataFrames and RDD operations")
print("- Performance optimization")
print("- Streaming and real-time processing") 
print("- MLlib integration")
print("- Enterprise architecture patterns")
print("- Data governance and quality")
print("Ready for your PySpark data management interview!")
print("="*80)
