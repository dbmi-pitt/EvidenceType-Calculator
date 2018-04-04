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
    $("#ic-comment-div").css("display","none");
}

// show specific evidence type form
function showEvidenceQuestionsByMethod(mp_method) {
    if (mp_method == "Case Report") { 
	$("#caseReport").css("display","block");
    } else if (mp_method == "Clinical study") {
	$("#clinicalTrial").css("display","block");		
    } else if (mp_method == "Metabolic Experiment") {
	$("#metabolic").css("display","block");		
    } else if (mp_method == "Transport Experiment") {
	$("#transport").css("display","block");			
    } else {
	console.log("[ERROR] evidence type undefined: " + mp_method);
    }
}

// show specific inclusion criteria form
function showInclusionCriteriaByMethod(mp_method, incCritQL) {
    if (mp_method == "Case Report"){
        $("#cr-ic-questions-div").css("display","block");
    }
    else if (mp_method == "Clinical study") {
        $("#ct-ic-questions-div").css("display","block");
	var icdiv = document.getElementById("ct_ic_table_div");
	var newHtml = '<input id="confirmedEvType-value" value="Clinical study" type="hidden" name="confirmedEvType" />';
	newHtml += '<table style="width:100%">'
	var n = i;
	var curGroup = "";
	for (var i = 0; i < incCritQL.length; i++) {
	    n = i + 1;
	    if (curGroup !== incCritQL[i]["icGroup"]){
		curGroup = incCritQL[i]["icGroup"]
		newHtml += '<tr><td style="width:50%"><h3>'+ incCritQL[i]["icGroup"] + '</h3></td><td/><td/><td/></tr>';
	    }

	    if (i % 2 == 0){
 		newHtml += '<tr style="background-color:#def2ef">';
	    } else {
		newHtml += '<tr>';
	    }
	    newHtml += '<td style="width:50%"><label data-toggle="tooltip" data-placement="right" title="Tooltip on right">' + n + '. ' +  incCritQL[i]["icText"] + '&nbsp;<a target="new" href="../static/pdf/FDA-2017-guidance-on-clinical-DDI-evalutations-UCM292362.pdf#nameddest=' + incCritQL[i]["icSourceRef"].replace(/ /g,"") + '">' + incCritQL[i]["icSourceRef"] + '</a></label></td>';
	    newHtml += '<td style="width:20%"><label class="radio-inline"><input type="radio" name="' + incCritQL[i]["icID"] + '" ng-model="myVar" value="yes">Yes</label></td>';
	    newHtml += '<td style="width:20%"><label class="radio-inline"><input type="radio" name="' + incCritQL[i]["icID"] + '" ng-model="myVar" value="no">No</label></td>';
	    newHtml += '<td style="width:20%"><label class="radio-inline"><input type="radio" name="' + incCritQL[i]["icID"] + '" ng-model="myVar" value="unsure">Unsure/NA</label></td>';
	    newHtml += '</tr>';
	}
	newHtml += '</table>';
	icdiv.innerHTML = newHtml;
    }

    else if (mp_method == "Metabolic Experiment"){
        $("#ex-mt-ic-questions-div").css("display","block");
    }
    else if (mp_method == "Transport Experiment"){
        $("#ex-tp-ic-questions-div").css("display","block");
    }
    else {
	console.log("[ERROR] evidence type undefined: " + mp_method);
    }
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
	$("#evidencetype-value").attr("value","Clinical study");
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

    $('#ic-agree').on("click", function(e){
	$("#ic-comment-div").css("display","block");
	$("#agree-with-ic-div").css("display","none");
    });

    $('#ic-disagree').on("click", function(e){
	$("#ic-comment-div").css("display","block");
	$("#agree-with-ic-div").css("display","none");
    });
    
});
