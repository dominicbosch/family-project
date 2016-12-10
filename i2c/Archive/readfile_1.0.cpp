#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <libconfig.h++>

int main(int argc, char **argv)
{


    config_t cfg, *cf;
    int iMinVal;

    cf = &cfg;
    config_init(cf);

    if (!config_read_file(cf, "carconfig.ini")) {
        fprintf(stderr, "%s:%d - %s\n",
            config_error_file(cf),
            config_error_line(cf),
            config_error_text(cf));
        config_destroy(cf);
        return(EXIT_FAILURE);
    }

    iMinVal = config_lookup(cf, "1.min");

    printf("%d\n", iMinVal);

return  0;

}
