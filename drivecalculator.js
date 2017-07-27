$(document).ready(function(){
	$('.dropdown-menu a.test').on("click", function(e){
		$(this).next('ul').toggle();
		e.stopPropagation();
		e.preventDefault();
	});

	$('.dropdown-menu a#1').click(function(e) {
		e.preventDefault();
		//alert("hi");
		$("#caseReport").css("display","block");
		$("#clinicalTrial").css("display","none");
		$("#metabolic").css("display","none");
		$("#transport").css("display","none");

	});

	$('.dropdown-menu a#2').click(function(e) {
		e.preventDefault();
		//alert("hi");
		$("#caseReport").css("display","none");
		$("#clinicalTrial").css("display","block");
		$("#metabolic").css("display","none");
		$("#transport").css("display","none");
	});

	$('.dropdown-menu a#3').click(function(e) {
		e.preventDefault();
		//alert("hi");
		$("#caseReport").css("display","none");
		$("#clinicalTrial").css("display","none");
		$("#metabolic").css("display","block");
		$("#transport").css("display","none");
	});

	$('.dropdown-menu a#4').click(function(e) {
		e.preventDefault();
		//alert("hi");
		$("#caseReport").css("display","none");
		$("#clinicalTrial").css("display","none");
		$("#metabolic").css("display","none");
		$("#transport").css("display","block");
	});

	$(document).on('click','#calculate', function(){
		doConfirm("The criteria you enter indicates that the evidence type is... is this consistent with your interpretation?", function yes()
			{
			   // go to inclusion criteria
			}, function no()
			{
			    // go to comments
			});
	});

});

function doConfirm(msg, yesFn, noFn)
{
    var confirmBox = $("#confirmBox");
    confirmBox.find(".message").text(msg);
    confirmBox.find(".yes,.no").unbind().click(function()
    {
        confirmBox.hide();
    });
    confirmBox.find(".yes").click(yesFn);
    confirmBox.find(".no").click(noFn);
    confirmBox.show();
}