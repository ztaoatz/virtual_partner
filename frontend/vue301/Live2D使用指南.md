# Live2D组件使用指南

## 已创建的文件

### 1. 核心工具模块
- `src/utils/live2d-init.js` - Live2D初始化工具

### 2. 可复用组件
- `src/components/Live2DCanvas.vue` - Live2D画布组件

### 3. 示例页面
- `src/view/Live2DDemo.vue` - 完整功能演示
- `src/view/Live2DSimple.vue` - 简单集成示例
- `src/view/ConversationWithLive2D.vue` - 对话页面集成示例

## 如何使用Live2D组件

### 基本用法

```vue
<template>
  <div class="your-page">
    <!-- 其他内容 -->
    
    <!-- Live2D组件 -->
    <Live2DCanvas 
      ref="live2dRef"
      :width="400"
      :height="600"
      :scale="0.3"
      :modelPath="'/live2d/Nahida_1080/Nahida_1080.model3.json'"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Live2DCanvas from '@/components/Live2DCanvas.vue'

const live2dRef = ref(null)

// 控制Live2D模型
const interactWithModel = () => {
  if (live2dRef.value) {
    // 播放动作
    live2dRef.value.playMotion('TapBody')
    
    // 设置表情
    live2dRef.value.setExpression('Happy1')
  }
}
</script>
```

### 组件属性 (Props)

- `modelPath`: 模型文件路径 (默认: Nahida模型)
- `width`: 画布宽度 (默认: 1920)
- `height`: 画布高度 (默认: 1080)
- `scale`: 模型缩放比例 (默认: 0.3)

### 可用方法

通过 `ref` 调用组件方法：

- `playMotion(motionGroup, index)` - 播放动作
- `setExpression(expressionName)` - 设置表情
- `getModel()` - 获取Live2D模型实例
- `getApp()` - 获取PIXI应用实例

### 可用的动作 (Motions)

- `'Idle'` - 待机动作
- `'TapBody'` - 点击身体
- `'TapHead'` - 点击头部

### 可用的表情 (Expressions)

- `'Happy1'` - 开心
- `'Sad1'` - 难过
- `'Angry'` - 生气
- `'Shy'` - 害羞
- `'StarEye'` - 星星眼
- `'Wink'` - 眨眼

## 访问示例页面

1. **完整演示**: `http://localhost:端口/#/live2d-demo`
2. **简单示例**: `http://localhost:端口/#/live2d-simple`
3. **对话集成**: `http://localhost:端口/#/conversation-live2d`

## 集成到现有页面

### 替换ConversationNew.vue中的静态图片

如果您想在现有的ConversationNew.vue中集成Live2D，只需要：

1. 导入Live2DCanvas组件
2. 替换静态图片部分
3. 添加Live2D控制逻辑

示例代码片段：
```vue
<!-- 替换原来的 img 标签 -->
<Live2DCanvas 
  ref="live2dRef"
  :width="300"
  :height="400"
  :scale="0.25"
/>

<!-- 在需要的时候控制模型 -->
<script setup>
import Live2DCanvas from '@/components/Live2DCanvas.vue'

const live2dRef = ref(null)

// 在AI说话时触发动作
const onAISpeaking = () => {
  if (live2dRef.value) {
    live2dRef.value.playMotion('TapBody')
  }
}

// 在用户互动时触发表情
const onUserInteraction = () => {
  if (live2dRef.value) {
    live2dRef.value.setExpression('Happy1')
  }
}
</script>
```

## 性能优化建议

1. **按需加载**: 使用动态import加载Live2D组件
2. **资源管理**: 在组件销毁时正确清理PIXI资源
3. **模型缓存**: 相同模型可以复用，避免重复加载

## 故障排除

1. **模型加载失败**: 检查模型文件路径是否正确
2. **白屏**: 确保index.html中的依赖文件已正确引入
3. **性能问题**: 适当调整模型缩放比例和画布大小
