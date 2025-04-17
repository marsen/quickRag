<template>
  <div class="p-6 max-w-4xl mx-auto space-y-8">
    <!-- 頂部標題 -->
    <header class="text-center">
      <h1 class="text-4xl font-extrabold text-gray-800 mb-2">RAG Notebook</h1>
      <p class="text-gray-600">文件上傳與問答系統</p>
    </header>

    <!-- 文件上傳卡片 -->
    <div class="bg-white shadow-md rounded-lg p-6">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">上傳文件</h2>
      <div class="flex items-center space-x-4">
        <input
          type="file"
          @change="handleFileUpload"
          class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button
          @click="uploadFile"
          class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition"
        >
          上傳
        </button>
      </div>
    </div>

    <!-- 問答卡片 -->
    <div class="bg-white shadow-md rounded-lg p-6">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">問答</h2>
      <div class="space-y-4">
        <input
          v-model="question"
          type="text"
          placeholder="輸入你的問題"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="askQuestion"
          class="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition w-full"
        >
          提交問題
        </button>
      </div>
    </div>

    <!-- 回答卡片 -->
    <div v-if="answer" class="bg-white shadow-md rounded-lg p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-2">回答：</h3>
      <p class="text-gray-700">{{ answer }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  setup() {
    const file = ref<File | null>(null);
    const question = ref<string>("");
    const answer = ref<string>("");

    const handleFileUpload = (event: Event) => {
      const target = event.target as HTMLInputElement;
      file.value = target.files?.[0] || null;
    };

    const uploadFile = async () => {
      if (!file.value) {
        alert("請選擇一個文件！");
        return;
      }

      const formData = new FormData();
      formData.append("file", file.value);

      try {
        const response = await axios.post(`${API_URL}/upload`, formData);
        alert(`文件已成功上傳！分割為 ${response.data.chunks} 個區塊。`);
      } catch (error) {
        alert("文件上傳失敗！");
      }
    };

    const askQuestion = async () => {
      if (!question.value) {
        alert("請輸入問題！");
        return;
      }

      try {
        const response = await axios.get(`${API_URL}/ask`, {
          params: { q: question.value },
        });
        answer.value = response.data.answer;
      } catch (error) {
        alert("無法獲取回答！");
      }
    };

    return {
      file,
      question,
      answer,
      handleFileUpload,
      uploadFile,
      askQuestion,
    };
  },
};
</script>

<style scoped>
/* 可選：自定義樣式 */
</style>