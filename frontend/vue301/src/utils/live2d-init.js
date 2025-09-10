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
  } = options;

  try {
    // 加载模型
    const model = await Live2DModel.from(modelPath, { 
      motionPreload: MotionPreloadStrategy.NONE 
    });

    // 创建模型对象
    const app = new PIXI.Application({
      // 配置模型舞台
      view: document.getElementById(canvasId),
      // 背景是否透明
      transparent,
      autoDensity: true,
      autoResize: true,
      antialias: true,
      // 高度
      height,
      // 宽度
      width
    });

    // 将模型添加到舞台
    app.stage.addChild(model);

    // 设置模型位置和缩放
    model.x = app.view.width / 2;
    model.y = app.view.height / 2;
    model.scale.set(0.3); // 适当缩放模型

    // 可选：添加交互功能
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
