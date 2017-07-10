$(document).ready(function(){

	$('#modal_resp').click(function(){
		$(this).addClass('hidden');
		$('#modal_resp_select').removeClass('hidden');
	});

	$('#modal_resp_select').dblclick(function(){
		if($(this).val() == 'Yes'){
			$('#modal_resp').text('Yes')
		}else{
			$('#modal_resp').text('No')
		}
		$(this).addClass('hidden');
		$('#modal_resp').removeClass('hidden');
	});

	$('#modal_status').click(function(){
		$(this).addClass('hidden');
		$('#modal_status_text').removeClass('hidden');
	});

	$('#modal_status_text').dblclick(function(){
		$('#modal_status').text($(this).val());
		$(this).addClass('hidden');
		$('#modal_status').removeClass('hidden');
	});

	$("tr[name='job_data']").click(function(){
		var job_id = $(this).children(':first-child').text();
		// console.log(job_id);
		$.post('/update',
		{
			status: "view",
			ID: job_id
		},
		function(data, status){
			obj = JSON.parse(data);
			$('#modal_comp').text(obj.company);
			$('#modal_pos').text(obj.pos);
			$('#modal_pid').text(obj.p_id);
			$('#modal_date').text(obj.date);
			$('#modal_country').text(obj.country);
			$('#modal_loc').text(obj.loc);
			$('#modal_portal').text(obj.portal);
			$('#modal_status').text(obj.status);
			$('#modal_status_text').val(obj.status);
			if(obj.resp == true){
				$('#modal_resp').text('Yes');
				$("#modal_resp_select").val('Yes').prop('selected',true);
			} else{
				$('#modal_resp').text('No');
				$("#modal_resp_select").val('No').prop('selected',true);
			}
			var ind = 0
			for(i = 0; i < obj.skills.length; i++){
				if(i == 30){
					break;
				}
				if(i%10 == 0){
					var div = $("<div class='col-sm-4'></div>");
					var ul = $("<ul></ul>");
					ind += 1;
					div.append(ul);
					$('#modal_skills').append(div);
				}
				li = $("<li></li>").text(obj.skills[i]);
				console.log(ind)
				var ul = $('#modal_skills').children('div:nth-of-type('+(ind)+')').children(':first-child').append(li);
			}
			$('#job_detail').modal();
		});
	});

});