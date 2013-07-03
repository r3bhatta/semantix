$('.search-button').on('click', function(evt){
    $('.data-header small').html('California Pizza Kitchen');
    $('#locationTags_tagsinput').html('Loading...');
    $('.data-name').html('California Pizza Kitchen');
    $('.data-business').html('Restaurant');
    $('.data-hours').html('Unknown');
    $.ajax({
        url: '/locations',
    }).done(function(addresses){
    	var locationsHTML = '';
    	JSON.parse(addresses).forEach(function(address){
            locationsHTML += '<span class="tag"><span>' + address.trim() + '</span></span>';
    	});
    	locationsHTML += 
    		'<input id="locationTags_tag" value="" data-default="" ' +
    		'style="color: rgb(102, 102, 102); width: 12px;"></div></div>';
    	$('#locationTags_tagsinput').html(locationsHTML);
    });
    $.ajax({
        url: '/menu',
    }).done(function(menu){
        var menuHTML = '';
        JSON.parse(menu).forEach(function(menuItem){
            menuHTML += '<span class="tag"><span>' + menuItem.trim() + '</span></span>';
        });
        menuHTML +=
    		'<input id="menuTags_tag" value="" data-default="" ' +
    		'style="color: rgb(102, 102, 102); width: 12px;"></div></div>';
    	$('#menuTags_tagsinput').html(menuHTML);
    });
});
