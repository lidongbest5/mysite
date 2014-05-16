var util = {
	content_index : 1,
	scrolling : false,
	getAjaxData : function(content_index){
		util.unbindAutoLoad();
		$('.saying-loading').show();
		$.ajax({
			url : '/sayingContent/'+util.content_index+'/',
			type : 'get',
			dataType: 'json',
			success : function(data){
				$(data.data).insertBefore('.saying-loading');
				if(data.hasMore == "true"){
					util.bindAutoLoad();
					$('.saying-loading').hide();
				}
				else{
					util.unbindAutoLoad();
					$('.saying-loading').css('background','none').html('That\'s enough...Thanks for visiting...');
				}
			}
		})
	},
	bindAutoLoad : function(){
		util.scrolling = false;
		$(window).bind("scroll",util.scrollLoad);
	},
	unbindAutoLoad : function(){
		$(window).unbind("scroll",util.scrollLoad);
	},
	scrollLoad : function(){
		if(!util.scrolling){
			var doc = $(document);
			util.scrolling = true;
			if(doc.height() - doc.scrollTop()-$(window).height()<100 ){
				util.getAjaxData(util.content_index++);
			}else{
				util.scrolling = false;
			}		
		}
	}
}
$(document).ready(function(){
	util.getAjaxData(util.content_index);
	$('.wrapper').delegate('.feed','mouseover',function(){
		var This = $(this);
		This.addClass('feed-hover');
	});
	$('.wrapper').delegate('.feed','mouseleave',function(){
		var This = $(this);
		This.removeClass('feed-hover');
	});
	$('.wrapper').delegate('.feed','click',function(){
		var This = $(this);
		if(This.hasClass('feed-active')){
			This.removeClass('feed-active');
			This.find('.reply-form').removeClass('reply-active').find('textarea').html('Reply to this saying...');
			This.find('.expand').html("Expand");
		}
		else{
			This.addClass('feed-active');
			This.find('.expand').html("Hide");
		}
	});
	$('.wrapper').delegate('.feed textarea','click',function(){
		var This = $(this);
		This.parent().addClass('reply-active');
		This.html("").focus();
		return false;
	});
	$('.wrapper').delegate('.feed input','click',function(){
		var This = $(this);
		return false;
	});
	$('.wrapper').delegate('.feed input','focus',function(){
		var This = $(this);
		if(This.attr('value') == 'Your name...')
			This.attr('value','').css('color','black');
	});
	$('.wrapper').delegate('.feed input','blur',function(){
		var This = $(this);
		if(This.attr('value') == '')
			This.attr('value','Your name...').css('color','#AAA');
	});
	$('.wrapper').delegate('.reply-form a','click',function(){
		var This = $(this);
		This.parent().find('i').show();
		input_val = This.parent().find('input').val();
		if(This.parent().find('input').val() == 'Your name...')
			input_val = '';
		$.ajax({
			url : '/saying/setReply/',
			type : 'post',
			data : {"SayingId":parseInt(This.attr('id')),"name":input_val,"content":This.parent().find('textarea').val()},
			success : function(data){
				data = JSON.parse(data);
				This.parent().find('p').hide();
				if(data.code == 1){
					This.parent().parent().find('ul').append(data.data.split('utf-8')[1]);
					This.parent().parent().find('.reply-form').removeClass('reply-active');
				}
				else{
					var content = '';
					for(var i = 0;i < data.data.length;i++){
						if(data.data[i].error.length)
							content += data.data[i].name+':'+data.data[i].error[0]+'<br/>';
					}
					This.parent().find('p').html(content).show();
				}
				This.parent().find('i').hide();
			}
		});
		return false;
	});
	$('.wrapper').delegate('.reply','click',function(){
		var This = $(this);
		ThisParent = This.parent().parent().parent().parent();
		if(ThisParent.hasClass('feed-active') && ThisParent.find('.reply-form').hasClass('reply-active'))
			return false;
		else if(ThisParent.hasClass('feed-active')){
			ThisParent.find('textarea').trigger('click');
			return false;
		}
		else
			ThisParent.find('textarea').trigger('click');
	});
	$('.wrapper').delegate('.favourite','click',function(){
		var This = $(this);
		This.find('i').css('display','inline-block');
		$.ajax({
			url : '/saying/setFavourite/',
			type : 'post',
			data : {"num":parseInt(This.attr('num'))+1,"id":This.attr('id')},
			success : function(data){
				data = JSON.parse(data);
				This.html('Favourite('+data.favourite+')<i></i>').css('color','#FF9B00').attr('num',data.favourite).find('i').css('display','none');
			}
		});
		return false;
	});
	$('.wrapper').delegate('.imgcontainer img','click',function(){
		var This = $(this);
		if(parseInt(This.css('width')) == 120){
			This.css('width','auto');
			This.parent().addClass('imgbig');
		}
		else{
			This.css('width',120);
			This.parent().removeClass('imgbig');
		}
		return false;
	});
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
})
