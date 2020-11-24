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
    .then(res => res.json())
    .then(data => {
      console.log(data)
      if(data.path){
        let filePath = data.path;
        let fileName = data.filename;
        let downloadForm = document.getElementById("downloadForm");
        let filePathElem = document.createElement("input");
        let fileNameElem = document.createElement("input");
        filePathElem.value=filePath;
        filePathElem.name="path";
        downloadForm.appendChild(filePathElem);

        fileNameElem.value=fileName;
        fileNameElem.name="filename";
        downloadForm.appendChild(fileNameElem);
        console.log("Submitting download form")
        downloadForm.submit();
        console.log("Form submitted")
        downloadForm.reset();
         setTimeout(function() {
              window.location.replace("/index");
            }, 500);
      }else{
        console.log("Could not download")
      }
    })
    .catch(data => console.log("error"))



    // download_form = $('<form style="display:none;" action="'+ data.url +'" method="post">' +
    //             '<input type="text" name="filename" value="' + data.filename + '"  />' +
    //             '</form>');
}




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