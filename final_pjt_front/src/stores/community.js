export const getComments = (threadId) => {
  return api.get(`/threads/${threadId}/comments/`)
}

export const createComment = (threadId, content) => {
  return api.post(`/threads/${threadId}/comments/create/`, { content })
}

export const updateComment = (threadId, commentId, content) => {
  return api.put(`/threads/${threadId}/comments/${commentId}/`, { content })
}

export const deleteComment = (threadId, commentId) => {
  return api.delete(`/threads/${threadId}/comments/${commentId}/`)
}
