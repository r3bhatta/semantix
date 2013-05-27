$('.search-button').on('click', function(evt){
    $('.data-header small').html('California Pizza Kitchen');
    $('#locationTags_tagsinput').html('Loading...');
    $('.data-name').html('California Pizza Kitchen');
    $('.data-business').html('Restaurant');
    $('.data-hours').html('Unknown');
    $.ajax({
        url: '/locations',
    }).done(function(data){
    	var locationsHTML = '';
    	JSON.parse(data).forEach(function(address){
    		locationsHTML += '<span class="tag"><span>' + address + '</span></span>';
    	});
    	locationsHTML += 
    		'<input id="locationTags_tag" value="" data-default="" ' +
    		'style="color: rgb(102, 102, 102); width: 12px;"></div></div>';
    	$('#locationTags_tagsinput').html(locationsHTML);
    });
});
