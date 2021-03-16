//var esp_websocket = new WebSocket("ws://localhost:9900/SASESP/publishers/thermal_hotspot_detection3/thermal_hotspot_detection/w_receive_image/?blocksize=1&dateformat=%25Y%25m%25dT%25H%3A%25M%3A%25S.%25f&format=json&opcode=insert&pause=0&rate=0");
var esp_websocket = new WebSocket('ws://dach-viya4-k8s:9900/SASESP/publishers/thermal_hotspot_detection3/thermal_hotspot_detection/w_receive_image/?blocksize=1&dateformat=%25Y%25m%25dT%25H%3A%25M%3A%25S.%25f&format=json&opcode=insert&pause=0&rate=0');
var server_path = "/data/notebooks/images/"
//var esp_websocket_progress = new WebSocket("ws://localhost:9900/SASESP/subscribers/thermal_hotspot_detection3/thermal_hotspot_detection/w_filter_cluster/?format=json&mode=streaming&pagesize=50&precision=6&schema=false");
var esp_websocket_progress = new WebSocket("ws://dach-viya4-k8s:9900/SASESP/subscribers/thermal_hotspot_detection3/thermal_hotspot_detection/w_filter_cluster/?format=json&mode=streaming&pagesize=50&precision=6&schema=false");
var progress_counter = 0;
var num_files = 0;

esp_websocket_progress.onmessage = function(event) {
	console.log(event.data.startsWith('status'));
	var elem = document.getElementById('myBar');
	if (!event.data.startsWith('status')){
		progress_counter = progress_counter+1;
		elem.style.width = progress_counter/num_files*100 + "%";
		console.log(progress_counter);
	};
};

function readFiles(){
	console.log('AAAAAAAAAAAAAAAA');
	var customer_name = document.getElementById('customer_name').value;
	var files   = document.querySelector('input[type=file]').files;
	var min_degree_celsius = document.getElementById('min_degree_celsius').value;
	var min_size = document.getElementById('min_size').value;
	var max_size = document.getElementById('max_size').value;
	var folder_name = document.getElementById('folder_name').value;
	var current_timestamp = Date.now();
	num_files = files.length;
	progress_counter = 0;
	var elem = document.getElementById('myBar');
	elem.style.width = "1%";
	console.log("call");
	
	function publish(file){
		if ( /\.(jpe?g|png|gif)$/i.test(file.name) ) {
			var reader = new FileReader();
			reader.addEventListener("load", function () {
				// create event
				var esp_event = {id:"1", 
										  customer:customer_name,
										  filename:file.name, 
										  save_path:server_path+folder_name+"/",
										  timestamp:current_timestamp,
										  image:reader.result.split(',')[1], 
										  min_degree_celsius:min_degree_celsius, 
										  min_size:min_size, 
										  max_size:max_size
										  };
				var msg = {opcode: "insert", event:esp_event};
				console.log(msg);
				var json = JSON.stringify(msg);
				json = "["+json+"]";
				esp_websocket.send(json);
			}, false);
			reader.readAsDataURL(file);
		}
	};
	if (files){
		[].forEach.call(files, publish);
	};
};