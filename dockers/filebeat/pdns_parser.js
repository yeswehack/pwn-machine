function unescape(s) {
  function replacer(s){
    return String.fromCharCode(parseInt(s.slice(1), 10))
  }
  return s.replace(/\\\d{3}/g, replacer);
}

function process(event) {  
  var queryRegex = /.*?Remote (\d+\.\d+\.\d+\.\d+) wants '(.+?)\|([A-Z]+)', /;
  var line = event.Get("message");
  var date = line.slice(0, 15)
  var message = line.slice(15).split(":").slice(1).join(":").trim();
  var match = queryRegex.exec(message);
  if (!match) {
    event.Cancel();
    return;
  }
  event.Put("origin", match[1]);
  event.Put("query", unescape(match[2]));
  event.Put("type", match[3]);
  event.Put("date", date);
}
