#!/usr/bin/octave
#author: LuboJ
#date: Oct 2020
#

#MUST START WITH SOMETHING ELSE THAN FUNCTION DEFINITION, OTHERWISE SCRIPT NOT RUN!
disp('Running...')

function y = deg2rad(x)
	y = x * 3.14 / 180;
	return;
endfunction

disp('Test 180 deg -> rad:');
deg2rad(180)
disp('Test 45 deg -> rad:');
deg2rad(45)

disp('Toto je dis :D :D :D')
