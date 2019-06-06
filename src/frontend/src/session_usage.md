# API
- `this.$session.getAll()`, returns all data stored in the Session.
- `this.$session.set(key,value)`, sets a single value to the Session.
- `this.$session.get(key)`, returns the value attributed to the given key.
- `this.$session.start()`, initializes a session with a 'session-id'. If you attempt to save a value without having started a new session, the plugin will automatically start a new session.
- `this.$session.exists()`, checks whether a session has been initialized or not.
- `this.$session.has(key)`, checks whether the key exists in the Session
- `this.$session.remove(key)`, removes the given key from the Session
- `this.$session.clear()`, clear all keys in the Session, except for 'session-id', keeping the Session alive
- `this.$session.destroy()`, destroys the Session
- `this.$session.id()`, returns the 'session-id'
- `this.$session.renew(session_id)`, allows a user to renew a previous session by manually inputting the session_id

# Warning
前端存储ID格式如: `"sess:219192e8-49ae-44aa-87e5-825c023bb62a"`, 后端直接为`219192e8-49ae-44aa-87e5-825c023bb62a`, 所以前后端交互时注意修改, 修改方式: 

```javascript
this.$session.id().replace('sess', '');
```

# Reference
[vue-session](https://www.npmjs.com/package/vue-session)