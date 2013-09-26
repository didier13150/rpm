#!/bin/bash

for size in 16 22 32 48 64 128 256
do
    if [ ! -f "fracplanet-hi${size}.png" ]
    then
        povray -W${size} -H${size} +Ifracplanet.pov +UA +Ofracplanet-hi${size}.png
    fi
done

