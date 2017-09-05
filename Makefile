CC=g++
CFLAGS=-Wall
I2CDIR=i2c

all: 
	gcc $(CFLAGS) -o $(I2CDIR)/arduino5 $(I2CDIR)/arduino5.c -I$(I2CDIR)
	-$(CC) $(CFLAGS) -o $(I2CDIR)/cardo_1.1 $(I2CDIR)/cardo_1.1.cpp -I$(I2CDIR)
	-$(CC) $(CFLAGS) -o $(I2CDIR)/getDist $(I2CDIR)/getDist.cpp
	-$(CC) $(CFLAGS) -o $(I2CDIR)/myConvert $(I2CDIR)/myConvert.cpp
	-$(CC) $(CFLAGS) -o $(I2CDIR)/myPWM $(I2CDIR)/myPWM.cpp -I$(I2CDIR)
	$(CC) $(CFLAGS) -o $(I2CDIR)/sigtest $(I2CDIR)/sigtest.cpp

clean:
	$(RM) $(I2CDIR)/arduino5
	$(RM) $(I2CDIR)/cardo_1.1
	$(RM) $(I2CDIR)/getDist
	$(RM) $(I2CDIR)/myConvert
	$(RM) $(I2CDIR)/myPWM
	$(RM) $(I2CDIR)/sigtest
	$(RM) camera/detected-faces/*.jpg
	$(RM) camera/snapshots/*.jpg
	$(RM) visualizations/www/thumbs/*.jpg