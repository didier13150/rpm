#!/bin/bash

for size in 16 22 32 48 64 128 256
do
    povray -W${size} -H${size} +Ifracplanet.pov +UA +Ofracplanet-hi${size}.png
done

