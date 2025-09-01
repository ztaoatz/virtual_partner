<template>
  <div class="page-container">
    <div class="left-section">
      <div class="form-group">
        <label for="action-select">请选择具体行为:</label>
        <select id="action-select" v-model="selectedAction">
          <option>向长辈敬酒</option>
          <option>向老板敬酒</option>
          <option>向朋友敬酒</option>
          <option>宴会开场白</option>
		  <option>自由聊天</option>
          <!-- 其他选项 -->
        </select>
      </div>

      <div class="helper-section">
        <p>帮你的社交小助手选择一个人设吧:</p>
        <textarea readonly>{{ helperText }}</textarea>
        <button @click="dislikeCharacter">确认</button>
      </div>
    </div>

    <div class="right-section">
      <div class="response-box">
        <p>好的, 请提供具体的请求内容</p>
        <textarea readonly>{{ responseText }}</textarea>
      </div>
      <textarea v-model="userInput" placeholder="请在此输入..."></textarea>
      <div class="button-group">
        <button @click="clearRecords">清空输入框</button>
        <button @click="submit">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedAction: '向长辈敬酒',  // 默认行为
      userInput: '',
      responseText: '好的, 请提供具体的请求内容...',
    };
  },
  computed: {
    // 动态生成的辅助文本，基于所选的行为
    helperText() {
      if (this.selectedAction === '向长辈敬酒') {
        return '你是一个懂得尊敬长辈的社交高手，帮我生成一个适合敬酒的表达方式。';
      } else if (this.selectedAction === '向老板敬酒') {
        return '你是一个职场老手，帮我生成一个向老板敬酒时的体面发言。';
      } else if (this.selectedAction === '向朋友敬酒') {
        return '你是一个社交达人，帮我写一个轻松愉快的敬酒词。';
      } else if (this.selectedAction === '宴会开场白') {
        return '你是一个宴会主持人，帮我写一段优雅的宴会开场白。';
      } else if(this.selectedAction == '自由聊天'){
		  return '请在输入框中自由输入';
	  }
	    else{
        return '选择一个场景后，我将为你生成合适的句子。';
      }
    }
  },
  methods: {
    dislikeCharacter() {
      // 这里可以随机改变角色介绍
	  if(this.helperText == '请在输入框中自由输入')
	   this.userInput = '';
	  else
      this.userInput = this.helperText ;
    },
    clearRecords() {
      this.userInput = '';
    },
    submit() {
      // 提交逻辑
      axios.post('http://127.0.0.1:8000/chat/', {
        "prompt": this.userInput,
        "history": '',
        "system": '你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。'
      }).then(result => {
        this.responseText = result.data.result;
        console.log(result);
      });
    }
  }
};
</script>
<style scoped>
.page-container {
  display: flex;
  justify-content: space-around;
  padding: 50px 20px; /* 增加顶部的内边距 */
  background-color: #f0f4ff;
  height: 85vh;
}

.left-section {
  width: 20%; /* 更宽的宽度 */
  height: 80%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.right-section {
  width: 60%; /* 较窄的宽度 */
  height: 80%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 18px;
  color: #1d2975;
}

select {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  margin-top: 10px;
}

.helper-section {
  margin-top: 20px;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  margin-top: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #1d2975;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.response-box p {
  background-color: #e0ebff;
  padding: 10px;
  border-radius: 5px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
