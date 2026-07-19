#include <iostream>
#include <limits>

int initialization()
{
  double price{9.99};
  // If you wrote int dollars {price} (direct list initialization) it would not work because you would be losing data.
  // int dollars = price (copy initialization) does not seem to care.
  int dollars = price;
  std::cout << dollars << "\n";
  return price;
}

int main()
{
  int width = initialization();
  std::cout
    << width
    << std::endl; // endl is slower so use sparingly. It flushes the buffer immediatley making it good only for
                  // debugging, progress indication, and interactive programs waiting for user input. If it sees endl at
                  // all, it will print immedaitley whereas with \n it will wait for system to end to flush.
  int x{};
  std::cin >> x; // You use >> because >> is like where the stream is pointing. For cout you take the stream and put it
                 // into character out (cout) to print and for cin you take input with cin and put it into x.
  std::cout << x;
}
