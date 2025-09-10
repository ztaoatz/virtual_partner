import * as PIXI from 'pixi.js'
import {
  Live2DModel,
  MotionPreloadStrategy,
  InternalModel,
} from 'pixi-live2d-display';

// 挂载PIXI到全局
window.PIXI = PIXI;

// 导出初始化方法，注意要加async关键字保证模型读取完整
export async function init(options = {}) {
  const {
    modelPath = '/live2d/Nahida_1080/Nahida_1080.model3.json',
    canvasId = 'canvas_view',
    width = 1920,
    height = 1080,
    transparent = true
  } = options;  try {
    // 获取canvas元素
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
      throw new Error(`找不到ID为 ${canvasId} 的canvas元素`);
    }

    // 创建PIXI应用 - 使用PIXI v6的API
    const app = new PIXI.Application({
      view: canvas,
      transparent: transparent,
      antialias: true,
      width: width,
      height: height,
      autoDensity: true,
      autoStart: true
    });

    console.log('PIXI应用创建成功');

    // 加载模型
    const model = await Live2DModel.from(modelPath, { 
      motionPreload: MotionPreloadStrategy.NONE 
    });    console.log('Live2D模型加载成功');

    // 将模型添加到舞台
    app.stage.addChild(model);    // 设置模型缩放 - 使用较小的缩放值确保能看到
    model.scale.set(0.15);    // 设置模型锚点为中心，确保居中对齐
    model.anchor.set(0.5, 0.5);
    
    // 智能位置计算 - 根据画布尺寸自适应调整
    const centerX = width / 2;
    const centerY = height / 2;
    
    // 根据画布宽度进行微调，确保在不同尺寸下都能良好居中
    const xOffset = width > 500 ? -8 : -5; // 大画布偏移更多
    
    model.x = centerX + xOffset;
    model.y = centerY;
    
    console.log(`模型位置设置: x=${model.x}, y=${model.y}, 画布尺寸: ${width}×${height}`);

    // 启用交互（替代 trackedPointers）
    model.interactive = true;
    model.buttonMode = true;

    // 添加交互功能
    model.on('hit', (hitAreas) => {
      console.log('模型被点击，命中区域：', hitAreas);
      // 播放随机动作
      model.motion('TapBody');
    });

    console.log('Live2D模型初始化成功');
    return { app, model };

  } catch (error) {
    console.error('Live2D模型初始化失败:', error);
    throw error;
  }
}

// 导出清理方法
export function destroy(app) {
  if (app) {
    app.destroy(true);
  }
}
