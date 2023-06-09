import os, sys
import shutil
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import DataValidationConfig
from signLanguage.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact


class DataValidation:
    def __init__(self, 
                 data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise SignException(e, sys)
        
    
    def validate_all_files_exist(self)->bool:
        try:
            validation_status = None

            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            for file in all_files:
                if file not in self.data_validation_config.required_file_list:
                    validation_status = False
                else:
                    validation_status = True

            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                f.write(f"Validation status : {validation_status}")

            return validation_status

        except Exception as e:
            raise SignException(e, sys)
        

    def initiate_data_validation(self):
        logging.info("Initiating data validation")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(validation_status=status)

            logging.info("Data Validation Completed Successfully")
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            
            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())

            return data_validation_artifact
            

        except Exception as e:
            raise SignException(e, sys)
        
