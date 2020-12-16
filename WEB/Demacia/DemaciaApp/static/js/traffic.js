// CSRF Token
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
$(document).ready(function() {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});


var isPause = false;
var timer;
var timer1;
var my_chart;
$(document).ready(function () {
    var frame=0;
    ajax_func(0,frame);
    chart_func(0,frame);
    timer = setInterval(function(){
        frame +=1000;
        if(frame > 8000){
            // frame = 9000;
            clearInterval(timer);
        }
        ajax_func(0,frame);
        chart_func(0,frame);
        }, 2000)   
});

function click_func(input){
    clearInterval(timer);
    var input_val = input;
    var frame = 0;
    ajax_func(0,frame);
    chart_func(0,frame);

    var vid = videojs("livestation-player1")
    switch (input_val) {
        case 0:
            vid.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/video/Seoul_Plaza_2020_11_25_14_54_28.mp4" });
            break;
        case 1:
            vid.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/video/Seoul_Plaza_2020_11_25_22_54_28.mp4" });
            break;
        case 2:
            vid.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/video/Cheonggye_morning.mkv"});
            break;
        case 3:
            vid.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/video/Cheonggye_night.mkv" });
            break;
    }
    var vid2 = videojs("livestation-player2")
    switch(input_val){
        case 0:
            vid2.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/converted_video/Convert_Seoul_Plaza_morning.mp4" });
            break;
        case 1:
            vid2.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/converted_video/Convert_Seoul_Plaza_night_best.mp4" });
            break;
        case 2:
            vid2.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/converted_video/Convert_Cheonggye_morning.mp4" });
            break;
        case 3:
            vid2.src({ type: 'video/mp4', src: "https://demacia-s3-second.s3-us-west-1.amazonaws.com/real_video/converted_video/Convert_Cheonggye_night.mp4" });
            break;
    }
    timer = setInterval(function(){
        frame += 1000;
        if(frame > 8000){
            // frame = 9000;
            clearInterval(timer);
        }
        console.log(input_val)
        ajax_func(input_val,frame);
        chart_func(input_val,frame);

    }, 2000)
}
function ajax_func(input=0,frame){
    var input_data = input;
    var frame_val = frame;
    console.log(input_data);
    console.log(frame_val);
    $.ajax({
        cache : false,
        url: "../traffic_volumne_research_data/",  
        type: "POST",  
        data_type:'json',
        data : {'sign':input_data, 'frame':frame_val},
        success:function(data){
            console.log("성공");
            $("#call_ajax").html(data);
         },error:function(request,status,error){
            console.log(error);
        }
    });
};

function chart_func(input=0,frame){
    var input_data = input;
    var frame_val = frame;
    console.log(frame_val);
    $.ajax({
        cache : false,
        url: "../traffic_volumne_research_chart_data/",  
        type: "POST",  
        data_type:'json',
        data : {'sign':input_data, 'frame':frame_val},
        success:function(data){
            console.log("성공차트");
            var hour_list = new Array();
            var min_list = new Array();
            var bus_list = new Array();
            var car_list = new Array();
            var truck_list = new Array();
            var label_list = new Array();
            for(i =0; i < data['hour'].length; i++){
                label_list.push(data['hour'][i]+" : "+data['min'][i]);
                hour_list.push(data['hour'][i]);
                min_list.push(data['min'][i]);
                bus_list.push(data['bus'][i]);
                car_list.push(data['car'][i]);
                truck_list.push(data['truck'][i]);
            }
            console.log(label_list);
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
                        
                    },{
                        label: 'Truck',
                        fill: false,
                        backgroundColor: "rgba(239, 247, 19,0.2)",
                        borderColor: "rgba(239, 247, 19,1)",
                        data: truck_list,
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    legend:{
                        labels:{
                            fontSize:15
                        }
                    },
                    title: {
                        display: true,
                        text: '통계',
                        fontSize:25,
                        fontFamily:' sans-serif'
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
                            ticks:{
                                fontSize:14,
                                
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Time',
                                fontStyle:'bold'
                            }
                        }],
                        yAxes: [{
                            display: true,
                            ticks:{
                                fontSize:14,
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Count',
                                fontStyle:'bold'
                            }
                        }]
                    }
                }
            }; 
            if(my_chart){
                console.log("있다");
                // my_chart.destroy();
                // var ctx = document.getElementById('canvas').getContext('2d');
                // my_chart = new Chart(ctx,config);
                my_chart.config.data.labels = label_list;
                my_chart.config.data.datasets[0].data = bus_list;
                my_chart.config.data.datasets[1].data = car_list;
                my_chart.config.data.datasets[2].data = truck_list;
                my_chart.update();
            }
            else{
                console.log("없다");
                var ctx = document.getElementById('canvas').getContext('2d');
                my_chart = new Chart(ctx,config);
            }
        
        },error:function(request,status,error){
            console.log(error);
        }
    });
};


// function chart_func(input=0,frame){
//     var input_data = input;
//     var frame_val = frame;
//     console.log(frame_val);
//     $.ajax({
//         cache : false,
//         url: "../traffic_volumne_research_chart_data/",  
//         type: "POST",  
//         data_type:'json',
//         data : {'sign':input_data, 'frame':frame_val},
//         success:function(data){
//             console.log("성공차트");
//             $("#call_chart_ajax").html(data);
            
//         },error:function(request,status,error){
//             console.log(error);
//         }
//     });
// };

// function ajax_func(input=0,frame){
//     var input_data = input;
//     var frame_val = frame;
//     console.log(input_data);
//     console.log(frame_val);
//     $.ajax({
//         cache : false,
//         url: "../traffic_volumne_research_data/",  
//         type: "POST",  
//         data_type:'json',
//         data : {'sign':input_data, 'frame':frame_val},
//         success:function(data){
//             console.log("성공");
//             console.log(data)
//             // $("#call_ajax").html(data[0]);
//             var keys = Object.keys(data[0]);
//             console.log(keys);

//             // tbody를 가리킴
//             var table_list = document.querySelector("#tbody_area");

//             // tbody의 tr의 노드 수가 데이터의 인덱스와 맞지 않으면 실행
//             if( document.querySelectorAll("#tbody_area > tr").length != data.length && document.querySelectorAll("#tbody_area > tr").length < data.length){
//                 for( i =0; i < data.length; i++){
//                     var newTR = document.createElement("tr");
//                     newTR.setAttribute("class","value_table");
//                     table_list.appendChild(newTR);    
//                 }
//                 console.log("tr",table_list);
//             } // end if
//             else{
//                 var tr_count = document.querySelectorAll("#tbody_area > tr");
//                 console.log("티알카운트", tr_count);
//                 for(i = 0; i < tr_count.length; i++){
//                     tr_count[i].remove();
//                 }

//                 for( i =0; i < data.length; i++){
//                     var newTR = document.createElement("tr");
//                     newTR.setAttribute("class","value_table");
//                     table_list.appendChild(newTR);    
//                 }
//                 console.log("tr",table_list);
//             }

//             var td_target = document.querySelectorAll("#tbody_area > tr");
            
//             console.log("td갯수", document.querySelectorAll("#tbody_area > tr > td").length);
//             if( document.querySelectorAll("#tbody_area > tr > td").length != (keys.length * data.length) && document.querySelectorAll("#tbody_area > tr > td").length < (keys.length * data.length)){
                
//                 for(y = 0; y < td_target.length; y++){
//                     for( t =0; t < td_target.length; t++){
//                         var newTD = document.createElement("td");
//                         newTD.textContent = data[y][keys[t]];
//                         td_target[y].appendChild(newTD);
//                     }
//                 }
//             } // end if
//             else{
//                 var td_count = document.querySelectorAll("#tbody_area > tr > td");
//                 console.log("티디카운트",td_count);
//                 console.log("티디타겟",td_target);

//                 for(i = 0; i < td_count.length; i++){
//                     td_count[i].remove();
//                 }
//                 for(y = 0; y < td_target.length; y++){
//                     for( t =0; t < td_target.length; t++){
//                         var newTD = document.createElement("td");
//                         newTD.textContent = data[y][keys[t]];
//                         td_target[y].appendChild(newTD);
//                     }
//                 }

//             }
//          },error:function(request,status,error){
//             console.log(error);
//         }
//     });
// };






            

  
