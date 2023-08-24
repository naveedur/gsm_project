(function($) {
    console.log("workeddddd")
    $(document).ready(function() {
      // Disable the location field by default
      $('#id_location').prop('disabled', true);
  
      // Listen for changes in the select_page field
      $('#id_select_page').on('change', function() {
        var selectedPage = $(this).val();
  
        // Enable or disable the location field based on the selected page value
        if (selectedPage === 'other') {
          $('#id_location').prop('disabled', false);
        } else {
          $('#id_location').prop('disabled', true);
        }
      });
    });
  })(django.jQuery);
  