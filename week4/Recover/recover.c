/**
 * Recovers lost jpeg files
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define Blocksize 512

typedef uint8_t  Byte;

//function to check if block is start of jpeg
bool jpgtst(fileptr);

int main(int argc, char *argv[])
{
    int n = 1;
    Byte Block[Blocksize];
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    //ensure file is not empty
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL)
    {
        fprintf(stderr, "File is empty!\n");
        fclose (fp);
    }
    //Count for new file names
    int name_count = 0;

    //establish file name variable
    char jpgname[sizeof "100.jpg"];


    //keep looping if not at end of file or fread does not return 0
    while (n != EOF) {

        n = fread (&Block, Blocksize, 1, fp);
        if (n == 0)
        break;

        if (jpgtst(Block) == true)
        {
            //map name to formated string
            sprintf(jpgname, "%03d.jpg", name_count);
            //open new file for jpg output
            FILE *OPF = fopen(jpgname,"w");

            do {
                fwrite (Block, Blocksize, 1, OPF);
            
            }
            while(
                 jpgtst(Block) != true
            );

            fclose (OPF);
            name_count = name_count + 1;        
        }

    }

    fclose (fp);
}

bool jpgtst(int *fileptr)
{
    if (fileptr[0] == 0xff &&
        fileptr[1] == 0xd8 &&
        fileptr[2] == 0xff &&
        (fileptr[3] & 0xf0) == 0xe0)
        {
            return true;
        }

}