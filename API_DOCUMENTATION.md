# Video Generation API 文件

## 專案簡介

Video Generation API 是一個視頻生成 API 服務，提供文字轉視頻（Text-to-Video）和圖片轉視頻（Image-to-Video）功能。

## 基本資訊

- **基礎 URL**: `https://video-gen.aimate.am` 
- **API 版本**: v1
- **內容類型**: `application/json`

## API 端點列表

### 1. 創建視頻生成任務 (Create Video Task)

**端點**: `POST /api/v1/videos/tasks`

**描述**: 創建一個新的視頻生成任務，支援純文字或文字+圖片兩種模式。

#### 請求參數

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| prompt | string | 是 | 視頻生成的文字提示詞
| image_url | string | 否 | 可選的圖片 URL，用於圖片轉視頻功能 |

#### 請求範例

##### 範例 1: 文字轉視頻 (Text-to-Video)

```bash
curl -X POST "https://video-gen.aimate.am/api/v1/videos/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat playing piano in a cozy living room"
  }'
```

使用 Python:

```python
import requests

url = "https://video-gen.aimate.am/api/v1/videos/tasks"
payload = {
    "prompt": "A cat playing piano in a cozy living room"
}

response = requests.post(url, json=payload)
result = response.json()
print(result)
```

##### 範例 2: 圖片轉視頻 (Image-to-Video)

```bash
curl -X POST "https://video-gen.aimate.am/api/v1/videos/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset scene with moving clouds",
    "image_url": "https://example.com/image.jpg"
  }'
```

使用 Python:

```python
import requests

url = "https://video-gen.aimate.am/api/v1/videos/tasks"
payload = {
    "prompt": "A beautiful sunset scene with moving clouds",
    "image_url": "https://example.com/image.jpg"
}

response = requests.post(url, json=payload)
result = response.json()
print(result)
```

#### 成功回應 (HTTP 201)

```json
{
  "code": 0,
  "message": "Video generation task created successfully",
  "data": {
    "id": "task_abc123xyz",
    "model": "ep-20260129105436-445p4",
    "status": "pending",
    "created_at": 1706601234,
    "updated_at": null,
    "result": null,
    "error": null
  }
}
```

#### 錯誤回應

##### 400 Bad Request (無效參數)
```json
{
  "detail": "Prompt cannot be empty"
}
```

##### 503 Service Unavailable (API 連接錯誤)
```json
{
  "detail": "Failed to connect to video generation service"
}
```

##### 500 Internal Server Error (系統錯誤)
```json
{
  "detail": "Unexpected error: [error message]"
}
```

---

### 2. 查詢任務狀態 (Query Video Task)

**端點**: `GET /api/v1/videos/tasks/{task_id}`

**描述**: 查詢指定任務的生成狀態和結果。

#### 路徑參數

| 參數名 | 類型 | 必填 | 說明 |
|--------|------|------|------|
| task_id | string | 是 | 從創建任務接口返回的任務 ID |

#### 請求範例

```bash
curl -X GET "https://video-gen.aimate.am/api/v1/videos/tasks/task_abc123xyz"
```

使用 Python:

```python
import requests

task_id = "task_abc123xyz"
url = f"https://video-gen.aimate.am/api/v1/videos/tasks/{task_id}"

response = requests.get(url)
result = response.json()
print(result)
```

#### 成功回應 (HTTP 200)

##### 任務處理中
```json
{
  "code": 0,
  "message": "Task query successful",
  "data": {
    "id": "task_abc123xyz",
    "model": "ep-20260129105436-445p4",
    "status": "processing",
    "created_at": 1706601234,
    "updated_at": 1706601240,
    "result": null,
    "error": null
  }
}
```

##### 任務完成
```json
{
  "code": 0,
  "message": "Task query successful",
  "data": {
    "id": "task_abc123xyz",
    "model": "ep-20260129105436-445p4",
    "status": "completed",
    "created_at": 1706601234,
    "updated_at": 1706601350,
    "result": {
      "video_url": "https://example.com/videos/generated_video.mp4",
      "duration": 5.0,
      "resolution": "1920x1080"
    },
    "error": null
  }
}
```

##### 任務失敗
```json
{
  "code": 0,
  "message": "Task query successful",
  "data": {
    "id": "task_abc123xyz",
    "model": "ep-20260129105436-445p4",
    "status": "failed",
    "created_at": 1706601234,
    "updated_at": 1706601350,
    "result": null,
    "error": "Video generation failed: Invalid prompt format"
  }
}
```

#### 任務狀態說明

| 狀態 | 說明 |
|------|------|
| pending | 任務已創建，等待處理 |
| processing | 任務正在處理中 |
| completed | 任務已完成，可以獲取視頻 URL |
| failed | 任務失敗，查看 error 欄位了解原因 |

#### 錯誤回應

##### 503 Service Unavailable
```json
{
  "detail": "Failed to connect to video generation service"
}
```

##### 500 Internal Server Error
```json
{
  "detail": "Unexpected error: [error message]"
}
```

---

### 3. 健康檢查 (Health Check)

**端點**: `GET /api/v1/videos/health`

**描述**: 檢查視頻生成服務是否正常運行。

#### 請求範例

```bash
curl -X GET "https://video-gen.aimate.am/api/v1/videos/health"
```

#### 成功回應 (HTTP 200)

```json
{
  "status": "healthy",
  "service": "video_generation",
  "message": "Service is running normally"
}
```

---

## 完整使用流程範例

### Python 完整範例

```python
import requests
import time
import json

# 配置
BASE_URL = "https://video-gen.aimate.am"
API_ENDPOINT = f"{BASE_URL}/api/v1/videos/tasks"

def create_and_wait_for_video(prompt: str, image_url: str = None, max_wait_seconds: int = 300):
    """
    創建視頻生成任務並等待完成
    
    Args:
        prompt: 文字提示詞
        image_url: 可選的圖片 URL
        max_wait_seconds: 最大等待時間（秒）
    
    Returns:
        dict: 完成的任務結果或 None（如果失敗）
    """
    # 步驟 1: 創建任務
    print("步驟 1: 創建視頻生成任務...")
    payload = {"prompt": prompt}
    if image_url:
        payload["image_url"] = image_url
    
    try:
        response = requests.post(API_ENDPOINT, json=payload)
        response.raise_for_status()
        create_result = response.json()
        
        if create_result.get("code") != 0:
            print(f"任務創建失敗: {create_result.get('message')}")
            return None
        
        task_id = create_result["data"]["id"]
        print(f"✓ 任務創建成功！任務 ID: {task_id}")
        
    except Exception as e:
        print(f"✗ 創建任務時發生錯誤: {e}")
        return None
    
    # 步驟 2: 輪詢查詢任務狀態
    print("\n步驟 2: 等待視頻生成完成...")
    query_url = f"{API_ENDPOINT}/{task_id}"
    start_time = time.time()
    
    while True:
        # 檢查是否超時
        if time.time() - start_time > max_wait_seconds:
            print(f"✗ 等待超時（超過 {max_wait_seconds} 秒）")
            return None
        
        try:
            # 查詢任務狀態
            response = requests.get(query_url)
            response.raise_for_status()
            query_result = response.json()
            
            if query_result.get("code") != 0:
                print(f"✗ 查詢失敗: {query_result.get('message')}")
                return None
            
            task_data = query_result["data"]
            status = task_data["status"]
            
            print(f"  當前狀態: {status}")
            
            if status == "completed":
                print("\n✓ 視頻生成完成！")
                print(f"視頻結果: {json.dumps(task_data['result'], indent=2)}")
                return task_data
            
            elif status == "failed":
                print(f"\n✗ 視頻生成失敗: {task_data.get('error')}")
                return None
            
            elif status in ["pending", "processing"]:
                # 繼續等待
                time.sleep(5)  # 每 5 秒查詢一次
                continue
            
            else:
                print(f"\n✗ 未知狀態: {status}")
                return None
                
        except Exception as e:
            print(f"✗ 查詢任務時發生錯誤: {e}")
            time.sleep(5)
            continue


if __name__ == "__main__":
    # 範例 1: 文字轉視頻
    print("=" * 60)
    print("範例 1: 文字轉視頻")
    print("=" * 60)
    result = create_and_wait_for_video(
        prompt="A cat playing piano in a cozy living room"
    )
    
    print("\n" + "=" * 60)
    print("範例 2: 圖片轉視頻")
    print("=" * 60)
    # 範例 2: 圖片轉視頻
    result = create_and_wait_for_video(
        prompt="A beautiful sunset scene with moving clouds --duration 5",
        image_url="https://example.com/image.jpg"
    )
```

### JavaScript/TypeScript 範例

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';
const API_ENDPOINT = `${BASE_URL}/api/v1/videos/tasks`;

async function createAndWaitForVideo(prompt, imageUrl = null, maxWaitSeconds = 300) {
    try {
        // 步驟 1: 創建任務
        console.log('步驟 1: 創建視頻生成任務...');
        const payload = { prompt };
        if (imageUrl) {
            payload.image_url = imageUrl;
        }
        
        const createResponse = await axios.post(API_ENDPOINT, payload);
        const createResult = createResponse.data;
        
        if (createResult.code !== 0) {
            console.log(`任務創建失敗: ${createResult.message}`);
            return null;
        }
        
        const taskId = createResult.data.id;
        console.log(`✓ 任務創建成功！任務 ID: ${taskId}`);
        
        // 步驟 2: 輪詢查詢任務狀態
        console.log('\n步驟 2: 等待視頻生成完成...');
        const queryUrl = `${API_ENDPOINT}/${taskId}`;
        const startTime = Date.now();
        
        while (true) {
            // 檢查是否超時
            if ((Date.now() - startTime) / 1000 > maxWaitSeconds) {
                console.log(`✗ 等待超時（超過 ${maxWaitSeconds} 秒）`);
                return null;
            }
            
            const queryResponse = await axios.get(queryUrl);
            const queryResult = queryResponse.data;
            
            if (queryResult.code !== 0) {
                console.log(`✗ 查詢失敗: ${queryResult.message}`);
                return null;
            }
            
            const taskData = queryResult.data;
            const status = taskData.status;
            
            console.log(`  當前狀態: ${status}`);
            
            if (status === 'completed') {
                console.log('\n✓ 視頻生成完成！');
                console.log('視頻結果:', JSON.stringify(taskData.result, null, 2));
                return taskData;
            } else if (status === 'failed') {
                console.log(`\n✗ 視頻生成失敗: ${taskData.error}`);
                return null;
            } else if (status === 'pending' || status === 'processing') {
                // 等待 5 秒後繼續
                await new Promise(resolve => setTimeout(resolve, 5000));
                continue;
            } else {
                console.log(`\n✗ 未知狀態: ${status}`);
                return null;
            }
        }
    } catch (error) {
        console.error('發生錯誤:', error.message);
        return null;
    }
}

// 使用範例
(async () => {
    console.log('='.repeat(60));
    console.log('範例 1: 文字轉視頻');
    console.log('='.repeat(60));
    await createAndWaitForVideo(
        'A cat playing piano in a cozy living room --duration 5'
    );
    
    console.log('\n' + '='.repeat(60));
    console.log('範例 2: 圖片轉視頻');
    console.log('='.repeat(60));
    await createAndWaitForVideo(
        'A beautiful sunset scene with moving clouds --duration 5',
        'https://example.com/image.jpg'
    );
})();
```

---

## 注意事項

1. **圖片格式**: image_url 需要是可公開訪問的 HTTPS URL
2. **輪詢間隔**: 建議每 5-10 秒查詢一次任務狀態，避免過於頻繁的請求
3. **超時處理**: 視頻生成可能需要較長時間，建議設置適當的超時時間（如 5 分鐘）
4. **錯誤處理**: 務必處理所有可能的錯誤狀態，包括網絡錯誤、API 錯誤等

---

## 常見問題

### Q1: 任務一直處於 pending 狀態怎麼辦？
A: 可能是服務繁忙，建議繼續等待或檢查服務狀態。

### Q2: 如何知道視頻生成需要多長時間？
A: 生成時間取決於提示詞複雜度和服務負載，通常需要 1-5 分鐘。

### Q3: 可以同時創建多個任務嗎？
A: 可以，每個任務都有獨立的 task_id，可以並行處理。

### Q4: 生成的視頻保存在哪裡？
A: 視頻 URL 會在任務完成後通過 result.video_url 返回。

---

## API 測試工具

推薦使用以下工具測試 API：
- **Swagger UI**: 訪問 `https://video-gen.aimate.am/docs` 使用互動式 API 文件
- **Postman**: 匯入 API 端點進行測試
- **curl**: 使用命令列快速測試
- **Python/JavaScript**: 使用上述範例程式碼

---

## 聯繫資訊

如有問題或建議，請聯繫開發團隊。
