from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.data_generation import generate_lidar
from src.lidar_metrics import canopy_metrics
print(canopy_metrics(generate_lidar()))
