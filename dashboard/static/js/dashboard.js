// PhiLaunch Dashboard JavaScript

let refreshInterval = null;
const REFRESH_RATE = 5000; // 5 seconds

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', () => {
    console.log('PhiLaunch Dashboard initializing...');
    initDashboard();
});

function initDashboard() {
    // Load initial data
    refreshDashboard();

    // Start auto-refresh
    startAutoRefresh();

    // Update timestamps
    updateTimestamp();
    setInterval(updateTimestamp, 1000);
}

function startAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }

    refreshInterval = setInterval(() => {
        refreshDashboard();
    }, REFRESH_RATE);

    document.getElementById('auto-refresh').textContent = 'ON';
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
    document.getElementById('auto-refresh').textContent = 'OFF';
}

async function refreshDashboard() {
    try {
        await Promise.all([
            loadSystemStatus(),
            loadMetrics(),
            loadTasks(),
            loadWowMonitor(),
            loadLogs(),
            loadSystemInfo()
        ]);
        updateLastUpdate();
    } catch (error) {
        console.error('Error refreshing dashboard:', error);
    }
}

async function loadSystemStatus() {
    try {
        const response = await fetch('api/status.json');
        const data = await response.json();

        // System Status
        updateStatusCard('system-status', data.system);

        // Services Status
        updateStatusCard('services-status', data.services);

        // Tasks Status
        updateStatusCard('tasks-status', data.tasks);

        // Uptime
        if (data.uptime) {
            document.getElementById('uptime').textContent = `Uptime: ${data.uptime}`;
        }
    } catch (error) {
        console.error('Error loading system status:', error);
        setOfflineStatus();
    }
}

async function loadMetrics() {
    try {
        const response = await fetch('api/metrics.json');
        const data = await response.json();

        // CPU
        updateMetric('cpu', data.cpu);

        // Memory
        updateMetric('mem', data.memory);

        // Disk
        updateMetric('disk', data.disk);

        // Network
        updateNetworkMetric(data.network);
    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}

async function loadTasks() {
    try {
        const response = await fetch('api/tasks.json');
        const data = await response.json();

        const tasksList = document.getElementById('tasks-list');

        if (data.tasks && data.tasks.length > 0) {
            tasksList.innerHTML = data.tasks.map(task => `
                <div class="task-item">
                    <span class="task-name">${escapeHtml(task.name)}</span>
                    <span class="task-status ${task.status}">${task.status}</span>
                </div>
            `).join('');
        } else {
            tasksList.innerHTML = '<div class="loading-spinner">No active tasks</div>';
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

async function loadWowMonitor() {
    try {
        const response = await fetch('api/wow.json');
        const data = await response.json();

        const monitorDiv = document.getElementById('wow-monitor');

        if (data.enabled && data.stats) {
            monitorDiv.innerHTML = `
                <div class="monitor-stat">
                    <span>Latency (Avg)</span>
                    <span style="color: ${getLatencyColor(data.stats.avg_latency)}">${data.stats.avg_latency}ms</span>
                </div>
                <div class="monitor-stat">
                    <span>Latency (Best)</span>
                    <span style="color: var(--success)">${data.stats.best_latency}ms</span>
                </div>
                <div class="monitor-stat">
                    <span>Latency (Worst)</span>
                    <span style="color: var(--warning)">${data.stats.worst_latency}ms</span>
                </div>
                <div class="monitor-stat">
                    <span>Jitter</span>
                    <span>${data.stats.jitter}ms</span>
                </div>
                <div class="monitor-stat">
                    <span>Packet Loss</span>
                    <span style="color: ${data.stats.loss > 0 ? 'var(--danger)' : 'var(--success)'}">
                        ${data.stats.loss}
                    </span>
                </div>
            `;
        } else {
            monitorDiv.innerHTML = '<div class="loading-spinner">WoW monitor not running</div>';
        }
    } catch (error) {
        console.error('Error loading WoW monitor:', error);
        document.getElementById('wow-monitor').innerHTML = '<div class="loading-spinner">Monitor unavailable</div>';
    }
}

async function loadLogs() {
    try {
        const response = await fetch('api/logs.json');
        const data = await response.json();

        const logsDiv = document.getElementById('logs-content');

        if (data.logs && data.logs.length > 0) {
            logsDiv.innerHTML = data.logs.map(log => `
                <div class="log-entry">
                    <span class="log-timestamp">${log.timestamp}</span>
                    <span>${escapeHtml(log.message)}</span>
                </div>
            `).join('');
        } else {
            logsDiv.innerHTML = '<div class="loading-spinner">No recent logs</div>';
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

async function loadSystemInfo() {
    try {
        const response = await fetch('api/info.json');
        const data = await response.json();

        const infoDiv = document.getElementById('system-info');

        infoDiv.innerHTML = `
            <div class="info-item">
                <span class="info-label">Hostname</span>
                <span class="info-value">${escapeHtml(data.hostname)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">OS</span>
                <span class="info-value">${escapeHtml(data.os)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Kernel</span>
                <span class="info-value">${escapeHtml(data.kernel)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">IP Address</span>
                <span class="info-value">${escapeHtml(data.ip)}</span>
            </div>
        `;
    } catch (error) {
        console.error('Error loading system info:', error);
    }
}

function updateStatusCard(cardId, status) {
    const card = document.getElementById(cardId);
    const indicator = card.querySelector('.status-indicator');

    if (status.online) {
        indicator.className = 'status-indicator online';
        indicator.innerHTML = '<span class="pulse"></span><span>Online</span>';
    } else if (status.warning) {
        indicator.className = 'status-indicator warning';
        indicator.innerHTML = '<span class="pulse"></span><span>Warning</span>';
    } else {
        indicator.className = 'status-indicator offline';
        indicator.innerHTML = '<span class="pulse"></span><span>Offline</span>';
    }
}

function updateMetric(type, data) {
    const usageEl = document.getElementById(`${type}-usage`);
    const barEl = document.getElementById(`${type}-bar`);

    if (data && typeof data.percent !== 'undefined') {
        usageEl.textContent = `${data.percent}%`;
        barEl.style.width = `${data.percent}%`;

        if (data.percent > 80) {
            barEl.classList.add('warning');
        } else {
            barEl.classList.remove('warning');
        }
    }
}

function updateNetworkMetric(data) {
    const statusEl = document.getElementById('network-status');
    const barEl = document.getElementById('net-bar');

    if (data && data.status) {
        statusEl.textContent = data.status;
        barEl.style.width = data.connected ? '100%' : '0%';
    }
}

function setOfflineStatus() {
    ['system-status', 'services-status', 'tasks-status'].forEach(id => {
        const card = document.getElementById(id);
        const indicator = card.querySelector('.status-indicator');
        indicator.className = 'status-indicator offline';
        indicator.innerHTML = '<span class="pulse"></span><span>Offline</span>';
    });
}

function updateLastUpdate() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('last-update').textContent = `Last update: ${timeStr}`;
}

function updateTimestamp() {
    // Update any relative timestamps if needed
}

function getLatencyColor(latency) {
    const ms = parseFloat(latency);
    if (ms < 50) return 'var(--success)';
    if (ms < 100) return 'var(--primary)';
    if (ms < 150) return 'var(--warning)';
    return 'var(--danger)';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Quick Actions
function viewLogs() {
    window.location.href = '/logs';
}

function openScripts() {
    window.location.href = '/scripts';
}

function openConfig() {
    window.location.href = '/config';
}

// Export functions for HTML onclick handlers
window.refreshDashboard = refreshDashboard;
window.viewLogs = viewLogs;
window.openScripts = openScripts;
window.openConfig = openConfig;
