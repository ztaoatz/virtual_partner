<template>
  <div class="page-container">
    <div class="left-section">
      <div class="form-group">
        <label for="action-select">请选择具体行为:</label>
        <select id="action-select" v-model="selectedAction">
          <option>破冰尴尬</option>
          <option>解决矛盾</option>
          <option>酒桌冷场</option>
          <option>忘记对方身份</option>
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
      <textarea v-model="userInput" placeholder="请你重新生成一个..."></textarea>
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
      selectedAction: '破冰尴尬',  // 默认行为
      userInput: '',
      responseText: '好的, 请提供具体的请求内容...',
    };
  },
  computed: {
    // 动态生成的辅助文本，基于所选的行为
    helperText() {
      if (this.selectedAction === '破冰尴尬') {
        return '你第一次见一个新朋友，场面有点冷，你需要幽默地打破沉默，建立初步的交流氛围，你该怎么说？';
      } else if (this.selectedAction === '解决矛盾') {
        return '你和小王有些小矛盾，彼此沉默了一段时间。现在你想积极地化解这段僵局，应该如何委婉地开口让气氛缓和下来？';
      } else if (this.selectedAction === '酒桌冷场') {
        return '公司聚餐时，酒桌上的气氛有些冷场，大家都不太说话。你想通过几句幽默话活跃气氛，你该怎么说？';
      } else if (this.selectedAction === '忘记对方身份') {
        return '在酒局上，有人问你“您还记得我吗？”但你不认得对方，为了不尴尬，你该怎么高情商地回应？';
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
      // Submit form logic
	  //console.log(result);
	  axios.post('http://127.0.0.1:8000/chat/',{"prompt":this.userInput,"history":'',"system":'你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。在处理问题时，你应当考虑到文化背景、社会规范和个人情感，以帮助用户更好地理解复杂的人际关系和社会互动。'})
			.then(result=>{
				this.responseText=result.data.result
				console.log(result)
			})
      
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
