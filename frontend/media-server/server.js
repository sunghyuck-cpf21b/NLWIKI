
const express = require('express')
const path = require('path')
// require에 대해
// https://velog.io/@sms8377/Javascript-require-%EA%B0%84%EB%8B%A8-%EB%8F%99%EC%9E%91-%EC%9B%90%EB%A6%AC-%EB%B0%8F-module.export-%EC%99%80-export%EC%9D%98-%EC%B0%A8%EC%9D%B4

const app = express()
const PORT = 3000 

// 정적 파일 제공
app.use(express.static(path.join(__dirname, 'public')))

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'))
})

app.listen(PORT, ()=>{
    console.log(`Media server is running on http://localhost:${PORT}`)
})