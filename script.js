// Code goes here
$(document).ready(function() {
	hideAddForm();
	$('.info').text('');
	getAppointments();
	var dateToday = new Date();
	$('#date').datepicker({minDate: dateToday});
	$('#search').on('click',function(){
		$('.info').text('');
		getAppointments($('#query_str').val());
	})
});

function addForm(){
	if($('#new').val() == 'New' ){
		showAddForm();
	}else{
		submitForm();
	}
}

function showAddForm() {
	$('#add_form').show();
	$('#cancel').show();
	$('#new').val('Add');
}

function hideAddForm() {
	$('#add_form').hide();
	$('#cancel').hide();
	$('#new').val('New')	;
}

function validateAppointmentForm(){
	var isFormValid = true;
	var dateValue = $('#date').val();
	var timeValue = $('#time').val();
	$('#date-error').text(' ');
	$('#time-error').text(' ');
	
	if(dateValue == ''){
		$('#date-error').text("Date field is empty");
		isFormValid = false;
	}else{
		var isValidDate = /^(?:(0[1-9]|1[012])[\- \/.](0[1-9]|[12][0-9]|3[01])[\- \/.](19|20)[0-9]{2})$/.test(dateValue);
		if(!isValidDate){
			$('#date-error').text("Invalid date format: " +dateValue);
			$('#date').focus();
			isFormValid = false;
		}
	}
	if(timeValue == ''){
		$('#time-error').text("Time field is empty");
		isFormValid = false;
	}else{
		var isValidTime = /^([0-1]?[0-9]|2[0-4]):([0-5][0-9])(:[0-5][0-9])?(\s)*([apAP][Mm])?$/.test(timeValue);
		if(!isValidTime){
			$('#time-error').text("Invalid time format: " + timeValue);
			$('#time').focus();
			isFormValid = false;
		}
	}
	return isFormValid;
}

function submitForm() {
   if(validateAppointmentForm()){
       $('#appointmentForm').submit();
	   $('.info').text();
   }
}

function isShowTable(appointmentsData) {
	if($.isEmptyObject(appointmentsData)){
		return false;
	} else {
		return true;
	}
}

function getAppointments(searchString) {
	var url = "/index.cgi";
	url += "?ajax=getAppointments";
	if (searchString && searchString != '') {
		url += "&searchString=" + searchString;
	}
	$.ajax({
		url: url,
		type: "GET",
		dataType: "json",
		contentType: "application/json; charset=utf=8"
	}).success(function(data) {
		if(typeof(searchString) != 'undefined' && searchString != ''){
			if(data.length == '0'){
				$('.info').text(searchString +' No match(es) found');
				return getAppointments();
			}else{
				var resultFound = data.length+' Match(es) found for '+searchString;
				$('.info').text(resultFound);
			}
			
		}
		showTable(data);
	}).error(function(jqXHR,status){
		$('.info').text('Error while fatching data. Please try again')
		console.log('Error while fatching data: '+jqXHR);
	});
}

function showTable(appointmentsData) {
	if (isShowTable(appointmentsData)) {
		$('#appointmentTable').show();
		$('#appointmentTable td').parent().remove();
		for (var i = 0; i < appointmentsData.length; i++) {
			drawRow(appointmentsData[i]);
		}
	}
}

function drawRow(rowData) {
	var row = $("<tr />");
	$('#appointmentTable').append(row);
	row.append($("<td class='no-word-wrap'>" + rowData.date + "</td>"));
	row.append($("<td class='no-word-wrap'>" + rowData.time + "</td>"));
	row.append($("<td>" + rowData.desc + "</td>"));
}
