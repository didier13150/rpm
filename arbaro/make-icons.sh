#!/bin/bash

source="icon.svg"
app="@appname@"

for size in 16 22 32 48 64 128 256
do
    convert -transparent white -resize ${size}x${size} ${source} ${app}-hi${size}.png
done
