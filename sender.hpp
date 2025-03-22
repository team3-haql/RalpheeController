#include <string>
#include <array>

class Sender
{
public:
    Sender(const char* filename, int speed);
    ~Sender();

    void write(int data);
    int read();
private:
    int m_Fd;
};