import os
import sys
from InsurancePremiumPrediction.exception import CustomException
from InsurancePremiumPrediction.logger import logging
import pandas as pd
from InsurancePremiumPrediction.utils import *

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from InsurancePremiumPrediction.components.data_transformation import DataTransformation
from InsurancePremiumPrediction.components.data_transformation import DataTransformationConfig

from InsurancePremiumPrediction.components.model_trainer import ModelTrainerConfig
from InsurancePremiumPrediction.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data ingestion phase.")
        try:
            df = pd.read_csv("E:\\Projects\\Insurance-Premium-Prediction\\Data\\insurance.csv")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))