/**
 * Smart Study Management System Client API Module
 * Handles all asynchronous interactions with the FastAPI backend.
 */

const API_BASE = window.location.origin + "/api/v1";

const SmartStudyAPI = {
    // Auth Token Helpers
    getToken() {
        return localStorage.getItem("smart_study_token") || "mock-token-usr_alex_001";
    },
    setToken(token) {
        localStorage.setItem("smart_study_token", token);
    },
    clearToken() {
        localStorage.removeItem("smart_study_token");
        localStorage.removeItem("smart_study_user");
    },
    getCurrentUser() {
        const u = localStorage.getItem("smart_study_user");
        return u ? JSON.parse(u) : { id: "usr_alex_001", name: "Alex Morgan", role: "student" };
    },

    // HTTP Helper
    async request(endpoint, options = {}) {
        const headers = {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.getToken()}`,
            ...options.headers
        };

        try {
            const url = endpoint.startsWith("http") ? endpoint : `${API_BASE}${endpoint}`;
            const res = await fetch(url, { ...options, headers });
            if (!res.ok) {
                const errData = await res.json().catch(() => ({ detail: "Unknown server error" }));
                throw new Error(errData.detail || `Request failed with status ${res.status}`);
            }
            return await res.json();
        } catch (error) {
            console.error(`[API Error] ${endpoint}:`, error);
            throw error;
        }
    },

    // 1. Auth Services
    async login(email, password) {
        const data = await this.request("/auth/login", {
            method: "POST",
            body: JSON.stringify({ email, password })
        });
        if (data.token) {
            this.setToken(data.token);
            localStorage.setItem("smart_study_user", JSON.stringify(data.user));
        }
        return data;
    },

    async getProfile() {
        return await this.request("/auth/me");
    },

    // 2. Student Services
    async getStudentSchedule() {
        const user = this.getCurrentUser();
        return await this.request(`/student/schedule?user_id=${user.id || 'usr_alex_001'}`);
    },

    async toggleStudyBlock(blockId, completed) {
        return await this.request(`/student/schedule/blocks/${blockId}/toggle`, {
            method: "POST",
            body: JSON.stringify({ completed })
        });
    },

    async getStudentProgress() {
        const user = this.getCurrentUser();
        return await this.request(`/student/progress?user_id=${user.id || 'usr_alex_001'}`);
    },

    // 3. Faculty Services
    async getFacultyOverview() {
        return await this.request("/faculty/overview");
    },

    async getFacultyStudents() {
        return await this.request("/faculty/students");
    },

    // 4. Syllabus Services
    async getSyllabi() {
        return await this.request("/syllabi");
    },

    async uploadSyllabus(course_code, course_title, term, syllabus_text) {
        return await this.request("/syllabi/upload", {
            method: "POST",
            body: JSON.stringify({ course_code, course_title, term, syllabus_text })
        });
    },

    // 5. Quiz Services
    async getQuizHistory() {
        const user = this.getCurrentUser();
        return await this.request(`/quizzes/history?user_id=${user.id || 'usr_alex_001'}`);
    },

    async generateQuiz(course_code, topic, question_count = 3, difficulty = "Medium") {
        const user = this.getCurrentUser();
        return await this.request(`/quizzes/generate?user_id=${user.id || 'usr_alex_001'}`, {
            method: "POST",
            body: JSON.stringify({ course_code, topic, question_count, difficulty })
        });
    },

    async submitQuiz(quizId, answers) {
        const user = this.getCurrentUser();
        return await this.request(`/quizzes/${quizId}/submit?user_id=${user.id || 'usr_alex_001'}`, {
            method: "POST",
            body: JSON.stringify({ answers })
        });
    }
};

window.SmartStudyAPI = SmartStudyAPI;
