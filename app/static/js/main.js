$('.search-button').on('click', function(evt){
    console.log('Clicked on search button.');
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
