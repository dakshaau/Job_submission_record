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

	$('#modal_resp_select').change(function(){
		if($(this).val() == 'Yes'){
			$('#modal_resp').text('Yes')
		}else{
			$('#modal_resp').text('No')
		}
	});

	$('#modal_status').click(function(){
		$(this).addClass('hidden');
		$('#modal_status_text').removeClass('hidden');
	});

	$('#modal_status_label').click(function(){
		$('#modal_status').addClass('hidden');
		$('#modal_status_text').removeClass('hidden');
	});

	$('#modal_status_text').dblclick(function(){
		$('#modal_status').text($(this).val());
		$(this).addClass('hidden');
		$('#modal_status').removeClass('hidden');
	});

	$('#modal_status_text').change(function(){
		$('#modal_status').text($(this).val());
	});

	$("tr[name='job_data']").click(function(){
		var job_id = $(this).children(':first-child').text();
		$('#modal_skills').empty();
		$('#modal_status').removeClass('hidden');
		$('#modal_status_text').addClass('hidden');
		$('#modal_resp_select').addClass('hidden');
		$('#modal_resp').removeClass('hidden');
		$('.alert-dismissable').remove();


		// console.log(job_id);
		$.post('/update',
		{
			status: "view",
			ID: job_id
		},
		function(data, status){
			obj = JSON.parse(data);
			$('#modal_id').text(obj.ID);
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

	$('#modal_update').click(function(){
		obj = {
			status: "update",
			ID: $('#modal_id').text(),
			stat: $('#modal_status').text()
		}
		if($('#modal_resp_select').val() == 'Yes'){
			obj.resp = true;
		}else{
			obj.resp = false;
		}
		$.post('/update',obj, function(data, status){
			_obj = JSON.parse(data);
			// console.log(_obj);
			if(_obj.status == 'Success'){
				div = $("<div class='alert alert-success alert-dismissable fade in'></div>");
				a = $("<a href='#' class='close' data-dismiss='alert' aria-label='close'></a>").html('&times;');
				div.append(a);
				strong = $("<strong></strong>").text('Success!')
				div.append(strong);
				div.append(' Application updated.')
				$('.modal-body').append(div)
			}else if(_obj.status == 'Error'){
				div = $("<div class='alert alert-danger alert-dismissable fade in'></div>");
				a = $("<a href='#' class='close' data-dismiss='alert' aria-label='close'></a>").html('&times;');
				div.append(a);
				strong = $("<strong></strong>").text('Error!');
				div.append(strong);
				div.append(' Unable to update application.');
				$('.modal-body').append(div);
			}
		});
	});

});