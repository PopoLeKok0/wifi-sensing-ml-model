Project  blueprint (wip)

csi_detection/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── config/
│   ├── preprocessing.yaml
│   ├── training.yaml
│   └── experiments.yaml
│
├── preprocessing/
│   ├── data_loader.py
│   ├── segmentation.py
│   ├── filtering.py
│   ├── normalization.py
│   └── data_split.py
│
├── models/
│   ├── random_forest.py
│   └── cnn_1d.py
│
├── training/
│   ├── train_rf.py
│   ├── train_cnn.py
│   └── trainer.py
│
├── tests/
│   ├── standard_test.py
│   ├── open_set.py
│   └── zero_shot.py
│
├── evaluation/
│   ├── metrics.py
│   ├── confusion_matrix.py
│   └── visualization.py
│
├── results/
│   ├── models/
│   ├── metrics/
│   └── figures/
│
├── utils/
│   ├── seed.py
│   └── logger.py
│
├── main.py
│
└── requirements.txt