import mysql.connector
from collections import Counter


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

    # Check if the 'openie_generlize' column exists
    check_column_query = """
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_name = 'nlu_table' AND column_name = 'openie_generlize';
    """
    cursor.execute(check_column_query)
    column_exists = cursor.fetchone()[0]

    # If 'openie_generlize' does not exist, add the column
    if not column_exists:
        add_column_query = """
        ALTER TABLE nlu_table
        ADD COLUMN openie_generlize VARCHAR(255);
        """
        cursor.execute(add_column_query)
        connection.commit()

    # Update values in the 'openie_generalize' column based on conditions
    update_query = """
        UPDATE nlu_table
        SET openie_generlize = 
            CASE
                WHEN openie_prediction LIKE '%CEO%' THEN 'managerOf'
                WHEN openie_prediction LIKE '%head%' THEN 'managerOf'
                WHEN openie_prediction LIKE '%founder%' THEN 'managerOf'
                WHEN openie_prediction LIKE '%CFO%' THEN 'managerOf'
                WHEN openie_prediction LIKE 'worked %' THEN 'employedBy'
                WHEN openie_prediction LIKE 'works%' THEN 'employedBy'
                WHEN openie_prediction LIKE 'work%' THEN 'employedBy'
                WHEN openie_prediction LIKE 'working%' THEN 'employedBy'
                WHEN openie_prediction LIKE 'was employed%' THEN 'employedBy'
                WHEN openie_prediction LIKE 'employed%' THEN 'employedBy'
                WHEN openie_prediction LIKE 'hired%' THEN 'employedBy'
                WHEN openie_prediction LIKE 'served%' THEN 'employedBy'
                WHEN openie_prediction LIKE '%located%' THEN 'locatedAt'
                WHEN openie_prediction LIKE '%is in%' THEN 'locatedAt'
                WHEN openie_prediction IS NULL THEN 'noRelation'
                ELSE 'noRelation'
            END;
    """
    cursor.execute(update_query)
    connection.commit()

    # # Add the columns 'acc_custom' and 'acc_pretrained' to the table run only once to create the column
    # add_acc_columns_query = """
    #     ALTER TABLE nlu_table
    #     ADD COLUMN acc_custom INT,
    #     ADD COLUMN acc_pretrained INT;
    # """
    # cursor.execute(add_acc_columns_query)
    # connection.commit()

    # Update values in the new columns based on accuracy conditions
    update_acc_columns_query = """
        UPDATE nlu_table
        SET acc_custom = CASE WHEN ground_truth = custom_bert_prediction THEN 1 ELSE 0 END,
            acc_pretrained = CASE WHEN ground_truth = openie_generlize THEN 1 ELSE 0 END;
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
            openie_generlize,
            acc_custom,
            acc_pretrained
        FROM
            nlu_table;
    """
    cursor.execute(accuracy_query)
    accuracy_results = cursor.fetchall()

    ## Print table
    # for row in accuracy_results:
    #     print(row)

    # Find total number of each label in ground_truth
    ground_truth_values = [row[4] for row in accuracy_results]
    count_per_category = Counter(ground_truth_values)
    divisor_noRelation = count_per_category.get('noRelation', 1)
    divisor_managerOf = count_per_category.get('managerOf', 1)
    divisor_employedBy = count_per_category.get('employedBy', 1)
    divisor_locatedAt = count_per_category.get('locatedAt', 1)
    print(f"Total number of each label: {count_per_category}")
    print(divisor_noRelation, divisor_managerOf, divisor_employedBy, divisor_locatedAt)
    

    # Calculate and print the total accuracy
    total_rows = len(accuracy_results)
    acc_custom_total = sum(row[6] for row in accuracy_results)
    acc_pretrained_total = sum(row[7] for row in accuracy_results)

    acc_custom_accuracy = acc_custom_total / total_rows if total_rows > 0 else 0
    acc_pretrained_accuracy = acc_pretrained_total / total_rows if total_rows > 0 else 0

    print(f"Total accuracy for acc_custom: {acc_custom_accuracy:.2%}")
    print(f"Total accuracy for acc_pretrained: {acc_pretrained_accuracy:.2%}")

    # Calculate and print the specific accuracy
    # acc_custom
    acc_custom_noRelation = sum(1 for row in accuracy_results if row[6] == 1 and row[4] == 'noRelation')
    acc_custom_employedBy = sum(1 for row in accuracy_results if row[6] == 1 and row[4] == 'employedBy')
    acc_custom_managerOf = sum(1 for row in accuracy_results if row[6] == 1 and row[4] == 'managerOf')
    acc_custom_locatedAt = sum(1 for row in accuracy_results if row[6] == 1 and row[4] == 'locatedAt')
    specific_noRelation = (acc_custom_noRelation/divisor_noRelation) 
    specific_employedBy = (acc_custom_employedBy/divisor_employedBy) 
    specific_managerOf = (acc_custom_managerOf/divisor_managerOf) 
    specific_locatedAt = (acc_custom_locatedAt/divisor_locatedAt) 
    print(f"Specific accuracy for acc_custom: ('noRelation':{specific_noRelation:.2%}, 'employedBy':{specific_employedBy:.2%}, 'managerOf':{specific_managerOf:.2%}, 'locatedAt':{specific_locatedAt:.2%})")
    
    # acc_pretrained
    acc_pretrained_noRelation = sum(1 for row in accuracy_results if row[7] == 1 and row[4] == 'noRelation')
    acc_pretrained_employedBy = sum(1 for row in accuracy_results if row[7] == 1 and row[4] == 'employedBy')
    acc_pretrained_managerOf = sum(1 for row in accuracy_results if row[7] == 1 and row[4] == 'managerOf')
    acc_pretrained_locatedAt = sum(1 for row in accuracy_results if row[7] == 1 and row[4] == 'locatedAt')
    specific_noRelation_pre = (acc_pretrained_noRelation/divisor_noRelation) 
    specific_employedBy_pre = (acc_pretrained_employedBy/divisor_employedBy) 
    specific_managerOf_pre = (acc_pretrained_managerOf/divisor_managerOf) 
    specific_locatedAt_pre = (acc_pretrained_locatedAt/divisor_locatedAt) 
    print(f"Specific accuracy for acc_pretrained: ('noRelation':{specific_noRelation_pre:.2%}, 'employedBy':{specific_employedBy_pre:.2%}, 'managerOf':{specific_managerOf_pre:.2%}, 'locatedAt':{specific_locatedAt_pre:.2%})")



# Call the function to update the 'openie_generlize,' column, add new columns, and calculate accuracy
update_acc_pre_column()



'''
# Find the total numbers of labels
SELECT ground_truth, COUNT(*) AS count_per_category
FROM nlu_table
GROUP BY ground_truth;
'''
