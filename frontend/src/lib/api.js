import qs from 'qs'
import { access_token, username, is_login } from './store'
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

// 요청 방식, 경로, 전달한 매개변수, 성공시 동작, 실패시 동작
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)     // params 데이터를 content_type의 형식에 맞게 변환하는 역할을 한다
    }       // OAuth2의 로그인을 수행할 때 content-type은 application/json이 아니라 위의 content-type을 사용해야 한다.

    let _url = import.meta.env.VITE_SERVER_URL+url
    // .env 파일에 작성한 환경변수를 불러온다
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }


    let options = {
        method: method,
        headers: {
            "Content-Type": content_type 
        }   // header 중에서 Content-Type 는 요청의 본문에 포함된 데이터의 유형을 나타낸다. 주로 post, put 요청과 함게 사용되며, application/json, application/x-www-form-urlencoded 등의 값을 가질 수 있습니다. 
    }       // Authorization, User-Agent 등의 header도 있다.
    // 헤더 : 요청이나 응답의 속성 및 정보를 포함하며, 클라이언트와 서바 간의 통신을 관리하는데 사용된다.
    // 헤더는 메타데이터로, 메타데이터는 데이터에 대한 데이터, 다른 데이터를 설명하거나 분류하기 위한 정보를 말한다. 
    // -> 헤더는 어떠한 데이터를 대표하는 정보이다. HTTP 요청이나 응답과 관련된 정보를 설명하거나 특성을 기술한다.
    // 요청 헤더, 응답 헤더, 일반 헤더 등이 있다.

    const _access_token = get(access_token) // get을 이용해 상태저장소(여기서는 access_token)의 현재 값을 가져온다.
    if (_access_token) {                    // $ 를 사용할 수 없기 때문에 get으로
        options.headers['Authorization'] = 'Bearer ' + _access_token // access_token에 값이 있으면 options.headers에 해당 딕셔너리를 추가
    }                                       // Bearer 뒤에 띄어쓰기 해줘야함

    if (method !== 'get') {
        options['body'] = body 
    }

// fetch 로 호출, then 으로 응답을 처리
// then : promise가 성공, 또는 실패 상태일 때 호출될 콜백 함수를 등록한다.
// fetch로 promise를 return -> promise의 then 메소드를 이용해 성공/실패 상태에서 호출될 콜백 함수를 등록

/*
*****  then(a => {}) 일 때, a(response, data 등)가 성공적으로 처리되었다면(response: 성공적인 응답, data: 데이터 확인됨) {}에 해당하는 함수를 실행한다.
*/

// response는 fetch 함수가 반환하는 promise의 결과로 받는 객체이다. 요청에 대한 응답을 나타내며, HTTP 응답 헤더와 실제 응답 본문 등을 포함한다.
// -> 실제 서버로부터 받은 응답에 대한 정보를 담고 있는 객체이다. 이 객체를 사용하여 응답 본문을 json 형식으로 파싱하거나 다양한 응답 정보를 확인할 수 있다.
// promise는 비동기 작업의 결과를 나타내는 javascript 객체로, 작업이 완료되면 값을 반환하거나 오류를 발생시키는데 사용된다.
// -> 네트워크
    try {
        const response = await fetch(_url, options)
        if (response.status === 204) {
            if (success_callback) {
                await success_callback();
            }
            return
        }
        const json = await response.json()
        if (response.status >= 200 && response.status < 300) {
            if (success_callback) {
                await success_callback(json)
            }
            return json
        } else if (operation !== 'login' && response.status === 401) {
            access_token.set('')
            username.set('')
            is_login.set('')
            alert(operation)
            alert(response.status)
            push('/login')
        } else {
            if (failure_callback) {
                failure_callback(json)
            } else {
                alert(JSON.stringify(json))
            }
            throw new Error(json.message || 'Fetch failed')
        }
    } catch (error) {
        alert(JSON.stringify(error))
        throw error
    }
}
// _url에 요청을 보낸다.
// then 에서는 fetch 함수가 반환한 promise를 처리하는데 사용된다. 서버로부터 받은 응답을 처리한다.
// response.json() 에서 응답 본문을 json 형식으로 파싱한다. -> 이는 promise를 반환하므로 then 을 사용하여 파싱된 json 데이터를 처리한다.




export default fastapi
// 파일만 import 해도 fastapi 함수는 자동으로 불러와짐, export default에 의해