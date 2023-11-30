# NLU Orcawise Project
NLU project is developed by [Orcawise](https://www.orcawise.com/) NLP team, which focus on uncovering named entity relations (NER) within the data, leading to the extraction of valuable insights and knowledge. We achieve this by employing both a pre-defined model (StanfordOpenIE) and a fine-tuned model (CustomBertModel). Our primary goal is to extract relations from sentences, specifically targeting four key relationships: managerOf, employedBy, locatedAt, and noRelation.


##  Pretrained OpenIE Model

- **Name:** Stanford OpenIE
- **Description:** The pretrained OpenIE model is based on Stanford's OpenIE library. It extracts relations from input text using natural language processing techniques.

##  Custom BERT Model

- **Name:** Custom BERT Model
- **Description:** The custom BERT model is fine-tuned for relation classification. It uses the 'bert-base-uncased' pretrained model and has four labels: 'noRelation', 'employedBy', 'managerOf', and 'locatedAt'.
- **Diagram:**
 ![Diagram](Diagram/Custom_code_diagram.drawio.png)

## How to Run the Code

1. **Pretrained OpenIE Model:**
    - Install the requirement library `pip install OpenIE`
    - Install [Java](http://jdk.javTa.net/archive/) in windows.
    - Clone the [core NLP model](https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip) and unzip it. Then set the path to unzipped file in environment variables.
    - Run the `nlu_pretrained_model.py` file to initialize and use the OpenIE model.

    ```python
    from nlu_pretrained_model import OpenIEExtractor

    obj1 = OpenIEExtractor()
    text = 'Barack Obama was born in Hawaii.'
    prediction1 = obj1.extract_relations(text)
    print(f"Predicted Relation: {prediction1}")
    ```

3. **Custom BERT Model:**
    - Run the `nlu_custom_model.py` file to initialize and use the Custom BERT model.

    ```python
    from nlu_custom_model import CustomBertModel

    obj2 = CustomBertModel(model_name="bert-base-uncased", num_labels=4, checkpoint_path='path/to/your/checkpoint.ckpt')
    sentence = 'The Colosseum is an ancient amphitheater in Rome.'
    predicted_relation = obj2.predict_relation(sentence)
    print(f"Predicted Relation: {predicted_relation}")
    ```

## Database

- **Database Used:** MySQL
- **Connection from Python with Database:**
    - The database connection is established using the `mysql.connector` library.
    - Connection details:
        - Host: localhost
        - Port: 3306
        - User: root
        - Password: [YourPassword]
        - Database: test_nlu
- **How to Execute the Code:**
    - Run the `connect_my_sql.py` file to connect to the database, create a table, store predictions, and close the connection.

    ```python
    # Example usage
    obj1 = OpenIEExtractor()
    obj2 = CustomBertModel(model_name="bert-base-uncased", num_labels=4, checkpoint_path='path/to/your/checkpoint.ckpt')

    sentence = "Finland is often referred to as the 'Land of a Thousand Lakes', but in reality, it has over 188,000 lakes."
    prediction1 = obj1.extract_relations(sentence)
    prediction2 = obj2.predict_relation(sentence)

    store_predictions(sentence, prediction2, prediction1)
    ```

Make sure to replace placeholders such as 'path/to/your/checkpoint.ckpt' and '[YourPassword]' with the actual paths and passwords.


