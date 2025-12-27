// ================= ANALYSIS LOGIC =================
let isAnalyzing = false;
let pollInterval;

async function startAnalysis() {
    const videoUrl = document.getElementById('videoUrl').value.trim();

    if (!videoUrl) {
        showStatus('⚠️ Please enter a YouTube URL', 'error');
        return;
    }

    if (!isValidYouTubeUrl(videoUrl)) {
        showStatus('❌ Invalid input: Please enter a valid YouTube URL', 'error');
        return;
    }

    isAnalyzing = true;
    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-block';
    document.getElementById('statsGrid').style.display = 'grid';
    document.getElementById('commentsSection').style.display = 'block';

    try {
        const response = await fetch('http://localhost:5000/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ video_url: videoUrl })
        });

        const data = await response.json();
        
        console.log('Backend response:', data); // Debug log

        // ================= FIX: handle non-live videos =================
        if (data.status === 'success' && data.is_live === true) {
            showStatus('✨ Live stream detected! Capturing vibes ...', 'status');
            pollComments();
        } else if (data.is_live === false) {
            showStatus('❌ The link is not a live video', 'error');
            stopAnalysis(false); // Don't show "paused" message
        } else {
            // fallback for other errors
            showStatus('❌ ' + (data.message || 'Unknown error'), 'error');
            stopAnalysis(false); // Don't show "paused" message
        }
    } catch (error) {
        showStatus('🔌 Backend connection failed: ' + error.message, 'error');
        stopAnalysis(false);
    }
}

function stopAnalysis(showPausedMessage = true) {
    isAnalyzing = false;
    clearTimeout(pollInterval);
    document.getElementById('analyzeBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';
    
    
    if (showPausedMessage) {
        showStatus('⏹️ Analysis paused', 'status');
    }
}

async function pollComments() {
    if (!isAnalyzing) return;

    try {
        const response = await fetch('http://localhost:5000/comments');
        const data = await response.json();

        updateStats(data.stats);
        updateComments(data.comments);

        pollInterval = setTimeout(pollComments, 3000);
    } catch (error) {
        console.error('Error polling comments:', error);
        pollInterval = setTimeout(pollComments, 3000);
    }
}


// ================= YOUTUBE URL VALIDATION =================
function isValidYouTubeUrl(url) {
    const regex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}/;
    return regex.test(url);
}


// ================= COMMENT ANIMATION =================
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'slideIn 0.6s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

function updateComments(comments) {
    const commentsList = document.getElementById('commentsList');
    commentsList.innerHTML = '';

    comments.slice(-50).reverse().forEach((comment, index) => {
        const div = document.createElement('div');
        div.className = `comment ${comment.sentiment.toLowerCase()}`;
        div.style.animationDelay = `${index * 0.05}s`;
        div.innerHTML = `
            <div class="comment-header">
                <span class="comment-author">${escapeHtml(comment.author)}</span>
                <span class="comment-sentiment ${comment.sentiment.toLowerCase()}">
                    ${comment.sentiment}
                </span>
            </div>
            <div class="comment-text">${escapeHtml(comment.text)}</div>
        `;
        commentsList.appendChild(div);
        observer.observe(div);
    });
}


// ================= STATS =================
function updateStats(stats) {
    document.getElementById('totalComments').textContent = stats.total;
    document.getElementById('positiveCount').textContent = stats.positive;
    document.getElementById('neutralCount').textContent = stats.neutral;
    document.getElementById('negativeCount').textContent = stats.negative;

    const total = stats.total || 1;
    document.getElementById('positivePercent').textContent =
        `${Math.round((stats.positive / total) * 100)}%`;
    document.getElementById('neutralPercent').textContent =
        `${Math.round((stats.neutral / total) * 100)}%`;
    document.getElementById('negativePercent').textContent =
        `${Math.round((stats.negative / total) * 100)}%`;
}


// ================= UTILITIES =================
function showStatus(message, type) {
    const statusMsg = document.getElementById('statusMsg');
    statusMsg.className = type;
    statusMsg.textContent = message;
    statusMsg.style.display = 'block';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}