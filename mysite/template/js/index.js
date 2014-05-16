var util = {
	setError : function(data){
		for(var i = 0;i < data.length;i++){
			var old_text = $('.comment-form p[type="'+data[i].name+'"]').html();
			if(data[i].error.length)
				$('.comment-form p[type="'+data[i].name+'"]').html(old_text+'<span class="error">'+data[i].error[0]+'</span>');
		}
	}
}
$(document).ready(function(){
	$(".comment-form a").bind("click",function(){
		$('.loading').fadeIn();
		$('.error').remove();
		var comment_form = {
			blogid : $(".comment-form").attr("blogid"),
			name : $(".comment-form input:eq(0)").val(),
			email : $(".comment-form input:eq(1)").val(),
			website : $(".comment-form input:eq(2)").val(),
			message : $(".comment-form textarea").val()
		}
		$.ajax({
			url : "/blog/setComment/",
			data : comment_form,
			type : "post",
			success : function(data){
				data = JSON.parse(data);
				if(data.code == 0){
					util.setError(data.message);
				}
				else{
					if($(".content-comment section").hasClass("comment-box")){
						var comment_len = parseInt($(".comment-box h4").attr("len"))+1;
						$(".comment-box h4").html('COMMENTS('+comment_len+')').attr("len",comment_len);
					}
					else{
						$(".content-comment").prepend('<section class="comment-box"><h4 len="1">COMMENTS(1)</h4><ul></ul></section>');
					}
					var current_date = new Date();
					$(".comment-box ul").append('<li><div class="comment-avatar"><img src="/static/images/head.png" width=75 height=75></div><div class="comment-meta"><h5>'+data.message.name+'</h5><p>'+String(current_date).substring(3,16)+'</p></div><div class="comment-content"><p>'+data.message.message+'</p></div></li>');
					$('.comment-form input,.comment-form textarea').val("");
				}
				$('.loading').fadeOut();
			}
		})
	});
    	$('.search-submit').bind('click',function(){
		if($('.search-box').val() == "")
			return false;
	});
	$(window).bind('scroll',function(){
		if($(window).scrollTop() > 980){
			var right = ($(window).width() - 980)/2 + 100;
			$(".backToTop").addClass("fixed").css('right',right);
		}
		else
			$(".backToTop").removeClass("fixed");
	});
	$('.backToTop').bind('click',function(){
		$(window).scrollTop(0,0);
	});
})
