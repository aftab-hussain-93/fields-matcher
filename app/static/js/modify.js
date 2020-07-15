$(document).ready(function () {
        var download_form;
        $('#downloadBtn').hide();
        $(".head").prop("disabled", true);
        $("#reorderBtn").click(function () {
          $(".head").prop("disabled", true);
          if ($("#form-contents").data("uiSortable")) {
            $("#form-contents").sortable("enable");
          }
          else{
          $("#form-contents").sortable();
          }
        });
        $("#renameBtn").click(function () {
          $(".head").prop("disabled", false);
          if ($("#form-contents").data("uiSortable")) {
            $("#form-contents").sortable("disable");
          }
        });
        var output = {};
        let i = 1;        
        let file_id = $("#fileId").text();
        output.file_id = file_id;
        let header = {};
        $("#applyBtn").click(function () {
          // for
          // console.log()
          let ext = $("input#extension").val();
          output.extension = ext;
          var elems = $("#form-contents input").map(function (idx, elem) {
            if($(elem).hasClass("head")){
              head = $(elem).attr("id");
            }else{
              head = $(elem).val();
            }            
            new_head = $(elem).val();
            new_position = i;
            header[head] = {
              header_name: new_head,
              position: new_position,
            };
            i++;
          });
          output.headers = header;
          req_op = JSON.stringify(output);
          i = 1;
          $(".head").prop("disabled", true);
          if ($("#form-contents").data("uiSortable")) {
            $("#form-contents").sortable("disable");
          }

          $.ajax({
            contentType: "application/json",
            data: req_op,
            url: "/api/v1.0/modify",
            type: "POST",
            success: function (data) {
                console.log(data.url);
                console.log(data.filename);
                download_form = $('<form style="display:none;" action="'+ data.url +'" method="post">' +
                '<input type="text" name="filename" value="' + data.filename + '"  />' +
                '</form>');
                $('body').append(download_form);
                console.log("form created.")
                $('#downloadBtn').show();
            },
            error: function (error) {
                console.log("Error");
                console.log(error);
            }
          });
        });
        $('#downloadBtn').click(function(event){
            console.log("Submitting the form");
            download_form.submit();
            setTimeout(function() {
              window.location.replace("/index");
            }, 500);
        });
      });