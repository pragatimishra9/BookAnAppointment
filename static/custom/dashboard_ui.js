
$(document).ready(function(){ 
    $('#update_timeslots').click(function(){
        
        start_time = $('#day_start').val();
        end_time = $('#day_end').val();
        time_slot = $('#time_slot').val();
        
        $.ajax({
            type: 'POST',
            url: '/dashboard/update_timeslot',
            contentType: 'application/json',
            data: JSON.stringify({ 'start_time': start_time,'end_time':end_time,'time_slot': time_slot}),
            dataType: 'json',
            success: function(result){
                alert("Data updated")
            },
            error: function(data){
                alert("Please Select correct time");
             }
        });
  
    })


});


$(document).ready(function(){ 
    $('.appointment_div').hide();

    var idArray = [];
        $('.doctor_details').each(function () {
            idArray.push(this.id);
        });

    $('.appoinment_btn').click(function(){
        doctor_id = $(this).attr('id').split("_")[3];
        $(this).hide();

        $.each( idArray, function( i, doctor_details_id ){
            if (doctor_details_id.indexOf(doctor_id) == -1){
                $("#"+doctor_details_id).hide();
            }
        });

        doctor_start_time = $("#doctor_start_time_"+doctor_id).val();
        doctor_end_time = $("#doctor_end_time_"+doctor_id).val();
        doctor_time_slot = $("#doctor_time_slot_"+doctor_id).val();

        var start_time_obj = new Date("1/1/1900 " + doctor_start_time);
        var end_time_obj = new Date("1/1/1900 " + doctor_end_time);

        

        var time_slots = [];
        doctor_time_slot = parseInt(doctor_time_slot.split(" ")[0]);

        var current_hour_time = new Date();
        
        
        while(start_time_obj<end_time_obj){
            if (start_time_obj.getHours()>current_hour_time.getHours()){
                slot = start_time_obj.getHours()+":"+start_time_obj.getMinutes();
                start_time_obj.setMinutes(start_time_obj.getMinutes()+parseInt(doctor_time_slot));
                slot += " - "+start_time_obj.getHours()+":"+start_time_obj.getMinutes();
                
                if(start_time_obj<=end_time_obj){
                    time_slots.push(slot);
                }
                
            }
            else{
                start_time_obj.setMinutes(start_time_obj.getMinutes()+parseInt(doctor_time_slot));
            }
            
            
            
        }
        
        time_slot_html = ""
        $.each( time_slots, function( i, time_slot ){
            if ( (i+1)%7 != 0 ){
                
                time_slot_html += '<input type="checkbox" id="'+doctor_id+time_slot+'" style="margin:1%;width:20px;height:20px" class="checkboxes" value="'+time_slot+'"><label for="'+doctor_id+time_slot+'" style="font-size:15px;margin-bottom:1%">'+time_slot+'</label>';
            }
            else{
                time_slot_html += '<input type="checkbox" id="'+doctor_id+time_slot+'" style="margin:1%;width:20px;height:20px" class="checkboxes"><label for="'+doctor_id+time_slot+'" style="font-size:15px;margin-bottom:1%">'+time_slot+'</label></br>';
            }
            
        });
        $("#doctor_time_slot_div_"+doctor_id).html('');
        $("#doctor_time_slot_div_"+doctor_id).html(time_slot_html);
        $('#appointment_div_'+doctor_id).show();
        
    });

    $('.cancel_appointment_btn').click(function(){
        doctor_id = $(this).attr('id').split("_")[3];
        $('#appointment_div_'+doctor_id).hide();
        $('#select_date_time_'+doctor_id).show();
        $.each( idArray, function( i, doctor_details_id ){
            $("#"+doctor_details_id).show();
            
        });
    });





});



$(document).ready(function(){ 
    

    $('.book_appointment_btn').click(function(){
        doctor_id = $(this).attr('id').split("_")[3];

        patient_name = $('#patient_name_'+doctor_id).val();
        patient_email = $('#patient_email_'+doctor_id).val();
        patient_contact = $('#patient_contact_'+doctor_id).val();

        if (patient_name == ""){
            alert("Please Enter Your Name");
        }

        if (patient_email == ""){
            alert("Please Enter Your Email Address");
        }

        if (patient_contact == ""){
            alert("Please Enter Your Contact Number");
        }

        appointment_date = $('#appointment_date_'+doctor_id).val();
        
        if (appointment_date == ""){
            alert("Please Select A Date For Appointment");
        }

        var checked_slots = 0;
        var time_slot = "";
        $('.checkboxes').each( function(){
            if ($(this).is(':checked')){
                checked_slots += 1;
                time_slot = $(this).val();

            }
        });

        if (checked_slots==0){
            alert("Please Select A Time Slot Of For Appointment")
        }

        if (checked_slots>=2){
            alert('Please select only one time slot');
        }
        
        if (appointment_date!="" && checked_slots==1 && patient_name !="" && patient_email !="" && patient_contact != ""){
            $.ajax({
                type: 'POST',
                url: '/dashboard/book_an_appointment',
                contentType: 'application/json',
                data: JSON.stringify({ 'doctor_id': doctor_id,'date':appointment_date,'time_slot': time_slot,'patient_name':patient_name,'patient_email':patient_email,'patient_contact':patient_contact}),
                dataType: 'json',
                success: function(result){
                    alert("Appointment Booked Successfully ..!")
                },
                error: function(data){
                    alert("Sorry We Are Facing Some Issue Please Try Again");
                 }
            });
        }
    });


});
