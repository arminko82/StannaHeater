// Frontend JS part of regulator project

var piemenu;
var STAGES = [ "0%", "20%", "40%", "60%", "80%", "100%" ];
//var STAGES = [ "0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%" ];
var mCurrentIndex = -1;

function createWheel() {
	piemenu = new wheelnav('piemenu');
	piemenu.sliceInitPathFunction = piemenu.slicePathFunction;
	piemenu.slicePathFunction = slicePath().DonutSlice;
	piemenu.clickModeRotate = false;
	piemenu.initPercent = 0.1;
	piemenu.wheelRadius = piemenu.wheelRadius * 1;
	piemenu.navItemsContinuous = true;
	piemenu.sliceAngle = 180 / STAGES.length;
	piemenu.navAngle = -180 + piemenu.sliceAngle / 2;
	piemenu.sliceSelectedAttr = {
		stroke : '#9CF',
		'stroke-width' : 4
	};
	piemenu.lineSelectedAttr = {
		stroke : '#9CF',
		'stroke-width' : 4
	};
	piemenu.titleSelectedAttr = {
		fill : '#9CF'
	};
	piemenu.createWheel(STAGES);

	for (i = 0; i < piemenu.navItems.length; i++) {
		var item = piemenu.navItems[i];
		item.navSlice.mouseup(beginPendingState);
		item.navTitle.mouseup(beginPendingState);
	}
	piemenu.animateFinishFunction = handleUserRequest;
	getCurrentPercent();
}

function getCurrentPercent() {
	$.ajax({
		type : 'POST',
		url : 'php/regulator.php',
		data : {
			"execGetAngle" : ''
		},
		timeout : 1000,
		success : function(data) {
			var parts = data.trim().split("|").map(parseFloat);
			var readPercent = parts[2] / (parts[1] - parts[0]) * 100;
			const regex = getPattern();
			var minDiff = Number.MAX_VALUE;
			var i = 0;
			for(; i < STAGES.length; i++) {
				stageValue = regex.exec(STAGES[i])[1];
				var d = diff(readPercent, stageValue); 
				if(d > minDiff)
					break; // have desired i now
				minDiff = d;
			}
			mCurrentIndex = i;
			piemenu.navigateWheel(i);
			clear();
		},
		error : function(data) { // timeout
			mCurrentIndex = -1;
			piemenu.navigateWheel(null);
			endPendingState(" State Request Failed");
			clearDelayed();
		}
	});
}

function handleUserRequest() {
	const regex = getPattern();
	var index = piemenu.currentClick;
	if(index == mCurrentIndex)
		return;
	var item = piemenu.navItems[index];
	var percent = regex.exec(item.title)[1];
	$.ajax({
		type : 'POST',
		url : 'php/regulator.php',
		data : {
			"execTurnPercent" : percent
		},
		timeout : 10000,
		success : function(data) {
			handleResponse(data, index);
		},
		error : function(data) { // timeout
			endPendingState("FAILED");
			clearDelayed();
		}
	});
}

function handleResponse(response, desiredIndex) {
	response = response.trim();
	switch (response) {
	case '0':
		mCurrentIndex = desiredIndex;
		endPendingState("OK", false);
		break;
	case '1':
		endPendingState("ERROR");
		break;
	case '2':
		endPendingState("DEVICE IN USE");
		break;
	case '3':
		endPendingState("ERROR");
		break;
	case '-361':
		endPendingState("ERROR");
		break;	
	default:
		endPendingState("ERROR: Unknown response: " + response);
		break;
	}
	clearDelayed();
}
function notify(text) {
	document.getElementById('status').innerHTML = text;
}
function clearDelayed() {
	setTimeout(clear, 5000);
}
function clear() {
	notify("");
}
function getHourglass() {
	return document.getElementById('hourglass'); 
}
function beginPendingState() {
	getHourglass().style.visibility = 'visible';
	notify("... working ...");
}
function endPendingState(result, error=true) {
	getHourglass().style.visibility = 'hidden';
	if(error)
		piemenu.navigateWheel(mCurrentIndex == -1 ? null : mCurrentIndex); // revert view
	notify(result);
}
function diff(a, b) {
	return Math.abs(a - b);
}
function getPattern() {
	return /(\d+)%/u;
}