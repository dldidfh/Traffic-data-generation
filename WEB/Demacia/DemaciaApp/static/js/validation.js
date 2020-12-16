
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
//==============================================================================================================================================================


// 뒤로가기 버튼 
function back(){   
    location.replace("/"); 
}   

//==============================================================================================================================================================


// 회원가입 유효성 검사
function validate() {
    var re = /^[a-zA-Z0-9]{4,12}$/ // 아이디와 패스워드가 적합한지 검사할 정규식
    var id = document.getElementById("user_id");
    var pw = document.getElementById("password");    

    if(!check(re,id,"아이디는 4~12자의 영문 대소문자와 숫자로만 입력")) {
        return false;
    }
    if(!check(re,pw,"패스워드는 4~12자의 영문 대소문자와 숫자로만 입력")) {
        return false;
    }
    if(join.password.value != join.password2.value) {
        alert("비밀번호가 다릅니다. 다시 확인해 주세요.");
        join.password2.value = "";
        join.password2.focus();
        return false;    
    }
    if(join.name.value=="") {
        alert("이름을 입력해 주세요");
        join.name.focus();
        return false;
    }
    
    alert("회원가입이 완료되었습니다.");
}
function check(re, what, message) {
    if(re.test(what.value)) {
        return true;
    }
    alert(message);
    what.value = "";
    what.focus();
    //return false;
}

//==============================================================================================================================================================

// 아이디 유효성 검사
function user_id_check(){
    var user_id = $('#user_id').val()
    var re = /^[a-zA-Z0-9]{4,12}$/ // 아이디와 패스워드가 적합한지 검사할 정규식
    var id = document.getElementById("user_id");
  
    if(!check(re,id,"아이디는 4~12자의 영문 대소문자와 숫자로만 입력")) {
        return false;
    }
    if(user_id === ""){
        alert("아이디를 입력하세요")
    }
    
    $.ajax({
        cache : false,
        // url: "{% url 'user_id_check' %}",
        url: "user_id_check/",
        type: "POST",  
        dataType: 'json',
        data : {'user_id':user_id},
        success:function(data){
            if(data['check']==='no'){
                alert("사용 가능한 아이디 입니다.");
            }
            else{
                alert("사용 불가능한 아이디 입니다."); 
            }
        },
        error: function(data){
            alert("Error");
        }
    })
    
}
//==============================================================================================================================================================


// 로그인
function login_validate() {
   
    if(join.user_id.value=="") {
        alert("이름을 입력해 주세요");
        join.user_id.focus();
        return false;
    }
    if(join.password.value=="") {
        alert("비밀번호를 입력해 주세요");
        join.password.focus();
        return false;
    }
    var user_id = $('#user_id').val()
    var password = $('#password').val()
    var chkbox = join.admin_check.checked;
    var isCheck = false;
    if(chkbox){
        isCheck = true;
    }
    else{
        isCheck = false;
    }
    $.ajax({
        cache : false,
        url: "/login/",  
        type: "POST",  
        dataType: 'json',
        data : {'user_id':user_id, 'password':password, 'isCheck':isCheck},
        success:function(data){
            if(data['check']==='yes'){
                // alert("로그인 되었습니다.");
                location.replace("/");  
            }
            else if(data['check']==='admin_yes'){
                // alert("로그인 되었습니다.");
                location.replace("/admin_home/"); 
            }          
            else if(data['check'] === 'no' || data['check'] === 'admin_no'){
                alert("아이디를 확인하세요.");  
                location.replace("/login/");       
            }     
            else if(data['check'] === 'nopassword' || data['check']==='admin_nopassword'){
                alert("패스워드를 확인하세요.");
                // location.replace("../login/");
                location.replace("/login/");    
            }
            else{
                location.replace("/login/"); 
            }
        },
        error: function(data){
            alert("Error");
            location.replace("/login/"); 
        }
    })
}

// 파일 업로드 정규화
function file_info(){
    var file_name = join.upload_file.value;

    if( file_name){
        var startIndex = (file_name.indexOf('\\') >= 0 ? file_name.lastIndexOf('\\') : file_name.lastIndexOf('/'));
        var filename2 = file_name.substring(startIndex);
        if (filename2.indexOf('\\') === 0 || filename2.indexOf('/') === 0) {
            filename2 = filename2.substring(1);
        }
        document.getElementById("file_name").innerText = filename2;
    }
    else{
        document.getElementById("file_name").innerText = '파일을 선택해주세요.';
    }
}

function load_login_page(){
    location.replace("/login");
}


function upload_file_ajax(){
    var user_id = document.getElementById("user_id").value;
    var csrftoken = getCookie('csrftoken');
    // var formData = new FormData();
    // formData.append("file", $("#ex_file")[0].files[0]);
        if (confirm("업로드 하시겠습니까")){
            var formData = new FormData();
            // upload_file = document.getElementById("ex_file").files;
            formData.append("upload_file", $("#ex_file")[0].files[0]);       
            formData.append("csrfmiddlewaretoken", csrftoken);
            formData.append("user_id",user_id)
            // if (formData.has('file')){return alert(formData.get('file'))} 
            $.ajax({ 
                type : 'POST',
                url :'file_upload/',
                processData : false,
                contentType : false,
                data :  formData,
                success:function(response){ 
                    if (response == "실패"){
                    alert("파일을 확인해 주세요")
                  } else{
                    $("#spead_list").html(response);   
                  }   
                },
          beforeSend: function () {
          var width = 0;
          var height = 0;
          var left = 0;
          var top = 0;
         width = 350;
          height = 350;
          top = ( $(window).height() - height ) / 2 + $(window).scrollTop();
          left = ( $(window).width() - width ) / 2 + $(window).scrollLeft();
          if($("#div_ajax_load_image").length != 0) {
                 $("#div_ajax_load_image").css({
                        "top": top+"px",
                        "left": left+"px"
                 });
                 $("#div_ajax_load_image").show();
          }
          else {
                 $('body').append('<div id="div_ajax_load_image" style="position:absolute; top:' + top + 'px; left:' + left + 'px; width:' + width + 'px; height:' + height + 'px; z-index:9999; background:#f0f0f0; filter:alpha(opacity=50); opacity:alpha*0.5; margin:auto; padding:0; "><img src="../static/img/load.GIF" style="width:350px; height:350px;"></div>');
          }
   }
   , complete: function () {
                 $("#div_ajax_load_image").hide();
                 alert('업로드 성공')
                 location.href = '../video_analysis/';
   }
            }) 
        }
}

    // $(document).on("change", ".file_input", function(){
    //     alert("들어왓냐");
    //     $filename = $(this).val();
        
    //     if($filename == "")
    //     $filename = "파일을 선택해주세요.";
        
    //     $(".file_name").text($filename);
        
    //     })

// 파일 업로드 중복 확인
// function double_check(){
//     $.ajax({
//         cache : false,
//         url: "file_upload/",  
//         type: "POST",  
//         data : {ajax_file:document.getElementById('ex_file').files[0]},
//         success:function(data){
//             alert("성공")
//         },
//         error: function(data){
//             alert("실패");
//         }
//     })
// }
