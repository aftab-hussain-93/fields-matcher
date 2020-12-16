const file_id = document.querySelector("#fileId").textContent;
let output = {};
output.file_id = file_id;

const makeUpper = () => {
  let allElems = document.querySelectorAll('#form-contents input');
  allElemText = Array.from(allElems).map((elem) => {
    current_value = elem.value
    elem.value = current_value.toUpperCase();
    return elem.value;
  })
}

const makeLower = () => {
  let allElems = document.querySelectorAll('#form-contents input');
  allElemText = Array.from(allElems).map((elem) => {
    console.log(elem.hasAttribute('id'))
    console.log(elem.hasAttribute('asd'))
    current_value = elem.value
    elem.value = current_value.toLowerCase();
    return elem.value;
  })
}

const makeCapital = () => {
  let allElems = document.querySelectorAll('#form-contents input');
  allElemText = Array.from(allElems).map((elem) => {
    current_value = elem.value
    let separateWord = current_value.toLowerCase().split(' ')
    for (var i = 0; i < separateWord.length; i++) {
      separateWord[i] = separateWord[i].charAt(0).toUpperCase() +
        separateWord[i].substring(1);
    }
    elem.value = separateWord.join(' ')
    return elem.value;
  })
}

const downloadFile = (extension) => {
  output.extension = extension;
  output.file_id = file_id;
  let allElems = document.querySelectorAll('#form-contents input');
  let header = {};
  Array.from(allElems).forEach((elem, idx) => {
    if (elem.hasAttribute('id')) {
      head = elem.id
    } else {
      head = elem.value
    }
    new_head = elem.value;
    new_position = idx + 1;
    header[head] = {
      header_name: new_head,
      position: new_position
    };
  })
  output.headers = header;
  console.log("Array being sent post modification is")
  console.log(output)

  fetch("/modify_file", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(output)
  })
    .then(res => {
      console.log(res)
      return res.json()
    })
    .then(data => {
      console.log("Post modification request")
      console.log(data)

      if (data.key) {

        downloadFormSubmit(key = data.key, attachementName = data.attachment_name);
        // Redirecting back to home page after file has been downloaded.
        redirectHome();
      }
      else {
        console.log("Could not download")
      }
    })
    .catch(data => console.log(`error ${data}`));
}

// Download Form Function
const downloadFormSubmit = (key, attachmentName) => {
  let filePath = key;
  let attachementName = attachmentName;

  let downloadForm = document.getElementById("downloadForm");
  let filePathElem = document.createElement("input");
  let attachmentNameElem = document.createElement("input");
  filePathElem.value = filePath;
  filePathElem.name = "key";
  downloadForm.appendChild(filePathElem);

  attachmentNameElem.value = attachementName;
  attachmentNameElem.name = "attachment_name";
  downloadForm.appendChild(attachmentNameElem);

  console.log("Submitting download form")
  downloadForm.submit();
}

// Function to redirect home after delay

const redirectHome = () => {
  setTimeout(function () {
    window.location.replace("/index");
  }, 800);
}


// Drop Header function
const dropSelectedHeader = e => {
  const selectElem = e.relatedTarget;
  if (!(typeof selectElem === 'undefined' || selectElem === null)) {
    if (selectElem.tagName == 'INPUT') {
      if (selectElem.getAttribute("class") == "head") {
        flashMessages(`Dropping Header "${selectElem.value}"`, "success");
        selectElem.parentNode.remove();
      }
    }
  } else {
    console.log("No header selected")
    flashMessages(`Please select a header to drop`, "warning");
  }
};
// JQuery code for grabbing and re-ordering of the headers
$(document).ready(function () {
  let download_form;

  // Disable input into the file columns
  $(".head").prop("readonly", true);

  function disableSortable() {

    if ($("#form-contents").data("uiSortable")) {
      $("#form-contents").sortable("disable");
      $(".head").removeClass("reorder");
    }
  };

  function enableSortable() {
    $(".head").prop("readonly", true);
    $(".head").addClass("reorder");
    if ($("#form-contents").data("uiSortable")) {
      $("#form-contents").sortable("enable");
    }
    else {
      $("#form-contents").sortable({
        opacity: 0.9,
        cancel: null,
        cursor: "grabbing"
      });
    }
  };

  // Re-order click
  $("#reorderBtn").click(function () {

    if ($(".head").hasClass("reorder")) {
      $("#reorderBtn").removeClass("activated");
      disableSortable();
    } else {
      $("#reorderBtn").addClass("activated");
      enableSortable();
    }
  });

  // Rename click
  $("#renameBtn").click(function () {
    $(".head").prop("readonly", false);
    disableSortable();
  });
});