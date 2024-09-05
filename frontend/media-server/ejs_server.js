const express = require('express')
const fs = require('fs')
const path = require('path')
const app = express() 
const port = 4000;

// ejs 템플릿 엔진 설정
app.set('view engine', 'ejs')

// 정적 파일 제공(css, 이미지 등)
app.use(express.static('public'))

// 라우팅 및 동적 페이지 렌더링
app.get('/', (req, res)=>{
    res.render('index', {title: '홈페이지', message: 'Express로 동적 페이지 만들기'})
})
app.get('/about', (req, res)=>{
    res.render('about', {title: '소개 페이지', description: '이 페이지는 Express로 렌더링됩니다.'})
})

app.get('/:img_file', (req,res)=>{
    const variable = req.params.img_file
    console.log(req)
    res.render('image', {variable})
})


app.listen(port, () => {
    console.log(`Express 서버가 http://localhost:${port} 에서 실행중입니다.`)
})