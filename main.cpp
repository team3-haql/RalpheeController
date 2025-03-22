#include "sender.hpp"
#include <chrono>
#include <thread>

int main()
{
    Sender sender("/dev/ttyACM0", 9600);

    sender.write(100);
    sender.read();
}