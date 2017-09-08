function hideForms() {
    // hide evidence type questions
    $("#clinicalTrial").css("display","none");
    $("#metabolic").css("display","none");
    $("#transport").css("display","none");
    $("#caseReport").css("display","none");
    
    $("#inferred-evidencetype-div").css("display","none");
    $("#entered-evidencetype-div").css("display","none");
    $("#agree-with-inferred-div").css("display","none");
    $("#evidencetype-value").attr("value","");

    // hide inclusion criteria questions
    $("#cr-ic-questions-div").css("display","none");
    $("#ct-ic-questions-div").css("display","none");
    $("#ex-mt-ic-questions-div").css("display","none");
    $("#ex-tp-ic-questions-div").css("display","none");

    $("#ic-div").css("display","none");
    $("#agree-with-ic-div").css("display","none");
}

$(document).ready(function(){
    // select high level evidence type (mp method) 
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


    $('#ev-type-disagree').on("click", function(e){
	$("#entered-evidencetype-div").css("display","block");
    });

    
});
