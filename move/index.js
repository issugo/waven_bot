var robot = require("robotjs");

var args = process.argv

//Mouse down at 0, 0 and then drag to 100, 100 and release.
robot.setMouseDelay(300);
robot.moveMouse(parseInt(args[2]), parseInt(args[3]));
robot.mouseClick('left')
robot.mouseToggle("down");
robot.dragMouse(parseInt(args[4]), parseInt(args[5]));
robot.dragMouse(parseInt(args[4]), parseInt(args[5]) + 1);
robot.mouseToggle("up");