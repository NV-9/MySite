$(document).ready(function() {
    $('.lesson-button').click(function() {
      var lessonButton = $(this);
      var lessonId = lessonButton.data('lesson-id');
      var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
      $.ajax({
        type: 'POST',
        url: window.location.href,
        data: {
          lesson_id: lessonId,
          csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
          console.log(response);
          if (response.success) {
            lessonButton.closest('.card').removeClass('unpaid').addClass('paid');
            lessonButton.remove();
          } else {
          }
        },
        error: function(xhr, textStatus, error) {
          console.log(xhr.statusText);
        }
      });
    });
  });
  