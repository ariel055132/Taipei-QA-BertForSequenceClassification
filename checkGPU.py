import torch

# Check GPU is available or not
# If GPU is available, show the no. of GPU
if torch.cuda.is_available():
    print("GPU available") 
    print(torch.cuda.device_count())
else:
    print("No GPU")