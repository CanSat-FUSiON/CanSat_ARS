#include "mbed.h"
#include "FUSiON_RM92A.h"

RM92::RM92(Serial &serial) {
    _serial = &serial;
    _serial -> attach(callback(this, &RM92::receive), Serial::RxIrq);   // 受信割り込みを登録
    memset(tx_buf, '\0', 7);    
    rx_size = 25;
    memset(rx_buf, '\0', rx_size);
    
    index = 0;
    flag = 0;
}

void RM92::send_cmd(int dst, char *cmd) {
    tx_buf[0] = '@';
    tx_buf[1] = '@';
    tx_buf[2] = 1;
    tx_buf[3] = dst >> 8 & 0xff;
    tx_buf[4] = dst >> 0 & 0xff;
    tx_buf[5] = cmd[0];
    tx_buf[6] = 0xAA;
    for (int i = 0; i < 7; i++) {
        _serial->putc(tx_buf[i]);
    }
    flag = 0;
    response = true;
}

// データ処理関数を設定
void RM92::attach(void(*func_ptr)(char*)) {
    func = func_ptr;
}

void RM92::receive() {
    if(flag == 0){
        memset(rx_buf, '\0', rx_size);
        index = 0;
        flag = 1;
    }
    if(flag == 1){
        rx_buf[index] = _serial->getc();
        if(index == rx_size - 1) {
            if(!response) {
                if(func != NULL) {
                    (*func)(rx_buf);
                }
            } else {
                response = false;
            }
            flag = 0;
        } else {
            index ++;
        }
    
    }
}