import torch
import random
import torchmetrics
import numpy as np
from transformers import BertTokenizer
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertForSequenceClassification

class CustomBertModel:
    def __init__(self, model_name, num_labels=4, max_length=213, checkpoint_path=None):
        # Set random seed
        seed_value = 46
        random.seed(seed_value)
        np.random.seed(seed_value)
        torch.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)

        self.tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=True)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # Initialize a new model if checkpoint_path is not provided
        if checkpoint_path:
            self.load_checkpoint(checkpoint_path, model_name, num_labels, strict = False)
        else:
            self.model = None  # Set model to None if no checkpoint path is provided

    def encode_sentence(self, sentence):
        encoded_dict = self.tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=213,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        # Convert the dictionary into a TensorDataset
        return TensorDataset(encoded_dict['input_ids'], encoded_dict['attention_mask'])

    def load_checkpoint(self, checkpoint_path, model_name, num_labels, strict=False):
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.load_state_dict(checkpoint, strict=strict)
        self.model.to(self.device)
        self.model.eval()

    def predict_relation(self, sentence):
        if self.model is None:
            print("Error: Model has not been initialized. Provide a checkpoint_path during initialization.")
            return None

        input_data = self.encode_sentence(sentence)
        # Move input data to the device
        input_ids = input_data.tensors[0].to(self.device)
        attention_mask = input_data.tensors[1].to(self.device)
        # Make predictions
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
        # Get the predicted class
        _, predicted_class = torch.max(outputs.logits, 1)
        # Map the predicted class to the corresponding relation
        relation_mapping = {3: 'noRelation', 2: 'employedBy', 0: 'managerOf', 1: 'locatedAt'}
        predicted_relation = relation_mapping[predicted_class.item()]

        return predicted_relation

# Example:
obj2 = CustomBertModel(model_name="bert-base-uncased", num_labels=4, checkpoint_path='version_0/checkpoints/epoch=1-step=356.ckpt')
#sentence = 'Marie Curie was a pioneer in the field of radioactivity.'
#sentence='Amazon CEO Jeff Bezos stepped down from his position.'
#sentence='Albert Einstein developed the theory of relativity.'
sentence = 'The Colosseum is an ancient amphitheater in Rome.'
predicted_relation = obj2.predict_relation(sentence)
print(f"Predicted Relation: {predicted_relation}")