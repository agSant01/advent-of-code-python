#include <stdlib.h>
#include <stdio.h>

int next_a(int prev)
{
    int n = prev * 16807;
    int a = n & 2147483647;
    int b = n >> 31;
    // return (prev * 16807) % 2147483647;
    return a + b;
}

int next_b(int prev)
{
    int n = prev * 48271;
    int a = n & 2147483647;
    int b = n >> 31;
    // return (prev * 48271) % 2147483647;
    return a + b;
}

int part1()
{

    int A = 65;
    int B = 8921;
    size_t consider = 40000000;
    size_t matching_pairs = 0;
    for (size_t i = 0; i < consider; i++)
    {
        /* code */
        A = next_a(A);
        B = next_b(B);

        if ((short)(A ^ B) == 0)
        {
            matching_pairs++;
        }
    }

    printf("%ld pairs\n", matching_pairs);
}

int isMultipleOf4(size_t n)
{
    if (n == 0)
        return 1;
    return (((n >> 2) << 2) == n);
}

int isMultipleOf8(size_t n)
{
    if (n == 0)
        return 1;
    return (((n >> 3) << 3) == n);
}

size_t next_a_by4(size_t prev)
{
    size_t next = (prev * 16807) % 2147483647;

    while (next % 4 != 0)
    {
        next = (next * 16807) % 2147483647;
    }
    return next;
}

size_t next_b_by8(size_t prev)
{
    size_t next = (prev * 48271) % 2147483647;
    while (next % 8 != 0)
    {
        next = (next * 48271) % 2147483647;
    }
    return next;
}

int part2()
{
    size_t A = 722;
    size_t B = 354;
    size_t consider = 5000000;
    size_t matching_pairs = 0;
    for (size_t i = 0; i < consider; i++)
    {
        /* code */
        A = next_a_by4(A);
        B = next_b_by8(B);
        if ((short)(A ^ B) == 0)
        {
            matching_pairs++;
        }
    }

    printf("%ld pairs\n", matching_pairs);
}
int main()
{
    // part1();
    part2();
}