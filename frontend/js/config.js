const API_BASE = 'http://localhost:8000';
let currentUsername = '';

const formFields = [
    { name: 'heart_disease', label: '心脏病史', type: 'select', options: ['No', 'Yes'] },
    { name: 'bmi', label: 'BMI指数', type: 'number', step: '0.1', placeholder: '24.5' },
    { name: 'smoking', label: '吸烟', type: 'select', options: ['No', 'Yes'] },
    { name: 'alcohol_drinking', label: '饮酒', type: 'select', options: ['No', 'Yes'] },
    { name: 'stroke', label: '中风史', type: 'select', options: ['No', 'Yes'] },
    { name: 'physical_health', label: '身体不适天数(30天内)', type: 'number', min: 0, max: 30, placeholder: '0' },
    { name: 'mental_health', label: '心理不适天数(30天内)', type: 'number', min: 0, max: 30, placeholder: '0' },
    { name: 'diff_walking', label: '行走困难', type: 'select', options: ['No', 'Yes'] },
    { name: 'sex', label: '性别', type: 'select', options: ['男', '女'] },
    { name: 'age_category', label: '年龄组', type: 'select', options: ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+'] },
    { name: 'race', label: '种族', type: 'select', options: ['白人', '黑人', '亚洲人', '西班牙裔', '其他'] },
    { name: 'diabetic', label: '糖尿病', type: 'select', options: ['No', 'Yes'] },
    { name: 'physical_activity', label: '规律运动', type: 'select', options: ['No', 'Yes'] },
    { name: 'gen_health', label: '健康自评', type: 'select', options: ['优秀', '很好', '好', '一般', '差'] },
    { name: 'sleep_time', label: '睡眠时间(小时)', type: 'number', min: 0, max: 24, placeholder: '7' },
    { name: 'asthma', label: '哮喘', type: 'select', options: ['No', 'Yes'] },
    { name: 'kidney_disease', label: '肾病', type: 'select', options: ['No', 'Yes'] },
    { name: 'skin_cancer', label: '皮肤癌', type: 'select', options: ['No', 'Yes'] }
];

let currentNewsStart = 1;
let currentNewsEnd = 2;
let isLoadingNews = false;
