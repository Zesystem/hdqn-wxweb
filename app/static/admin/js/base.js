//实现显示系统时间功能
function startTime(){
	var times = document.getElementsByClassName('times')[0];
	var today=new Date();
	var h=today.getHours();
	var m=today.getMinutes();
	var s=today.getSeconds();
	var year = today.getFullYear();
	var month = today.getMonth();
	var day = today.getDate();
	var x = week(today.getDay());
	month = month + 1;
	m=checkTime(m);
	s=checkTime(s);
	time = year + '年' + month + '月' + day + '日' + " "+h + ":" + m + ":" + s + " " + x;
	times.innerHTML=time;
	t=setTimeout(function(){startTime()},500);

}
function checkTime(i){
	if (i<10){
		i="0" + i;
	}
	return i;
}

function week(day){
	var arr = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
	return arr[day];
}