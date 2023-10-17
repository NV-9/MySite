function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
  
var csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    $('.lesson-button').click(function() {
		var lessonButton = $(this);
		var lessonId = lessonButton.data('lesson-id');
		$.ajax({
			type: 'POST',
			url: window.location.href,
			data: {
				lesson_id: lessonId,
				csrfmiddlewaretoken: csrftoken
			},
			success: function(response) {
			console.log(response);
			if (response.success) {
				location.reload();
			} else {
			}
			},
			error: function(xhr, textStatus, error) {
				console.log(xhr.statusText);
			}
      	});
    });
});
  