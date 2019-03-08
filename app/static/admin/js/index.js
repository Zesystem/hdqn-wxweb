// setInterval(function(){
// 	var times = document.getElementsByClassName('times')[0];
// 	var span = document.getElementsByTagName('span')[0];
// 	span.innerHTML = times.innerHTML;
// },500)
setInterval(function(){
	var times = document.getElementsByClassName('times')[0];
	var span = document.getElementById('demo');
	span.innerHTML = times.innerHTML;
},500)