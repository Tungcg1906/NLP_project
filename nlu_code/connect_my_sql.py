import mysql.connector
from nlu_custom_model import CustomBertModel
from nlu_pretrained_model import OpenIEExtractor

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

# Create a table to store predictions if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sentence TEXT,
    custom_bert_prediction VARCHAR(255),
    openie_prediction VARCHAR(255)
);
"""
cursor.execute(create_table_query)
connection.commit()

# Store predictions in the database
def store_predictions(sentence, custom_bert_prediction, openie_prediction):
    insert_query = "INSERT INTO predictions (sentence, custom_bert_prediction, openie_prediction) VALUES (%s, %s, %s)"
    values = (sentence, custom_bert_prediction, openie_prediction)
    cursor.execute(insert_query, values)
    connection.commit()

# Example usage
obj1 = OpenIEExtractor()
obj2 = CustomBertModel(model_name="bert-base-uncased", num_labels=4, checkpoint_path='version_0/checkpoints/epoch=1-step=356.ckpt')

sentence = "Elon Musk was born in South Africa." 
prediction1 = obj1.extract_relations(sentence)
prediction2 = obj2.predict_relation(sentence)

store_predictions(sentence, prediction2, prediction1)

# Close the cursor and connection when you're done
cursor.close()
connection.close()