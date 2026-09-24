import os
from dotenv import load_dotenv
from ultralytics import YOLO
import roboflow
from config.settings import DATASET_DIR

load_dotenv()

# Login no Roboflow
roboflow.login()
api_key = os.getenv("API_KEY")
rf = roboflow.Roboflow(api_key)

# Carregar o projeto Roboflow
project = rf.workspace("trabalhoia-eompb").project("projeto-ia-mxnom")
dataset = project.version(21).download("yolov8")

# Carregar o modelo e iniciar o treinamento
model = YOLO("yolov8n.pt")

# Caminho para o arquivo de dados YAML de treinamento
data_yaml = 'datasets/Projeto-IA-21/data.yaml'

# Treinamento do modelo
# Se der erro é necessário alterar as configurações do ultralytics e colocar o path dos datasets para este projeto
results = model.train(data=data_yaml, epochs=100, imgsz=640, device='cpu')

# Salvar pesos do modelo treinado
model.save("weights/best.pt")
