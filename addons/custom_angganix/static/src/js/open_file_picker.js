odoo.define("custom_angganix.open_file_picker", function (require) {
  "use strict";
  window.open_file_picker = function () {
    var attachmentField = document.querySelector("input[name=attachment]");
    return attachmentField.click();
  };
});
