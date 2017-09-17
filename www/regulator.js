// Frontend JS part of regulator project

function createWheel() {
	var items = [ "0%", "20%", "40%", "60%", "80%", "100%" ];
	var piemenu = new wheelnav('piemenu');
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
		item.navSlice.mouseup(showPendingState);
		item.navTitle.mouseup(showPendingState);
	}
	// click handler which invokes backend
	piemenu.animateFinishFunction = function() {
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
				showResult("FAILED");
				setTimeout(function() {
				}, 5000)
			}
		});
	};
}

function handleResponse(response) {
	// TODO reset state on error
	response = response.trim();
	switch (response) {
	case '0':
		showResult("OK");
		break;
	case '1':
		showResult("ERROR");
		break;
	case '2':
		showResult("DEVICE IN USE");
		break;
	case '3':
		showResult("ERROR");
		break;
	case '-361':
		showResult("ERROR");
		break;
	}
}
function getStateElement() {
	return document.getElementById('status');
}
function showResult(resultName) {
	getStateElement().innerHTML = resultName;
}
function showPendingState() {
	showResult("... working ...");
}