// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const timetableData = [
        // Example timetable data
        { batch: '2024', course: 'CS101', day: 'Monday', time: '10:00 AM', room: 'A101' },
        { batch: '2024', course: 'CS102', day: 'Wednesday', time: '1:00 PM', room: 'B102' },
        // Add more entries as needed
    ];

    window.searchTimetable = () => {
        const batchYear = document.getElementById('batchYear').value;
        const courseName = document.getElementById('courseName').value.toLowerCase();
        const timetableContainer = document.getElementById('timetableContainer');
        timetableContainer.innerHTML = '';

        const filteredTimetable = timetableData.filter(entry => 
            (batchYear === '' || entry.batch === batchYear) && 
            (courseName === '' || entry.course.toLowerCase().includes(courseName))
        );

        if (filteredTimetable.length === 0) {
            timetableContainer.innerHTML = '<p>No timetable entries found.</p>';
        } else {
            filteredTimetable.forEach(entry => {
                const timetableEntry = document.createElement('div');
                timetableEntry.className = 'timetable-entry';
                timetableEntry.innerHTML = `
                    <p><strong>Course:</strong> ${entry.course}</p>
                    <p><strong>Day:</strong> ${entry.day}</p>
                    <p><strong>Time:</strong> ${entry.time}</p>
                    <p><strong>Room:</strong> ${entry.room}</p>
                `;
                timetableContainer.appendChild(timetableEntry);
            });
        }
    };
});
