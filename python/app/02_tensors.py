import torch

TORCH_VERSION = torch.__version__
# print(TORCH_VERSION)


def describe_tensor(t):
    print(t)
    # Will print 0 for scalar because there is no direction to a point
    # Will print 1 for vector because you can think of a vector line that has one direction
    # A tip for finding the dimensions is to count the number of left brackets ("[") on the outer tensor
    print(f"ndim: {t.ndim}")
    # Will print the number of elements in each dimension. If there are no dimensions, print empty array
    print(f"shape: {t.shape}")
    if t.ndim > 0:
        # Most common are torch.float16, torch.float32, and torch.float64 floats are the standard because neural networks need tiny adjustments
        # Pytorch defaults to float32 while NumPy defaults to float64.
        print(f"dtype: {t.dtype}\n")
    else:
        print(f"item: {t.item()}\n")


# Scalar
scalar = torch.tensor(7)
describe_tensor(scalar)

# Vector
vector = torch.tensor([7, 7])
describe_tensor(vector)

# Matrix
matrix = torch.tensor([[7, 7], [9, 10]])
describe_tensor(matrix)


# Tensor
tensor = torch.tensor([[[1, 2, 3], [3, 6, 9], [2, 4, 5]]])
describe_tensor(tensor)

# Random tesnsors
random_tensor = torch.rand(size=(3, 4))
describe_tensor(random_tensor)

# Zeroes and Ones tensor. This is good when masking some values to let model know not to learn
zeros = torch.zeros(size=(3, 4))
describe_tensor(zeros)


# Write tensor as a range of numbers
zero_to_ten = torch.arange(start=0, end=10, step=1)
describe_tensor(zero_to_ten)
