var csrfcookie = function () {
  var cookieValue = null,
    name = "csrftoken";
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

var xhr;
function menu(id, self) {
  if (self.className == "fas fa-heart") {
    self.className = "far fa-heart";
    decreaseLikes(id);
  }
  else if (self.className == "far fa-heart") {
    self.className = "fas fa-heart";
    increaseLikes(id);
  }
}
function likeByImage(id, self) {
  var classname = self.parentNode.childNodes[3].childNodes[1].className;
  if (classname == "far fa-heart") {
    self.parentNode.childNodes[3].childNodes[1].className = "fas fa-heart";
    increaseLikes(id)
  }
}
function increaseLikes(id) {
  xhr = new XMLHttpRequest();
  var params = 'y=' + id;
  xhr.open("POST", "increaseLikes", true);
  xhr.onreadystatechange = callback;
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrfcookie());
  xhr.send(params);
}
function decreaseLikes(id) {
  xhr = new XMLHttpRequest();
  var params = 'y=' + id;
  xhr.open("POST", "decreaseLikes", true);
  xhr.onreadystatechange = callback;
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrfcookie());
  xhr.send(params);
}
function callback() {
  if (xhr.readyState == 4 && xhr.status == 200) {
    var res = JSON.parse(xhr.responseText);
    var image = JSON.stringify(res.image);
    var y = document.querySelector("img[src=" + image + "]");
    var parent = y.parentNode;
    var totaLikes = parent.childNodes[5];
    totaLikes.querySelector('a').innerHTML = res.likes + " others ";
    var colorofHeart = parent.childNodes[3];
  }
}
function image_loaded(id, self) {
  var ob = new XMLHttpRequest();
  var params = 'y=' + id;
  ob.open("POST", "checkForLike", true);
  ob.onreadystatechange = function () {
    if (ob.readyState == 4 && ob.status == 200) {
      var res = JSON.parse(ob.responseText);
      var classname = res.classname;
      if (classname == "fas fa-heart") {
        self.parentNode.childNodes[3].childNodes[1].className = "fas fa-heart";
      }
    }
  };
  ob.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  ob.setRequestHeader("X-CSRFToken", csrfcookie());
  ob.send(params);
};
document.getElementById("close").addEventListener('click', close);
function close() {
  document.getElementById("likedby").style.display = "none";
};


function getLikes(id) {
  var ob = new XMLHttpRequest();
  var params = 'y=' + id;
  ob.open("POST", "ajaxgetLikes", true);
  ob.onreadystatechange = function () {
    if (ob.readyState == 4 && ob.status == 200) {
      var res = JSON.parse(ob.responseText);
      console.log(res);
      var l = document.getElementById("likedby");
      l.style.display = "inline-block";
      var content = document.getElementById("likes");
      content.innerHTML = "";
      for (var i = 0; i < res['usersLiked'].length; i++) {
        var parent = document.createElement("div");
        var randomuserimage = document.createElement("IMG");
        randomuserimage.setAttribute("src", res['images'][i]);
        randomuserimage.setAttribute("class", "randomsearchimages");
        randomuserimage.setAttribute("width", 40);
        randomuserimage.setAttribute("height", 40);
        parent.setAttribute("class", "parentclass");
        var randomusername = document.createElement("div");
        randomusername.setAttribute("class", "randomsearch-username");
        randomusername.setAttribute("onclick", "some(this)");
        randomusername.textContent = res['usersLiked'][i]['name'];
        document.getElementById("likes").appendChild(parent);
        var name = document.createElement("div");
        name.innerText = res['names'][i];
        name.setAttribute("class", "randomsearchuser-name");
        parent.appendChild(randomuserimage);
        var randomuserdiv = document.createElement("div");
        randomuserdiv.setAttribute("class", "randomusernames");
        parent.appendChild(randomuserdiv);
        randomuserdiv.appendChild(randomusername);
        randomuserdiv.appendChild(name);
      }
    }
  };
  ob.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  ob.setRequestHeader("X-CSRFToken", csrfcookie());
  ob.send(params);
};

//sending requests to other users when they click follow button via ajax
var otherob;
var id_obj;
function sendreq(id, self) {
  if (self.value == "Follow") {
    otherob = self;
    self.style.background = "green";
    self.style.color = "white";
    self.value = "request sent";
    var obj = new XMLHttpRequest();
    var para = "y=" + id;
    obj.open("POST", "send_request", true)
    obj.onreadystatechange = function () {
      if (obj.readyState == 4 && obj.status == 200) {

      }
    }
    obj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    obj.setRequestHeader("X-CSRFToken", csrfcookie());
    obj.send(para);
  }
  else if (self.value == "request sent") {
    otherob = self;
    self.value = "Follow";
    self.style.background = "blue";
    self.style.color = "white";
    var obj = new XMLHttpRequest();
    var para = "y=" + id;
    obj.open("POST", "unsend_request", true)
    obj.onreadystatechange = function () {
      if (obj.readyState == 4 && obj.status == 200) {

      }
    }
    obj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    obj.setRequestHeader("X-CSRFToken", csrfcookie());
    obj.send(para);
  }
  else if (self.value == "friends") {
    otherob = self;
    id_obj = id;
    var username = self.parentNode.parentNode.childNodes[1].childNodes[0].textContent;
    var x = document.getElementById("alert-heading");
    x.textContent = "Unfriend  " + username + "?";
    document.getElementById("unfriend-alert").style.display = "flex";
  }
  else if (self == "confirm-unfriend") {
    document.getElementById("unfriend-alert").style.display = "none";
    otherob.value = "Follow";
    otherob.style.background = "blue";
    otherob.style.color = "white";
    var obj = new XMLHttpRequest();
    var para = "id=" + id_obj;
    obj.open("POST", "remove_friend", true);
    obj.onreadystatechange = function () {
      if (obj.readyState == 4 && obj.status == 200) {

      }
    };
    obj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    obj.setRequestHeader("X-CSRFToken", csrfcookie());
    obj.send(para);
  }
}
//onloading the page check whether user is a friend or not

function checkforFriend(id, self) {
  var obj = new XMLHttpRequest();
  var param = "id=" + id;
  obj.open("POST", "checkFriend", true);
  obj.onreadystatechange = function () {
    if (obj.readyState == 4 && obj.status == 200) {
      var res = JSON.parse(obj.responseText);
      x = self.parentNode.childNodes[3].childNodes[3].childNodes[1];
      if (res['friend'] == "yes") {
        x.value = "friends";
        x.style.background = "white";
        x.style.color = "black";
      }
      else if (res['friend'] == "requested") {
        x.value = "request sent";
        x.style.background = "green";
        x.style.color = "white";
      }
      else {
        x.value = "Follow";
      }
    }
  }
  obj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  obj.setRequestHeader("X-CSRFToken", csrfcookie());
  obj.send(param);

};
document.getElementById("unfriend-user-btn").addEventListener("click", function () {
  sendreq(4, "confirm-unfriend");
});
document.getElementById("cancel-unfriend-btn").addEventListener('click', function (e) {
  document.getElementById("unfriend-alert").style.display = "none";
});