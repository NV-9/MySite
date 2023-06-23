document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var eventsDataElement = document.getElementById('events-data');
    var eventsData = JSON.parse(eventsDataElement.textContent || '[]');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        editable: true, 
        events: eventsData,
        aspectRatio: 3,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        views: {
            dayGridMonth: {
                dayMaxEventRows: 2,
                eventTimeFormat: {
                    hour: 'numeric',
                    minute: '2-digit',
                    omitZeroMinute: true,
                    meridiem: 'short'
                }
            }
        },
        eventClick: function(info) {
            // Handle event click
            console.log('Event clicked:', info.event);
        },
        eventDrop: function(info) {
            // Handle event drop (moving event)
            console.log('Event dropped:', info.event);
        },
        eventResize: function(info) {
            // Handle event resize
            console.log('Event resized:', info.event);
        },
        eventDidMount: function(info) {
            if (info.event.textColor) {
              info.el.style.color = info.event.textColor;
            }
          }
    });
  
    calendar.render();
  });