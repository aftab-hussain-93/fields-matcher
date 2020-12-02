const file_id = document.querySelector("#fileId").textContent;
let output = {};
output.file_id = file_id;

const makeUpper = ()=>{
  let allElems = document.querySelectorAll('#form-contents input');
  allElemText = Array.from(allElems).map( (elem) => {
    current_value = elem.value
    elem.value = current_value.toUpperCase();
    return elem.value;
  })
}

const makeLower = ()=>{
  let allElems = document.querySelectorAll('#form-contents input');
  allElemText = Array.from(allElems).map( (elem) => {
    console.log(elem.hasAttribute('id'))
    console.log(elem.hasAttribute('asd'))
    current_value = elem.value
    elem.value = current_value.toLowerCase();
    return elem.value;
  })
}

const makeCapital = () => {
  let allElems = document.querySelectorAll('#form-contents input');
  allElemText = Array.from(allElems).map( (elem) => {
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
  Array.from(allElems).forEach( (elem, idx) => {
    if(elem.hasAttribute('id')){
      head = elem.id
    }else{
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

  fetch("/modify_file",{
      method:'POST',
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

      if(data.key){
        let filePath = data.key;
        let attachementName = data.attachment_name;
        let downloadForm = document.getElementById("downloadForm");
        let filePathElem = document.createElement("input");
        let attachmentNameElem = document.createElement("input");

        filePathElem.value=filePath;
        filePathElem.name="key";
        downloadForm.appendChild(filePathElem);

        attachmentNameElem.value=attachementName;
        attachmentNameElem.name="attachment_name";
        downloadForm.appendChild(attachmentNameElem);

        console.log("Submitting download form")
        downloadForm.submit();

        // Redirecting back to home page after file has been downloaded.
        setTimeout(function() {
            window.location.replace("/index");
          }, 800);
      }else{
        console.log("Could not download")
      }
    })
    .catch(data => console.log(`error ${data}`))
}



// JQuery code for grabbing and re-ordering of the headers
$(document).ready(function () {
        let download_form;

        // Disable input into the file columns
        $(".head").prop("disabled", true);

        // Re-order click
        $("#reorderBtn").click(function () {
          $(".head").prop("disabled", true);

          if ($("#form-contents").data("uiSortable")) {
            $("#form-contents").sortable("enable");
          }
          else{
            $("#form-contents").sortable({opacity:0.5,
              cancel:null,
              cursor: "grabbing"});
            }
          });

        // Rename click
        $("#renameBtn").click(function () {
          $(".head").prop("disabled", false);
          if ($("#form-contents").data("uiSortable")) {
            $("#form-contents").sortable("disable");
          }
        });
      });