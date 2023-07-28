function formatTime(date) {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
}

document.addEventListener('DOMContentLoaded', function() {
	var eventsDataElement = document.getElementById('events-data');
    var eventsData = JSON.parse(eventsDataElement.textContent || '[]');
	var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, { 
		themeSystem: 'bootstrap5',
		editable: false,
		aspectRatio: 2,
		events: eventsData,
		headerToolbar: {
			start: 'dayGridMonth dayGridWeek timeGridDay',
			center: 'title',
			end: 'today prev,next'
		},
		footerToolbar: {
			start: ''
		},
		views: {
			dayGridMonth: {
				dayMaxEventRows: 2,
				eventTimeFormat: {
					hour: 'numeric',
					minute: '2-digit',
					meridiem: false,
					displayEventEnd: true
				}
			},
			timeGridWeek: {
				
			}
		},
		eventContent: function(arg) {
            return {
              html: `<div class="fc-content">
                        <span class="fc-time">${formatTime(arg.event.start)} - ${formatTime(arg.event.end)}</span>
                        <span class="fc-title">${arg.event.title}</span>
                    </div>`
            };
        },
        eventRender: function(info) {
            var contentElement = info.el.querySelector('.fc-content');
            var isOverflowing = contentElement.offsetWidth < contentElement.scrollWidth;
            if (isOverflowing) {
              	info.el.classList.add('fc-event-hide-text');
            }
        },
        eventClick: function(info) {
            console.log('Event clicked:', info.event);
        },
        eventDrop: function(info) {
            console.log('Event dropped:', info.event);
        },
        eventResize: function(info) {
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




// document.addEventListener('DOMContentLoaded', function() {
//     var eventsDataElement = document.getElementById('events-data');
//     var eventsData = JSON.parse(eventsDataElement.textContent || '[]');

//     var calendarEl = document.getElementById('calendar');
//     var calendar = new FullCalendar.Calendar(calendarEl, {
//         themeSystem: 'bootstrap5',
//         editable: false, 
//         events: eventsData,
//         aspectRatio: 2,
//         headerToolbar: {
//             left: 'prev,next today',
//             center: 'title',
//             right: 'dayGridMonth,timeGridWeek,timeGridDay'
//         },
//         slotDuration: '01:00:00', 
//         slotLabelInterval: '01:00:00',
//         views: {
//             dayGridMonth: {
//                 dayMaxEventRows: 2,
//                 eventTimeFormat: {
//                     hour: 'numeric',
//                     minute: '2-digit',
//                     meridiem: false,
//                     displayEventEnd: true
//                 }
//             },
//             timeGridWeek: {
//               eventContent: function(arg) {
//                 return {
//                   html: `<div class="fc-content">
//                             <span class="fc-time">${formatTime(arg.event.start)}</span>
//                             <span class="fc-title">${arg.event.title}</span>
//                         </div>`
//                 };
//               },
//             }
//         },
//         eventContent: function(arg) {
//             return {
//               html: `<div class="fc-content">
//                         <span class="fc-time">${formatTime(arg.event.start)} - ${formatTime(arg.event.end)}</span>
//                         <span class="fc-title">${arg.event.title}</span>
//                     </div>`
//             };
//         },
//         eventRender: function(info) {
//             var contentElement = info.el.querySelector('.fc-content');
//             var isOverflowing = contentElement.offsetWidth < contentElement.scrollWidth;
//             if (isOverflowing) {
//               	info.el.classList.add('fc-event-hide-text');
//             }
//         },
//         eventClick: function(info) {
//             // Handle event click
//             console.log('Event clicked:', info.event);
//         },
//         eventDrop: function(info) {
//             // Handle event drop (moving event)
//             console.log('Event dropped:', info.event);
//         },
//         eventResize: function(info) {
//             // Handle event resize
//             console.log('Event resized:', info.event);
//         },
//         eventDidMount: function(info) {
//             if (info.event.textColor) {
//               info.el.style.color = info.event.textColor;
//             }
//           }
//     });
  
//     calendar.render();
//   });

  $(document).ready(function() {
    $('.datetimepicker').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        minDate: '2023-07-01',  // Minimum allowed date
        maxDate: '2023-07-31',  // Maximum allowed date
        disabledTimeIntervals: [
            ['09:00', '10:00'],
            ['12:00', '13:00'],
            ['15:00', '16:00']
        ]  // Array of disabled time intervals
    });
});