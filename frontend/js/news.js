const NEWS_DATA = [
    { id: 1, title: "专家解读：如何预防冠心病", excerpt: "最新研究表明，健康的生活方式可以显著降低心血管疾病的风险...", tag: "预防", date: "2024-01-15" },
    { id: 2, title: "心率监测新技术发布", excerpt: "新一代可穿戴设备能够更精准地监测心率变化，及时预警...", tag: "科技", date: "2024-01-14" },
    { id: 3, title: "地中海饮食与心脏健康", excerpt: "研究证实地中海饮食模式对心血管系统有显著保护作用...", tag: "饮食", date: "2024-01-13" },
    { id: 4, title: "运动对心脏的益处", excerpt: "每周150分钟中等强度运动可有效改善心肺功能...", tag: "运动", date: "2024-01-12" },
    { id: 5, title: "冬季心血管防护指南", excerpt: "气温骤降，如何保护脆弱的心血管系统？专家给出建议...", tag: "季节", date: "2024-01-11" },
    { id: 6, title: "压力管理与心脏健康", excerpt: "长期压力是心血管疾病的重要危险因素，学会释放压力...", tag: "心理", date: "2024-01-10" }
];

let currentNewsIndex = 0;

function renderNews() {
    const container = document.getElementById('newsContainer');
    container.innerHTML = NEWS_DATA.map(news => `
        <div class="news-item">
            <div class="news-thumb">
                <div class="news-image-placeholder">
                    <i class="fas fa-newspaper"></i>
                </div>
                <span class="news-tag">${news.tag}</span>
            </div>
            <div class="news-content">
                <div class="news-meta">${news.date}</div>
                <div class="news-headline">${news.title}</div>
                <div class="news-excerpt">${news.excerpt}</div>
            </div>
        </div>
    `).join('');
}

function scrollNews(direction) {
    const container = document.getElementById('newsContainer');
    const scrollAmount = 340;
    container.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}
