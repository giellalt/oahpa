
function selectsahka ( selectedtype )
{
    document.gameform.dialogue.value = selectedtype ;
    document.gameform.submit() ;
}

function showPopup(w,h,elid){
   var popUp = document.getElementById(elid);

   var baseText = null;
 
   popUp.style.top = "200px";
   popUp.style.left = "400px";
   popUp.style.width = w + "px";
   popUp.style.height = h + "px";
 
   if (baseText === null) baseText = popUp.innerHTML;
   popUp.innerHTML = baseText + 
      "<div id=\"statusbar\"><button onclick=\"hidePopup(elid);\">Close window<button></div>";
 
   var sbar = document.getElementById("statusbar");
   sbar.style.marginTop = (parseInt(h)-70) + "px";
   popUp.style.visibility = "visible";
}

function hidePopup(elid){
   var popUp = document.getElementById(elid);
   popUp.style.visibility = "hidden";
}

function feedback(msg)
{
  var generator=window.open('','name','height=200,width=300');
  generator.moveTo(50,50);
  generator.document.write('<html><head><title>Tutorial</title>');
  generator.document.write('</head><body>');
  generator.document.write('<p>' + msg + '</p>');
  generator.document.write('<p><a href="javascript:self.close()">close</a></p>');
  generator.document.write('</body></html>');
  generator.document.close();
}

function process(strField, evtKeyPress,form)  {
	var aKey;
	if (window.event)
	   aKey = window.event.keyCode;
	else { 
		 aKey = evtKeyPress.keyCode ?  
		 evtKeyPress.keyCode :evtKeyPress.which ?  
		 evtKeyPress.which : evtKeyPress.charCode;  
    }  
    if (aKey == 13)  {
      var name = strField.name;
      var numbers = name.match(/^\w/);
      var newnum = parseInt(numbers[0]) + 1; 
      var newname = name.replace(numbers[0],newnum);
      if(newname in form){
          var i=1;
	      while(i<50) {
			if(form[i].name == 'test') {
				form[i].focus();
				return false;
			}
			if(form[i].name == newname)  {
			   var j=i;
			   while(j<60) {
			       if(form[j].type != 'hidden') {
				   	   form[j].focus();
					   return false;
                   }
				j++;
             }
		}
		i++;
	}
	}
      else {
        form.test.focus();
      }
     return false;
    }  
}

function processvasta(event,form){
    key = event.keyCode;
    if (key==13){
      form.submit();
    }
  }

function sahkaSetFocus(){

  document.getElementByName('test').focus();
  var node_list = document.getElementsByTagName('input');
	
  for (var i = 0; i < node_list.length; i++) {
    var node = node_list[i];
    if (node.getAttribute('type') == 'text') {
      node.focus();
      }
   }

} 

function setFocus(form){

  if (form.gametype == "sahka") {
    sahkaSetFocus();
    return;
  }
  var node_list = document.getElementsByTagName('input');
  var i=0;	
  var found=0;
  while (i < node_list.length & found==0) {
    i++;
    var node = node_list[i];
    if (node.getAttribute('type') == 'text') {
      node.focus();
      found=1;
    }
  }
} 

function scrollDown() { 
		 if (document.body.scrollHeight) {
		 		   window.scrollto(0, document.body.scrollHeight); 
		  } 
		  else if (screen.height) {
		 // IE5 window.scrollto(0, screen.height); 
	   } 
} 

