var flashTitleTimer;
function flashTitle(title, count){
// Clear the timeout
setTimeout(function(){flashTitleTimer=null})
var oldTitle = "";
var newTitle = "";
setInterval(function(){
document.setTitle(newTitle)
oldTitle = newTitle;

},2000)

}