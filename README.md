# NLU R&D Orcawise Project

Nature Language Understanding research & development project is developed by [Orcawise](https://www.orcawise.com/) NLP team, which focus on uncovering named entity relations (NER) within the data, leading to the extraction of valuable insights and knowledge. We achieve this by employing both a pre-trained model (StanfordOpenIE) and a custom fine-tuned model (CustomBertModel). Our primary goal is to extract relations from sentences, specifically targeting four key relationships: managerOf, employedBy, locatedAt, and noRelation.

## Table of Contents
  - [Preprocess the data](#preprocess-the-data)
  - [Pretrained OpenIE Model](#pretrained-openie-model)
  - [Custom BERT Model](#custom-bert-model)
  - [Database](#database)
  - [How to Run the Code](#how-to-run-the-code)
    

## Preprocess the data

The data collection process involves web scraping, followed by annotation using Doccano to extract information pertaining to entities such as PERSON, ORG, and GPE within sentences. Subsequently, the annotated data can be processed using `doccano_into_csv.py` to convert the JSONL file into a CSV format. This is followed by the execution of `Class_final_code_cleaning.py`, `augment_cleaned.py` and  `Combination_spin_class.py` to produce the final dataset for training the model.


##  Pretrained OpenIE Model

- **Name:** Stanford OpenIE
- **Description:** The pretrained OpenIE model is based on Stanford's OpenIE library. It extracts relations from input text using natural language processing techniques.
- **Diagram:**
  
 ![Diagram](Diagram/stanford.png)

##  Custom BERT Model

- **Name:** Custom BERT Model
- **Description:** The custom BERT model is fine-tuned for relation classification. It uses the 'bert-base-uncased' pretrained model and has four labels: 'noRelation', 'employedBy', 'managerOf', and 'locatedAt'.
- **Diagram:**
 ![Diagram](Diagram/NLU_diag.png)

## Database

- **Database Used:** MySQL
- **Description:** Open-source relational database management system, widely used for its reliability and scalability. Supports SQL, making it a popular choice for web applications and software projects.

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

2. **Custom BERT Model:**
    - Run the `nlu_custom_model.py` file to initialize and use the Custom BERT model.

    ```python
    from nlu_custom_model import CustomBertModel

    obj2 = CustomBertModel(model_name="bert-base-uncased", num_labels=4, checkpoint_path='path/to/your/checkpoint.ckpt')
    sentence = 'The Colosseum is an ancient amphitheater in Rome.'
    predicted_relation = obj2.predict_relation(sentence)
    print(f"Predicted Relation: {predicted_relation}")
    ```

3. **Connect to database:**
    - **Database Used:** MySQL
    - **Connection from Python with Database:**
        - The database connection is established using the `mysql.connector` library.
        - Connection details:
            - Host: localhost
            - Port: 3306
            - User: root
            - Password: [Password]
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

    Make sure to replace placeholders such as 'path/to/your/checkpoint.ckpt' and '[Password]' with the actual paths and passwords.
4. **Testing model with real-time data:**
    - Run the jupyter notebook `testing_custom_bert_on_real_time_data.ipynb` file to generalize the result of openie and the calculate the accuracy of the models' results.

    ```python
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Get the sentence from the 'sentence' column
        sentence = row['sentence']

        # Predict the relation for the current sentence
        predicted_relation = obj.predict_relation(sentence)
        predicted_relation1 = obj1.predict_relation(sentence)
        predicted_relation2 = obj2.extract_relations(sentence)
        
    
        # Append the predicted relation to the list
        predictions.append(predicted_relation)
        predictions1.append(predicted_relation1)
        predictions2.append(predicted_relation2)
    
        # Compare the predicted relation with the 'ground_truth' column
        ground_truth = row['ground_truth']
        accuracy = 1 if predicted_relation == ground_truth else 0
        accuracy1 = 1 if predicted_relation1 == ground_truth else 0
    
    
        # Append the accuracy value to the list
        accuracy_values.append(accuracy)
        accuracy_values1.append(accuracy1)

    ```   





