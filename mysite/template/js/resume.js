$(document).ready(function(){
	$(window).bind('scroll',function(){
		if($(window).scrollTop() > 300){
			var right = ($(window).width() - 980)/2 - 48;
			$(".backToTop").addClass("fixed").css('right',right);
		}
		else
			$(".backToTop").removeClass("fixed");
	});
	$('.backToTop').bind('click',function(){
		$(window).scrollTop(0,0);
	});
        $(".contactme a").bind("click",function(){
                            $('.resume-loading').fadeIn();
                            var message_form = {
                                    name : $(".input-name").val(),
                                    email : $(".input-email").val(),
                                    message : $(".contactme-message textarea").val()
                            }
                            $.ajax({
                                    url : "/resume/setMessage/",
                                    data : message_form,
                                    type : "post",
                                    success : function(data){
                                            data = JSON.parse(data);
                                            if(data.code == 0){
						var content = "";
						for(var i = 0;i < data.message.length;i++){
						    if(data.message[i].error.length)
							content += '<p>'+data.message[i].name+':'+data.message[i].error[0]+'</p>';
						}
                                                $(".resume-tip").html(content);
                                            }
                                            else{
						$(".resume-tip").html(data.message);
                                                $('.input-name,.input-email,.contactme-message textarea').val("");
                                            }
                                            $('.resume-loading').fadeOut();
                                    }
                            })
                    });
})
