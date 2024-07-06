<template>
  <div class="feedback-list">
    <h1>已提交的反馈</h1>
    <ul>
      <li v-for="(item, index) in feedbackList" :key="index">
        <div><strong>姓名:</strong> {{ item.name }}</div>
        <div><strong>邮箱:</strong> {{ item.email }}</div>
        <div><strong>联系电话:</strong> {{ item.phone }}</div>
        <div><strong>出错模块:</strong> {{ item.module }}</div>
        <div><strong>上传文件:</strong>
          <span v-for="(file, fileIndex) in item.files" :key="fileIndex">{{ file.name }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { GetFeedbackList } from "@/unity/api";

export default {
  data() {
    return {
      feedbackList: []
    };
  },
  mounted() {
    this.fetchFeedbackList();
  },
  methods: {
    fetchFeedbackList() {
      GetFeedbackList("http://localhost:8096/feedbackList")
          .then(resp => {
            this.feedbackList = resp.data;
          })
          .catch(error => {
            console.error('Error fetching feedback list:', error);
          });
    }
  }
};
</script>

<style>
.feedback-list {
  max-width: 800px;
  margin: 0 auto;
}
.feedback-list ul {
  list-style: none;
  padding: 0;
}
.feedback-list li {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
.feedback-list li div {
  margin-bottom: 5px;
}
.feedback-list li div strong {
  font-weight: bold;
}
.feedback-list li div:last-child {
  margin-bottom: 0;
}
</style>
