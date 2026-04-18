import os
import pickle
import numpy as np
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'multi_disease_model.pkl')

disease_models = None
all_features = None
disease_list = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    disease_models = model_data['disease_models']
    all_features = model_data['all_features']
    disease_list = model_data['disease_list']
    logger.info(f"多疾病预测模型加载成功，支持疾病: {disease_list}")
except FileNotFoundError:
    logger.error(f"模型文件未找到: {MODEL_PATH}")
except Exception as e:
    logger.error(f"加载模型失败: {str(e)}")


def convert_to_number(value):
    if value is None or value == '' or value == 'null' or value == 'NULL':
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    
    if isinstance(value, str):
        value = value.strip()
        
        if value.lower() in ['true', 'yes', '是', '有']:
            return 1.0
        if value.lower() in ['false', 'no', '否', '无']:
            return 0.0
        
        if '/' in value:
            try:
                parts = value.split('/')
                if len(parts) >= 1:
                    return float(parts[0])
            except (ValueError, IndexError):
                pass
        
        try:
            return float(value)
        except (ValueError, TypeError):
            pass
    
    return 0.0


def predict_diseases(medical_report_data):
    if disease_models is None or all_features is None:
        logger.error("多疾病预测模型未加载")
        return None
    
    try:
        feature_values = []
        for feature in all_features:
            value = medical_report_data.get(feature)
            num_value = convert_to_number(value)
            feature_values.append(num_value)
        
        X = np.array(feature_values).reshape(1, -1)
        
        predictions = {}
        for disease, model_info in disease_models.items():
            model = model_info['model']
            scaler = model_info['scaler']
            imputer = model_info['imputer']
            
            X_imputed = imputer.transform(X)
            X_scaled = scaler.transform(X_imputed)
            prob = model.predict_proba(X_scaled)[0, 1]
            
            if prob < 0.2:
                level = "低风险"
                advice = "保持健康生活方式"
            elif prob < 0.4:
                level = "中低风险"
                advice = "注意饮食运动"
            elif prob < 0.6:
                level = "中等风险"
                advice = "建议咨询医生"
            elif prob < 0.8:
                level = "中高风险"
                advice = "请尽快就医"
            else:
                level = "高风险"
                advice = "立即就医！"
            
            predictions[disease] = {
                'risk_score': round(float(prob), 4),
                'risk_level': level,
                'advice': advice,
                'accuracy': model_info['accuracy']
            }
        
        highest_risk = max(predictions.items(), key=lambda x: x[1]['risk_score'])
        
        result = {
            'predictions': predictions,
            'highest_risk_disease': highest_risk[0],
            'highest_risk_score': highest_risk[1]['risk_score']
        }
        
        logger.info(f"疾病预测完成，最高风险: {highest_risk[0]} ({highest_risk[1]['risk_score']})")
        return result
        
    except Exception as e:
        logger.error(f"疾病预测失败: {str(e)}", exc_info=True)
        return None
