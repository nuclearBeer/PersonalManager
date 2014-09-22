function externalLinks() {
alert(document.getElementById(widgetContext['widgetid']).innerHTML)
   if (!document.getElementsByTagName) return;

   var anchors = document.getElementsByClassName("a");
   for (var i=0; i<anchors.length; i++) {
      var anchor = anchors[i];
      if (anchor.getAttribute("target") == "_top") {
      alert(anchor);
         anchor.onclick = "return ! window.open(this.href);"
      }
   }
}
 
