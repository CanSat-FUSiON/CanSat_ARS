#include "mbed.h"
#include "PQ_RM92A.h"

Serial pc(USBTX, USBRX, 115200);
Serial rm_serial(D1, D0, 115200);

RM92 rm(rm_serial);

void downlink_handler(char* data);

char mission_timer_reset;
short mission_time_init;
float mission_time;
float flight_time;
char flags;
char flags2;

float lat10000;
float lon10000;
float press1;
float temp1;
float press2;
float temp2;
float alt;
float press;
float temp;
int phase;

int main(){
    while(1){
        rm.attach(downlink_handler);
        if(pc.readable()){
            char cmd[1];
            cmd[0] = pc.getc();
            rm.send_cmd(0x0000, cmd);
            pc.printf("send:\t%x\r\n", cmd[0]);
        }
    }  
    }




void downlink_handler(char* data){  
    press = (float(data[7]) * 256 + float(data[8])) / 10;
    temp = (float(data[9]) * 256 + float(data[10])) / 100;
    lat10000 = (float(data[11]) * 10000 + float(data[12]) * 100 + float(data[13])) / 10000;
    lon10000 = (float(data[14]) * 10000 + float(data[15]) * 100 + float(data[16])) / 10000;
    phase = int(data[17]);

    pc.printf(" LAT:\t\t%.6f\r\n", lat10000);
    pc.printf(" LON:\t\t%.6f\r\n", lon10000);
    pc.printf(" PRESS:\t\t%.2f[hPa]\r\n", press);
    pc.printf(" TEMPERATURE:\t%.2f[C]\r\n", temp);
    pc.printf("\r\n");
    
  
}
