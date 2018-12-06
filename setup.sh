#/usr/bin/env bash -e

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python2`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate


if [ ! -e "./Adafruit_Python_GPIO" ]
then
    git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
fi
cd Adafruit_Python_GPIO
python setup.py install
cd ..

if [ ! -e "./Adafruit_Python_SHT31" ]
then
    git clone https://github.com/ralf1070/Adafruit_Python_SHT31.git
fi
cd Adafruit_Python_SHT31
sudo python setup.py install
cp Adafruit_SHT31.py ..
cd ..

pip install -r requirements.txt

if [ ! -e "./config.ini" ]
then
    cp config.ini.default config.ini
fi
