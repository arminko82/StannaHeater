<?php
define("LOG_FILE", "out.log");
// Return values from controller script
define("RESULT_OK", '0');
define("ERROR_COMMON", '1');
define("ERROR_DEVICE_IN_USE", '2');
define("ERROR_UNKNOWN_FUNCTION", '3');
define("ERROR_ANGLE", '-361');

// Kind of init code in global space of this file's scope.
// This is used to determind the function the ajax query wanted to call
// and passes the given parameters to that function.
if (isset($_POST['execTurn']))
{
    log1("Executing isset1");
    return execTurn($_POST['execTurn']);
}
elseif (isset($_POST['execCalibrate']))
{
    log1("Executing isset2");
    return execCalibrate();
}
elseif (isset($_POST['execGetAngle']))
{
    log1("Executing isset3");
    return execGetAngle();
}
else
{
    log1("Executing isset4");
    return ERROR_UNKNOWN_FUNCTION;
}
// end "init code"

// Forwards the call to the backend controller.
// Tries to turn the lever to the desired end point.
function execTurn($desiredAngle)
{
    log1("Executing execTurn");
    return evaluateOutput(shell_exec('python ../backend/regulator.py -turn '.$desiredAngle));
}

// Tells the controller to calibrate itself.
function execCalibrate()
{
    log1("Executing execCalibrate");
    return evaluateOutput(shell_exec('python ../backend/regulator.py -calibrate'));
}

// Asks the controller for the current state.
// Returns false on error and null on a detected angle that differs from the error codes.
function execGetAngle()
{
    log1("Executing execGetAngle");
    $output = shell_exec('python ../backend/regulator.py -getAngle');
    $interpretation = evaluateOutput($output);
    if ($interpretation != null)
        return ERROR_ANGLE; // bool
    return $output;
}

// Interprets the received return values for the python scripts.
// Writes the response code to stdout which becomes part of the HTTP response
// on HTTP POST handling
// @return bool|null
function evaluateOutput($output)
{
    $out = bin2hex($output);
    log1("evaluateOutput: " . $out);
    echo strval($output); // actual HTTP response output writer
    switch ($output) {
        case RESULT_OK:
            return true;
        case ERROR_DEVICE_IN_USE:
        case ERROR_COMMON:
            return false;
        default:
            return null;
    }
}

// A logger that writes to stdout while in debug mode
function log1($msg)
{
    date_default_timezone_set('Europe/Vienna');
    $now = date("Y-m-d H:i:s");
    $line = sprintf("%s => %s\r\n", $now, $msg);
    file_put_contents(LOG_FILE, $line, FILE_APPEND);
}
?>