const API_BASE = "http://127.0.0.1:8000";
let currentGeneratedContent = null;

// Auth Check
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token && !window.location.href.includes('login.html') && !window.location.href.includes('signup.html')) {
        window.location.href = 'login.html';
    }

    if (document.getElementById('userName')) {
        document.getElementById('userName').textContent = localStorage.getItem('userEmail') || 'User';
    }
});

// Handle Generation
if (document.getElementById('generateForm')) {
    document.getElementById('generateForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const topic = document.getElementById('topic').value;
        const platform = document.getElementById('platform').value;
        const tone = document.getElementById('tone').value;
        const target_audience = document.getElementById('audience').value;

        const btn = document.getElementById('generateBtn');
        const loader = document.getElementById('generateLoader');

        btn.disabled = true;
        loader.classList.remove('hidden');

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE}/content/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ topic, platform, tone, target_audience })
            });

            if (response.status === 401) logout();

            const data = await response.json();
            if (response.ok) {
                currentGeneratedContent = data;
                displayPreview(data);
            } else {
                alert(data.detail || 'Generation failed');
            }
        } catch (err) {
            alert('Error connecting to server');
            console.error(err);
        } finally {
            btn.disabled = false;
            loader.classList.add('hidden');
        }
    });
}

function displayPreview(data) {
    document.getElementById('previewPlaceholder').classList.add('hidden');
    document.getElementById('previewContent').classList.remove('hidden');

    document.getElementById('generatedCaption').textContent = data.generated_text;
    document.getElementById('generatedHashtags').textContent = data.hashtags;

    const imgContainer = document.getElementById('generatedImageContainer');
    const img = document.getElementById('generatedImage');

    if (data.image_url) {
        img.src = data.image_url;
        imgContainer.classList.remove('hidden');
    } else {
        imgContainer.classList.add('hidden');
    }
}

async function postToLinkedin() {
    if (!currentGeneratedContent || !currentGeneratedContent.id) {
        showNotification("❌ No content generated to post.", "var(--error)");
        return;
    }

    showNotification("🚀 Posting to your LinkedIn profile...", "var(--primary)");

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/linkedin/post/${currentGeneratedContent.id}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            showNotification("✅ Successfully shared to your LinkedIn profile!", "var(--success)");

            const btn = document.querySelector('button[onclick="postToLinkedin()"]');
            if (btn) {
                btn.innerHTML = '<span>Shared to LinkedIn</span>';
                btn.disabled = true;
                btn.style.opacity = '0.7';
            }
        } else {
            if (data.detail === "LinkedIn not connected") {
                showNotification("❌ LinkedIn not connected. Go to Profile.", "var(--error)");
            } else {
                showNotification(`❌ Failed to post: ${data.detail || 'Unknown error'}`, "var(--error)");
            }
        }

    } catch (err) {
        showNotification("❌ Network error. Check your connection.", "var(--error)");
        console.error(err);
    }
}

async function connectLinkedin() {
    try {
        const response = await fetch(`${API_BASE}/linkedin/login-url`);
        const data = await response.json();
        if (data.url) {
            window.location.href = data.url;
        }
    } catch (err) {
        alert("Failed to get LinkedIn connection link.");
    }
}

function showNotification(text, color) {
    const notify = document.getElementById('notification');
    const notifyText = document.getElementById('notificationText');

    notifyText.textContent = text;
    notify.style.borderLeftColor = color;
    notify.classList.remove('hidden');

    setTimeout(() => {
        notify.classList.add('hidden');
    }, 4000);
}

function saveDraft() {
    showNotification("💾 Draft saved to your history", "var(--text-secondary)");
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    window.location.href = 'login.html';
}
