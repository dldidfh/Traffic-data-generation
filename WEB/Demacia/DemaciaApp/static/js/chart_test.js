    $(function(){
        var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        console.log( "hart_value_string",chart_value_string );
        console.log("chart_value_json",chart_value_json);
        console.log(chart_value_json['hour'].length);
        var hour_list = new Array();
        var min_list = new Array();
        var bus_list = new Array();
        var car_list = new Array();
        var truck_list = new Array();
        var label_list = new Array();
        for(i =0; i < chart_value_json['hour'].length; i++){
            label_list.push(chart_value_json['hour'][i]+" : "+chart_value_json['min'][i]);
            hour_list.push(chart_value_json['hour'][i]);
            min_list.push(chart_value_json['min'][i]);
            bus_list.push(chart_value_json['bus'][i]);
            car_list.push(chart_value_json['car'][i]);
            truck_list.push(chart_value_json['truck'][i]);
        }
        var config = {
            type: 'line',
            data: {
                labels: label_list,
                datasets: [{
                    label: 'Bus',
                    backgroundColor: "rgba(35, 50, 219,0.6)",
                    borderColor: "rgba(35, 50, 219,1)",
                    data: bus_list,
                    fill: false,
                }, {
                    label: 'Car',
                    fill: false,
                    backgroundColor: "rgba(239, 14, 21,0.4)",
                    borderColor: "rgba(239, 14, 21,1)",
                    data: car_list,
                    fill:false,
                },{
                    label: 'Truck',
                    fill: false,
                    backgroundColor: "rgba(239, 247, 19,0.2)",
                    borderColor: "rgba(239, 247, 19,1)",
                    data: truck_list,
                }],
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: '통계'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Count'
                        }
                    }]
                }
            }
        };  
        var ctx = document.getElementById('canvas').getContext('2d');
        new Chart(ctx,config);
});
    
		// window.onload = function() {
		// 	var ctx = document.getElementById('canvas').getContext('2d');
		// 	window.myLine = new Chart(ctx, config);
		// };

		// document.getElementById('randomizeData').addEventListener('click', function() {
		// 	config.data.datasets.forEach(function(dataset) {
		// 		dataset.data = dataset.data.map(function() {
		// 			return randomScalingFactor();
		// 		});

		// 	});

		// 	window.myLine.update();
		// });

		// var colorNames = Object.keys(window.chartColors);
		// document.getElementById('addDataset').addEventListener('click', function() {
		// 	var colorName = colorNames[config.data.datasets.length % colorNames.length];
		// 	var newColor = window.chartColors[colorName];
		// 	var newDataset = {
		// 		label: 'Dataset ' + config.data.datasets.length,
		// 		backgroundColor: newColor,
		// 		borderColor: newColor,
		// 		data: [],
		// 		fill: false
		// 	};

		// 	for (var index = 0; index < config.data.labels.length; ++index) {
		// 		newDataset.data.push(randomScalingFactor());
		// 	}

		// 	config.data.datasets.push(newDataset);
		// 	window.myLine.update();
		// });

		// document.getElementById('addData').addEventListener('click', function() {
		// 	if (config.data.datasets.length > 0) {
		// 		var month = MONTHS[config.data.labels.length % MONTHS.length];
		// 		config.data.labels.push(month);

		// 		config.data.datasets.forEach(function(dataset) {
		// 			dataset.data.push(randomScalingFactor());
		// 		});

		// 		window.myLine.update();
		// 	}
		// });

		// document.getElementById('removeDataset').addEventListener('click', function() {
		// 	config.data.datasets.splice(0, 1);
		// 	window.myLine.update();
		// });

		// document.getElementById('removeData').addEventListener('click', function() {
		// 	config.data.labels.splice(-1, 1); // remove the label first

		// 	config.data.datasets.forEach(function(dataset) {
		// 		dataset.data.pop();
		// 	});

		// 	window.myLine.update();
        // });
        

// ========================================================================

// var config ={
//     type: 'line',
//     data: {
//         labels: ['1', '2', '3', '4', '5', '6', '7'],
//         datasets: [{
//             label: '테스트 데이터셋',
//             borderColor: "rgba(255, 201, 14, 1)",
//             backgroundColor: "rgba(255, 201, 14, 0.5)",
//             data: [
//                 10,
//                 3,
//                 30,
//                 23,
//                 10,
//                 5,
//                 50
//             ],
//             fill: false,
//         }]
//     },
//     options: {
//         responsive: true,
//         title: {
//             display: true,
//             text: '라인 차트 테스트'
//         },
//         tooltips: {
//             mode: 'index',
//             intersect: false,
//         },
//         hover: {
//             mode: 'nearest',
//             intersect: true
//         },
//         scales: {
//             xAxes: [{
//                 display: true,
//                 scaleLabel: {
//                     display: true,
//                     labelString: 'x축'
//                 }
//             }],
//             yAxes: [{
//                 display: true,
//                 ticks: {
//                     suggestedMin: 0,
//                 },
//                 scaleLabel: {
//                     display: true,
//                     labelString: 'y축'
//                 }
//             }]
//         }
//     }
// };
// window.onload = function(){
//     var ctx = document.getElementById('linechart_material');
//     window.myLine = new Chart(ctx,config);
// };
   