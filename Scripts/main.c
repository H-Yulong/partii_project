#include <stdio.h>
#include <stdlib.h>
#include "uthash.h"
#include "utils.h"

typedef struct{
    int id;
    int min;    //Prob. of beating a score <= min is 100%.
    int max;    //Prob. of beating a score >= max is 0%.
    double* vals;
    UT_hash_handle hh;
} Dist;

int main(){

    int acc = 0;

    FILE* fpsource = fopen("D:\\Prog\\partii_project\\Table_Maximize\\0","rb");
    FILE* fp1 = fopen("D:\\Prog\\partii_project\\esti_table","ab");
    FILE* fp2 = fopen("D:\\Prog\\partii_project\\esti_table_readable.txt","a");
    ///*
    printf("Loading...\n");

    int buffer = 0;
    while(fread(&buffer, sizeof(int), 1, fpsource) == 1){

        // Read id
        int id = buffer;

        // Read min,max
        fread(&buffer, sizeof(int), 1, fpsource);
        int min = buffer;
        fread(&buffer, sizeof(int), 1, fpsource);
        int max = buffer;
  
        // Read vals
        double* vals;
        if ((max - min - 1) > 0){
            vals = malloc(sizeof(double) * (max - min - 1));
        }else{
            vals = NULL;
        }

        fread(vals, sizeof(double), max - min - 1, fpsource);
        ///*
        double esti =  min * (1 - vals[0]) + (max - 1) * (vals[max-min-2]);
        for(int i=0; i<(max - min - 2); i++){
            //printf("%f\n", vals[i]);
            esti += (min + 1 + i) * (vals[i] - vals[i+1]);
        }
        ///
        
        //Out id
        fwrite(&id, sizeof(int), 1, fp1);
        fwrite(&esti, sizeof(double), 1, fp1);
        fprintf(fp2, "%d %.6f\n", id, esti);
        //printf("%d\n", acc++);

    }
    fclose(fpsource);
    //*/ 
}
