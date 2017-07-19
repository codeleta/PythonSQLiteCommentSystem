/*
  AJAX
 */

function getXmlDoc() {
  var xml_doc;

  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xml_doc = new XMLHttpRequest();
  }
  else {
    // code for IE6, IE5
    xml_doc = new ActiveXObject("Microsoft.XMLHTTP");
  }

  return xml_doc;
}

function ajaxGet(url, callback) {
  var xml_doc = getXmlDoc();

  xml_doc.open('GET', url, true);

  xml_doc.onreadystatechange = function() {
    if (xml_doc.readyState === 4 && xml_doc.status === 200) {
      callback(xml_doc);
    }
  };

  xml_doc.send();
}

function ajaxDelete(url, data, callback) {
  var xml_doc = getXmlDoc();

  xml_doc.open('DELETE', url, true);
  xml_doc.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  xml_doc.onreadystatechange = function() {
    if (xml_doc.readyState === 4 && xml_doc.status === 200) {
      callback(xml_doc);
    }
  };

  xml_doc.send(data);
}

/*
  EVENT FUNCTIONS
 */

function deleteComment(event) {
  event.preventDefault();
  var link = this;
  link.removeEventListener("click", deleteComment);
  var comment_id = link.getAttribute("data-id");
  ajaxDelete(link.getAttribute("href"), "id=" + comment_id, function(xml_doc) {
    data = JSON.parse(xml_doc.response);
    if (data.success) {
      var deleted_tr = link.parentNode.parentNode;
      deleted_tr.parentNode.removeChild(deleted_tr);
    } else {
      link.addEventListener("click", deleteComment);
      alert("Не удалось удалить комментарий");
    }
  });
}

function clickRowAsLink(event) {
    var click = event.which;
    var url = this.getAttribute('data-href');
    if (url) {
        if (click === 2 || (click === 1 && (event.ctrlKey || event.metaKey))) {
            window.open(url, '_blank');
            window.focus();
        } else if (click === 1) {
            window.location.href = url;
        }
        return true;
    }
}

function citySelectLoadOptions() {

  var value = this.value;
  var city_select = document.getElementById('comment_city');
  var city_select_parent = city_select.parentNode;

  if (value) {
    ajaxGet("/get_cities/?region=" + value, function(xml_doc) {
      data = JSON.parse(xml_doc.response);
      city_select.options.length = 1;
      for (var i = 0; i < data.length; ++i) {
        city_select.options[i + 1] = new Option(data[i].title, data[i].id);
      }
    });
    if (city_select_parent.classList.contains("hidden")) {
      city_select_parent.classList.remove("hidden");
    }
  } else {
    if (!city_select_parent.classList.contains("hidden")) {
      city_select_parent.classList.add("hidden");
    }
  }
}

/*
  EVENTS
 */

function addEventToClassElements(class_name, event_function) {
  var delete_comment_links = document.getElementsByClassName(class_name);
  for (var i = 0; i < delete_comment_links.length; ++i) {
      delete_comment_links[i].addEventListener('click', event_function);
  }
}


window.onload = function() {
  addEventToClassElements("delete_comment", deleteComment);
  addEventToClassElements("row_as_link", clickRowAsLink);

  var region_select = document.getElementById('comment_region');
  region_select.onchange = citySelectLoadOptions;
};