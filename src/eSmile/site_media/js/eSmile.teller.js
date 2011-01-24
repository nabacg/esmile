//$("#sidebar").css('width', "30em");

eSmile.subscriber = (function (config){
	var subscribePanel = $(config.subscribePanel),
	innerPanel = $(config.subscribeInnerPanelId),
	subscribersList = $(config.subscribersList);
	if(!config.add_url)
		alert('Subscribe URL missing, can\'t work this way!!');
		
	var subscribeUser = function (email) {
		subscribePanel.addClass(config.ajaxLoaderClass);
		$.getJSON(config.add_url, 
			{
				subscriberEmail: email,
				tellerUsername: eSmile.username
			}, 
			function (data) {
			if(data && data.success === true)
				console.log('congrats, your\'re gonne listen to his jokes every day now!');
			else
				alert('Kambum, sth just blew up!');
			subscribePanel.removeClass(config.ajaxLoaderClass);	
			innerPanel.css('visibility', '');
			getSubscribersList(eSmile.username);
		});
		console.log('Subscribe post sent..');
	}
	
	var subcribeHandler = function () {
		var emailField = $("#subscribeInput"); 
		var email = emailField && emailField.val();
		if (email && eSmile.subscriber.validEmail(email)) {
			emailField.removeClass('error');
			//emailField.hide();
			innerPanel.css('visibility', 'hidden');
			subscribeUser(email);
			emailField.val('');
		}
		else
			emailField.addClass('error');
	};
	
	var unsubscribe = function (listenerUsername) {
			$.getJSON(config.delete_url, 
			{
				tellerUsername: eSmile.username,
				subscriberUsername: listenerUsername
			}, 
			function (response) {
				if(response.success)
					console.log('You\'re no longer listening to his jokes');
			});
	}
	
	var getSubscribersList = function(tellerName) {
		subscribePanel.addClass(config.ajaxLoaderClass);
		$.getJSON(config.get_url, 
			{
				tellerUsername: eSmile.username
			}, 
			function (response) {
			if (response && response.success === true) {
				var newEntry, removeButton, listenerName;
				for(var i = 0; i < response.data.length; i++){
					listenerName = response.data[i];
					newEntry = $("<li ></li>").text(listenerName);	
					removeButton = $("<p style='cursor:pointer;display:inline;'></p>").text('Remove?');
					removeButton.click((function(listenerName){
							return function(e){
								$(e.target).parent().remove();
								unsubscribe(listenerName);
							}
						})(listenerName));
					removeButton.appendTo(newEntry);
					
					newEntry.appendTo(subscribersList);
				}
				
				console.log('congrats, you just got your list!');
			}
			else 
				alert('Kambum, sth just blew up!');
			subscribePanel.removeClass(config.ajaxLoaderClass);	
			innerPanel.css('visibility', '');
		});
		console.log('Subscribe post sent..');
	}
	getSubscribersList(eSmile.username);
	return {
		validEmail: function (email) {
			var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;  
			return emailPattern.test(email);
		},
		subscribe: function(email){
			subscribeUser(email);			
		},
		onSubscribe: subcribeHandler
	}
})({
	add_url: '/subscribe/',
	get_url: '/subscribers/',
	delete_url: '/unsubscribe/',
	subscribePanel: '#subscribePanel',
	subscribeInnerPanelId: '#innerSubscribePannel',
	subscribersList: '#subscriberListPanel',
	ajaxLoaderClass: 'ajax-loader'
});