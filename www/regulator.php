<?php
// Returns values from controller script
define("RESULT_OK", 0);
define("ERROR_COMMON", 1);
define("ERROR_DEVICE_IN_USE", 2);
// Special return value is the current angle if mode -getAngel is used
	
$output = shell_exec('python ../src/regulator.py -calibrate');

switch ($output) {
    case RESULT_OK:
        echo "TODO Notify ok";
        break;
    case ERROR_COMMON:
        echo "TODO Notify on some error";
        break;
    case ERROR_DEVICE_IN_USE:
        echo "TODO Notfiy on hardware in use";
        break;
}

echo "<pre>$output</pre>";
