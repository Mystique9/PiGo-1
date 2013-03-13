echo | wget http://pypi.python.org/packages/source/p/pyserial/pyserial-2.6.tar.gz
echo | tar -zxvf pyserial-2.6.tar.gz
cd pyserial-2.6
echo | sudo python setup.py install
rm pyserial-2.6.tar.gz