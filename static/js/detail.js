$(function () {

    // write csrf
    $.getScript("/static/js/csrftoken.js");

    // like
    $("#like").click(function(){
      var video_id = $("#like").attr("video-id");
      $.ajax({
            url: '/video/like/',
            data: {
                video_id: video_id,
                'csrf_token': csrftoken
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var code = data.code
                if(code == 0){
                    var likes = data.likes
                    var user_liked = data.user_liked
                    $('#like-count').text(likes)
                    if(user_liked == 0){
                        $('#like').removeClass("grey").addClass("red")
                    }else{
                        $('#like').removeClass("red").addClass("grey")
                    }
                }else{
                    var msg = data.msg
                    alert(msg)
                }

            },
            error: function(data){
              alert("Like failed")
            }
        });
    });

     // collect
    $("#star").click(function(){
      var video_id = $("#star").attr("video-id");
      $.ajax({
            url: '/video/collect/',
            data: {
                video_id: video_id,
                'csrf_token': csrftoken
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var code = data.code
                if(code == 0){
                    var collects = data.collects
                    var user_collected = data.user_collected
                    $('#collect-count').text(collects)
                    if(user_collected == 0){
                        $('#star').removeClass("grey").addClass("red")
                    }else{
                        $('#star').removeClass("red").addClass("grey")
                    }
                }else{
                    var msg = data.msg
                    alert(msg)
                }

            },
            error: function(data){
              alert("Collection failed")
            }
        });
    });


    // submit comments
    var frm = $('#comment_form')
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            dataType:'json',
            data: frm.serialize(),
            success: function (data) {
                var code = data.code
                var msg = data.msg
                if(code == 0){
                    $('#id_content').val("")
                    $('.comment-list').prepend(data.html);
                    $('#comment-result').text("Comment successful")
                    $('.info').show().delay(2000).fadeOut(800)
                }else{
                    $('#comment-result').text(msg)
                    $('.info').show().delay(2000).fadeOut(800);
                }
            },
            error: function(data) {
            }
        });
        return false;
    });

})





