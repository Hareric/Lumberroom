#!/usr/bin/expect                   

set timeout 30                       
spawn ssh root@*********** -p 27997 
expect "*password:"                 
send "***********\r"              
send "sh /xs/restart.sh\r" 
interact                          
