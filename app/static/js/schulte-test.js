let sessionId = null;
let currentTable = 1;
let tablesCount = 5;
let times = [];
let startTime;
let timerInterval;
let currentNumber = 1;

function generateTable() {
    let numbers = Array.from({length: 25}, (_, i) => i + 1);
    numbers.sort(() => Math.random() - 0.5);
    
    const container = document.getElementById('table-container');
    container.innerHTML = '';
    
    const table = document.createElement('div');
    table.className = 'schulte-table';
    
    for (let i = 0; i < 25; i++) {
        const cell = document.createElement('div');
        cell.className = 'schulte-cell';
        cell.textContent = numbers[i];
        cell.dataset.number = numbers[i];
        cell.onclick = () => handleCellClick(cell);
        table.appendChild(cell);
    }
    
    container.appendChild(table);
}

function startTimer() {
    startTime = Date.now();
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        const elapsed = (Date.now() - startTime) / 1000;
        document.getElementById('timer').textContent = elapsed.toFixed(1);
    }, 100);
}

function handleCellClick(cell) {
    const number = parseInt(cell.dataset.number);
    
    if (number === currentNumber) {
        cell.classList.add('found');
        currentNumber++;
        
        if (currentNumber > 25) {
            finishTable();
        }
    }
}

function finishTable() {
    clearInterval(timerInterval);
    const endTime = Date.now();
    const timeSpent = (endTime - startTime) / 1000;
    times.push(timeSpent);
    if (currentTable === tablesCount) {
        document.querySelector('.btn').textContent = 'Завершить тестирование';
    }
    document.getElementById('next-table').style.display = 'block';
}

function startNextTable() {
    currentTable++;
    currentNumber = 1;
    
    if (currentTable > tablesCount) {
        submitResults();
        return;
    }
    
    document.getElementById('current-table').textContent = currentTable;
    document.getElementById('next-table').style.display = 'none';
    document.getElementById('timer').textContent = '0.0';
    
    generateTable();
    startTimer();
}

async function submitResults() {
    const response = await fetch('/results/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_id: sessionId,
            times: times
        })
    });
    
    const data = await response.json();
    window.location.href = `/results/${data.result_id}`;
}

document.addEventListener('DOMContentLoaded', function() {
    
    const testContainer = document.getElementById('test-container');
    if (testContainer) {
        
        const sessionIdAttr = testContainer.getAttribute('data-session-id')
        if (sessionIdAttr) {
            sessionId = sessionIdAttr
        }

        const nextBtn = document.getElementById('next-table-btn');
        if (nextBtn) {
            nextBtn.addEventListener('click', startNextTable);
        }
        
        generateTable();
        startTimer();
    }
});