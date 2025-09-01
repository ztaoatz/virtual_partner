
<template>
  <div class="button-container">
    <h1>请选择您想解决的问题</h1>
    <button class="custom-button color-1" @click="handleClick('敬酒', 'conversation')">敬酒</button>
    <button class="custom-button color-2" @click="handleClick('化解尴尬', 'conversation2')">化解尴尬</button>
    <button class="custom-button color-3" @click="handleClick('送祝福', 'conversation3')">送祝福</button>
    <button class="custom-button color-4" @click="handleClick('送祝福小红书版', 'conversation4')">送祝福小红书版</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
	const router = useRouter();
const handleClick = (scenario, page) => {
  console.log(`用户选择了场景: ${scenario}`);
  router.push({ name: page });
  
};



</script>

<style lang="scss" scoped>
.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.8); // 半透明背景以便背景图片可见
}

.custom-button {
  width: 30%; // 调整按钮宽度
  margin: 20px 0; // 调整按钮之间的间距
  padding: 25px; // 调整按钮内边距
  color: white; // 调整按钮文字颜色
  border: 3px solid transparent; // 增加边框，初始为透明
  border-radius: 5px; // 调整按钮圆角
  font-size: 20px; // 调整按钮文字大小
  cursor: pointer; // 鼠标悬停时显示指针
  transition: all 0.3s; // 过渡效果
}

.color-1 {
  background-color: #C3C8F0; // 敬酒按钮颜色
}

.color-2 {
  background-color: #98A1E7; // 请客按钮颜色
}

.color-3 {
  background-color: #7784E9; // 送礼按钮颜色
}

.color-4 {
  background-color: #5465E6; // 送祝福按钮颜色
}

.custom-button:hover {
  opacity: 0.9; // 鼠标悬停时的透明度变化
}
.button-container {
	justify-content: center; /* 使内容在容器中垂直居中 */
	  min-height: 100vh; /* 最小高度为视口高度 */
  background-image: url('../assets/背景.png'); /* 替换为您的图片路径 */
  background-size: cover; /* 覆盖整个容器 */
  background-position: center; /* 将图片置于容器中心 */
  background-repeat: no-repeat; /* 不重复图片 */
  }
</style>