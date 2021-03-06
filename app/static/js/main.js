// on enter while on search
$("#search").keyup(function(event){
    var enterKey = 13
    if(event.keyCode == enterKey ){
        $(".search-button").click();
    }
});

var categoryData;

$('.search-button').on('click', function(evt){

    var searchEl = $("#search");
    var inputURL = searchEl.val();

    // Do some more sanity check to ensure its a valid URL.
    if (inputURL.indexOf('www') != -1){

        // show up the wheel and hide any previously showing data
        $('.loader').removeClass('hide');
        $('.data-wrap').addClass('hide');

        searchEl.attr('disabled', true);
     
        $.get('classify_business', {business_name: JSON.stringify(inputURL)}, function(data){
            data = JSON.parse(data);
            if (data){
                categoryData = data;
                setLabels(data.labels);
                $('#tag-container').html("");
                $('.data-name').html(data.name);
                
                var probability = data.type.probability * 100;
                probability = probability.toString().substring(0,5);

                var label = data.type.label;
                label = label.replace(/_/g, ", ")

                $('.data-business').html(label + ' | ' + probability + '%');
                $('.loader').addClass('hide');
                $('.data-wrap').removeClass('hide');
            }
            searchEl.removeAttr('disabled');
        });
    }
});

function setLabels(data){
    var labels = new Array();
    for(var key in data) {
        if(data.hasOwnProperty(key)) {
            labels.push(key);
        }
    }

    $('.data-categories').html("");
    for(var i = 0; i < labels.length; i++){
        $('.data-categories').append("<li><div class='todo-content todo-name'>" + labels[i] + "</div></li>");    
    }
    
    $('.todo li').click(function() {
        $(this).toggleClass('todo-done');
    
        var allCategories = $('.data-categories').children('li');
        var clickedCategories = new Array();

        for(var i = 0; i < allCategories.length; i++){
            if(allCategories[i].className === "todo-done"){
                clickedCategories.push(allCategories[i].textContent);
            }
        }
        
        $('#tag-container').html("");
        for(var i = 0; i < clickedCategories.length; i++){
            var categoryContent = categoryData.labels[clickedCategories[i]];

            var outputHTML = '<div class="span6 data-item noRightMargin"><div class="label label-large label-primary span3">' + 
                            clickedCategories[i] + '</div>';

            var content = "";
            for(var j = 0; j < categoryContent.length; j++){
                content += '<span class="tag"><span>' +  categoryContent[j] + '</span></span>';
            }

            outputHTML += '<div class="span6 data-item noRightMargin">' +
                    '<input name="tagsinput" class="tagsinput tagsinput-primary" style="display: none;">' + 
                    '<div class="tagsinput tagsinput-primary">' + content +
                    '</div></div></div>';
            $('#tag-container').append(outputHTML);
        }
    });
}


//this is the data that is obtained by making a call to 
//businesscategories.getCategories()
var data;
var selectOptionsHTML='';
var selectOptionsNewCategory='';
$(function() {
    $.ajax({
        url: '/business_categories',
    }).done(function(get_request){
        selectOptionsHTML += '<option>Select Category</option>';
        selectOptionsNewCategory += '<option>Select Existing Directory</option>';
        data = JSON.parse(get_request);
        $.each(data, function(key, val){
            recursiveFunction(key, val);
        });
        $('#categoryA_select').html(selectOptionsHTML);
        $('#categoryB_select').html(selectOptionsHTML);
        $('#directory_select').html(selectOptionsNewCategory);
        $("select").selectpicker({
            style: 'btn-inverse',
            menuStyle: 'dropdown-inverse'
        });
    });
});

//used to set up the categories in the drop down select menu
function recursiveFunction(key, val) {
    if (val instanceof Array) {
        makeOption(key);
    } else if (val instanceof Object) {
        makeDirOption(key);
        $.each(val, function(key, value) {
            recursiveFunction(key, value);
        });
    }
}

//helper for recursiveFunction
//simply makes html that will be put into the select element
function makeOption(key) {
    selectOptionsHTML += '<option>' + key + '</option>';
}

//helper for recursiveFunction
//simply makes html that will be put into the directory select in modal
function makeDirOption(key) {
    selectOptionsNewCategory += '<option>' + key + '</option>';
}

//This makes the two main boxes with the draggable items droppable
//which means it allows elements with draggable class to be put into
//these boxes
$(function() {
    $("#catATags_tagsinput").droppable({
      accept: "#catBTags_tagsinput > span",
      drop: function( event, ui ) {
        var select_option = $("#categoryA_select").val();
        if(select_option != "Select Category") {
            deleteSpan( ui.draggable, "#catBTags_tagsinput", "#catATags_tagsinput");
        }
      }
    });

    $("#catBTags_tagsinput").droppable({
      accept: "#catATags_tagsinput > span",
      drop: function( event, ui ) {
        var select_option = $("#categoryB_select").val();
        if(select_option != "Select Category") {
            deleteSpan(ui.draggable, "#catATags_tagsinput", "#catBTags_tagsinput");
        }
      }
    });
});

//helper for when an element is dropped in the opposite box, need to remove it
//from its original box and add it to its new box
function deleteSpan($item, removeFrom, moveTo) {
    var $list = $(moveTo);
    $item.find(removeFrom).remove();
    $item.appendTo($list);
    updateData($item.text(), moveTo);
}

//this function updates the data dictionary, which stores information
//about what terms belong to what categories
function updateData(item, moveTo) {
    var fromCat, toCat;
    if(moveTo == "#catATags_tagsinput") {
        toCat = $("#categoryA_select").val();
        fromCat = $("#categoryB_select").val();
    } else {
        toCat = $("#categoryB_select").val();
        fromCat = $("#categoryA_select").val();
    }

    searchForItemAndRemove(item, data, fromCat);
    searchForLocationAndAdd(item, data, toCat);
}

function searchForItemAndRemove(item, obj, from) {
    $.each(obj, function(key, val) {
        if(from == key && $.isArray(val)) {
            val.splice(val.indexOf(item), 1);
            return;
        } else if(!$.isArray(val)) {
            searchForItemAndRemove(item, val, from);
        }
    });
}

function searchForLocationAndAdd(item, obj, to) {
    $.each(obj, function(key, val) {
        if(to == key && $.isArray(val)) {
            val.push(item);
            return;
        } else if(!$.isArray(val)) {
            searchForLocationAndAdd(item, val, to);
        }
    });
}

//This function helps to find the words that will be made into
//draggable tags when something from the dropdown menu is selected
var wordsList = [];
function searchForKey(key, obj) {
    $.each(obj, function(term, val){
        if(key == term && $.isArray(val)) {
            wordsList = val;
        } else if(!$.isArray(val)) {
            searchForKey(key, val);
        }
    });
}

//simply checks whether obj has this key
//returns true if it does exist
var keyExists = false;
function startKeySearch(key, obj) {
    keyExists = false;
    doesKeyExist(key, obj);
}

function doesKeyExist(key, obj) {
    $.each(obj, function(term, val){
        if(key == term && !$.isArray(val)) {
            keyExists = true;
        } else if(!$.isArray(val)) {
            doesKeyExist(key, val);
        }
    });
}

//simply adds the category to the directory if the category does
//not exists already
//the catDirDir flag if true means create another directory in the found directory
var catAlreadyExists = false;
var dirAlreadyExists = false;
function startAddingCategoryToDir(dir1, dir2, cat, obj, catDirDir) {
    catAlreadyExists = false;
    dirAlreadyExists = false;
    addCategoryToDirectory(dir1, dir2, cat, obj, catDirDir);
}

function addCategoryToDirectory(dir1, dir2, cat, obj, flag) {
    $.each(obj, function(term, val){
        if(dir1 == term && !$.isArray(val)) {
            if(flag) {
                if(dir2 in val) {
                    dirAlreadyExists = true;
                } else {
                    val[dir2] = {};
                    val[dir2][cat] = [];
                }
            } else {
                if(cat in val) {
                    catAlreadyExists = true;
                } else {
                    val[cat] = [];
                }
            }
        } else if(!$.isArray(val)) {
            addCategoryToDirectory(dir1, dir2, cat, val, flag);
        }
    });
}

//this functions finds all elements with draggable class
// and makes them draggable using the JQuery API
function setDraggable() {
    $('.draggable').draggable({
        revert: "invalid",
        containment: "document",
        helper: "clone",
    });
}

/*
helper: function (e,ui) {
    return $(this).clone().appendTo($(this));
},
containment: "#draggable_container"
*/

//This following 2 onChange functions do the following
//when the select option changes we need to fill in the box below
//with the words for that category which will be draggable items
$("#categoryA_select").change(function() {
    key = $(this).val();
    if(key != "Select Category") {
        searchForKey(key, data);
        var catA_HTML = '';
        for (var i in wordsList) {
            var word = wordsList[i]
            catA_HTML += '<span class="tag draggable"><span>' + word + 
            '<a class="tagsinput-remove-link"></a></span></span>';
        }
        $('#catATags_tagsinput').html(catA_HTML);
        setDraggable();
        setTagRemoval($("#categoryA_select").val());
    } else {
        $('#catATags_tagsinput').html('');
    }
});

$("#categoryB_select").change(function() {
    key = $(this).val();
    if(key != "Select Category") {
        searchForKey(key, data);
        var catB_HTML = '';
        for (var i in wordsList) {
            var word = wordsList[i]
            catB_HTML += '<span class="tag draggable"><span>' + word + 
            '<a class="tagsinput-remove-link"></a></span></span>';
        }
        $('#catBTags_tagsinput').html(catB_HTML);
        setDraggable();
        setTagRemoval($("#categoryB_select").val());
    } else {
        $('#catBTags_tagsinput').html('');
    }
});

//When you click on the X on a draggable item this funtion helps to
//remove that draggable item
function setTagRemoval(from) {
    $('.tagsinput-remove-link').click(function(event) {
        var $span = $(event.target).closest('span[class^="tag"]');
        var label = $span.text();
        searchForItemAndRemove(label, data, from);
        $span.remove();
    });
}

//for the two following onClick handlers (for the plus icon) when clicked 
//take the text in the input element and make that into a draggable 
//tag which is added into the box below
var addItem = function(label){
    var select_option = $("#categoryA_select").val();
    if (label.length != 0 && select_option != "Select Category") {
        var html = '<span class="tag draggable"><span>' + label + 
            '<a class="tagsinput-remove-link"></a></span></span>';
        $("#catATags_tagsinput").append(html);
        setDraggable();
        setTagRemoval($("#categoryA_select").val());
        searchForLocationAndAdd(label, data, select_option);
    }
};

$('.input_container_A').keypress(function(event){
    if (event.which === 13){
        event.preventDefault();
        addItem(event.target.value);
    }
});

$('#add_categoryA_label').click(function(event) {
    var $input = $(event.target).siblings('input');
    var label = $input.val();
    addItem(label);
    $input.val('');
});

$('#add_categoryB_label').click(function(event) {
    var $input = $(event.target).siblings('input');
    var label = $input.val();
    var select_option = $("#categoryB_select").val();
    if (label.length != 0 && select_option != "Select Category") {
        var html = '<span class="tag draggable"><span>' + label + 
            '<a class="tagsinput-remove-link"></a></span></span>';
        $("#catBTags_tagsinput").append(html);
        setDraggable();
        setTagRemoval($("#categoryB_select").val());
        searchForLocationAndAdd(label, data, select_option);
    }
    $input.val('');
});

//This is the save button on top of the page it make a post request to save
//all the current data
$("#save_button").click(function(event) {
    $.post(
        "save_classified_data",
        {classified_data : JSON.stringify(data)},
        function(response) {
            if(response === "True") {
                $('#save_popover_success').popover('show');
                setTimeout(function(){
                    $('#save_popover_success').popover('hide');
                }, 2500);
            } else {
                $('#save_popover_fail').popover('show');
                setTimeout(function(){
                    $('#save_popover_fail').popover('hide');
                }, 2500);
            }
        }
    );
});

$('#save_popover_success').popover();
$('#save_popover_fail').popover();

//specifying a dir puts it in '/' which is the Training directory
//OR you can select an existing directory from drop down
$("#new_category_button").click(function(event) {
    $('#create_category_modal').modal();
});

$("#add_new_cat_btn").click(function(event) {
    var dir_name_input = $("#directory_name").val();
    var dir_name_select = $("#directory_select").val();
    var cat_name = $("#category_name").val();
    var alert = $("#modal_alert");
    var firstOption = "Select Existing Directory";

    if(cat_name.length != 0) {
        if(dir_name_input.length != 0 && dir_name_select != firstOption) {
            startKeySearch(dir_name_input, data);
            if(keyExists) {
                alertErrorDirExists(alert);
            } else {
                startAddingCategoryToDir(dir_name_select, dir_name_input, cat_name, data, /*catDirDir = */true);
                if(catAlreadyExists) {
                    alertErrorCatExists(alert);
                } else if(dirAlreadyExists) {
                    alertErrorDirExists(alert);
                } else {
                    alertSuccess(alert, cat_name, dir_name_input);
                }
            }
        } else if (dir_name_input.length != 0) {
            startKeySearch(dir_name_input, data);
            if(keyExists) {
                alertErrorDirExists(alert);
            } else {
                data[dir_name_input] = {};
                data[dir_name_input][cat_name] = [];
                alertSuccess(alert, cat_name, dir_name_input);
            }
        } else if(dir_name_select != firstOption) {
            startAddingCategoryToDir(dir_name_select, null, cat_name, data, /*catDirDir = */false);
            if(catAlreadyExists) {
                alertErrorCatExists(alert);
            } else {
                alertSuccess(alert, cat_name, dir_name_select);
            }
        }
    } else {
        alertErrorMissingName(alert);
    }
});

//shows the success message on the dialog 
//also adds this new directory to the drop down in modal
//also adds new category to choose from in the trainer
function alertSuccess(alert, cat_name, dir_name) {
    alert.removeClass("alert-error alert-info").addClass("alert-success");
    alert.html("<strong>Success:</strong> Added " + cat_name + " as a new category");
    $("#directory_name").val('');
    $("#category_name").val('');
    $("ul li[rel=0] a").click();
    var option = '<option>' + cat_name + '</option>';
    var optionForNewDirectory = '<option>' + dir_name + '</option>';
    $(option).appendTo('#categoryA_select');
    $(option).appendTo('#categoryB_select');
    $(optionForNewDirectory).appendTo('#directory_select');
}

function alertErrorDirExists(alert) {
    alert.removeClass("alert-info alert-success").addClass("alert-error");
    alert.html("<strong>Error:</strong> New directory name already exists!");
}

function alertErrorMissingName(alert) {
    alert.removeClass("alert-info alert-success").addClass("alert-error");
    alert.html("<strong>Error:</strong> Missing name. Please provide a directory and category name!");
}

function alertErrorCatExists(alert) {
    alert.removeClass("alert-info alert-success").addClass("alert-error");
    alert.html("<strong>Error:</strong> Category name already exists in selected directory!");
}

function alertErrorCatExists(alert) {
    alert.removeClass("alert-info alert-success").addClass("alert-error");
    alert.html("<strong>Error:</strong> New directory name already exists in selected directory!");
}

$("#modal_close_btn").click(function(event) {
    $('#create_category_modal').modal('toggle');
    var alert = $("#modal_alert");
    alert.removeClass("alert-error alert-success").addClass("alert-info");
    alert.html("<strong>Note:</strong> A directory and category name must be provided!");
    $("ul li[rel=0] a").click();
});



