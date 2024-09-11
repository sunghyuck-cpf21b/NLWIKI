<script>
    import { push } from 'svelte-spa-router'
    import {fastapi} from '../lib/api'
    import Error from '../components/Error.svelte';
    import { access_token, username, is_login } from '../lib/store'

    import * as myurl from "../lib/myurl"

    let error = {detail:[]}
    let login_username = ''
    let login_password = ''

    async function login(event) {
        event.preventDefault()
        let url = "/api/user/login"
        let params = {
            username: login_username,
            password: login_password,
        }
        console.log('123123123')
        await fastapi('login', url, params,
            (json) => {
                $access_token = json.access_token 
                $username = json.username 
                $is_login = true 
                push(myurl.home_url)
            },
            (json_error) => {
                error = json_error
        })
    }
</script>

<div class='login_box'>
    <span class='info'>입력창 클릭이 안된다면 ESC를 눌러주세요</span>
    <h5>로그인</h5>
    <Error error={error} />
    <form method='post'>
        <div class='login_input'>
            <label for='username'>사용자 이름</label>
            <input type='text' id='username' bind:value='{login_username}'>
        </div>
        <div class='login_input'>
            <label for='password'>비밀번호</label>
            <input type='password' id='password' spellcheck="false" bind:value='{login_password}'>
        </div>
        <button type='submit' on:click='{login}'>로그인</button>
    </form>
</div>



<style>
    .login_box {
        border: 1px solid #000000;
        width: 400px;
        margin: 0 auto;
        display: flex;
        height: 300px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .info {
        font-size: 12px;
        color: #aaa;
        margin-top: 15px;
    }
    h5 {
        margin: auto;
    }
    form {
        display: flex;
        flex-direction: column;
        width: 60%;
        height: 180px;
        justify-content: space-evenly;
        align-items: center;
        margin-bottom: 25px;
    }
    .login_input{
        width: 80%;
        height: 40%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
    }
    input {
        width: 100%;
    }
</style>