#!/usr/bin/expect --
eval spawn -noecho rpm [lrange $argv 0 end];
expect {
   "Enter pass phrase:"  { send -- "\r"; exp_continue }
   eof
}