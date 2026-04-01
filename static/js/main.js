// 龙虾 Skill 合集平台 - 主 JavaScript

// 页面加载时获取平台统计
document.addEventListener('DOMContentLoaded', function() {
    loadPlatformStats();
});

// 加载平台统计
function loadPlatformStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            const statsEl = document.getElementById('platformStats');
            if (statsEl) {
                statsEl.innerHTML = `
                    <span>📦 ${data.total_skills} 个技能</span> | 
                    <span>👥 ${data.total_users} 位用户</span> | 
                    <span>⬇️ ${data.total_downloads} 次下载</span>
                `;
            }
        })
        .catch(error => {
            console.error('加载统计数据失败:', error);
        });
}

// 搜索功能增强
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    let timeout = null;
    searchInput.addEventListener('input', function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            // 可以添加实时搜索功能
            console.log('搜索关键词:', e.target.value);
        }, 500);
    });
}

// 文件上传预览
const fileInput = document.querySelector('input[type="file"]');
if (fileInput) {
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const fileSize = (file.size / 1024).toFixed(2);
            console.log(`选择文件：${file.name}, 大小：${fileSize} KB`);
        }
    });
}

// 采纳推荐功能（已在全局函数中定义）
function acceptRecommendation(skillId) {
    if (!confirm('确认采纳这个推荐吗？这将帮助系统更好地为你推荐技能。')) {
        return;
    }

    fetch('/api/recommendations/accept', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({skill_id: skillId})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('✓ 感谢反馈！推荐已记录，积分已发放给上传者。');
            // 移除该推荐卡片
            const card = document.querySelector(`[data-skill-id="${skillId}"]`);
            if (card) {
                card.style.opacity = '0.5';
                card.querySelector('.btn-accept-recommendation').textContent = '✓ 已采纳';
                card.querySelector('.btn-accept-recommendation').disabled = true;
            }
        } else {
            alert('操作失败，请重试');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请检查网络连接');
    });
}

// 记录技能使用
function recordUsage(skillId) {
    fetch(`/skill/${skillId}/use`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({duration: 0, success: true})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('✓ 已记录使用，感谢反馈！');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败');
    });
}

// 模态框关闭
window.onclick = function(event) {
    const modal = document.getElementById('loginModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// 表单验证
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredInputs = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('请填写所有必填项');
        }
    });
});

// 技能卡片点击跳转
document.querySelectorAll('.skill-card').forEach(card => {
    if (!card.querySelector('.btn-accept-recommendation')) {
        card.addEventListener('click', function(e) {
            if (!e.target.classList.contains('btn')) {
                const skillId = this.dataset.skillId || this.querySelector('a[href^="/skill/"]').href.split('/').pop();
                window.location.href = `/skill/${skillId}`;
            }
        });
    }
});

console.log('🦞 龙虾 Skill 平台已加载');
