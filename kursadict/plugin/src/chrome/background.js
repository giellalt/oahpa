// Generated by CoffeeScript 1.3.3

jQuery(document).ready(function (){
    // Enable options for inline clicking
    jQuery(document).selectToLookup({
      tooltip: true,
      displayOptions: true,
      spinnerImg: chrome.extension.getURL('spinner.gif'),
    });
});


// TODO: contextual trigger
chrome.contextMenus.create({
  title: "Oza '%s' sátnegirjjis",
  contexts: ["page", "selection"],
  onclick: function(info, tab) {
    var notification;
    notification = webkitNotifications.createHTMLNotification("http://testing.oahpa.no/kursadict/notify/sme/nob/" + info.selectionText + ".html");
    return notification.show();
  }
});
