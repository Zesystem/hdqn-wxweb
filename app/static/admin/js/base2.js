//实现导航功能
var demo = document.getElementsByClassName('demo');
var function_demo = document.getElementsByClassName('demo_demo');

var arr = [1,1,1,1];
for(var i = 0;i < 4;i++){
	var temp = function_demo[i].style.display;
	if(temp == 'block')
		arr[i] = 1;
	else
		arr[i] = 0;
}
// console.log(arr);
for(var i = 0;i < 4;i++){
	(function(j){
		demo[j].onclick=function(){
			if(arr[j] == 1){
				function_demo[j].style.display = 'block';
				arr[j] = 0;
			}else{
				function_demo[j].style.display = 'none';
				arr[j] = 1;
			}
		}
	}(i))
}