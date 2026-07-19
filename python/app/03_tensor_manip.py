import torch


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


# Addition

vector = torch.tensor([1, 2, 3])
vector = vector + 10
describe_tensor(vector)

# Matrix Multiplication
# Inner dimensions must match and the resulting matrix has the shape of the outer dimensions.
# (2, 3) works with (3, 4) and it will result in (2, 4)
vector = torch.tensor([1, 2, 3])
element_multiplication = vector * vector
# [1*1, 2*2, 3*3] = [1, 4, 9]
print(element_multiplication)
# [1 * 1 + 2 * 2 + 3*3] = [14]
# matmul is faster than doing it by hand
matrix_multiplication = torch.matmul(vector, vector)
print(matrix_multiplication)

# Transpose. Switch dimensions of given tensor
tensor_a = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
tensor_b = torch.tensor([[7.0, 10.0], [8.0, 11.0], [9.0, 12.0]])
print(f"tensor={tensor_a} shape={tensor_a.shape}")
print(f"tensor={tensor_b} shape={tensor_b.shape}")
# Switches tensor_b from [3, 2] to [2, 3]
print(f"tensor={tensor_b.T} shape={tensor_b.T.shape}")

# Linear
torch.manual_seed(42)
linear = torch.nn.Linear(in_features=3, out_features=8)
x = tensor_a.T
output = linear(x)
print(f"Input shape: {x.shape}\n")
print(f"Output:\n{output}\n\nOutput shape: {output.shape}")
