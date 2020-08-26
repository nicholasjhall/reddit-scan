'use strict';

console.log('Testing');

function runScan(input) {
	$.ajax({
		type: "POST",
		url: "/app.py",
		data: { param: input },
		success: displayData
	});
}

function displayData(response) {
	console.log(response);
}

runScan('input here');