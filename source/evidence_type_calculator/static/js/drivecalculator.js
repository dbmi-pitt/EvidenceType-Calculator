// var crStatus = false;
// var ctStatus = false;
// var emStatus = false;
// var etStatus = false;
var method = null

function hideForms() {
    $("#clinicalTrial").css("display","none");
    $("#metabolic").css("display","none");
    $("#transport").css("display","none");
    $("#caseReport").css("display","none");
    $("#evidence-type-field").css("display","none");
    $("#evidencetype-value").attr("value","");
}

$(document).ready(function(){
    
    $('.dropdown-menu a.test').on("click", function(e){
	$(this).next('ul').toggle();
	e.stopPropagation();
	e.preventDefault();
    });

    $('.dropdown-menu a#1').click(function(e) {
	e.preventDefault();
	hideForms();
	$("#caseReport").css("display","block");
	$("#evidencetype-value").attr("value","Case Report");
	crStatus = true;
	$(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
    });

    $('.dropdown-menu a#2').click(function(e) {
	e.preventDefault();
	hideForms();
	$("#clinicalTrial").css("display","block");
	$("#evidencetype-value").attr("value","DDI clinical trial");
	ctStatus = true;
	$(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
    });

    $('.dropdown-menu a#3').click(function(e) {
	e.preventDefault();
	hideForms();
	$("#metabolic").css("display","block");
	$("#evidencetype-value").attr("value","Metabolic Experiment");
	emStatus = true;
	$(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
	$("#transport").css("display","none");
    });

    $('.dropdown-menu a#4').click(function(e) {
	e.preventDefault();
	hideForms();
	$("#transport").css("display","block");
	$("#evidencetype-value").attr("value","Transport Experiment");
	etStatus = true;
	$(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
    });
    
    // $(document).on('click','#calculate', function(){
    // 	doConfirm("The criteria you enter indicates that the evidence type is... is this consistent with your interpretation?",
    // 		  function yes()
    // 		  {
    // 		      // go to inclusion criteria
    // 		      $("#calculateTwo").css("display","block");
    // 		      $("#comments").css("display","none");
    // 		      if (crStatus == true){
    // 			  $("#caseReportIC").css("display","block");
    // 		      } else if (ctStatus == true){
    // 			  $("#clinicalTrialIC").css("display","block");
    // 		      } else if (emStatus == true){
    // 			  $("#metabolicIC").css("display","block");
    // 		      } else if (etStatus == true){
    // 			  $("#transportIC").css("display","block");
    // 		      } else {
    // 			  alert("oh no! We can't find which evidence type you selected to display inclusion criteria.");
    // 		      }
		      
    // 		  }, function no()
    // 		  {
    // 		      // go to commenting
    // 		      $("#comments").css("display","block");
    // 		      $("#clinicalTrialIC").css("display","none");
    // 		      $("#metabolicIC").css("display","none");
    // 		      $("#transportIC").css("display","none");
    // 		      $("#calculateTwo").css("display","none");
		      
    // 		  });
    // });
    
    // $(document).on('click','#continue', function(){
    // 	// go to inclusion criteria
    // 	$("#calculateTwo").css("display","block");
    // 	$("#comments").css("display","none");
    // 	if (crStatus == true){
    // 	    $("#caseReportIC").css("display","block");
    // 	} else if (ctStatus == true){
    // 	    $("#clinicalTrialIC").css("display","block");
    // 	} else if (emStatus == true){
    // 	    $("#metabolicIC").css("display","block");
    // 	} else if (etStatus == true){
    // 	    $("#transportIC").css("display","block");
    // 	} else {
    // 	    alert("oh no! We can't find which evidence type you selected to display inclusion criteria.");
    // 	}
    // });
    
    // $(document).on('click','#calculateTwo', function(){
    // 	//alert("hi");
    // 	doConfirmTwo("The evidence criterion for this type is sufficient/insufficient because it fails to satisfy the following criterion:A. Is this consistent with your interpretation?", function yes()
    // 		     {
    // 			 //DONE!
    // 			 $("#lastStep").css("display","block");
    // 			 $("#commentsTwo").css("display","none");
    // 			},  function no()
    // 		     {
    // 			 // go to commenting part 2
    // 			 $("#commentsTwo").css("display","block");
    // 			 $("#lastStep").css("display","none");
    // 		     });
    // });
    
    // $(document).on('click','#complete', function(){
    // 	// DONE! go to final page
    // 	$("#comments").css("display","none");
    // 	$("#commentsTwo").css("display","none");
    // 	$("#lastStep").css("display","block");
    // });
    
    // $(document).on('click','#goBack', function(){
    // 	// ??? How do this?
    // 	$("#comments").css("display","block");
    // 	$("#commentsTwo").css("display","block");
    // });
    
    // $(document).on('click','#new', function(){
    // 	// start anew
    // 	window.location.reload();
    // });
    
});

// function doConfirm(msg, yesFn, noFn){
//     var confirmBox = $("#confirmBox");
//     confirmBox.find(".message").text(msg);
//     confirmBox.find(".yes,.no").unbind().click(function()
//     {
//         confirmBox.hide();
//     });
//     confirmBox.find(".yes").click(yesFn);
//     confirmBox.find(".no").click(noFn);
//     confirmBox.show();
// }

// function doConfirmTwo(msg, yesFn, noFn){
//     var confirmBoxTwo = $("#confirmBoxTwo");
//     confirmBoxTwo.find(".message").text(msg);
//     confirmBoxTwo.find(".yes,.no").unbind().click(function()
//     {
//         confirmBoxTwo.hide();
//     });
//     confirmBoxTwo.find(".yes").click(yesFn);
//     confirmBoxTwo.find(".no").click(noFn);
//     confirmBoxTwo.show();
// }
