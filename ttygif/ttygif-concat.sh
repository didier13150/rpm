#!/bin/bash

# avoid deleting file, if convert will fail
set -e

output=${1-"output.gif"}
prev_delay=0
skipped=0
first=1
prev_gif=
last_gif=
debug=0
timefactor="0.06"

# Put on array instead of scalar var
gifs=($(find . -maxdepth 1 -regex '.*[0-9][0-9][0-9][0-9][0-9]_[0-9].*.gif' | grep -v "$output" | sort) )
last_gif=${gifs[${#gifs[@]} - 1]}

# remove -loop 0 if you don't want it to repeat
_convert="convert -loop 0 "

for gif in ${gifs[@]}; do

	file=${gif##*/} 
	name=${file%.gif}
	delay=$(echo "${name#*_} * ${timefactor}" | bc)

	if [ $first == 1 ] ; then
		first=0
		prev_gif=$gif
		continue
	else
		# remove this is you don't want to trim zero delay frames
		if [ $delay == 0 ] && [ $prev_delay == 0 ]; then
			if [ $skipped -lt 5 ] ; then
				skipped=$(($skipped + 1))
				prev_delay=$delay
				continue
			else
				skipped=0
			fi
		fi
	fi
	# Force big delay for last image
	[ "$gif" == "$last_gif" ] && delay=100

	prev_delay=$delay

	_convert="$_convert -delay $delay $prev_gif"

	prev_gif=$gif

done

_convert="$_convert -layers Optimize $output"

echo "creating animated gif: $output"
[ $debug -ne 0 ] && echo $_convert
eval "$_convert"

echo "deleting temporary gifs"
for gif in ${gifs[@]}; do rm -f $gif ; done
