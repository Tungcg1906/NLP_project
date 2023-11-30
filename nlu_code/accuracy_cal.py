import mysql.connector

def update_acc_pre_column():
    # Establishing connection to MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='Dkmm12356@',
        database='test_nlu'
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Check if the 'ACC_PRE' column exists
    check_column_query = """
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_name = 'predictions' AND column_name = 'ACC_PRE';
    """
    cursor.execute(check_column_query)
    column_exists = cursor.fetchone()[0]

    # If 'ACC_PRE' does not exist, add the column
    if not column_exists:
        add_column_query = """
        ALTER TABLE predictions
        ADD COLUMN ACC_PRE VARCHAR(255);
        """
        cursor.execute(add_column_query)
        connection.commit()

    # Update values in the 'ACC_PRE' column based on conditions
    update_query = """
        UPDATE predictions
        SET ACC_PRE = 
            CASE
                WHEN TRIM(openie_prediction) = 'is' THEN 'managerOf'
                WHEN TRIM(openie_prediction) = 'was' THEN 'managerOf'
                WHEN openie_prediction LIKE '% is %' AND openie_prediction LIKE '% in %' THEN 'locatedAt' 
                WHEN openie_prediction LIKE '%located%' THEN 'locatedAt'
                WHEN openie_prediction LIKE 'is %' THEN 'employedBy'
                WHEN openie_prediction LIKE 'was %' THEN 'employedBy'
                WHEN openie_prediction IS NULL THEN 'noRelation'
                ELSE 'managerOf'
            END;
    """
    cursor.execute(update_query)
    connection.commit()

    # Add the columns 'acc_custom' and 'acc_pretrained' to the table run only once to create the column
    # add_acc_columns_query = """
    #     ALTER TABLE predictions
    #     ADD COLUMN acc_custom INT,
    #     ADD COLUMN acc_pretrained INT;
    # """
    # cursor.execute(add_acc_columns_query)
    # connection.commit()

    # Update values in the new columns based on accuracy conditions
    update_acc_columns_query = """
        UPDATE predictions
        SET acc_custom = CASE WHEN ground_truth = custom_bert_prediction THEN 1 ELSE 0 END,
            acc_pretrained = CASE WHEN ground_truth = ACC_PRE THEN 1 ELSE 0 END;
    """
    cursor.execute(update_acc_columns_query)
    connection.commit()

    # Output the accuracy results
    accuracy_query = """
        SELECT
            id,
            sentence,
            custom_bert_prediction,
            openie_prediction,
            ground_truth,
            ACC_PRE,
            acc_custom,
            acc_pretrained
        FROM
            predictions;
    """
    cursor.execute(accuracy_query)
    accuracy_results = cursor.fetchall()

    for row in accuracy_results:
        print(row)

    # Calculate and print accuracy
    total_rows = len(accuracy_results)
    acc_custom_total = sum(row[6] for row in accuracy_results)
    acc_pretrained_total = sum(row[7] for row in accuracy_results)

    acc_custom_accuracy = acc_custom_total / total_rows if total_rows > 0 else 0
    acc_pretrained_accuracy = acc_pretrained_total / total_rows if total_rows > 0 else 0

    print(f"Accuracy for acc_custom: {acc_custom_accuracy:.2%}")
    print(f"Accuracy for acc_pretrained: {acc_pretrained_accuracy:.2%}")

    # Close the database connection
    cursor.close()
    connection.close()

# Call the function to update the 'ACC_PRE' column, add new columns, and calculate accuracy
update_acc_pre_column()
