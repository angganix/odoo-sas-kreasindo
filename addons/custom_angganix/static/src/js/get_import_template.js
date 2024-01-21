odoo.define("custom_angganix.get_import_template", function (require) {
  "use strict";
  window.get_import_template = function () {
    window.open(
      "/custom_angganix/static/src/files/import_template.csv",
      "_blank"
    );
  };
});
