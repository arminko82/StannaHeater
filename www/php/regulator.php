<?php
// Return values from controller script
define("RESULT_OK", 0);
define("ERROR_COMMON", 1);
define("ERROR_DEVICE_IN_USE", 2);
define("ERROR_UNKNOWN_FUNCTION", 3);
define("ERROR_ANGLE", -361);

// Forwards the call to the backend controller.
// Tries to turn the lever to the desired end point.
function execTurn($desiredAngle)
{
    return evaluateOutput(shell_exec('python ../backend/regulator.py -turn '.$desiredAngle));
}

// Tells the controller to calibrate itself.
function execCalibrate()
{
    return evaluateOutput(shell_exec('python ../backend/regulator.py -calibrate'));
}

// Asks the controller for the current state.
// Returns false on error and null on a detected angle that differs from the error codes.
function execGetAngle()
{
    $output = shell_exec('python ../backend/regulator.py -getAngle');
    $interpretation = evaluateOutput($output);
    if ($interpretation != null)
        return ERROR_ANGLE; // bool
    return $output;
}

// Kind of init code in global space of this file's scope.
// This is used to determind the function the ajax query wanted to call
// and passes the given parameters to that function.
if (isset($_POST['execTurn']))
{
    return execTurn($_POST['execTurn']);
} 
elseif (isset($_POST['execCalibrate']))
{
    return execCalibrate();
} 
elseif (isset($_POST['execGetAngle']))
{
    return execGetAngle();
}
else
{
    return ERROR_UNKNOWN_FUNCTION;
}
// end "init code"

// Interprets the received return values for the python scripts.
// @return bool|null
function evaluateOutput($output)
{
    switch ($output) {
        case RESULT_OK:
            //echo "TODO Notify ok";
            return true;
        case ERROR_COMMON:
            //echo "TODO Notify on some error";
            return false;
        case ERROR_DEVICE_IN_USE:
            //echo "TODO Notfiy on hardware in use";
            return false;
        default:
            return null;
    }
}