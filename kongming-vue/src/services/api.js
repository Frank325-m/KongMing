
const API_BASE = 'http://localhost:8000'

export const createNewSession = async () => {
  try {
    const response = await fetch(API_BASE + '/new-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return await response.json()
  } catch (error) {
    console.error('创建会话失败:', error)
    throw error
  }
}

export const fetchSessions = async () => {
  try {
    const response = await fetch(API_BASE + '/sessions')
    return await response.json()
  } catch (error) {
    console.error('获取会话列表失败:', error)
    throw error
  }
}

export const fetchSession = async (sessionId) => {
  try {
    const response = await fetch(API_BASE + '/session/' + sessionId)
    return await response.json()
  } catch (error) {
    console.error('获取会话失败:', error)
    throw error
  }
}

export const deleteSession = async (sessionId) => {
  try {
    await fetch(API_BASE + '/session/' + sessionId, {
      method: 'DELETE'
    })
  } catch (error) {
    console.error('删除会话失败:', error)
    throw error
  }
}

export const restoreSession = async (sessionId, history) => {
  try {
    const response = await fetch(API_BASE + '/restore-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId,
        history: history
      })
    })
    return await response.json()
  } catch (error) {
    console.error('恢复会话失败:', error)
    throw error
  }
}

export const updateSessionTitle = async (sessionId, title) => {
  try {
    const response = await fetch(API_BASE + '/update-session-title', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        session_id: sessionId,
        title: title
      })
    })
    return await response.json()
  } catch (error) {
    console.error('更新标题失败:', error)
    throw error
  }
}

export const sendChatRequest = (question, sessionId, onChunk, onError, onComplete) => {
  let url = API_BASE + '/chat-stream?question=' + encodeURIComponent(question)
  if (sessionId) {
    url += '&session_id=' + encodeURIComponent(sessionId)
  }

  fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'text/event-stream',
      'Cache-Control': 'no-cache'
    }
  }).then(response => {
    if (!response.ok) {
      throw new Error('HTTP错误: ' + response.status)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let receivedSessionId = null

    const readStream = async () => {
      try {
        while (true) {
          const { done, value } = await reader.read()
          if (done) {
            onComplete(receivedSessionId)
            break
          }

          const chunk = decoder.decode(value, { stream: true })

          if (chunk.includes('session_id:')) {
            const match = chunk.match(/session_id:(.+)/)
            if (match && match[1]) {
              receivedSessionId = match[1].trim()
            }
            continue
          }

          if (chunk.includes('[DONE]')) continue

          if (chunk.includes('error:')) {
            onError(new Error(chunk))
            return
          }

          if (chunk.trim()) {
            onChunk(chunk)
          }
        }
      } catch (error) {
        onError(error)
      }
    }

    readStream()
  }).catch(onError)
}
