"""
10 Technical Delta Lake Interview Questions for Databricks
Focus: Delta Tables, Medallion Architecture, Data Pipelines
Ordered by ascending skill level (Beginner → Intermediate → Advanced)
Each question designed to be solved in under 5 minutes

Key Areas: Delta Lake operations, ACID transactions, Time Travel, 
Medallion Architecture, CDC, Data Quality, Performance Optimization

Author: Interview Preparation - Delta Lake Edition
Date: December 11, 2025
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, current_timestamp, to_timestamp, when, lit, coalesce, 
    sha2, concat, row_number, lag, lead, max as spark_max, 
    min as spark_min, count, sum as spark_sum, avg, stddev,
    split, regexp_replace, trim, upper, lower
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import delta

# Initialize Spark Session with Delta Lake support
def get_spark_session_with_delta():
    """Initialize Spark Session with Delta Lake configurations."""
    return SparkSession.builder \
        .appName("Delta Lake Interview Questions") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
        .getOrCreate()

print("Delta Lake Interview Questions - Databricks Focus")
print("="*60)

# =============================================================================
# BEGINNER LEVEL (Questions 1-3)
# =============================================================================

# Question 1: Create and write to Delta table
def create_delta_table(spark, data_path, table_path):
    """
    Q1: How do you create a Delta table and write data to it?
    
    Scenario: You need to create a new Delta table for customer data.
    """
    
    # Sample customer data
    customer_data = [
        (1, "Alice Johnson", "alice@email.com", "2023-01-15", "Premium"),
        (2, "Bob Smith", "bob@email.com", "2023-02-20", "Standard"),
        (3, "Charlie Brown", "charlie@email.com", "2023-03-10", "Premium"),
        (4, "Diana Wilson", "diana@email.com", "2023-04-05", "Standard")
    ]
    
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("registration_date", StringType(), True),
        StructField("tier", StringType(), True)
    ])
    
    df = spark.createDataFrame(customer_data, schema)
    
    # Write to Delta table
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .save(table_path)
    
    # Alternative: Save as managed table
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable("customers_delta")
    
    return df

print("Q1 - Create and write Delta table")

# Question 2: Read Delta table and basic operations
def read_delta_operations(spark, table_path):
    """
    Q2: How do you read from Delta table and perform basic operations?
    
    Scenario: Query customer data with filtering and aggregations.
    """
    
    # Read Delta table
    df = spark.read.format("delta").load(table_path)
    
    # Alternative: Read managed table
    df_managed = spark.table("customers_delta")
    
    # Basic operations
    premium_customers = df.filter(col("tier") == "Premium")
    
    customer_stats = df.groupBy("tier") \
        .agg(
            count("*").alias("customer_count"),
            spark_max("registration_date").alias("latest_registration")
        )
    
    # Show results
    df.show()
    premium_customers.show()
    customer_stats.show()
    
    return df, premium_customers, customer_stats

print("Q2 - Read Delta table and basic operations")

# Question 3: Delta table metadata and history
def delta_metadata_operations(spark, table_path):
    """
    Q3: How do you inspect Delta table metadata, schema, and history?
    
    Scenario: You need to understand table structure and track changes.
    """
    
    # Describe table structure
    spark.sql("DESCRIBE TABLE customers_delta").show()
    
    # Show table details
    spark.sql("DESCRIBE DETAIL customers_delta").show()
    
    # Show table history
    spark.sql("DESCRIBE HISTORY customers_delta").show()
    
    # Using Delta table API
    delta_table = DeltaTable.forPath(spark, table_path)
    
    # Get table history
    history_df = delta_table.history()
    history_df.show()
    
    # Show table properties
    spark.sql("SHOW TBLPROPERTIES customers_delta").show()
    
    return history_df

print("Q3 - Delta table metadata and history")

# =============================================================================
# INTERMEDIATE LEVEL (Questions 4-7)
# =============================================================================

# Question 4: Delta table MERGE operations (UPSERT)
def delta_merge_operations(spark, table_path):
    """
    Q4: How do you implement UPSERT operations using Delta MERGE?
    
    Scenario: Update existing customers and insert new ones in a single operation.
    """
    
    # New customer updates and additions
    updates_data = [
        (1, "Alice Johnson-Updated", "alice.new@email.com", "2023-01-15", "Premium"),
        (3, "Charlie Brown", "charlie.updated@email.com", "2023-03-10", "Gold"),
        (5, "Eve Davis", "eve@email.com", "2023-05-15", "Standard"),
        (6, "Frank Miller", "frank@email.com", "2023-06-01", "Premium")
    ]
    
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("registration_date", StringType(), True),
        StructField("tier", StringType(), True)
    ])
    
    updates_df = spark.createDataFrame(updates_data, schema)
    
    # Get existing Delta table
    delta_table = DeltaTable.forPath(spark, table_path)
    
    # Perform MERGE operation
    delta_table.alias("target") \
        .merge(
            updates_df.alias("source"),
            "target.customer_id = source.customer_id"
        ) \
        .whenMatchedUpdate(set={
            "name": "source.name",
            "email": "source.email",
            "tier": "source.tier"
        }) \
        .whenNotMatchedInsert(values={
            "customer_id": "source.customer_id",
            "name": "source.name",
            "email": "source.email",
            "registration_date": "source.registration_date",
            "tier": "source.tier"
        }) \
        .execute()
    
    # Alternative: SQL MERGE
    updates_df.createOrReplaceTempView("customer_updates")
    
    spark.sql("""
        MERGE INTO customers_delta target
        USING customer_updates source
        ON target.customer_id = source.customer_id
        WHEN MATCHED THEN
            UPDATE SET
                name = source.name,
                email = source.email,
                tier = source.tier
        WHEN NOT MATCHED THEN
            INSERT (customer_id, name, email, registration_date, tier)
            VALUES (source.customer_id, source.name, source.email, source.registration_date, source.tier)
    """)
    
    return delta_table

print("Q4 - Delta MERGE operations (UPSERT)")

# Question 5: Time Travel and versioning
def delta_time_travel(spark, table_path):
    """
    Q5: How do you implement time travel queries and version control?
    
    Scenario: Analyze data at different points in time and recover from mistakes.
    """
    
    # Time travel by version
    df_version_0 = spark.read.format("delta").option("versionAsOf", 0).load(table_path)
    df_version_1 = spark.read.format("delta").option("versionAsOf", 1).load(table_path)
    
    # Time travel by timestamp
    df_timestamp = spark.read.format("delta") \
        .option("timestampAsOf", "2023-06-01") \
        .load(table_path)
    
    # SQL time travel queries
    spark.sql("SELECT * FROM customers_delta VERSION AS OF 0").show()
    
    spark.sql("SELECT * FROM customers_delta TIMESTAMP AS OF '2023-06-01'").show()
    
    # Compare versions
    current_count = spark.table("customers_delta").count()
    previous_count = df_version_0.count()
    
    print(f"Current version count: {current_count}")
    print(f"Version 0 count: {previous_count}")
    print(f"Records added: {current_count - previous_count}")
    
    # Restore table to previous version (if needed)
    # spark.sql("RESTORE TABLE customers_delta TO VERSION AS OF 0")
    
    return df_version_0, df_version_1

print("Q5 - Time Travel and versioning")

# Question 6: Medallion Architecture Implementation
def medallion_architecture_pipeline(spark):
    """
    Q6: How do you implement a Medallion Architecture with Delta tables?
    
    Scenario: Build Bronze → Silver → Gold data pipeline for customer analytics.
    """
    
    # BRONZE LAYER - Raw data ingestion
    def create_bronze_layer(raw_data_path, bronze_path):
        """Ingest raw data with minimal transformations"""
        
        # Simulate raw JSON data ingestion
        raw_data = [
            ('{"customer_id": 1, "name": "Alice Johnson", "email": "alice@email.com", "signup_date": "2023-01-15", "tier": "premium", "source": "web"}',),
            ('{"customer_id": 2, "name": "Bob Smith", "email": "bob@email.com", "signup_date": "2023-02-20", "tier": "standard", "source": "mobile"}',),
            ('{"customer_id": 3, "name": "Charlie Brown", "email": "charlie@email.com", "signup_date": "2023-03-10", "tier": "premium", "source": "web"}',)
        ]
        
        raw_df = spark.createDataFrame(raw_data, ["raw_data"])
        
        # Add metadata columns for bronze layer
        bronze_df = raw_df \
            .withColumn("ingestion_timestamp", current_timestamp()) \
            .withColumn("source_file", lit("customers.json")) \
            .withColumn("data_quality", lit("raw"))
        
        # Write to bronze Delta table
        bronze_df.write \
            .format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .save(bronze_path)
        
        return bronze_df
    
    # SILVER LAYER - Cleaned and validated data
    def create_silver_layer(bronze_path, silver_path):
        """Transform and clean bronze data"""
        
        bronze_df = spark.read.format("delta").load(bronze_path)
        
        # Parse JSON and clean data
        from pyspark.sql.functions import from_json, col
        
        json_schema = StructType([
            StructField("customer_id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("signup_date", StringType(), True),
            StructField("tier", StringType(), True),
            StructField("source", StringType(), True)
        ])
        
        silver_df = bronze_df \
            .withColumn("parsed_data", from_json(col("raw_data"), json_schema)) \
            .select("parsed_data.*", "ingestion_timestamp") \
            .withColumn("tier_standardized", upper(col("tier"))) \
            .withColumn("email_domain", split(col("email"), "@").getItem(1)) \
            .withColumn("signup_date_clean", to_timestamp(col("signup_date"), "yyyy-MM-dd")) \
            .withColumn("data_quality", lit("validated"))
        
        # Data quality checks
        silver_clean = silver_df \
            .filter(col("customer_id").isNotNull()) \
            .filter(col("email").rlike("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")) \
            .dropDuplicates(["customer_id"])
        
        # Write to silver Delta table with optimization
        silver_clean.write \
            .format("delta") \
            .mode("overwrite") \
            .partitionBy("tier_standardized") \
            .save(silver_path)
        
        return silver_clean
    
    # GOLD LAYER - Business-ready aggregations
    def create_gold_layer(silver_path, gold_path):
        """Create business aggregations and metrics"""
        
        silver_df = spark.read.format("delta").load(silver_path)
        
        # Customer metrics by tier and source
        gold_df = silver_df \
            .groupBy("tier_standardized", "source", "email_domain") \
            .agg(
                count("*").alias("customer_count"),
                spark_min("signup_date_clean").alias("first_signup"),
                spark_max("signup_date_clean").alias("last_signup")
            ) \
            .withColumn("analysis_date", current_timestamp())
        
        # Write to gold Delta table
        gold_df.write \
            .format("delta") \
            .mode("overwrite") \
            .save(gold_path)
        
        return gold_df
    
    # Execute medallion pipeline
    bronze_path = "/tmp/bronze/customers"
    silver_path = "/tmp/silver/customers"
    gold_path = "/tmp/gold/customer_metrics"
    
    bronze_df = create_bronze_layer("/raw/customers", bronze_path)
    silver_df = create_silver_layer(bronze_path, silver_path)
    gold_df = create_gold_layer(silver_path, gold_path)
    
    print("✅ Medallion Architecture Pipeline Completed")
    print(f"Bronze records: {bronze_df.count()}")
    print(f"Silver records: {silver_df.count()}")
    print(f"Gold records: {gold_df.count()}")
    
    return bronze_df, silver_df, gold_df

print("Q6 - Medallion Architecture Implementation")

# Question 7: Change Data Capture (CDC) with Delta
def implement_cdc_pipeline(spark):
    """
    Q7: How do you implement Change Data Capture (CDC) with Delta tables?
    
    Scenario: Track and apply incremental changes from source systems.
    """
    
    # Create initial customer table
    initial_data = [
        (1, "Alice", "alice@email.com", "2023-01-15", "active", 1, "insert"),
        (2, "Bob", "bob@email.com", "2023-02-20", "active", 1, "insert"),
        (3, "Charlie", "charlie@email.com", "2023-03-10", "active", 1, "insert")
    ]
    
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("signup_date", StringType(), True),
        StructField("status", StringType(), True),
        StructField("version", IntegerType(), True),
        StructField("operation", StringType(), True)
    ])
    
    initial_df = spark.createDataFrame(initial_data, schema) \
        .withColumn("processed_timestamp", current_timestamp())
    
    # Create target table
    target_path = "/tmp/cdc_target/customers"
    initial_df.write.format("delta").mode("overwrite").save(target_path)
    
    # Simulate CDC changes
    cdc_changes = [
        (1, "Alice Johnson", "alice.new@email.com", "2023-01-15", "active", 2, "update"),
        (2, "Bob Smith", "bob@email.com", "2023-02-20", "inactive", 2, "update"),
        (4, "Diana", "diana@email.com", "2023-04-01", "active", 1, "insert"),
        (3, "Charlie Brown", "charlie@email.com", "2023-03-10", "deleted", 2, "delete")
    ]
    
    cdc_df = spark.createDataFrame(cdc_changes, schema) \
        .withColumn("processed_timestamp", current_timestamp())
    
    # Apply CDC changes using MERGE
    delta_table = DeltaTable.forPath(spark, target_path)
    
    # Get the latest version for each customer_id from CDC
    window = Window.partitionBy("customer_id").orderBy(col("version").desc())
    latest_cdc = cdc_df.withColumn("rn", row_number().over(window)) \
        .filter(col("rn") == 1).drop("rn")
    
    # Apply CDC using MERGE
    delta_table.alias("target") \
        .merge(
            latest_cdc.alias("cdc"),
            "target.customer_id = cdc.customer_id"
        ) \
        .whenMatchedUpdate(
            condition="cdc.operation = 'update' AND cdc.version > target.version",
            set={
                "name": "cdc.name",
                "email": "cdc.email",
                "status": "cdc.status",
                "version": "cdc.version",
                "processed_timestamp": "cdc.processed_timestamp"
            }
        ) \
        .whenMatchedDelete(condition="cdc.operation = 'delete'") \
        .whenNotMatchedInsert(
            condition="cdc.operation = 'insert'",
            values={
                "customer_id": "cdc.customer_id",
                "name": "cdc.name",
                "email": "cdc.email",
                "signup_date": "cdc.signup_date",
                "status": "cdc.status",
                "version": "cdc.version",
                "operation": "cdc.operation",
                "processed_timestamp": "cdc.processed_timestamp"
            }
        ) \
        .execute()
    
    # Show final result
    final_df = spark.read.format("delta").load(target_path)
    final_df.show()
    
    return final_df

print("Q7 - Change Data Capture (CDC) implementation")

# =============================================================================
# ADVANCED LEVEL (Questions 8-10)
# =============================================================================

# Question 8: Delta table optimization and performance tuning
def delta_optimization_strategies(spark, table_path):
    """
    Q8: How do you optimize Delta table performance for large-scale operations?
    
    Scenario: Optimize a large customer table for better query performance.
    """
    
    # 1. OPTIMIZE command for file compaction
    spark.sql("OPTIMIZE customers_delta")
    
    # 2. Z-ORDER optimization for better data skipping
    spark.sql("OPTIMIZE customers_delta ZORDER BY (tier, registration_date)")
    
    # 3. Table properties optimization
    spark.sql("""
        ALTER TABLE customers_delta SET TBLPROPERTIES (
            'delta.autoOptimize.optimizeWrite' = 'true',
            'delta.autoOptimize.autoCompact' = 'true',
            'delta.dataSkippingStatsColumns' = 'tier,registration_date',
            'delta.deletedFileRetentionDuration' = 'interval 7 days'
        )
    """)
    
    # 4. Partition optimization
    def repartition_by_business_logic(df, partition_cols):
        return df.repartition(*partition_cols)
    
    # 5. Bloom filter optimization for high-cardinality columns
    spark.sql("""
        ALTER TABLE customers_delta SET TBLPROPERTIES (
            'delta.bloomFilter.email' = 'true',
            'delta.bloomFilter.email.fpp' = '0.1'
        )
    """)
    
    # 6. Data skipping statistics
    spark.sql("ANALYZE TABLE customers_delta COMPUTE STATISTICS FOR ALL COLUMNS")
    
    # 7. Vacuum old files (be careful in production)
    spark.sql("VACUUM customers_delta RETAIN 168 HOURS")  # 7 days
    
    # Performance monitoring
    stats = spark.sql("DESCRIBE DETAIL customers_delta").collect()[0]
    print(f"Table size: {stats['sizeInBytes']} bytes")
    print(f"Number of files: {stats['numFiles']}")
    
    return stats

print("Q8 - Delta table optimization and performance tuning")

# Question 9: Advanced streaming with Delta tables
def delta_streaming_pipeline(spark):
    """
    Q9: How do you implement real-time streaming pipelines with Delta tables?
    
    Scenario: Process real-time customer events and maintain Delta tables.
    """
    
    # Create streaming source simulation
    def create_streaming_source():
        # Simulate streaming data generation
        streaming_data = [
            ("2023-06-01 10:00:00", 1, "login", "web"),
            ("2023-06-01 10:05:00", 1, "purchase", "mobile"),
            ("2023-06-01 10:10:00", 2, "login", "web"),
            ("2023-06-01 10:15:00", 3, "logout", "web"),
        ]
        
        streaming_df = spark.createDataFrame(streaming_data, 
            ["timestamp", "customer_id", "event_type", "channel"])
        
        return streaming_df
    
    # Streaming pipeline with Delta sink
    def process_streaming_events():
        
        # Read stream (in practice, this would be from Kafka, Kinesis, etc.)
        # stream_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").load()
        
        # For demo, create a streaming DataFrame from memory
        streaming_df = create_streaming_source()
        
        # Add processing timestamp and event ID
        processed_df = streaming_df \
            .withColumn("processing_time", current_timestamp()) \
            .withColumn("event_id", sha2(concat(col("timestamp"), col("customer_id"), col("event_type")), 256))
        
        # Write to Delta table with streaming
        delta_stream_path = "/tmp/streaming/customer_events"
        
        # In a real streaming scenario:
        # query = processed_df.writeStream \
        #     .format("delta") \
        #     .outputMode("append") \
        #     .option("checkpointLocation", "/tmp/checkpoint/customer_events") \
        #     .trigger(processingTime="10 seconds") \
        #     .start(delta_stream_path)
        
        # For demo, write batch
        processed_df.write.format("delta").mode("overwrite").save(delta_stream_path)
        
        return processed_df
    
    # Real-time aggregations with Delta
    def create_realtime_aggregations(events_path):
        events_df = spark.read.format("delta").load(events_path)
        
        # Customer activity summary
        activity_summary = events_df \
            .groupBy("customer_id", "event_type") \
            .agg(count("*").alias("event_count")) \
            .withColumn("summary_timestamp", current_timestamp())
        
        # Write aggregations to Delta
        summary_path = "/tmp/streaming/customer_activity_summary"
        activity_summary.write.format("delta").mode("overwrite").save(summary_path)
        
        return activity_summary
    
    # Execute streaming pipeline
    events_df = process_streaming_events()
    summary_df = create_realtime_aggregations("/tmp/streaming/customer_events")
    
    print("✅ Streaming pipeline with Delta tables completed")
    events_df.show()
    summary_df.show()
    
    return events_df, summary_df

print("Q9 - Advanced streaming with Delta tables")

# Question 10: Enterprise Delta Lake governance and monitoring
def enterprise_delta_governance(spark):
    """
    Q10: How do you implement enterprise-grade governance, monitoring, and data lineage with Delta?
    
    Scenario: Build comprehensive data governance framework for Delta Lake.
    """
    
    # 1. Data lineage tracking
    def track_data_lineage(source_table, target_table, transformation, user):
        lineage_data = [(
            source_table,
            target_table,
            transformation,
            user,
            current_timestamp()
        )]
        
        lineage_schema = StructType([
            StructField("source_table", StringType(), True),
            StructField("target_table", StringType(), True),
            StructField("transformation", StringType(), True),
            StructField("user", StringType(), True),
            StructField("execution_time", TimestampType(), True)
        ])
        
        lineage_df = spark.createDataFrame(lineage_data, lineage_schema)
        
        # Store lineage in Delta table
        lineage_df.write.format("delta").mode("append").saveAsTable("data_lineage")
        
        return lineage_df
    
    # 2. Data quality monitoring
    def implement_data_quality_framework(table_name):
        
        # Define quality rules
        quality_rules = {
            "null_check": "customer_id IS NOT NULL",
            "email_format": "email RLIKE '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}$'",
            "tier_values": "tier IN ('Standard', 'Premium', 'Gold')",
            "date_range": "registration_date >= '2020-01-01'"
        }
        
        df = spark.table(table_name)
        quality_results = []
        
        for rule_name, rule_condition in quality_rules.items():
            total_records = df.count()
            valid_records = df.filter(rule_condition).count()
            quality_score = valid_records / total_records if total_records > 0 else 0
            
            quality_results.append((
                table_name,
                rule_name,
                rule_condition,
                total_records,
                valid_records,
                quality_score,
                current_timestamp()
            ))
        
        quality_schema = StructType([
            StructField("table_name", StringType(), True),
            StructField("rule_name", StringType(), True),
            StructField("rule_condition", StringType(), True),
            StructField("total_records", IntegerType(), True),
            StructField("valid_records", IntegerType(), True),
            StructField("quality_score", DoubleType(), True),
            StructField("check_timestamp", TimestampType(), True)
        ])
        
        quality_df = spark.createDataFrame(quality_results, quality_schema)
        
        # Store quality metrics
        quality_df.write.format("delta").mode("append").saveAsTable("data_quality_metrics")
        
        return quality_df
    
    # 3. Access control and auditing
    def setup_access_control():
        
        # Row-level security example
        spark.sql("""
            CREATE OR REPLACE FUNCTION mask_email(email STRING)
            RETURNS STRING
            LANGUAGE SQL
            AS '
                CASE 
                    WHEN current_user() LIKE "%admin%" THEN email
                    ELSE regexp_replace(email, "(.{2}).*(@.*)", "$1***$2")
                END
            '
        """)
        
        # Column-level security view
        spark.sql("""
            CREATE OR REPLACE VIEW customers_secure AS
            SELECT 
                customer_id,
                name,
                mask_email(email) as email,
                registration_date,
                tier
            FROM customers_delta
        """)
        
        return "Access control configured"
    
    # 4. Performance monitoring
    def monitor_delta_performance():
        
        # Query performance metrics
        metrics_query = """
            SELECT 
                table_name,
                operation,
                COUNT(*) as operation_count,
                AVG(execution_time_ms) as avg_execution_time,
                MAX(execution_time_ms) as max_execution_time,
                SUM(rows_processed) as total_rows_processed
            FROM delta_log_performance  -- This would be a system table in practice
            WHERE date >= current_date() - interval 7 days
            GROUP BY table_name, operation
        """
        
        # In practice, you'd query actual Delta metrics
        performance_data = [
            ("customers_delta", "SELECT", 150, 120.5, 500, 1000000),
            ("customers_delta", "MERGE", 25, 2500.0, 5000, 50000),
            ("customers_delta", "OPTIMIZE", 5, 10000.0, 15000, 1000000)
        ]
        
        performance_schema = StructType([
            StructField("table_name", StringType(), True),
            StructField("operation", StringType(), True),
            StructField("operation_count", IntegerType(), True),
            StructField("avg_execution_time", DoubleType(), True),
            StructField("max_execution_time", DoubleType(), True),
            StructField("total_rows_processed", IntegerType(), True)
        ])
        
        performance_df = spark.createDataFrame(performance_data, performance_schema)
        
        return performance_df
    
    # 5. Automated maintenance
    def setup_automated_maintenance():
        
        maintenance_commands = {
            "daily_optimize": "OPTIMIZE customers_delta ZORDER BY (tier)",
            "weekly_vacuum": "VACUUM customers_delta RETAIN 168 HOURS",
            "monthly_stats": "ANALYZE TABLE customers_delta COMPUTE STATISTICS FOR ALL COLUMNS"
        }
        
        # In practice, these would be scheduled jobs
        for job_name, command in maintenance_commands.items():
            print(f"Scheduled job: {job_name} -> {command}")
        
        return maintenance_commands
    
    # Execute governance framework
    lineage = track_data_lineage("source.customers", "customers_delta", "data_ingestion", "data_engineer")
    quality_metrics = implement_data_quality_framework("customers_delta")
    access_control = setup_access_control()
    performance_metrics = monitor_delta_performance()
    maintenance_jobs = setup_automated_maintenance()
    
    print("✅ Enterprise Delta Lake governance framework implemented")
    print("Components:")
    print("- Data lineage tracking")
    print("- Data quality monitoring")
    print("- Access control and security")
    print("- Performance monitoring")
    print("- Automated maintenance")
    
    lineage.show()
    quality_metrics.show()
    performance_metrics.show()
    
    return {
        "lineage": lineage,
        "quality_metrics": quality_metrics,
        "access_control": access_control,
        "performance_metrics": performance_metrics,
        "maintenance_jobs": maintenance_jobs
    }

print("Q10 - Enterprise Delta Lake governance and monitoring")

print("\n" + "="*80)
print("All 10 Delta Lake questions completed!")
print("\nKey areas covered:")
print("✅ Delta table creation and basic operations")
print("✅ MERGE operations and UPSERT patterns")
print("✅ Time travel and version control")
print("✅ Medallion Architecture (Bronze-Silver-Gold)")
print("✅ Change Data Capture (CDC) pipelines")
print("✅ Performance optimization strategies")
print("✅ Real-time streaming with Delta")
print("✅ Enterprise governance and monitoring")
print("\nReady for your Delta Lake/Databricks interview!")
print("="*80)
