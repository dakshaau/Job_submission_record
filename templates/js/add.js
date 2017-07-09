$(document).ready(function(){

    $("[name='skills']").attr('required','true')
    $("#other_skills").attr('required','true')

    $("[name='portals']").change(function(){
        if($(this).val() == "Other"){
        	$("#other_portal").parent().removeClass("hidden");
        	$("#other_portal").attr("required",'true')
        }
        else{
        	$("#other_portal").removeAttr("required")
        	$("#other_portal").parent().addClass("hidden");
        }
    });

   	$("#country").change(function(){
   		if($(this).val() == "Other"){
   			$("[name='other_country']").parent().removeClass('hidden')
   			$("[name='other_country']").attr('required','true')
   		}
   		else{
   			$("[name='other_country']").removeAttr('required')
   			$("[name='other_country']").parent().addClass('hidden')
   		}
   	});

   	$("[name='skills']").change(function(){
   		if($(this).is(':checked') == true){
   			$("[name='skills']").removeAttr('required')
   			$('#other_skills').removeAttr('required')
   		}
   		else{
   			$("[name='skills']").attr('required','true')
   			$('#other_skills').attr('required','true')
   		}
   	});

   	$('#other_skills').change(function(){
   		if($('#other_skills').val() != ""){
   			$("[name='skills']").removeAttr('required');
		    $(this).removeAttr('required');
   		}
   		else{
   			$("[name='skills']").attr('required','true')
   			$(this).attr('required','true')
   		}
   	});

   	$('#clear').click(function(){
   		window.location.replace('/');
   	});

});