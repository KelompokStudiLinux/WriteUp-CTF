#include <stdio.h>
#include <stdlib.h>

int main () {
	int v8 ;
	int v6;
	int i;
	srand(1);
for ( i = 0; i <= 99; ++i )
{
    v8 = rand() % 100000 + 1;
    printf("%d ",v8);

}  
}
