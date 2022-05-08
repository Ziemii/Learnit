$(document).ready(function() {
    $('#summernote').summernote({
        height: 400,
        toolbar: [
          ['style', ['bold', 'italic', 'underline', 'clear']],
          ['font', ['superscript', 'subscript']],
          ['fontsize', ['fontsize']],
          ['color', ['color']],
          ['para', ['ul', 'ol', 'paragraph']],
          ['height', ['height']],
          ['table', ['table']],
          ['link'],
        ]
      });
  });