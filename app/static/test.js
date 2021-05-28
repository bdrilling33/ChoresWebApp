 $(document).on('click', '.btn-delete', function() {
    var chore_id = $(this).attr("id");
    $.ajax({
        url:"/chore_select",
        method:"POST",
        data:{chore_id:chore_id},
        success:function(data) {
            $('#deleteChore').modal('show');
            var chore_rs = JSON.parse(data);
            $('#viewid').val(chore_rs[0]['id']);
            $('#viewdesr').val(chore_rs[0]['description']);
           }
        });
    });
