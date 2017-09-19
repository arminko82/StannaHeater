// Frontend JS part of regulator project

var piemenu;

function createWheel() {
	var items = [ "0%", "20%", "40%", "60%", "80%", "100%" ];
	piemenu = new wheelnav('piemenu');
	piemenu.sliceInitPathFunction = piemenu.slicePathFunction;
	piemenu.slicePathFunction = slicePath().DonutSlice;
	piemenu.clickModeRotate = false;
	piemenu.initPercent = 0.1;
	piemenu.wheelRadius = piemenu.wheelRadius * 1;
	piemenu.navItemsContinuous = true;
	piemenu.sliceAngle = 180 / items.length;
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
	piemenu.createWheel(items);

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
			
			piemenu.selectedNavItemIndex = data;
			clear();
		},
		error : function(data) { // timeout
			piemenu.selectedNavItemIndex = null;
			endPendingState(" State Request Failed");
			clearDelayed();
		}
	});
}

function handleUserRequest() {
	
	const regex = /(\d+)%/u;
	var item = piemenu.navItems[piemenu.currentClick];
	var percent = regex.exec(item.title)[1];

	// TODO handle percent as absolute on php side
	$.ajax({
		type : 'POST',
		url : 'php/regulator.php',
		data : {
			"execTurn" : percent
		},
		timeout : 10000,
		success : function(data) {
			handleResponse(data);
		},
		error : function(data) { // timeout
			endPendingState("FAILED");
			clearDelayed();
		}
	});
}

function handleResponse(response) {
	// TODO reset state on error
	response = response.trim();
	switch (response) {
	case '0':
		endPendingState("OK");
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
function endPendingState(result) {
	getHourglass().style.visibility = 'hidden';
	notify(result);
}