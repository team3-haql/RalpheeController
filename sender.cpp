#include "sender.hpp"
#include <cstring>
#include <errno.h>
#include <fcntl.h>
#include <iostream>
#include <termios.h>
#include <unistd.h>

Sender::Sender(const char* filename, int speed)
{
    m_Fd = open(filename, O_WRONLY | O_NOCTTY | O_SYNC);
    if (m_Fd < 0)
    {
        throw std::runtime_error("Invalid port!");
    }
    struct termios tty;
    if (tcgetattr(m_Fd, &tty) != 0) 
    {
        throw std::runtime_error("Failed to make termios");
    }
    cfsetispeed(&tty, speed);
    cfsetospeed(&tty, speed);

    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8; // 8-bit characters
    tty.c_iflag &= ~IGNBRK; // disable break processing
    tty.c_lflag = 0; // no signaling chars, no echo, no
                     // canonical processing
    tty.c_oflag = 0; // no remapping, no delays
    tty.c_cc[VMIN] = 0; // read doesn't block
    tty.c_cc[VTIME] = 5; // 0.5 seconds read timeout

    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // shut off xon/xoff ctrl

    tty.c_cflag |= (CLOCAL | CREAD); // ignore modem controls,
                             // enable reading
    tty.c_cflag &= ~(PARENB | PARODD); // shut off parity
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CRTSCTS;

    if (tcsetattr(m_Fd, TCSANOW, &tty) != 0) 
    {
        throw std::runtime_error("tcsetattr failed!");
    }
}
Sender::~Sender()
{
    close(m_Fd);
}

void helpWrite(int fd, int data)
{
    std::string s = std::to_string(data);
    write(fd, s.c_str(), s.length());
}

void Sender::write(int data)
{
    helpWrite(m_Fd, data);
}

int helpRead(int fd)
{
    const size_t size = sizeof(int);
    char buffer[size];
    read(fd, buffer, size);
    int data = *(int*)buffer;
    std::cout << data << '\n';
    return data;
}

int Sender::read()
{
    return helpRead(m_Fd);
}