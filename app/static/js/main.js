$(document).ready(function(){

    var next = 1;
    $(".add-more").click(function(e){
      console.log("Test");

        e.preventDefault();
        var addto = "#field" + next;
        var addRemove = "#field" + (next);
        next = next + 1;
        var newIn = '<input autocomplete="off" class="input form-control" id="food' + next + '" name="field' + next + '" type="text">';
        // var newIn2 = = '<input autocomplete="off" class="input form-control" id="cost' + next + '" name="field' + next + '" type="text">';
        var newInput = $(newIn);
        // var newInput2 = $(newIn2);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >-</button></div><div id="food">';
        var removeButton = $(removeBtn);
        $(addto).append(newInput);
        // $(addto).after(newInput2);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#field" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
            });
    });



});
