#ifndef FUSiON_RM92_H
#define FUSiON_RM92_H

#include "mbed.h"

class RM92 {
    private:
        Serial *_serial;
        char c;
        char tx_buf[7];
        char rx_buf[30];
        char rx_size;
        char rx_dollar;
        int index;
        int flag;
        bool response;
        
        void (*func)(char*);

    public:
        RM92(Serial &serial);

        void send_cmd(int dst, char *cmd);

        void attach(void(*func_ptr)(char*));

    private:
        void receive();
};

#endif