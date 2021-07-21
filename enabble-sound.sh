#!/bin/bash
sudo modprobe snd_bcm2835 && sudo amixer cset numid=3 1
speaker-test -c1 -t sine -f 800 -P 2 -p 0.4 -l 1