#include <iostream>

void uninitialized_variables()
{
  int x;
  std::cout << x << "\n";
}

int main()
{
  uninitialized_variables();
  return 0;
}
