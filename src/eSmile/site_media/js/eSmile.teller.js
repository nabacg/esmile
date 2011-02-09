var eSmile = {}
//to refactor
eSmile.jokeController = {};
eSmile.jokeView = {};
eSmile.username = window.username;

$('#nextButton').click(function () {
	eSmile.jokeModel.showNext();
});

$('#prevButton').click(function () {
	eSmile.jokeModel.showPrev();
});

eSmile.subscriber = (function (config){
	var subscribePanel = $(config.subscribePanel),
	innerPanel = $(config.subscribeInnerPanelId),
	subscribersList = $(config.subscribersList);
	if(!config.add_url)
		alert('Subscribe URL missing, can\'t work this way!!');
		
	var subscribeUser = function (email) {
		addListElement(email, subscribersList);
		//subscribePanel.addClass(config.ajaxLoaderClass);
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
			//subscribePanel.removeClass(config.ajaxLoaderClass);	
			//innerPanel.css('visibility', '');
			//getSubscribersList(eSmile.username);
			
		});
		//console.log('Subscribe post sent..');
	}
	
	var subcribeHandler = function () {
		var emailField = $("#subscribeInput"); 
		var email = emailField && emailField.val();
		if (email && eSmile.subscriber.validEmail(email)) {
			emailField.removeClass('error');
			//emailField.hide();
			//innerPanel.css('visibility', 'hidden');
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
	
	var addListElement = function (listenerName, subscribersList)
	{
		var newEntry, removeButton;
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
	
	var getSubscribersList = function(tellerName) {
		subscribePanel.addClass(config.ajaxLoaderClass);
		$.getJSON(config.get_url, 
			{
				tellerUsername: eSmile.username
			}, 
			function (response) {
			if (response && response.success === true) {
				//var newEntry, removeButton, listenerName;
				for(var i = 0; i < response.data.length; i++){
					//listenerName = response.data[i];
					addListElement(response.data[i], subscribersList);
					/*
					newEntry = $("<li ></li>").text(listenerName);	
					removeButton = $("<p style='cursor:pointer;display:inline;'></p>").text('Remove?');
					removeButton.click((function(listenerName){
							return function(e){
								$(e.target).parent().remove();
								unsubscribe(listenerName);
							}
						})(listenerName));
					removeButton.appendTo(newEntry);
					

					newEntry.appendTo(subscribersList);*/
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

//troche mi sie nie podoba ze ten obiekt zajmuje sie wszystkim na raz
//pobiera dane, iteruje i manipuluje DOM'a
//moze by to ostatnie przeniesc do osobnego obiektu?
eSmile.jokeModel = (function(config){
	//debugger;
	var jokeList = [],
	currentJoke = 0,
	jokeField = $(config.jokeFieldId),
	dateField = $(config.dateFieldId),
	jokePanel = $(config.jokePanel),
	addJokePanel = $(config.addJokePanel),
	ajaxClass = config.ajaxLoaderClass,
	historyPanel = $(config.historyPanelId),
	innerAddJokePanel = $(config.innerAddJokePanelId),
	innerJokePanel = $(config.innerJokePanelId),
	newJokeValue = $(config.jokeInputId);
	
		
	if(!jokeField)
		alert('JokeFieldFatalError: JokeField not found under #joke_field id');
	if(!config.getUrl)
		alert('JsonURLFatalError: Json GET_URL not found, I can\'t work like this!');
	if(!config.addUrl)
		alert('JsonURLFatalError: Json ADD_URL not found, I can\'t work like this!');
	if(!dateField)
		alert('Joke date posted field was not found, I can\'t work like this!');
		
	var getJokeList = function(){
		jokePanel.addClass(ajaxClass);
		innerJokePanel.css('visibility', 'hidden');
		$.post(config.getUrl,
			{jokeTeller: eSmile.username},
			function(data){
				jokePanel.removeClass(ajaxClass);
				innerJokePanel.css('visibility', '');
				data = eval('(' + data + ')');
				//console.log('I acctualy did get some answer!')
				if(data && data.length > 0)
				{
					//console.log('and it was a good one!')
					jokeList = data;
					renderJokeHistory(historyPanel, data);
					firstJoke = jokeList[currentJoke];
					if(firstJoke)
						showJoke(firstJoke);
				}
			
		});
		
	}
	
	var renderJokeHistory = function(historyPanel, jokeList){
		$(config.historyPanelId + ' li').remove();
		var newEntry = null, 
		entryText = '';
		for(var i = 0; i < jokeList.length; i ++)
		{
			entryText = jokeList[i].datePosted;
			if(jokeList[i].hasOwnProperty('sent') && jokeList[i].sent === false)
				entryText = ' not sent ' + entryText;
			newEntry = $("<li style='cursor:pointer;'></li>")
				.text(entryText);
			if(i == currentJoke)
				newEntry.addClass(config.highlightClass);
			jokeList[i].historyEntry = {
					entry: newEntry,
					mark: function(){
						this.entry.addClass(config.highlightClass);
					},
					hide: function(){
						this.entry.removeClass(config.highlightClass);
					}
				};
			
			newEntry.click((function(i){		
				return function (e) {
					var joke = getJoke(i);
					if(joke)	
						showPassedJoke(joke, i);
				}
			})(i));
			
			newEntry.appendTo(historyPanel);
		}
	}
	
	var addNewJoke = function (joke) {
		addJokePanel.addClass(ajaxClass);
		$.post(config.addUrl, 
			{jokeValue: joke, jokeTeller: eSmile.username}, 
			function(data){
				addJokePanel.removeClass(ajaxClass);
				innerAddJokePanel.css("visibility", "");
				data = eval('(' + data + ')');
				
				if(data && data.joke)
				{
	
				for (var i = 0; i < data.joke.length; i++) {
					var joke = data.joke[i],
					newEntry = $("<li style='cursor:pointer;'></li>").text(joke.datePosted);
					newEntry.addClass(config.highlightClass);
					joke.historyEntry = {
						entry: newEntry,
						mark: function(){
							this.entry.addClass(config.highlightClass);
						},
						hide: function(){
							this.entry.removeClass(config.highlightClass);
						}
					};
					
					newEntry.click((function(i){
						return function(e){
							var joke = getJoke(i);
							if (joke) 
								showPassedJoke(joke, i);
						}
					})(0));
					
					newEntry.appendTo(historyPanel);
					jokeList.unshift(joke);
				}
					currentJoke = 0;
					renderJokeHistory(historyPanel, jokeList);
					firstJoke = jokeList[currentJoke];
					if(firstJoke)
						showJoke(firstJoke);	
								
				}
				else
					console.log("Kabom, sth just exploded"+ data.msg);
		});
		
	}
	
	var addJokeHandler = function(){
		var newJoke = newJokeValue &&  newJokeValue.val();
		if(newJoke)
		{	
			innerAddJokePanel.css("visibility", "hidden");
			addNewJoke(newJoke);
			newJokeValue.val('');
		}
	};

	
	var nextExist = function(index)
	{
		return index > -1 && jokeList && jokeList.length > 0 && jokeList.length > index;
	}

	var getJoke = function(index){
		if(nextExist(index))
			return jokeList[index];
	}
	
	var showJoke = function(joke) {
		jokePanel.stop().fadeTo('fast', 0.3);
		//jokePanel.fadeOut();
		jokeField.html(joke.value);
		dateField.text('Posted on: ' + joke.datePosted);
		joke.historyEntry.mark();
		jokePanel.fadeTo('slow', 1);
		//jokePanel.fadeIn('slow');
	}
	
	var showNextJoke = function(){		
		var joke = getJoke(currentJoke+1);
		if(joke)
		{
			var previousJoke = getJoke(currentJoke);	
			previousJoke.historyEntry.hide();
			showJoke(joke);
			currentJoke += 1;
		}
		console.log(currentJoke);
	}
	
	var showPrevJoke = function(){
		var joke = getJoke(currentJoke-1);
		if(joke)
		{
			var previousJoke = getJoke(currentJoke);
			previousJoke.historyEntry.hide();
			showJoke(joke);
			currentJoke -= 1;
		}		
		console.log(currentJoke);
	}
	
	var showPassedJoke = function(joke, index){
		if(joke)
		{
			var previousJoke = getJoke(currentJoke);
			previousJoke.historyEntry.hide();
			showJoke(joke);
			currentJoke = index;
		}	
		console.log(currentJoke);
	}
	
	
	// start show
	getJokeList();
	return {
		showNext: function(){
			showNextJoke();
		},
		showPrev: function(){
			showPrevJoke();
		},
		addNew: function(jokeValue){
			addNewJoke(jokeValue);	
		},
		showJoke: function(jokeObj, index){
			showPassedJoke(jokeObj, index);
		},
		onAddJoke: addJokeHandler		
	}
	
})({
	getUrl: '/jokes/get/',
	addUrl: '/jokes/add/',
	jokeFieldId: '#joke_field',
	dateFieldId: '#joke_date',
	addJokePanel: "#addJokePanel",
	innerAddJokePanelId: '#innerAddJokePanel',
	innerJokePanelId: '#innerJokePanel',
	historyPanelId: "#historyPanel",
	jokeInputId: "#jokeValue",
	jokePanel: "#jokePanel",
	ajaxLoaderClass: 'ajax-loader',
	highlightClass: 'highlight'
});


//command routing (maybe go for a controller? )
// ADD NEW JOKE event to handler mapping
$("#addJokeButton").click( eSmile.jokeModel.onAddJoke);
//SUBSCRIBE event to handler mapping
$("#subscribeButton").click(eSmile.subscriber.onSubscribe);
$("#newJokePreview").click(function(){
	var jokePreview = $("#jokePreview"), jokeValue = $("#jokeValue");
	jokeValue.hide();
	var jokeString = jokeValue.val();
	//najpierw rozdzielanie zartow
	jokeString = jokeString.replace(/\n\n\n/gi, '<br/><br/> <hr /><br/>');
	//potem formatowanie lini
	jokeString = jokeString.replace(/\n/gi, '<br/>');
	jokePreview.html(jokeString);
	jokePreview.show();
});

$("#newJokeEdit").click(function(){
	var jokePreview = $("#jokePreview"), jokeValue = $("#jokeValue");
	jokePreview.hide();
	jokeValue.show();
});
