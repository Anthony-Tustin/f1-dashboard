// Converts milliseconds to a readable lap time
function msToLapTime(ms) {
    if (!ms) return "N/A";
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const millis = ms % 1000;
    return `${minutes}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
}

// Shows a notification at the bottom right
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${isError ? 'error' : ''}`;
    setTimeout(() => { toast.className = 'toast hidden'; }, 3000);
}

// Shows and hides tabs when nav buttons are clicked
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`tab-${tabName}`).classList.add('active');
    event.target.classList.add('active');
}

// Returns a CSS class for position colouring (gold/silver/bronze)
function posClass(pos) {
    if (pos === 1) return 'pos-1';
    if (pos === 2) return 'pos-2';
    if (pos === 3) return 'pos-3';
    return '';
}

async function loadDriverStandings() {
    const res = await fetch('/standings/drivers');
    const data = await res.json();
    const el = document.getElementById('driver-standings');

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Pos</th>
                    <th>Driver</th>
                    <th>Team</th>
                    <th>Pts</th>
                    <th>Wins</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(d => `
                    <tr>
                        <td class="pos ${posClass(d.position)}">${d.position}</td>
                        <td class="driver-name">${d.full_name}</td>
                        <td>${d.team_name}</td>
                        <td class="points">${d.points}</td>
                        <td>${d.wins}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

async function loadConstructorStandings() {
    const res = await fetch('/standings/constructors');
    const data = await res.json();
    const el = document.getElementById('constructor-standings');

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Pos</th>
                    <th>Constructor</th>
                    <th>Pts</th>
                    <th>Wins</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(d => `
                    <tr>
                        <td class="pos ${posClass(d.position)}">${d.position}</td>
                        <td class="driver-name">${d.name}</td>
                        <td class="points">${d.points}</td>
                        <td>${d.wins}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}


async function populateRoundSelectors() {
    const res = await fetch('/results/races');
    const data = await res.json();

    const rounds = [...new Set(data.map(r => r.round))].sort((a, b) => a - b);
    const raceName = {};
    data.forEach(r => { raceName[r.round] = r.race_name; });

    const selectors = [
        'results-round-select',
        'qualifying-round-select',
        'laps-round-select',
        'pitstops-round-select',
        'weather-round-select'
    ];

    selectors.forEach(id => {
        const el = document.getElementById(id);
        el.innerHTML = '<option value="">Select a round...</option>';
        rounds.forEach(round => {
            el.innerHTML += `<option value="${round}">Round ${round} — ${raceName[round]}</option>`;
        });
    });
}


async function loadRaceResults() {
    const round = document.getElementById('results-round-select').value;
    if (!round) return;

    const res = await fetch(`/results/races/${round}`);
    const data = await res.json();
    const el = document.getElementById('race-results');

    if (data.length === 0) {
        el.innerHTML = '<p class="loading">No results available for this round.</p>';
        return;
    }

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Pos</th>
                    <th>Driver</th>
                    <th>Team</th>
                    <th>Grid</th>
                    <th>Laps</th>
                    <th>Status</th>
                    <th>Pts</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(r => `
                    <tr>
                        <td class="pos ${posClass(r.position)}">${r.position ?? 'DNF'}</td>
                        <td class="driver-name">${r.driver_name}</td>
                        <td>${r.team_name}</td>
                        <td>${r.grid}</td>
                        <td>${r.laps_completed}</td>
                        <td>${r.status}</td>
                        <td class="points">${r.points}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}


async function loadQualifying() {
    const round = document.getElementById('qualifying-round-select').value;
    if (!round) return;

    const res = await fetch(`/results/qualifying/${round}`);
    const data = await res.json();
    const el = document.getElementById('qualifying-results');

    if (data.length === 0) {
        el.innerHTML = '<p class="loading">No qualifying data available for this round.</p>';
        return;
    }

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Pos</th>
                    <th>Driver</th>
                    <th>Team</th>
                    <th>Q1</th>
                    <th>Q2</th>
                    <th>Q3</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(q => `
                    <tr>
                        <td class="pos ${posClass(q.position)}">${q.position}</td>
                        <td class="driver-name">${q.driver_name}</td>
                        <td>${q.team_name}</td>
                        <td>${q.q1_time ?? '—'}</td>
                        <td>${q.q2_time ?? '—'}</td>
                        <td>${q.q3_time ?? '—'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}


async function loadDriversForRound() {
    const round = document.getElementById('laps-round-select').value;
    if (!round) return;

    const res = await fetch('/standings/drivers');
    const data = await res.json();
    const select = document.getElementById('laps-driver-select');

    select.innerHTML = '<option value="">Select a driver...</option>';
    data.forEach(d => {
        select.innerHTML += `<option value="${d.driver_id}">${d.full_name}</option>`;
    });
}

async function loadLapTimes() {
    const round = document.getElementById('laps-round-select').value;
    const driver = document.getElementById('laps-driver-select').value;
    if (!round || !driver) return;

    const res = await fetch(`/laps/${round}/${driver}`);
    const data = await res.json();
    const el = document.getElementById('lap-times');

    if (data.length === 0) {
        el.innerHTML = '<p class="loading">No lap data available.</p>';
        return;
    }

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Lap</th>
                    <th>Time</th>
                    <th>S1</th>
                    <th>S2</th>
                    <th>S3</th>
                    <th>Compound</th>
                    <th>Best</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(l => `
                    <tr>
                        <td>${l.lap_number}</td>
                        <td>${msToLapTime(l.lap_time_ms)}</td>
                        <td>${msToLapTime(l.sector_1_ms)}</td>
                        <td>${msToLapTime(l.sector_2_ms)}</td>
                        <td>${msToLapTime(l.sector_3_ms)}</td>
                        <td class="compound-${l.compound}">${l.compound ?? '—'}</td>
                        <td>${l.is_personal_best ? '⚡' : ''}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}


async function loadPitStops() {
    const round = document.getElementById('pitstops-round-select').value;
    if (!round) return;

    const res = await fetch(`/laps/pitstops/${round}`);
    const data = await res.json();
    const el = document.getElementById('pit-stops');

    if (data.length === 0) {
        el.innerHTML = '<p class="loading">No pit stop data available.</p>';
        return;
    }

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Driver</th>
                    <th>Stop</th>
                    <th>Lap</th>
                    <th>Duration</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(p => `
                    <tr>
                        <td class="driver-name">${p.driver_name}</td>
                        <td>${p.stop_number}</td>
                        <td>${p.lap}</td>
                        <td>${msToLapTime(p.duration_ms)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}


async function loadWeather() {
    const round = document.getElementById('weather-round-select').value;
    if (!round) return;

    const res = await fetch(`/laps/weather/${round}`);
    const data = await res.json();
    const el = document.getElementById('weather-data');

    if (data.length === 0) {
        el.innerHTML = '<p class="loading">No weather data available.</p>';
        return;
    }

    el.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Air Temp</th>
                    <th>Track Temp</th>
                    <th>Humidity</th>
                    <th>Wind</th>
                    <th>Rain</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(w => `
                    <tr>
                        <td>${w.timestamp}</td>
                        <td>${w.air_temp_c ?? '—'}°C</td>
                        <td>${w.track_temp_c ?? '—'}°C</td>
                        <td>${w.humidity_pct ?? '—'}%</td>
                        <td>${w.wind_speed_ms ?? '—'} m/s</td>
                        <td>${w.rainfall ? '🌧️' : '☀️'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}


async function triggerRefresh() {
    const btn = document.getElementById('refresh-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Refreshing...';

    try {
        const res = await fetch('/refresh', { method: 'POST' });
        const data = await res.json();

        if (data.status === 'success') {
            showToast(`Data refreshed in ${data.duration_ms}ms`);
            loadAllData();
        } else {
            showToast(`Refresh failed: ${data.message}`, true);
        }
    } catch (err) {
        showToast('could not reach server', true);
    } finally {
        btn.disabled = false;
        btn.textContent = '↻ Refresh Data';
    }
}

async function loadLastUpdated() {
    try {
        const res = await fetch('/refresh/status');
        const data = await res.json();
        const el = document.getElementById('last-updated');

        if (data.last_refresh) {
            const date = new Date(data.last_refresh);
            el.textContent = `Last updated: ${date.toLocaleString()}`;
        } else {
            el.textContent = 'Never refreshed';
        }
    } catch {
        document.getElementById('last-updated').textContent = '';
    }
}


async function loadAllData() {
    await loadDriverStandings();
    await loadConstructorStandings();
    await populateRoundSelectors();
    await loadLastUpdated();
}

loadAllData();
