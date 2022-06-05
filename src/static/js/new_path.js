
// New path text editor initialization parameters
$(document).ready(function() {
    $('#summernote').summernote({
        height: 400,
        lineHeights: ['0.2', '0.3', '0.4', '0.5', '0.6', '0.8', '1.0', '1.2', '1.4', '1.5', '2.0', '3.0'],
        toolbar: [
          ['style', ['bold', 'italic', 'underline', 'clear']],
          ['font', ['superscript', 'subscript']],
          ['fontsize', ['fontsize']],
          ['color', ['color']],
          ['para', ['ul', 'ol', 'paragraph']],
          ['height', ['height']],
          ['table', ['table']],
          ['insert', ['link', 'picture', 'video']],
          ['misc', ['codeview']]
          
        ],
        placeholder: 'It\'s all yours'
      });
     
  });