function renderActivityCalendar(activityData, startDateStr, endDateStr) {
    const startDate = new Date(startDateStr);
    const endDate = new Date(endDateStr);

    function getColor(count) {
        if (count === 0) return "#ebebf0";
        if (count === 1) return "#c6e48b";
        if (count === 4) return "#7bc96f";
        if (count === 9) return "#239a3b";
        return "#196127"  
    }

    function formatDate(date) {
        return date.toISOString().split("T")[0];
    }

    const MOUTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    const days = [];
    const cur = new Date(startDate);
    while (cur <= endDate) {
        days.push(new Date(cur));
        cur.setDate(cur.getDate() + 1);
    }

    const firstDow = (startDate.getDay() + 6) % 7;
    const totalCells = firstDow + days.length;
    const totalWeeks = Math.ceil(totalCells / 7);

    const CELL = 42;
    const GAP = 5;
    const LEFT = 56;
    const TOP = 36;

    const svgW = LEFT + totalWeeks * (CELL + GAP);
    const svgH = TOP + 7 * (CELL + GAP);

    let svg = `<svg width="${svgW}" height="${svgH}" xmlns="http://www.w3.org/2000/svg">`;
  
    DAYS.forEach((d, i) => {
        if (d) {
            svg += `<text x="0" y="${TOP + i * (CELL + GAP) + CELL - 3}"
                font-size="14" fill="#767676" font-family="inherit">${d}</text>`;
        }
    });

    let lastMonth = -1;
    days.forEach((date, idx) => {
        const cell = firstDow + idx;
        const col = Math.floor(cell/7);
        const row = cell % 7;

        const x = LEFT + col * (CELL + GAP);
        const y = TOP + row * (CELL + GAP);

        if (date.getMonth() !== lastMonth && row === 0) {
            svg += `<text x="${x}" y="${TOP - 8}"
                font-size="14" fill="#767676" font-family="inherit">
                ${MOUTHS[date.getMonth()]}</text>`;

            lastMonth = date.getMonth();
        }

        const key = formatDate(date);
        const count = activityData[key] || 0;
        const color = getColor(count);
        const title = count > 0 
            ? `${count} task${count > 1 ? "s" : ""} on ${key}`
            : `No tasks on ${key}`;

        svg += `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}"
        rx="3" ry="3" fill="${color}" style="cursor:pointer;">
        <title>${title}</title>
        </rect>`;

    });

    svg += `</svg>`;
    document.getElementById("activityCalendar").innerHTML = svg;


}